"""Train a NEW measured-data model; package research candidate, NOT an approved submission.
No old prediction file is read until after output is computed, for comparison only.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hashlib, json, zipfile
import numpy as np
import rasterio
from scipy.ndimage import distance_transform_edt
from src.modeling import fit_model, predict, thin
from scripts.validate_submission import validate

if __name__ == "__main__":
    validation = json.loads(Path("knowledge/validation-results.json").read_text())
    if "pooled" not in validation:
        raise RuntimeError("Finish locked spatial validation before packaging")
    foot = np.load("data/footprint_mask.npy")
    X = np.load("data/derived/X.npy", mmap_mode="r")
    y = np.load("data/derived/y.npy")
    coord = np.load("data/derived/coords.npy")
    columns = list(range(20))
    indices = np.arange(len(y))
    model, median, train_receipt = fit_model(X, y, indices, columns)
    scores = predict(model, median, X, indices, columns)
    with rasterio.open("data/labels.tif") as s:
        catalogue = s.read(1, masked=True).filled(0) > 0
    eligible = distance_transform_edt(~catalogue)[foot] > 2
    # This 200m suppression is an explicit heuristic, NOT the organizer mask (pixel-exact).
    scores[~eligible] = 0
    pred = thin(scores, coord[:, 0], coord[:, 1], foot.shape, round(foot.sum() * 0.008))
    pred[~foot] = 0
    digest = hashlib.sha256(pred.astype("<f4").tobytes()).hexdigest()
    name = f"gems38-realdata-A-20261005-{digest[:12]}"
    out = Path("docs/downloads")
    out.mkdir(exist_ok=True)
    with rasterio.open("data/sample_submission.tif") as t:
        profile = dict(
            driver="GTiff",
            width=t.width,
            height=t.height,
            count=1,
            dtype="float32",
            crs=t.crs,
            transform=t.transform,
            compress="deflate",
            predictor=3,
            tiled=True,
            blockxsize=256,
            blockysize=256,
        )
    receipts = []
    for outside in ["zero", "nan"]:
        a = pred.copy()
        a[~foot] = 0 if outside == "zero" else np.nan
        path = out / (name + "-" + outside + ".tif")
        with rasterio.open(
            path, "w", **profile, nodata=None if outside == "zero" else np.nan
        ) as dst:
            dst.write(a, 1)
        receipt = validate(path, outside=outside)
        if not receipt["passed"]:
            raise RuntimeError(receipt)
        receipts.append(receipt)
    primary = Path(receipts[0]["path"])
    with zipfile.ZipFile(primary.with_suffix(".zip"), "w", zipfile.ZIP_DEFLATED) as z:
        z.write(primary, primary.name)
    with rasterio.open("data/research/h33-reference.tif") as s:
        old = s.read(1)
    different = int(np.count_nonzero(np.nan_to_num(old) != pred))
    if not different:
        raise RuntimeError("Prediction duplicates reference")
    note = "G38 measured 19 bands + low-relief multiscale magnetic edge; HGB120, d2.8 sparse. Research-only: holdout gate closed; no leaderboard score."
    assert len(note) <= 200
    manifest = {
        "name": name,
        "submission_note": note,
        "status": "RESEARCH_ONLY_DO_NOT_SPEND_SLOT",
        "approved_for_competition_submission": False,
        "leaderboard_score": None,
        "algorithm": "Fresh HGB fit on measured 19 bands + preregistered A. No prior prediction used as input; no random fault geometry.",
        "training": train_receipt,
        "prediction_encoding": "binary ranking decision, NOT calibrated fault probability",
        "geometry": {
            "separation_px": 2.8,
            "catalogue_exclusion_px": 2,
            "positive_pixels": int(pred.sum()),
        },
        "compared_h33": {
            "pixel_difference_count": different,
            "reference_sha256": hashlib.sha256(
                Path("data/research/h33-reference.tif").read_bytes()
            ).hexdigest(),
        },
        "canonical_pixels_sha256": digest,
        "files": receipts,
        "validation": validation["pooled"],
        "gate_reason": validation["gate"]["reason"],
        "postprocessing_caveat": "Off-catalogue 200m prune is used only for final prediction; cannot be validated against the same full catalogue (it removes its positives). Fresh-baseline holdout tests unpruned emission rules; not final file hidden-label performance.",
        "reproduction": "bash scripts/download_competition_data.sh; python scripts/prepare_data.py; python scripts/build_features.py; python scripts/run_mine.py; python scripts/run_validation.py; python scripts/generate_submission.py",
    }
    Path("knowledge/submission-manifest.json").write_text(
        json.dumps(manifest, indent=2, allow_nan=False)
    )
    (out / "submission-audit.json").write_text(
        json.dumps(manifest, indent=2, allow_nan=False)
    )
    print(primary, flush=True)
    print("Different pixels vs H33:", different, flush=True)
