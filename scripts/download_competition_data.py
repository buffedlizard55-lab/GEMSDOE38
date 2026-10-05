"""Restore checksum-pinned owner mirrors via gh. No credentials stored or synthetic fallback."""

import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "knowledge/upstream-data-manifest.json"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def download(entry):
    dest = ROOT / "data" / entry["dest"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and sha(dest) == entry["sha256"]:
        print("Verified cached", dest.name, flush=True)
        return
    tmp = dest.with_suffix(".partial")
    with tmp.open("wb") as out:
        for p in entry.get("parts", [entry.get("path")]):
            print("Downloading", p, flush=True)
            subprocess.run(
                [
                    "gh",
                    "api",
                    "-H",
                    "Accept: application/vnd.github.raw+json",
                    f"repos/{entry['repo']}/contents/{p}?ref={entry['ref']}",
                ],
                stdout=out,
                check=True,
            )
    if sha(tmp) != entry["sha256"]:
        tmp.unlink()
        raise ValueError("Checksum mismatch: " + str(dest))
    tmp.replace(dest)
    print("Verified", dest.name, dest.stat().st_size, flush=True)


if __name__ == "__main__":
    manifest = json.loads(MANIFEST.read_text())
    for entry in manifest["files"]:
        if entry["group"] in ("core", "comparison_only"):
            download(entry)
