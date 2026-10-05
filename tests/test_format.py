import numpy as np
import pytest, rasterio
from rasterio.transform import from_origin
from scripts.validate_submission import validate


def write(path, a, nodata=None, transform=None):
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        width=5,
        height=5,
        count=1,
        dtype="float32",
        crs="EPSG:32611",
        transform=transform or from_origin(243350, 4508550, 100, 100),
        nodata=nodata,
    ) as s:
        s.write(a.astype("float32"), 1)


@pytest.fixture
def files(tmp_path):
    a = np.zeros((5, 5))
    a[0, :] = np.nan
    t = tmp_path / "template.tif"
    write(t, a, np.nan)
    return t, tmp_path / "p.tif"


def test_zero_and_nan(files):
    t, p = files
    a = np.zeros((5, 5))
    a[2, 2] = 1
    write(p, a)
    assert validate(p, t)["passed"]
    a[0, :] = np.nan
    write(p, a, np.nan)
    assert validate(p, t, "nan")["passed"]


@pytest.mark.parametrize("bad", [np.nan, np.inf, -3.4028234663852886e38, -0.01, 1.01])
def test_bad_inside_fails(files, bad):
    t, p = files
    a = np.zeros((5, 5))
    a[2, 2] = bad
    write(p, a)
    assert not validate(p, t)["passed"]


def test_outside_and_alignment(files):
    t, p = files
    a = np.zeros((5, 5))
    a[0, 0] = 1
    write(p, a)
    assert not validate(p, t)["passed"]
    write(p, a * 0, transform=from_origin(0, 0, 100, 100))
    assert not validate(p, t)["passed"]


def test_nan_inside_not_hidden_by_nan_nodata(files):
    t, p = files
    a = np.zeros((5, 5))
    a[0, :] = np.nan
    a[2, 2] = np.nan
    write(p, a, np.nan)
    assert not validate(p, t, "nan")["passed"]
