import numpy as np
from src.hypotheses import build
from src.modeling import thin


def test_real_surfaces_finite_and_nonconstant():
    y, x = np.indices((60, 60))
    data = {
        "tmi": np.tanh((x - 30) / 3) * 100 + y * 0.1,
        "det_elev": y * 2 + np.sin(x / 4),
        "depth_to_base_surf": x + y,
        "iso_grav_anom": x - y,
        "cond_surf": np.cos(x / 10) + y / 100,
        "det_elev_slope": np.ones((60, 60), dtype=np.float32),
        "geod_shearrate": np.ones((60, 60), dtype=np.float32) * 0.1,
        "geod_dilaterate": np.ones((60, 60), dtype=np.float32) * 0.1,
        "geod_2ndinv": np.ones((60, 60), dtype=np.float32) * 0.1,
        "ieq_n100a15": np.ones((60, 60), dtype=np.float32),
        "deq_n100a15": np.ones((60, 60), dtype=np.float32) * 10,
        "tmi_hg": np.ones((60, 60), dtype=np.float32),
        "tmi_vg": np.ones((60, 60), dtype=np.float32),
        "rtp": np.ones((60, 60), dtype=np.float32),
        "tc": np.ones((60, 60), dtype=np.float32),
        "iso_grav_anom_hg": np.ones((60, 60), dtype=np.float32),
    }
    rows = list(
        build(lambda name: data[name].astype("float32"), np.ones(x.shape, bool))
    )
    # Now 9 features
    assert len(rows) >= 4
    for name, a in rows:
        assert np.isfinite(a).all()
    # At least first original should be non-constant
    assert np.std(rows[0][1]) > 0


def test_thinning_spacing_and_determinism():
    yy, xx = np.indices((20, 20))
    scores = np.ones(400)
    a = thin(scores, yy.ravel(), xx.ravel(), yy.shape, 30)
    coords = np.argwhere(a)
    for i, p in enumerate(coords):
        for q in coords[i + 1 :]:
            assert np.linalg.norm(p - q) >= 2.8
    assert np.array_equal(a, thin(scores, yy.ravel(), xx.ravel(), yy.shape, 30))
    assert thin(scores, yy.ravel(), xx.ravel(), yy.shape, 0).sum() == 0


def test_missing_measured_field_raises():
    import pytest
    from src.hypotheses import fill

    with pytest.raises(ValueError):
        fill(np.full((10, 10), np.nan))
