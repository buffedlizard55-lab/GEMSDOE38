"""Locked v3 spatial catalogue-proxy comparison; never certifies hidden-label skill.

Primary preregistered comparison: 19 + D + J vs 19 + D, at an identical
0.8% per-quadrant budget and 2.8-cell spacing, with fixed HGB settings and
four geographic quadrants. The public label raster is positive-unlabelled;
this is a proxy benchmark, not the competition's hidden test.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
import math
import numpy as np

from src.hypotheses_v3 import V3_NAMES
from src.metrics import contributions, from_terms
from src.modeling import fit_model, predict, thin


def _block_terms(pred, truth, test_y, test_x, shape, block_px=200):
    """Sum official metric contributions into occupied 20 km spatial blocks."""
    terms = contributions(pred, truth)
    rr, cc = np.indices(shape)
    n_cols = math.ceil(shape[1] / block_px)
    block_id = (rr // block_px) * n_cols + cc // block_px
    area = np.zeros(shape, dtype=bool)
    area[test_y, test_x] = True
    occupied = np.flatnonzero(np.bincount(block_id[area], minlength=n_cols * math.ceil(shape[0] / block_px)))
    matrix = np.stack(
        [
            np.bincount(
                block_id.ravel(),
                weights=term.ravel(),
                minlength=n_cols * math.ceil(shape[0] / block_px),
            )[occupied]
            for term in terms
        ],
        axis=1,
    )
    return matrix


def _paired_bootstrap(a, b, seed=38, draws=1000):
    if a.shape != b.shape or a.ndim != 2 or a.shape[1] != 3:
        raise ValueError("Paired block terms must have matching shape (blocks, 3)")
    rng = np.random.default_rng(seed)
    delta = np.empty(draws, dtype=np.float64)
    n = len(a)
    for i in range(draws):
        idx = rng.integers(0, n, n)
        delta[i] = from_terms(*a[idx].sum(0)) - from_terms(*b[idx].sum(0))
    return np.quantile(delta, [0.025, 0.975]).tolist()


def main():
    X = np.load("data/derived/X_v3.npy", mmap_mode="r")
    y = np.load("data/derived/y_v3.npy")
    fold = np.load("data/derived/folds_v3.npy")
    coord = np.load("data/derived/coords_v3.npy")
    foot = np.load("data/footprint_mask.npy")
    h, w = foot.shape
    if X.shape != (int(foot.sum()), 23) or len(y) != len(coord) or len(y) != len(fold):
        raise ValueError("v3 matrix, labels, coordinates and footprint are not aligned")

    j_column = 19 + 1  # X_v3 columns: 0:19 base bands, 19 D, 20 J, 21 K, 22 L.
    d_column = 19
    configs = {
        "baseline_19": list(range(19)),
        "plus_D": list(range(19)) + [d_column],
        "plus_D_J": list(range(19)) + [d_column, j_column],
    }
    report = {
        "version": 3,
        "label_status": "spatial known-catalogue proxy only; zero is unlabelled; hidden labels unavailable",
        "protocol": {
            "primary_candidate": "J_asymmetric_magnetic_flank, preregistered before feature/MINE computation",
            "folds": "4 geographic quadrants",
            "training_exclusion": "expanded test-quadrant rectangle by 10 pixels (1 km) on each side",
            "emission_density_per_test_footprint": 0.008,
            "minimum_spacing_px": 2.8,
            "model": "HistGradientBoosting 120 rounds, 15 leaves, lr .07, L2 10; fixed from modeling.py",
            "negative_training_rows": "up to 200,000 sampled uniformly without replacement from public zero/unlabelled cells; this is a proxy assumption",
            "bootstrap": "paired 20 km blocks, 1,000 resamples, conditional on the fitted models",
            "feature_transform_scope": "footprint-wide and label-free, but transductive rather than fold-local; this limits strict spatial-independence claims",
            "no_tuning": True,
        },
        "configs": {
            "baseline_19": "19 measured bands",
            "plus_D": "19 measured bands + fixed D_topographic_step_proxy",
            "plus_D_J": "19 measured bands + fixed D + preregistered J",
        },
        "folds": [],
        "pooled": {},
    }
    terms_by_config = {name: [] for name in configs}
    for f in range(4):
        r0, r1 = (0, h // 2) if f < 2 else (h // 2, h)
        c0, c1 = (0, w // 2) if f % 2 == 0 else (w // 2, w)
        test = np.flatnonzero(fold == f)
        yy, xx = coord[:, 0], coord[:, 1]
        excluded = (
            (yy >= r0 - 10)
            & (yy < r1 + 10)
            & (xx >= c0 - 10)
            & (xx < c1 + 10)
        )
        train = np.flatnonzero(~excluded)
        sy = coord[test, 0] - r0
        sx = coord[test, 1] - c0
        shape = (r1 - r0, c1 - c0)
        truth = np.zeros(shape, dtype=np.uint8)
        truth[sy, sx] = y[test]
        row = {
            "fold": f,
            "test_footprint_pixels": int(len(test)),
            "test_known_catalogue_positives": int(y[test].sum()),
            "train_footprint_pixels_after_exclusion": int(len(train)),
            "train_known_catalogue_positives": int(y[train].sum()),
            "models": {},
        }
        for name, columns in configs.items():
            model, median, training = fit_model(X, y, train, columns, seed=38)
            score = predict(model, median, X, test, columns)
            pred = thin(
                score,
                sy,
                sx,
                shape,
                round(len(test) * report["protocol"]["emission_density_per_test_footprint"]),
                separation=report["protocol"]["minimum_spacing_px"],
            )
            block = _block_terms(pred, truth, sy, sx, shape)
            terms_by_config[name].append(block)
            sums = block.sum(0)
            row["models"][name] = {
                "dti": float(from_terms(*sums)),
                "terms_tp_fp_fn": sums.tolist(),
                "predicted_pixels": int(pred.sum()),
                "training": training,
            }
            print(f"fold {f} {name}: {row['models'][name]['dti']:.8f}", flush=True)
        report["folds"].append(row)
        Path("knowledge/validation-v3.json").write_text(
            json.dumps(report, indent=2, allow_nan=False)
        )

    combined = {name: np.concatenate(parts, axis=0) for name, parts in terms_by_config.items()}
    for name, blocks in combined.items():
        sums = blocks.sum(0)
        report["pooled"][name] = {
            "dti": float(from_terms(*sums)),
            "terms_tp_fp_fn": sums.tolist(),
            "n_occupied_20km_blocks": int(len(blocks)),
        }
    baseline = combined["baseline_19"]
    d = combined["plus_D"]
    dj = combined["plus_D_J"]
    for target, reference in [("plus_D", "baseline_19"), ("plus_D_J", "baseline_19"), ("plus_D_J", "plus_D")]:
        target_blocks = combined[target]
        ref_blocks = combined[reference]
        delta = report["pooled"][target]["dti"] - report["pooled"][reference]["dti"]
        ci = _paired_bootstrap(target_blocks, ref_blocks)
        key = f"{target}_vs_{reference}"
        report["comparisons"] = report.get("comparisons", {})
        report["comparisons"][key] = {
            "delta_dti": float(delta),
            "paired_block_bootstrap_95": ci,
            "positive_folds": int(
                sum(
                    report["folds"][i]["models"][target]["dti"]
                    > report["folds"][i]["models"][reference]["dti"]
                    for i in range(4)
                )
            ),
            "blocks_resampled": int(len(target_blocks)),
        }
    report["interpretation"] = {
        "status": "catalogue-proxy only; not an estimate of hidden-fault leaderboard performance",
        "J_primary_internal_gate": "PASS" if (
            report["comparisons"]["plus_D_J_vs_plus_D"]["delta_dti"] > 0
            and report["comparisons"]["plus_D_J_vs_plus_D"]["positive_folds"] == 4
            and report["comparisons"]["plus_D_J_vs_plus_D"]["paired_block_bootstrap_95"][0] > 0
        ) else "FAIL",
        "competition_slot_gate": "CLOSED; no compatible reproducible current-best holdout checkpoint or hidden-label evidence",
        "confidence_note": "Bootstrap is conditional on the fitted models. Twenty-kilometre blocks need not be independent; four broad geographic folds provide limited geographic replication."
    }
    Path("knowledge/validation-v3.json").write_text(
        json.dumps(report, indent=2, allow_nan=False)
    )
    print(json.dumps(report["comparisons"], indent=2))
    print(report["interpretation"])


if __name__ == "__main__":
    main()
