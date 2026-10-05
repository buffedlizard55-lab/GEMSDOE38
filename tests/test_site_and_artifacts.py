import hashlib, json, zipfile
from pathlib import Path
from urllib.parse import urlparse, unquote
import numpy as np
import pytest, rasterio
from bs4 import BeautifulSoup
from scripts.refresh_sources import parse_best


def test_internal_site_links_exist():
    for page in Path("docs").glob("*.html"):
        soup = BeautifulSoup(page.read_text(), "html.parser")
        assert soup.find("main") and soup.find("title")
        for tag in soup.select("[href],[src]"):
            link = tag.get("href") or tag.get("src")
            url = urlparse(link)
            if url.scheme or url.netloc or not url.path:
                continue
            assert (page.parent / unquote(url.path)).exists(), (page, link)


def test_packaged_artifacts_match_receipts():
    m = json.loads(Path("knowledge/submission-manifest.json").read_text())
    arrays = []
    for receipt in m["files"]:
        path = Path(receipt["path"])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == receipt["sha256"]
        with rasterio.open(path) as s:
            a = s.read(1)
            assert s.count == 1 and s.dtypes == ("float32",)
            assert s.shape == (3730, 3292) and s.crs.to_epsg() == 32611
            assert not np.isinf(a).any()
            finite = a[np.isfinite(a)]
            assert finite.min() >= 0 and finite.max() <= 1
            if receipt["outside_policy"] == "zero":
                assert np.isfinite(a).all() and s.nodata is None
            digest = hashlib.sha256(
                np.nan_to_num(a, nan=0).astype("<f4").tobytes()
            ).hexdigest()
            assert digest == m["canonical_pixels_sha256"]
            arrays.append(digest)
    primary = Path(m["files"][0]["path"])
    with zipfile.ZipFile(primary.with_suffix(".zip")) as z:
        assert z.namelist() == [primary.name]
        assert (
            hashlib.sha256(z.read(primary.name)).hexdigest() == m["files"][0]["sha256"]
        )
    assert arrays[0] == arrays[1]
    assert len(m["submission_note"]) <= 200
    assert m["approved_for_competition_submission"] is False
    assert m["leaderboard_score"] is None


def test_no_duplicate_and_gate_closed():
    u = json.loads(Path("knowledge/uniqueness-audit.json").read_text())
    v = json.loads(Path("knowledge/validation-results.json").read_text())
    assert u["duplicates"] == 0 and u["compared_same_grid"] >= 208
    assert v["gate"]["approved"] is False
    assert v["pooled"]["paired_block_bootstrap_95pct"][0] < 0


def test_feed_fail_closed():
    assert (
        parse_best("<table><tr><td>0.1234</td></tr><tr><td>0.3262</td></tr></table>")
        == 0.3262
    )
    with pytest.raises(ValueError):
        parse_best("<html>Login</html>")
