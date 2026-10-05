"""Compare raster CONTENT against retrievable public submission artifacts, not filenames."""

import concurrent.futures, hashlib, json, subprocess
from pathlib import Path
import numpy as np
import rasterio
from rasterio.io import MemoryFile

if __name__ == "__main__":
    manifest = json.loads(Path("knowledge/submission-manifest.json").read_text())
    with rasterio.open(manifest["files"][0]["path"]) as s:
        prediction = s.read(1)
        grid = (s.shape, s.crs, s.transform)
    sites = json.loads(Path("knowledge/site-review.json").read_text())["sites"]
    items = []
    failures = []
    for site in sites:
        repo = site["repo"]
        ref = site["commit"]
        cmd = [
            "gh",
            "api",
            f"repos/buffedlizard55-lab/{repo}/git/trees/{ref}?recursive=1",
        ]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode:
            failures.append({"repo": repo, "error": "tree inaccessible"})
            continue
        tree = json.loads(r.stdout)
        for entry in tree.get("tree", []):
            p = entry["path"]
            if p.endswith(".tif") and (
                "downloads/" in p or p.startswith("submissions/")
            ):
                items.append(
                    {
                        "repo": repo,
                        "ref": ref,
                        "path": p,
                        "blob": entry["sha"],
                        "bytes": entry.get("size", 0),
                    }
                )
    # Identical Git blobs across many repositories need just one content read.
    groups = {}
    for item in items:
        groups.setdefault(item["blob"], []).append(item)

    def compare(group):
        item = group[0]
        result = {"artifacts": group}
        if item["bytes"] > 60_000_000:
            return {**result, "status": "skipped over 60MB"}
        r = subprocess.run(
            [
                "gh",
                "api",
                "-H",
                "Accept: application/vnd.github.raw+json",
                f"repos/buffedlizard55-lab/{item['repo']}/git/blobs/{item['blob']}",
            ],
            capture_output=True,
        )
        if r.returncode:
            return {**result, "status": "unavailable"}
        try:
            with MemoryFile(r.stdout) as mem, mem.open() as s:
                if (s.shape, s.crs, s.transform) != grid or s.count != 1:
                    return {**result, "status": "different grid/bands"}
                a = np.nan_to_num(s.read(1), nan=0)
                diff = int(np.count_nonzero(a != prediction))
                return {
                    **result,
                    "status": "DIFFERENT" if diff else "DUPLICATE",
                    "different_pixels": diff,
                    "sha256": hashlib.sha256(r.stdout).hexdigest(),
                    "canonical_pixels_sha256": hashlib.sha256(
                        a.astype("<f4").tobytes()
                    ).hexdigest(),
                }
        except Exception as e:
            return {**result, "status": "unreadable", "error": str(e)[:300]}

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(compare, groups.values()))
    receipt = {
        "date": "2026-10-05",
        "candidate": manifest["name"],
        "scope": "all .tif paths under downloads/ or submissions/ in pinned trees of 36 supplied repositories; not private/unlisted files or unspecified 37-40 sites",
        "artifact_paths": len(items),
        "distinct_git_blobs": len(groups),
        "compared_same_grid": sum(
            r["status"] in ["DIFFERENT", "DUPLICATE"] for r in results
        ),
        "duplicates": sum(r["status"] == "DUPLICATE" for r in results),
        "tree_failures": failures,
        "results": results,
    }
    Path("knowledge/uniqueness-audit.json").write_text(json.dumps(receipt, indent=2))
    print({k: v for k, v in receipt.items() if k != "results"}, flush=True)
    if receipt["duplicates"]:
        raise SystemExit("Duplicate detected")
