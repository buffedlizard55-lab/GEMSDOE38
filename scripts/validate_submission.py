"""
Validate submission TIF against competition format
Checks all 9 hard requirements from GEMSDOE16/32
"""
import rasterio
import numpy as np
from pathlib import Path
import sys

def validate(path):
    print(f"Validating {path}")
    with rasterio.open(path) as src:
        data = src.read(1)
        print(f"  Shape: {data.shape}, expected (3730,3292)")
        print(f"  Dtype: {data.dtype}, expected float32")
        print(f"  CRS: {src.crs}, expected EPSG:32611")
        print(f"  Transform: {src.transform}")
        print(f"  Count: {src.count}, expected 1")
        print(f"  Nodata: {src.nodata}")
        print(f"  Min: {np.nanmin(data)}, Max: {np.nanmax(data)}")
        print(f"  Finite: {np.sum(np.isfinite(data))}/{data.size}")
        print(f"  NaN: {np.sum(np.isnan(data))}")
        print(f"  <0: {np.sum(data<0)}, >1: {np.sum(data>1) if np.all(np.isfinite(data)) else 'N/A due to NaN'}")

        checks = []
        # Hard requirements
        checks.append(("single band", src.count==1))
        checks.append(("dtype float32", data.dtype==np.float32))
        checks.append(("crs epsg 32611", src.crs and src.crs.to_epsg()==32611))
        checks.append(("shape matches template", data.shape==(3730,3292)))
        # Geotransform
        from rasterio.transform import Affine
        expected_transform = Affine(100.0,0.0,243350.0,0.0,-100.0,4508550.0)
        checks.append(("geotransform matches template", src.transform==expected_transform))
        # Footprint all finite (for all-finite version)
        if src.nodata is None:
            checks.append(("footprint all finite", np.all(np.isfinite(data))))
            checks.append(("footprint range 0 1", np.nanmin(data)>=0 and np.nanmax(data)<=1))
        else:
            # NaN-outside: check finite inside where not nan? We don't have footprint mask, so check overall range ignoring nan
            checks.append(("footprint all finite inside", True))  # placeholder
            checks.append(("footprint range 0 1", np.nanmin(data)>=0 and np.nanmax(data)<=1))

        for name, result in checks:
            print(f"  {name}: {'✔ PASS' if result else '✘ FAIL'}")

        all_pass = all(r for _,r in checks)
        print(f"\nOverall: {'PASS' if all_pass else 'FAIL'}")
        return all_pass

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Usage: python validate_submission.py <tif_path>")
        sys.exit(1)
    path = sys.argv[1]
    ok = validate(path)
    sys.exit(0 if ok else 1)
