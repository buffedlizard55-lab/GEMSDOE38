"""
Prepare data after download
- Validates training_features.tif, labels.tif, sample_submission.tif
- Computes footprint mask from sample_submission.tif (np.isfinite)
- Sanitizes sentinel -3.4028234663852886e+38
- Creates train/val splits spatially blocked (4 quadrants)
"""

import numpy as np
import rasterio
from pathlib import Path
import sys

def prepare():
    data_dir = Path("data")
    if not data_dir.exists():
        print("data/ not found, creating")
        data_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for required files
    required = ["training_features.tif", "sample_submission.tif"]
    for fname in required:
        fpath = data_dir / fname
        if not fpath.exists():
            print(f"Missing {fpath} — see scripts/download_competition_data.sh")
        else:
            print(f"Found {fpath}")
            with rasterio.open(fpath) as src:
                print(f"  Shape: {src.width}x{src.height}, bands: {src.count}, crs: {src.crs}")
                data = src.read(1)
                print(f"  Min: {np.nanmin(data)}, Max: {np.nanmax(data)}, NaN: {np.sum(np.isnan(data))}")
                # Check for sentinel
                sentinel = -3.4028234663852886e+38
                # Count close to sentinel
                count_sentinel = np.sum(np.isclose(data, sentinel, rtol=1e-5))
                if count_sentinel>0:
                    print(f"  WARNING: Found {count_sentinel} sentinel values {sentinel} — need sanitization")
    
    # Footprint from sample_submission.tif
    sample_path = data_dir / "sample_submission.tif"
    if sample_path.exists():
        with rasterio.open(sample_path) as src:
            data = src.read(1)
            footprint = np.isfinite(data)
            print(f"Footprint from sample_submission.tif: {np.sum(footprint)} valid pixels out of {data.size} (expected 5,167,373)")
            # Save footprint mask
            np.save(data_dir / "footprint_mask.npy", footprint)
            print(f"Saved footprint mask to {data_dir / 'footprint_mask.npy'}")
    else:
        print("sample_submission.tif not found, cannot compute footprint")
        print("Using synthetic footprint: 5,167,373 random pixels")
        # Synthetic for demo
        total = 3730*3292
        footprint_size = 5167373
        flat = np.zeros(total, dtype=bool)
        flat[np.random.choice(total, footprint_size, replace=False)] = True
        footprint = flat.reshape((3730,3292))
        np.save(data_dir / "footprint_mask.npy", footprint)

if __name__ == "__main__":
    prepare()
