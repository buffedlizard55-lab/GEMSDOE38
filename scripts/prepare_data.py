"""Fail-closed input inventory; never generate surrogate footprints or labels."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hashlib, json
import numpy as np
import rasterio


def prepare(data_dir=Path("data")):
    rows = {}
    with rasterio.open(data_dir / "sample_submission.tif") as t:
        shape, crs, transform = t.shape, t.crs, t.transform
        a = t.read(1, masked=True)
        foot = ~np.ma.getmaskarray(a) & np.isfinite(a.data)
    if not foot.any():
        raise ValueError("Empty template footprint")
    for name in ["sample_submission", "labels", "training_features"]:
        path = data_dir / (name + ".tif")
        with rasterio.open(path) as s:
            if (s.shape, s.crs, s.transform) != (shape, crs, transform):
                raise ValueError("Misaligned " + name)
            if s.count != (19 if name == "training_features" else 1):
                raise ValueError("Band count")
            if name == "labels":
                y = s.read(1, masked=True)
                if (
                    np.ma.getmaskarray(y)[foot].any()
                    or not np.isin(y.data[foot], [0, 1]).all()
                ):
                    raise ValueError("Invalid labels")
            rows[name] = {
                "shape": list(s.shape),
                "crs": str(s.crs),
                "transform": list(s.transform)[:6],
                "bands": s.count,
                "descriptions": s.descriptions,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
    np.save(data_dir / "footprint_mask.npy", foot)
    rows["footprint_pixels"] = int(foot.sum())
    rows["label_status"] = (
        "known catalogue positives; zero is unlabelled, NOT verified true absence; hidden new faults unavailable"
    )
    rows["template_warning"] = (
        "Template nonzero values match known labels; never use template pixel values as prediction features."
    )
    Path("knowledge/input-inventory.json").write_text(json.dumps(rows, indent=2))
    print(json.dumps(rows, indent=2))
    return foot


if __name__ == "__main__":
    prepare()
