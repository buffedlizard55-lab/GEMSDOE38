"""Independent disk reread against actual template. Never placeholder-pass missing checks."""

from pathlib import Path
import argparse, hashlib, json
import numpy as np
import rasterio


def validate(path, template="data/sample_submission.tif", outside="zero"):
    with rasterio.open(template) as t:
        a = t.read(1, masked=True)
        foot = ~np.ma.getmaskarray(a) & np.isfinite(a.data)
        expected = (t.shape, t.crs, t.transform)
    with rasterio.open(path) as s:
        p = s.read(1)
        checks = {
            "single_band": s.count == 1,
            "float32": s.dtypes == ("float32",),
            "shape": s.shape == expected[0],
            "crs": s.crs == expected[1],
            "transform": s.transform == expected[2],
            "epsg_32611": s.crs is not None and s.crs.to_epsg() == 32611,
        }
        if s.shape == foot.shape:
            checks.update(
                inside_finite=bool(np.isfinite(p[foot]).all()),
                inside_range=bool(np.all((p[foot] >= 0) & (p[foot] <= 1))),
            )
            if outside == "zero":
                checks.update(
                    all_finite=bool(np.isfinite(p).all()),
                    outside_zero=bool(np.all(p[~foot] == 0)),
                    nodata_unset=s.nodata is None,
                )
            elif outside == "nan":
                checks.update(
                    outside_nan=bool(np.isnan(p[~foot]).all()),
                    nodata_nan=s.nodata is not None and bool(np.isnan(s.nodata)),
                )
            else:
                raise ValueError("Outside policy must be zero or nan")
        else:
            checks["footprint_check"] = False
        values = p[np.isfinite(p)]
        return {
            "path": str(path),
            "passed": bool(all(checks.values())),
            "checks": checks,
            "outside_policy": outside,
            "shape": list(s.shape),
            "crs": str(s.crs),
            "transform": list(s.transform)[:6],
            "positive_pixels": int(np.count_nonzero(p > 0)),
            "finite_pixels": int(np.isfinite(p).sum()),
            "nan_pixels": int(np.isnan(p).sum()),
            "min": float(values.min()) if len(values) else None,
            "max": float(values.max()) if len(values) else None,
            "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            "canonical_pixels_sha256": hashlib.sha256(
                np.nan_to_num(p, nan=0).astype("<f4").tobytes()
            ).hexdigest(),
            "portal_certification": False,
            "format_note": "Zero outside is compatibility encoding; official prose specifies null/NaN outside. NaN twin follows that wording. Portal acceptance not tested.",
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--template", default="data/sample_submission.tif")
    parser.add_argument("--outside", choices=["zero", "nan"], default="zero")
    args = parser.parse_args()
    receipt = validate(args.path, args.template, args.outside)
    print(json.dumps(receipt, indent=2, allow_nan=False))
    raise SystemExit(0 if receipt["passed"] else 1)
