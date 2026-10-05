"""Actual computed raster overview, NOT an AI image or geological ground truth."""

import json, struct, zlib
from pathlib import Path
import numpy as np
import rasterio
from rasterio.enums import Resampling

if __name__ == "__main__":
    m = json.loads(Path("knowledge/submission-manifest.json").read_text())
    h, w = 746, 659
    with rasterio.open("data/training_features.tif") as s:
        a = s.read(14, out_shape=(h, w), masked=True, resampling=Resampling.average)
    valid = ~np.ma.getmaskarray(a)
    v = a.filled(0)
    lo, hi = np.quantile(v[valid], [0.03, 0.97])
    v = np.clip((v - lo) / (hi - lo), 0, 1)
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    rgb[:] = [17, 41, 36]
    for i, (base, scale) in enumerate([(37, 58), (72, 69), (63, 65)]):
        rgb[:, :, i][valid] = (base + scale * v[valid]).astype(np.uint8)
    with rasterio.open(m["files"][0]["path"]) as s:
        full = s.read(1)
    p = (
        np.pad(full, ((0, h * 5 - full.shape[0]), (0, w * 5 - full.shape[1])))
        .reshape(h, 5, w, 5)
        .max(axis=(1, 3))
    )
    rgb[p > 0] = [239, 193, 104]

    def chunk(k, data):
        return (
            struct.pack("!I", len(data))
            + k
            + data
            + struct.pack("!I", zlib.crc32(k + data) & 0xFFFFFFFF)
        )

    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack("!2I5B", w, h, 8, 2, 0, 0, 0))
        + chunk(
            b"IDAT", zlib.compress(b"".join(b"\0" + row.tobytes() for row in rgb), 9)
        )
        + chunk(b"IEND", b"")
    )
    Path("docs/assets").mkdir(exist_ok=True)
    Path("docs/assets/prediction-overview.png").write_bytes(png)
