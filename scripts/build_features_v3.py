"""Build D, preregistered J/K and exploratory unsigned L from measured rasters."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hashlib
import json

import numpy as np
import rasterio

from src.hypotheses import NAMES as V2_NAMES, build as build_v2
from src.hypotheses_v3 import V3_NAMES, build_v3


def _digest_array(a):
    return hashlib.sha256(np.asarray(a, dtype="<f4").tobytes()).hexdigest()


def _digest_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out = Path("data/derived")
    out.mkdir(parents=True, exist_ok=True)
    foot = np.load("data/footprint_mask.npy")
    if foot.ndim != 2 or not foot.any():
        raise ValueError("Missing or empty prepared footprint; run prepare_data.py")

    feature_arrays = {}
    with rasterio.open("data/sample_submission.tif") as template:
        expected_grid = (template.shape, template.crs, template.transform)
    if foot.shape != expected_grid[0]:
        raise ValueError("Prepared footprint does not match the submission grid")
    with rasterio.open("data/training_features.tif") as src:
        if (src.shape, src.crs, src.transform) != expected_grid or src.count != 19:
            raise ValueError("Training features do not match the verified 19-band submission grid")
        lookup = {d.split(" - ")[0]: i + 1 for i, d in enumerate(src.descriptions)}

        def read_band(name):
            if name not in lookup:
                raise KeyError(f"Required feature band missing: {name}")
            return src.read(lookup[name], masked=True).filled(np.nan)

        # The existing D transform is reused exactly; the v2 generator yields
        # it after A/B/C and stops before doing any later E-I computation.
        for name, a in build_v2(read_band, foot):
            if name == V2_NAMES[3]:
                feature_arrays["D_topographic_step_proxy"] = a
                break
        else:
            raise RuntimeError("D feature was not produced")

        feature_arrays.update(dict(build_v3(read_band, foot)))
        if list(feature_arrays) != ["D_topographic_step_proxy", *V3_NAMES]:
            raise RuntimeError(f"Unexpected feature order: {list(feature_arrays)}")

        stats = {}
        for name, a in feature_arrays.items():
            a = np.asarray(a, dtype=np.float32)
            if a.shape != foot.shape or not np.isfinite(a[foot]).all():
                raise ValueError(f"Invalid footprint values for {name}")
            if not np.isfinite(a).all():
                raise ValueError(f"Nonfinite whole-grid values for {name}")
            a[~foot] = 0
            np.save(out / (name + ".npy"), a)
            vals = a[foot]
            stats[name] = {
                "sha256_little_endian_float32_full_grid": _digest_array(a),
                "min_in_footprint": float(vals.min()),
                "max_in_footprint": float(vals.max()),
                "mean_in_footprint": float(vals.mean()),
                "std_in_footprint": float(vals.std()),
                "finite_in_footprint": int(np.isfinite(vals).sum()),
            }

        # Compact feature matrix used by the locked MINE and spatial benchmark:
        # columns 0:19 are provided bands, then D, J, K, L.
        X = np.lib.format.open_memmap(
            out / "X_v3.npy",
            mode="w+",
            dtype="float32",
            shape=(int(foot.sum()), 23),
        )
        for b in range(19):
            X[:, b] = src.read(b + 1, masked=True).filled(np.nan)[foot]
        for j, name in enumerate(["D_topographic_step_proxy", *V3_NAMES]):
            X[:, 19 + j] = np.load(out / (name + ".npy"), mmap_mode="r")[foot]
        X.flush()
        matrix_digest = hashlib.sha256()
        for start in range(0, X.shape[0], 50_000):
            matrix_digest.update(np.asarray(X[start : start + 50_000], dtype="<f4").tobytes(order="C"))
        matrix_sha256 = matrix_digest.hexdigest()

    y, x = np.where(foot)
    coords = np.stack([y, x], axis=1).astype(np.int16)
    labels_path = Path("data/labels.tif")
    with rasterio.open(labels_path) as labels:
        if (labels.shape, labels.crs, labels.transform) != expected_grid or labels.count != 1:
            raise ValueError("Labels do not match the verified submission grid")
        label_array = labels.read(1, masked=True)
        if np.ma.getmaskarray(label_array)[foot].any():
            raise ValueError("Masked labels inside footprint")
        target = label_array.data[foot].astype(np.uint8)
        if not np.isin(target, [0, 1]).all():
            raise ValueError("Nonbinary labels inside footprint")
    folds = (
        (y >= foot.shape[0] // 2) * 2 + (x >= foot.shape[1] // 2)
    ).astype(np.uint8)
    np.save(out / "coords_v3.npy", coords)
    np.save(out / "folds_v3.npy", folds)
    np.save(out / "y_v3.npy", target)

    receipt = {
        "status": "features_built_label_free_with_l_implementation_deviation",
        "feature_order": ["D_topographic_step_proxy", *V3_NAMES],
        "matrix": "data/derived/X_v3.npy; 19 provided bands followed by D,J,K,L",
        "population": int(foot.sum()),
        "positive_catalogue_labels": int(target.sum()),
        "zero_semantics": "unlabelled, not confirmed fault absence",
        "folds": "4 geographic quadrants as preregistered; same 1km exclusion used in the prior fixed benchmark",
        "scaling": "feature transforms use input bands and footprint only; no labels, distances, candidate rasters, or hidden labels",
        "statistics_scope": "footprint-wide quantile/scale statistics are label-free but transductive, not recomputed separately within each spatial training fold",
        "implementation_deviation": {
            "feature": V3_NAMES[2],
            "registered_hypothesis": "L_signed_basin_side_step",
            "status": "exploratory_as_coded_only; preregistered signed opposing-side contrast was not implemented",
            "record": "knowledge/hypotheses-v3-review-amendment.md",
        },
        "features": stats,
        "matrix_sha256_little_endian_float32_row_major": matrix_sha256,
        "input_sha256": {
            "training_features.tif": _digest_file("data/training_features.tif"),
            "labels.tif": _digest_file(labels_path),
            "sample_submission.tif": _digest_file("data/sample_submission.tif"),
        },
    }
    Path("knowledge/hypotheses-v3-features.json").write_text(
        json.dumps(receipt, indent=2, allow_nan=False)
    )
    print(json.dumps(receipt, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
