"""Full-label MINE screen for J/K and the exploratory as-coded L variant."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
import numpy as np

from src.hypotheses_v3 import V3_NAMES
from src.mine_estimator import MINE, entropy


def main():
    matrix = np.load("data/derived/X_v3.npy", mmap_mode="r")
    y = np.load("data/derived/y_v3.npy")
    fold = np.load("data/derived/folds_v3.npy")
    if matrix.shape[0] != len(y) or len(fold) != len(y):
        raise ValueError("v3 matrix, labels and folds are not aligned")
    seeds = [38, 138, 238]
    report = {
        "version": 3,
        "units": "nats",
        "label_status": "public known catalogue vs unlabelled; not hidden new-fault truth",
        "population": int(len(y)),
        "positives": int(y.sum()),
        "label_entropy_nats": entropy(y),
        "method": "DV-MINE; natural prevalence; exact binary product marginal; EMA .99; 24 tanh units; 800 stochastic steps; batch 512; all-pixel evaluation",
        "seeds": seeds,
        "evaluation_population_per_fit": "all rows in the named full or spatial test population",
        "upstream_feature_statistics_scope": "footprint-wide, label-free normalization/transforms; transductive, not fold-local",
        "limitations": [
            "Full-fit estimates are evaluated on training labels and can be optimistic.",
            "Finite-capacity, bounded DV critics can miss dependence and their estimates are not guaranteed unbiased or low-variance.",
            "Spatial OOF estimates are diagnostics; they are not an independent hidden-label estimate or a confidence interval.",
            "Global shuffled-label controls destroy spatial autocorrelation and are optimization controls, not spatial significance tests.",
            "Marginal I(feature; label) is not conditional/incremental information given the existing 19 bands or D.",
            "Upstream feature normalization uses the full footprint without labels; the spatial folds therefore have a label-free transductive preprocessing step, not strictly fold-local preprocessing.",
            "The public catalogue is incomplete positive-unlabelled data; label zero is not verified absence.",
            "The as-coded unsigned L variant differs from the preregistered signed opposing-side L transform; its MINE result is exploratory only (see knowledge/hypotheses-v3-review-amendment.md).",
        ],
        "features": {},
    }
    for offset, name in enumerate(V3_NAMES, start=20):
        x = np.asarray(matrix[:, offset])
        row = {"full_fit_nats": [], "spatial_oof_fold_nats": [], "shuffled_null_nats": []}
        for seed in seeds:
            model = MINE(seed=seed).fit(x, y)
            row["full_fit_nats"].append(model.evaluate(x, y))
            null_y = np.random.default_rng(seed).permutation(y)
            null_model = MINE(seed=seed).fit(x, null_y)
            row["shuffled_null_nats"].append(null_model.evaluate(x, null_y))
            folds = []
            for f in range(4):
                train_idx = np.flatnonzero(fold != f)
                test_idx = np.flatnonzero(fold == f)
                oof = MINE(seed=seed).fit(x, y, train_idx)
                folds.append(oof.evaluate(x, y, test_idx))
            row["spatial_oof_fold_nats"].append(folds)
            print(name, seed, row["full_fit_nats"][-1], folds, flush=True)
        row["full_fit_mean_nats"] = float(np.mean(row["full_fit_nats"]))
        row["full_fit_seed_sd_nats"] = float(np.std(row["full_fit_nats"], ddof=1))
        row["oof_weighted_mean_nats"] = float(
            np.mean(
                [
                    np.average(values, weights=np.bincount(fold, minlength=4))
                    for values in row["spatial_oof_fold_nats"]
                ]
            )
        )
        row["oof_seed_sd_nats"] = float(
            np.std(
                [
                    np.average(values, weights=np.bincount(fold, minlength=4))
                    for values in row["spatial_oof_fold_nats"]
                ],
                ddof=1,
            )
        )
        row["null_mean_nats"] = float(np.mean(row["shuffled_null_nats"]))
        if row["oof_weighted_mean_nats"] > max(row["null_mean_nats"], 0):
            row["screen"] = (
                "predeclared primary; positive marginal OOF screen; proceed to locked J comparison"
                if name == V3_NAMES[0]
                else "positive marginal OOF screen only; no solo spatial model comparison run"
            )
        else:
            row["screen"] = "no stable positive OOF marginal evidence; do not claim information-free"
        if name == V3_NAMES[2]:
            row["registered_hypothesis"] = "L_signed_basin_side_step"
            row["implementation_status"] = (
                "exploratory unsigned variant; preregistered signed opposing-side contrast was not implemented"
            )
            row["screen"] = (
                "EXPLORATORY ONLY: positive marginal OOF estimate belongs to the unsigned as-coded variant, "
                "not registered L; no solo spatial model comparison run"
            )
        report["features"][name] = row
        Path("knowledge/mine-results-v3.json").write_text(
            json.dumps(report, indent=2, allow_nan=False)
        )
    print(json.dumps(report["features"], indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
