"""CPU NumPy MINE for binary labels, DV objective in NATS.
Belghazi et al. (2018): https://proceedings.mlr.press/v80/belghazi18a.html

Exact sum over binary p(y) replaces shuffled marginal Monte Carlo. Balanced
minibatches use natural-prevalence importance weights; class balancing MUST
NOT change the estimand. EMA denominator corrects stochastic log-gradient
bias. Neural optimization can underestimate MI; in-sample estimates can
be optimistic. Negative estimates are retained, never clipped into evidence.
"""

import numpy as np
from scipy.special import logsumexp


class MINE:
    def __init__(self, dim=1, hidden=24, seed=38):
        rng = np.random.default_rng(seed)
        self.rng = rng
        self.params = [
            rng.normal(0, 0.3, (dim + 1, hidden)),
            np.zeros(hidden),
            rng.normal(0, 0.1, (hidden, 1)),
            np.zeros(1),
        ]
        self.m = [np.zeros_like(a) for a in self.params]
        self.v = [np.zeros_like(a) for a in self.params]
        self.ema = None

    def forward(self, x, y):
        z = np.column_stack([x, y])
        h = np.tanh(z @ self.params[0] + self.params[1])
        raw = (h @ self.params[2] + self.params[3]).ravel()
        t = 12 * np.tanh(raw / 12)  # bounded critic for numerical stability
        return t, (z, h, 1 - (t / 12) ** 2)

    def gradient(self, cache, dt):
        z, h, slope = cache
        dr = (dt * slope)[:, None]
        dh = dr @ self.params[2].T * (1 - h * h)
        return [z.T @ dh, dh.sum(0), h.T @ dr, dr.sum(0)]

    def step(self, x, y, p, iteration, lr=0.003):
        # x consists of equal-sized strata, not the population distribution.
        weight = np.where(y == 1, p, 1 - p) / (len(y) / 2)
        t0, c0 = self.forward(x, np.zeros(len(x)))
        t1, c1 = self.forward(x, np.ones(len(x)))
        e0, e1 = np.exp(t0), np.exp(t1)
        marginal = float(np.sum(weight * ((1 - p) * e0 + p * e1)))
        self.ema = marginal if self.ema is None else 0.99 * self.ema + 0.01 * marginal
        d0 = weight * ((1 - y) - (1 - p) * e0 / self.ema)
        d1 = weight * (y - p * e1 / self.ema)
        grads = [a + b for a, b in zip(self.gradient(c0, d0), self.gradient(c1, d1))]
        for j, (param, g) in enumerate(zip(self.params, grads)):
            g = np.clip(g, -5, 5)
            self.m[j] = 0.9 * self.m[j] + 0.1 * g
            self.v[j] = 0.999 * self.v[j] + 0.001 * g * g
            param += (
                lr
                * (self.m[j] / (1 - 0.9**iteration))
                / (np.sqrt(self.v[j] / (1 - 0.999**iteration)) + 1e-8)
            )

    def fit(self, x, y, indices=None, steps=800, batch=512):
        x = np.asarray(x)
        if x.ndim == 1:
            x = x[:, None]
        if not np.isfinite(x).all():
            raise ValueError("MINE requires finite inputs")
        if not np.isin(y, [0, 1]).all():
            raise ValueError("Binary labels required")
        idx = np.arange(len(y)) if indices is None else np.asarray(indices)
        pos = idx[y[idx] == 1]
        neg = idx[y[idx] == 0]
        if not len(pos) or not len(neg):
            raise ValueError("Both classes required")
        probe = idx[self.rng.integers(len(idx), size=min(100000, len(idx)))]
        self.mean = x[probe].mean(0)
        self.std = np.maximum(x[probe].std(0), 1e-6)
        p = len(pos) / len(idx)
        for i in range(1, steps + 1):
            sel = np.concatenate(
                [self.rng.choice(neg, batch // 2), self.rng.choice(pos, batch // 2)]
            )
            xx = np.clip((x[sel] - self.mean) / self.std, -8, 8)
            self.step(xx, y[sel], p, i)
        return self

    def evaluate(self, x, y, indices=None, batch=32768):
        x = np.asarray(x)
        if x.ndim == 1:
            x = x[:, None]
        idx = np.arange(len(y)) if indices is None else np.asarray(indices)
        p = float(np.mean(y[idx]))
        joint = 0.0
        logtotal = -np.inf
        for start in range(0, len(idx), batch):
            sel = idx[start : start + batch]
            xx = np.clip((x[sel] - self.mean) / self.std, -8, 8)
            t0, _ = self.forward(xx, np.zeros(len(sel)))
            t1, _ = self.forward(xx, np.ones(len(sel)))
            joint += np.where(y[sel] == 1, t1, t0).sum()
            marginal = np.logaddexp(
                t0 + np.log(max(1 - p, 1e-300)), t1 + np.log(max(p, 1e-300))
            )
            logtotal = np.logaddexp(logtotal, logsumexp(marginal))
        return float(joint / len(idx) - (logtotal - np.log(len(idx))))


def entropy(y):
    p = np.mean(y)
    return float(-p * np.log(p) - (1 - p) * np.log(1 - p)) if 0 < p < 1 else 0.0
