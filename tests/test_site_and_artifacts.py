import hashlib
import json
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlparse

import numpy as np
import pytest
import rasterio
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


def test_packaged_artifacts_match_receipts_and_slot_stays_closed():
    manifest = json.loads(Path("knowledge/submission-manifest.json").read_text())
    gate = json.loads(Path("knowledge/slot-gate.json").read_text())
    assert json.loads(Path("docs/downloads/submission-audit.json").read_text()) == manifest
    assert json.loads(Path("docs/evidence/submission-manifest.json").read_text()) == manifest
    arrays = []
    for receipt in manifest["files"]:
        path = Path(receipt["path"])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == receipt["sha256"]
        with rasterio.open(path) as src:
            values = src.read(1)
            assert src.count == 1 and src.dtypes == ("float32",)
            assert src.shape == (3730, 3292) and src.crs.to_epsg() == 32611
            assert tuple(src.transform)[:6] == (100.0, 0.0, 243350.0, 0.0, -100.0, 4508550.0)
            assert not np.isinf(values).any()
            inside = np.isfinite(values) if receipt["outside_policy"] == "zero" else ~np.isnan(values)
            finite = values[inside]
            assert finite.min() >= 0 and finite.max() <= 1
            if receipt["outside_policy"] == "zero":
                assert np.isfinite(values).all() and src.nodata is None
            else:
                assert src.nodata is not None and np.isnan(src.nodata)
            canonical = hashlib.sha256(
                np.nan_to_num(values, nan=0).astype("<f4").tobytes()
            ).hexdigest()
            assert canonical == manifest["canonical_pixels_sha256"]
            arrays.append(canonical)
    assert arrays[0] == arrays[1]
    primary = Path(manifest["files"][0]["path"])
    with zipfile.ZipFile(primary.with_suffix(".zip")) as archive:
        assert archive.namelist() == [primary.name]
        assert hashlib.sha256(archive.read(primary.name)).hexdigest() == manifest["files"][0]["sha256"]
    assert len(manifest["submission_note"]) <= 200
    assert manifest["status"] == "LOCAL_FORMAT_CHECKED_RESEARCH_ARTIFACT_SLOT_GATE_CLOSED"
    assert manifest["approved_for_competition_submission"] is False
    assert gate["status"] == "CLOSED"
    assert gate["approved_for_competition_submission"] is False
    assert manifest["leaderboard_score"] is None
    assert all(item["portal_certification"] is False for item in manifest["files"])


def test_uniqueness_and_v3_incremental_gate():
    unique = json.loads(Path("knowledge/uniqueness-audit.json").read_text())
    assert unique["duplicates"] == 0 and unique["compared_same_grid"] >= 208

    gate = json.loads(Path("knowledge/slot-gate.json").read_text())
    assert gate["status"] == "CLOSED"
    validation = json.loads(Path("knowledge/validation-v3.json").read_text())
    comparison = validation["comparisons"]["plus_D_J_vs_plus_D"]
    assert validation["interpretation"]["J_primary_internal_gate"] == "FAIL"
    assert comparison["positive_folds"] == 2
    assert comparison["paired_block_bootstrap_95"][0] < 0 < comparison["paired_block_bootstrap_95"][1]


def test_v3_mine_receipt_is_full_population_and_keeps_limits():
    mine = json.loads(Path("knowledge/mine-results-v3.json").read_text())
    assert mine["population"] == 5_167_373
    assert mine["positives"] == 60_988
    assert set(mine["features"]) == {
        "J_asymmetric_magnetic_flank",
        "K_multiscale_crossfield_junction",
        "L_unsigned_basin_depth_gravity_conductivity_gradient",
    }
    assert any("marginal" in limit.lower() for limit in mine["limitations"])
    assert all(len(row["full_fit_nats"]) == 3 for row in mine["features"].values())
    exploratory_l = mine["features"]["L_unsigned_basin_depth_gravity_conductivity_gradient"]
    assert "exploratory" in exploratory_l["implementation_status"].lower()
    assert "not registered L" in exploratory_l["screen"]
    feature_receipt = json.loads(Path("knowledge/hypotheses-v3-features.json").read_text())
    assert "exploratory" in feature_receipt["implementation_deviation"]["status"]
    assert "not implemented" in feature_receipt["implementation_deviation"]["status"]
    assert feature_receipt["matrix_sha256_little_endian_float32_row_major"] == "54291ede6222b3da5d9ea9b78996aedeeed0494e1b1d806f40edd805aa83d2db"


def test_site_labels_artifact_as_research_only():
    for filename in ["index.html", "executive_summary.html", "methodology.html"]:
        text = Path("docs", filename).read_text()
        assert "SLOT GATE CLOSED" in text or "slot gate is CLOSED" in text
        assert "Do not submit" in text or "do not submit" in text
    assert "VALIDATED · 4/4 FOLDS · CI>0" not in Path("docs/index.html").read_text()


def test_candidate_generators_are_fail_closed_and_workflow_is_research_only():
    for filename in ["scripts/generate_submission.py", "scripts/generate_submission_v2.py"]:
        source = Path(filename).read_text()
        assert '"approved_for_competition_submission": False' in source
        assert '"approved_for_competition_submission": True' not in source
    workflow = Path(".github/workflows/research.yml").read_text().lower()
    assert "no competition upload" in workflow
    assert "actions/upload-artifact@v4" in workflow  # research evidence only
    assert "generate_submission" not in workflow
    assert "drivendata" not in workflow


def test_feed_fail_closed():
    assert parse_best("<table><tr><td>0.1234</td></tr><tr><td>0.3262</td></tr></table>") == 0.3262
    with pytest.raises(ValueError):
        parse_best("<html>Login</html>")
