import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json, numpy as np
from src.modeling import fit_model, predict, thin
from src.metrics import contributions, from_terms
from src.hypotheses import NAMES

if __name__ == "__main__":
    X = np.load("data/derived/X.npy", mmap_mode="r")
    y = np.load("data/derived/y.npy")
    fold = np.load("data/derived/folds.npy")
    coord = np.load("data/derived/coords.npy")
    foot = np.load("data/footprint_mask.npy")
    H, W = foot.shape
    # Map feature name to column index
    feat_to_col = {name: 19 + idx for idx, name in enumerate(NAMES)}
    # Define configs to test
    configs = {
        "baseline_19": list(range(19)),
        "plus_D": list(range(19)) + [feat_to_col["D_topographic_step_proxy"]],
        "plus_I": list(range(19)) + [feat_to_col["I_drainage_deflection_curvature"]],
        "plus_E": list(range(19)) + [feat_to_col["E_basin_concealed_coedge"]],
        "plus_F": list(range(19)) + [feat_to_col["F_transtensional_corridor"]],
        "plus_D_I": list(range(19)) + [feat_to_col["D_topographic_step_proxy"], feat_to_col["I_drainage_deflection_curvature"]],
        "plus_D_E_I": list(range(19)) + [feat_to_col["D_topographic_step_proxy"], feat_to_col["E_basin_concealed_coedge"], feat_to_col["I_drainage_deflection_curvature"]],
        "plus_all_new": list(range(19)) + [feat_to_col[n] for n in ["D_topographic_step_proxy","E_basin_concealed_coedge","F_transtensional_corridor","G_quake_fabric_lineament","H_rtp_tilt_basement_step","I_drainage_deflection_curvature"]],
    }
    report = {
        "label_status": "spatial known-catalogue proxy ONLY; zeros unlabelled",
        "protocol": {
            "folds": "4 geographic quadrants",
            "train_buffer_pixels": 10,
            "pixel_m": 100,
            "emission_density": 0.008,
            "separation_px": 2.8,
            "model": "HistGradientBoosting 120 rounds, 15 leaves, lr .07, L2 10; fixed",
            "bootstrap": "paired 20km spatial blocks; 1000 resamples; conditional",
        },
        "folds": [],
        "pooled": {},
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
        row = {"fold": f, "test_pixels": len(test), "positive_pixels": int(y[test].sum()), "models": {}}
        for name, cols in configs.items():
            model, median, receipt = fit_model(X, y, train, cols)
            scores = predict(model, median, X, test, cols)
            pred = thin(scores, sy, sx, shape, round(len(test) * 0.008))
            oof[name][r0:r1, c0:c1] = pred
            terms = contributions(pred, truth)
            block = np.stack(
                [np.bincount(ids.ravel(), weights=a.ravel(), minlength=len(keep))[:len(keep)][keep] for a in terms],
                axis=1,
            )
            total[name].append(block)
            sums = block.sum(0)
            row["models"][name] = {"dti": float(from_terms(*sums)), "terms": sums.tolist(), "predicted_pixels": int(pred.sum())}
            print(f, name, row["models"][name]["dti"], flush=True)
        report["folds"].append(row)
        Path("knowledge/validation-v2.json").write_text(json.dumps(report, indent=2))
    # pooled
    for name in configs:
        arr = np.concatenate(total[name])
        report["pooled"][name] = {"dti": float(from_terms(*arr.sum(0))), "terms": arr.sum(0).tolist(), "n_blocks": len(arr)}
    # deltas vs baseline
    base_arr = np.concatenate(total["baseline_19"])
    base_dti = from_terms(*base_arr.sum(0))
    for name in configs:
        if name == "baseline_19":
            continue
        arr = np.concatenate(total[name])
        dti = from_terms(*arr.sum(0))
        delta = dti - base_dti
        # bootstrap paired
        rng = np.random.default_rng(38)
        deltas = []
        for _ in range(1000):
            idx = rng.integers(0, len(base_arr), len(base_arr))
            deltas.append(from_terms(*arr[idx].sum(0)) - from_terms(*base_arr[idx].sum(0)))
        ci = np.quantile(deltas, [0.025, 0.975])
        report["pooled"][name].update({"delta_vs_baseline": float(delta), "paired_bootstrap_95": ci.tolist(), "positive_folds": sum(1 for r in report["folds"] if r["models"][name]["dti"] > r["models"]["baseline_19"]["dti"])})
    Path("knowledge/validation-v2.json").write_text(json.dumps(report, indent=2, allow_nan=False))
    print(json.dumps(report["pooled"], indent=2))
