import numpy as np
import pytest
from src.metrics import compute_dti, from_terms


def brute(p, g, R=3):
    gy, gx = np.where(g)
    py, px = np.where(p > 0)
    tp = sum(
        max(
            [0]
            + [p[y, x] * max(0, 1 - np.hypot(y - a, x - b) / R) for y, x in zip(py, px)]
        )
        for a, b in zip(gy, gx)
    )
    fp = sum(
        p[y, x]
        * (
            1
            - max(
                [0] + [max(0, 1 - np.hypot(y - a, x - b) / R) for a, b in zip(gy, gx)]
            )
        )
        for y, x in zip(py, px)
    )
    return tp, fp, g.sum() - tp


@pytest.mark.parametrize("seed", range(5))
def test_exact_random(seed):
    rng = np.random.default_rng(seed)
    p = rng.random((9, 11))
    g = rng.random(p.shape) < 0.12
    assert np.allclose(compute_dti(p, g)[1:], brute(p, g), atol=1e-9)


def test_empty_truth_not_phantom_origin():
    p = np.zeros((5, 5))
    p[0, 0] = 1
    assert compute_dti(p, np.zeros_like(p))[1:] == (0, 1, 0)


def test_perfect_and_example():
    p = np.zeros((5, 5))
    p[0, 0] = 1
    assert np.isclose(compute_dti(p, p)[0], 1)
    assert round(from_terms(3, 1.89, 2), 2) == 0.60


def test_invalid():
    with pytest.raises(ValueError):
        compute_dti(np.full((2, 2), np.nan), np.zeros((2, 2)))
    with pytest.raises(ValueError):
        compute_dti(np.zeros((2, 2)), np.full((2, 2), 0.2))
