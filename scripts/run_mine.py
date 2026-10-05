import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json, numpy as np
from src.mine_estimator import MINE, entropy
from src.hypotheses import NAMES

if __name__ == "__main__":
    X = np.load("data/derived/X.npy", mmap_mode="r")
    y = np.load("data/derived/y.npy")
    fold = np.load("data/derived/folds.npy")
    result = {
        "units": "nats",
        "label_semantics": "known catalogue vs unlabelled; NOT hidden new-fault truth",
        "population": len(y),
        "positives": int(y.sum()),
        "label_entropy_nats": entropy(y),
        "method": "DV-MINE, natural prevalence, binary-exact product marginal, EMA .99, 24 tanh units, 800 stochastic steps, batch 512",
        "seeds": [38, 138, 238],
        "features": {},
        "limitations": [
            "Full-fit estimates use training labels at evaluation and can be optimistic.",
            "OOF values are fold-wise neural DV diagnostics, not a guaranteed unbiased or lower-variance MI estimator.",
            "Full-set feature screening would contaminate model validation if used to select features before that validation. The top candidate was preregistered independently.",
            "No marginal-MI threshold can safely discard all synergistic features.",
            "Null is globally label-shuffled; destroys spatial autocorrelation, so it is an optimization control, not spatial significance.",
            "Sampling for optimization uses the whole training population as its sampling frame, but finite steps need not visit every row; evaluation does visit every row.",
        ],
    }
    for j, name in enumerate(NAMES):
        x = np.array(X[:, 19 + j])
        row = {
            "full_fit_nats": [],
            "spatial_oof_fold_nats": [],
            "shuffled_null_nats": [],
        }
        for seed in result["seeds"]:
            model = MINE(seed=seed).fit(x, y)
            row["full_fit_nats"].append(model.evaluate(x, y))
            null = np.random.default_rng(seed).permutation(y)
            row["shuffled_null_nats"].append(
                MINE(seed=seed).fit(x, null).evaluate(x, null)
            )
            folds = []
            for f in range(4):
                model = MINE(seed=seed).fit(x, y, np.flatnonzero(fold != f))
                folds.append(model.evaluate(x, y, np.flatnonzero(fold == f)))
            row["spatial_oof_fold_nats"].append(folds)
            print(name, seed, row["full_fit_nats"][-1], folds, flush=True)
        row["full_fit_mean_nats"] = float(np.mean(row["full_fit_nats"]))
        row["full_fit_seed_sd"] = float(np.std(row["full_fit_nats"], ddof=1))
        row["oof_weighted_mean_nats"] = float(
            np.mean(
                [
                    np.average(r, weights=np.bincount(fold))
                    for r in row["spatial_oof_fold_nats"]
                ]
            )
        )
        row["null_mean_nats"] = float(np.mean(row["shuffled_null_nats"]))
        row["screen"] = (
            "retain for interaction study only"
            if row["oof_weighted_mean_nats"] > max(row["null_mean_nats"], 0)
            else "no stable positive OOF marginal evidence; do not claim information-free"
        )
        result["features"][name] = row
        Path("knowledge/mine-results.json").write_text(
            json.dumps(result, indent=2, allow_nan=False)
        )
