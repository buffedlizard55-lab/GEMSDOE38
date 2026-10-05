"""Daily network refresh for Pages. Preserve last verified snapshot on any failure."""

from datetime import datetime, timezone
import json, re, hashlib
from pathlib import Path
import requests
from bs4 import BeautifulSoup


def parse_best(html):
    soup = BeautifulSoup(html, "html.parser")
    scores = []
    for row in soup.select("tr"):
        scores.extend(
            float(x) for x in re.findall(r"\b0\.\d{4}\b", row.get_text(" ", strip=True))
        )
    if not scores:
        raise ValueError(
            "No leaderboard score rows; page may be login/challenge or layout changed"
        )
    return max(scores)


if __name__ == "__main__":
    path = Path("knowledge/feed.json")
    feed = json.loads(path.read_text())
    now = datetime.now(timezone.utc).isoformat()
    feed["last_attempt_utc"] = now
    try:
        r = requests.get(feed["leaderboard_url"], timeout=30)
        r.raise_for_status()
        best = parse_best(r.text)
        feed.update(
            last_success_utc=now,
            status="fresh HTTP parse",
            leaderboard_best=best,
            source_sha256=hashlib.sha256(r.content).hexdigest(),
        )
        feed.pop("error", None)
    except (requests.RequestException, ValueError) as e:
        feed.update(
            status="refresh failed; previous snapshot retained", error=str(e)[:350]
        )
    path.write_text(json.dumps(feed, indent=2))
    print(json.dumps(feed, indent=2))
