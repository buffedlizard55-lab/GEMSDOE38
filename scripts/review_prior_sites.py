"""Audit supplied public site entry points via GitHub content mirror; no score invention."""

import concurrent.futures, hashlib, json, subprocess
from pathlib import Path
from bs4 import BeautifulSoup

REPOS = [
    "GEMSDOE",
    "6GEMSDOE",
    "GEMSDOE3",
    "GEMSDOE2",
    "GEMSDOE4",
    "5GEMSDOE",
    "7GEMSDOE",
    "8GEMSDOE",
    "GEMSDOE9",
    "11GEMSDOE",
    "12GEMSDOE",
    "15GEMSDOE",
    "14GEMSDOE",
    "17GEMSDOE",
    "18GEMSDOE",
    "19GEMSDOE",
    "GEMSDOE10",
    "13GEMSDOE",
    "16GEMSDOE",
    "GEMSDOE21",
    "20GEMSDOE",
    "GEMSDOE22",
    "GEMSDOE23",
    "GEMSDOE24",
    "GEMSDOE25",
    "GEMSDOE26",
    "GEMSDOE27",
    "GEMSDOE28",
    "GEMSDOE29",
    "GEMSDOE30",
    "GEMSDOE31",
    "GEMSDOE32",
    "GEMSDOE33",
    "GEMSDOE34",
    "GEMSDOE35",
    "GEMSDOE36",
]


def review(repo):
    prefix = f"repos/buffedlizard55-lab/{repo}"
    ref = subprocess.run(
        ["gh", "api", prefix + "/commits/main", "--jq", ".sha"],
        capture_output=True,
        text=True,
    )
    if ref.returncode:
        return {"repo": repo, "error": ref.stderr[:300]}
    commit = ref.stdout.strip()
    for path in ["docs/index.html", "index.html"]:
        r = subprocess.run(
            [
                "gh",
                "api",
                "-H",
                "Accept: application/vnd.github.raw+json",
                prefix + f"/contents/{path}?ref={commit}",
            ],
            capture_output=True,
        )
        if not r.returncode:
            soup = BeautifulSoup(r.stdout, "html.parser")
            text = soup.get_text(" ", strip=True)
            Path("knowledge/site-snapshots").mkdir(exist_ok=True)
            Path(f"knowledge/site-snapshots/{repo}.txt").write_text(text)
            return {
                "repo": repo,
                "commit": commit,
                "path": path,
                "site": f"https://buffedlizard55-lab.github.io/{repo}/{path}",
                "sha256": hashlib.sha256(r.stdout).hexdigest(),
                "text_chars": len(text),
                "tif_links": [
                    a["href"] for a in soup.select("a[href]") if ".tif" in a["href"]
                ],
                "evidence": "owner page, not organizer score verification",
            }
    return {"repo": repo, "commit": commit, "error": "Neither entry point retrievable"}


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(review, REPOS))
    Path("knowledge/site-review.json").write_text(
        json.dumps(
            {
                "checked_date": "2026-10-05",
                "scope": "entry pages only; not exhaustive code review",
                "sites": rows,
            },
            indent=2,
        )
    )
    print(
        "Reviewed", len(rows), "sites;", sum("error" in r for r in rows), "unavailable"
    )
