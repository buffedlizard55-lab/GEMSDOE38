import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json, numpy as np
from src.modeling import fit_model, predict, thin
from src.metrics import contributions, from_terms

if __name__ == "__main__":
    X = np.load("data/derived/X.npy", mmap_mode="r")
    y = np.load("data/derived/y.npy")
    fold = np.load("data/derived/folds.npy")
    coord = np.load("data/derived/coords.npy")
    foot = np.load("data/footprint_mask.npy")
    H, W = foot.shape
    configs = {"baseline_19": list(range(19)), "candidate_19_plus_A": list(range(20))}
    report = {
        "label_status": "spatial known-catalogue proxy ONLY; zeros unlabelled",
        "hypothesis": "A preregistered; no model tuning after results",
        "folds": [],
        "gate": {
            "approved": False,
            "reason": "No independently held-out current-best H33 checkpoint; hidden new-fault truth unavailable. Never auto-submit.",
        },
        "protocol": {
            "folds": "4 geographic quadrants",
            "train_buffer_pixels": 10,
            "pixel_m": 100,
            "emission_density": 0.008,
            "separation_px": 2.8,
            "model": "HistGradientBoosting 120 rounds, 15 leaves, learning_rate .07, L2 10; fixed a priori",
            "bootstrap": "paired 20km spatial blocks; 1000 resamples; conditional on models; not total uncertainty",
        },
    }
    total = {k: [] for k in configs}
    oof = {k: np.zeros(foot.shape, dtype=np.float32) for k in configs}
    for f in range(4):
        r0, r1 = (0, H // 2) if f < 2 else (H // 2, H)
        c0, c1 = (0, W // 2) if f % 2 == 0 else (W // 2, W)
        test = np.flatnonzero(fold == f)
        yy, xx = coord[:, 0], coord[:, 1]
        exclude = (yy >= r0 - 10) & (yy < r1 + 10) & (xx >= c0 - 10) & (xx < c1 + 10)
        train = np.flatnonzero(~exclude)
        sy, sx = coord[test, 0] - r0, coord[test, 1] - c0
        shape = (r1 - r0, c1 - c0)
        truth = np.zeros(shape, dtype=np.uint8)
        truth[sy, sx] = y[test]
        rr, cc = np.indices(shape)
        ids = (rr // 200) * ((shape[1] + 199) // 200) + cc // 200
        area = np.zeros(shape, bool)
        area[sy, sx] = True
        keep = np.bincount(ids[area]) > 0
        row = {
            "fold": f,
            "test_pixels": len(test),
            "positive_pixels": int(y[test].sum()),
            "models": {},
        }
        for name, cols in configs.items():
            model, median, receipt = fit_model(X, y, train, cols)
            scores = predict(model, median, X, test, cols)
            pred = thin(scores, sy, sx, shape, round(len(test) * 0.008))
            oof[name][r0:r1, c0:c1] = pred
            terms = contributions(pred, truth)
            block = np.stack(
                [
                    np.bincount(ids.ravel(), weights=a.ravel(), minlength=len(keep))[
                        : len(keep)
                    ][keep]
                    for a in terms
                ],
                axis=1,
            )
            total[name].append(block)
            sums = block.sum(0)
            row["models"][name] = {
                "dti": float(from_terms(*sums)),
                "terms": sums.tolist(),
                "predicted_pixels": int(pred.sum()),
                **receipt,
            }
            print(f, name, row["models"][name]["dti"], flush=True)
        row["delta"] = (
            row["models"]["candidate_19_plus_A"]["dti"]
            - row["models"]["baseline_19"]["dti"]
        )
        report["folds"].append(row)
        Path("knowledge/validation-results.json").write_text(
            json.dumps(report, indent=2)
        )
    a = np.concatenate(total["baseline_19"])
    b = np.concatenate(total["candidate_19_plus_A"])
    base = from_terms(*a.sum(0))
    candidate = from_terms(*b.sum(0))
    rng = np.random.default_rng(38)
    deltas = []
    for _ in range(1000):
        idx = rng.integers(0, len(a), len(a))
        deltas.append(from_terms(*b[idx].sum(0)) - from_terms(*a[idx].sum(0)))
    ci = np.quantile(deltas, [0.025, 0.975])
    report["pooled"] = {
        "baseline_dti": float(base),
        "candidate_dti": float(candidate),
        "delta": float(candidate - base),
        "paired_block_bootstrap_95pct": ci.tolist(),
        "n_blocks": len(a),
        "positive_folds": sum(r["delta"] > 0 for r in report["folds"]),
    }
    report["beats_fresh_baseline"] = bool(
        ci[0] > 0 and report["pooled"]["positive_folds"] >= 3
    )
    for name, p in oof.items():
        np.save("data/derived/oof_" + name + ".npy", p)
    Path("knowledge/validation-results.json").write_text(
        json.dumps(report, indent=2, allow_nan=False)
    )
    print(json.dumps(report["pooled"], indent=2), flush=True)
