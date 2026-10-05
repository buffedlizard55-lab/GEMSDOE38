import numpy as np
from src.mine_estimator import MINE, entropy


def test_informative_vs_null():
    rng = np.random.default_rng(8)
    y = (rng.random(10000) < 0.05).astype(int)
    x = y + rng.normal(0, 0.15, len(y))
    noise = rng.normal(size=len(y))
    signal = MINE(seed=8).fit(x, y, steps=800).evaluate(x, y)
    null = MINE(seed=8).fit(noise, y, steps=800).evaluate(noise, y)
    assert 0.10 < signal < entropy(y) + 0.03
    assert abs(null) < 0.01


def test_neural_derivative_finite_difference():
    m = MINE(seed=2)
    x = np.array([[0.2], [0.5], [0.9]])
    y = np.array([0, 1, 0])
    dt = np.array([0.1, -0.2, 0.3])
    _, cache = m.forward(x, y)
    grad = m.gradient(cache, dt)
    for j, p in enumerate(m.params):
        ix = tuple(0 for _ in p.shape)
        v = p[ix]
        e = 1e-5
        p[ix] = v + e
        plus = np.dot(m.forward(x, y)[0], dt)
        p[ix] = v - e
        minus = np.dot(m.forward(x, y)[0], dt)
        p[ix] = v
        assert np.isclose(grad[j][ix], (plus - minus) / (2 * e), atol=1e-7)


def test_natural_prevalence_not_balanced_entropy():
    # Low-prevalence perfectly predictive input should approach H(Y), not log(2).
    rng = np.random.default_rng(38)
    y = (rng.random(20000) < 0.01).astype(int)
    mi = MINE(seed=38).fit(y.astype(float), y, steps=1000).evaluate(y.astype(float), y)
    assert 0.7 * entropy(y) < mi < 1.1 * entropy(y)
