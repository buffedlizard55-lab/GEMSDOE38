import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import rasterio
from src.hypotheses import build

if __name__ == "__main__":
    out = Path("data/derived")
    out.mkdir(exist_ok=True)
    foot = np.load("data/footprint_mask.npy")
    with rasterio.open("data/training_features.tif") as s:
        lookup = {d.split(" - ")[0]: i + 1 for i, d in enumerate(s.descriptions)}

        def read(name):
            return s.read(lookup[name], masked=True).filled(np.nan)

        for name, a in build(read, foot):
            if not np.isfinite(a[foot]).all():
                raise ValueError("Nonfinite " + name)
            a[~foot] = 0
            np.save(out / (name + ".npy"), a)
            print(name, float(a[foot].min()), float(a[foot].max()), flush=True)
        # Compact rows aligned to footprint; NaNs kept for fold-local imputation.
        from src.hypotheses import NAMES as H_NAMES

        X = np.lib.format.open_memmap(
            out / "X.npy",
            mode="w+",
            dtype="float32",
            shape=(int(foot.sum()), 19 + len(H_NAMES)),
        )
        for b in range(19):
            X[:, b] = s.read(b + 1, masked=True).filled(np.nan)[foot]
        for j, name in enumerate(
            __import__("src.hypotheses", fromlist=["NAMES"]).NAMES
        ):
            X[:, 19 + j] = np.load(out / (name + ".npy"), mmap_mode="r")[foot]
        X.flush()
    y, x = np.where(foot)
    np.save(out / "coords.npy", np.stack([y, x], axis=1).astype(np.int16))
    np.save(
        out / "folds.npy",
        ((y >= foot.shape[0] // 2) * 2 + (x >= foot.shape[1] // 2)).astype(np.uint8),
    )
    with rasterio.open("data/labels.tif") as s:
        np.save(out / "y.npy", s.read(1)[foot].astype(np.uint8))
