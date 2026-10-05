"""Exact published distance-weighted Tversky terms (300m = 3 cells).
https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/
"""

import numpy as np
from scipy.ndimage import distance_transform_edt


def triangular_kernel(d, R=3):
    if R <= 0:
        raise ValueError("R must be positive")
    return np.maximum(1 - np.asarray(d) / R, 0)


def contributions(pred, gt, R=3):
    pred = np.asarray(pred, dtype=np.float64)
    gt = np.asarray(gt)
    if pred.shape != gt.shape or pred.ndim != 2:
        raise ValueError("Matching 2D arrays required")
    if not np.isfinite(pred).all() or np.any((pred < 0) | (pred > 1)):
        raise ValueError("Invalid probability")
    if not np.isin(gt, [0, 1]).all():
        raise ValueError("Binary truth required")
    gt = gt.astype(bool)
    if R <= 0:
        raise ValueError("Positive kernel radius required")
    k = (
        triangular_kernel(distance_transform_edt(~gt), R)
        if gt.any()
        else np.zeros_like(pred)
    )
    best = np.zeros_like(pred)
    n, m = pred.shape
    radius = int(np.ceil(R))
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            weight = max(1 - np.hypot(dx, dy) / R, 0)
            if not weight or abs(dy) >= n or abs(dx) >= m:
                continue
            dest = (
                slice(max(0, dy), min(n, n + dy)),
                slice(max(0, dx), min(m, m + dx)),
            )
            src = (
                slice(max(0, -dy), min(n, n - dy)),
                slice(max(0, -dx), min(m, m - dx)),
            )
            np.maximum(best[dest], pred[src] * weight, out=best[dest])
    return best * gt, pred * (1 - k), (1 - best) * gt


def from_terms(tp, fp, fn):
    return tp / (tp + 0.2 * fp + 0.8 * fn + 1e-12)


def compute_dti(pred, gt, R=3, alpha=0.2, beta=0.8, eps=1e-12):
    terms = tuple(float(x.sum()) for x in contributions(pred, gt, R))
    tp, fp, fn = terms
    return tp / (tp + alpha * fp + beta * fn + eps), tp, fp, fn
