import numpy as np
import pytest

from src.hypotheses_v3 import V3_NAMES, _profile_asymmetry, build_v3


def test_profile_asymmetry_distinguishes_one_sided_flank():
    cols = np.arange(101, dtype=np.float32) - 50
    symmetric_1d = 20 * np.tanh(cols / 4)
    asymmetric_1d = np.where(cols < 0, 0.5 * cols, 1.5 * cols)
    symmetric = np.broadcast_to(symmetric_1d, (31, 101)).copy()
    asymmetric = np.broadcast_to(asymmetric_1d, (31, 101)).copy()
    foot = np.ones(symmetric.shape, dtype=bool)
    sym = _profile_asymmetry(symmetric, sigma=2, foot=foot)
    asym = _profile_asymmetry(asymmetric, sigma=2, foot=foot)
    assert asym[:, 50].mean() > sym[:, 50].mean() + 0.1
    assert np.all((sym >= 0) & (sym <= 1))
    assert np.all((asym >= 0) & (asym <= 1))


def _measured_fields(shape):
    yy, xx = np.indices(shape, dtype=np.float32)
    return {
        "tmi": 100 * np.tanh((xx - shape[1] / 2) / 4) + 0.03 * yy,
        "iso_grav_anom": 0.4 * xx + 0.2 * yy + 4 * np.sin(xx / 7),
        "cond_surf": np.sin(xx / 11) + yy / 100,
        "det_elev_slope": np.abs(np.sin(xx / 15)) + 0.01,
        "depth_to_base_surf": xx + 0.7 * yy + np.sin(yy / 9),
    }


def test_v3_builds_finite_label_free_feature_surfaces():
    shape = (64, 72)
    foot = np.ones(shape, dtype=bool)
    foot[:3, :5] = False
    fields = _measured_fields(shape)
    rows = list(build_v3(lambda name: fields[name], foot))
    assert [name for name, _ in rows] == V3_NAMES
    for _, surface in rows:
        assert surface.shape == shape
        assert surface.dtype == np.float32
        assert np.isfinite(surface).all()
        assert np.all(surface >= 0)
        assert np.all(surface[~foot] == 0)
        assert surface[foot].std() > 0


def test_v3_fails_loudly_on_missing_band_or_empty_footprint():
    fields = _measured_fields((32, 32))
    foot = np.ones((32, 32), dtype=bool)
    del fields["cond_surf"]
    with pytest.raises(KeyError):
        list(build_v3(lambda name: fields[name], foot))
    with pytest.raises(ValueError):
        list(build_v3(lambda name: fields[name], np.zeros_like(foot)))
