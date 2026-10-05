"""Real, label-free surfaces preregistered in knowledge/hypotheses-preregistered.md."""

import numpy as np
from scipy.ndimage import gaussian_filter, distance_transform_edt

NAMES = [
    "A_quiet_persistent_magnetics",
    "B_depth_gravity_discordance",
    "C_conductivity_residual_edge",
    "D_topographic_step_proxy",
]


def fill(a):
    ok = np.isfinite(a)
    if not ok.any():
        raise ValueError("No valid feature cells")
    # Nearest measured values, not a constant cliff at footprint edges.
    if ok.all():
        return a.astype(np.float32, copy=True)
    idx = distance_transform_edt(~ok, return_distances=False, return_indices=True)
    return a[tuple(idx)].astype(np.float32)


def gradient(a, sigma):
    return (
        gaussian_filter(a, sigma, order=(1, 0)) * sigma,
        gaussian_filter(a, sigma, order=(0, 1)) * sigma,
    )


def magnitude(g):
    return np.hypot(*g)


def agreement(a, b):
    return np.clip(
        (a[0] * b[0] + a[1] * b[1]) / (magnitude(a) * magnitude(b) + 1e-10), -1, 1
    )


def unit(a, foot):
    # Label-free transductive scaling, no fault-label statistics.
    q = max(float(np.quantile(a[foot], 0.95)), 1e-10)
    return np.clip(a / q, 0, 5).astype(np.float32)


def build(read_band, foot):
    mag = fill(read_band("tmi"))
    elev = fill(read_band("det_elev"))
    gs = [gradient(mag, s) for s in (1, 3, 9)]
    persist = np.maximum(agreement(gs[0], gs[1]), 0) * np.maximum(
        agreement(gs[1], gs[2]), 0
    )
    amp = (
        unit(magnitude(gs[0]), foot)
        * unit(magnitude(gs[1]), foot)
        * unit(magnitude(gs[2]), foot)
    ) ** (1 / 3)
    rough = np.sqrt(
        np.maximum(gaussian_filter(elev * elev, 9) - gaussian_filter(elev, 9) ** 2, 0)
    )
    yield NAMES[0], (amp * persist / (1 + unit(rough, foot))).astype(np.float32)
    depth = fill(read_band("depth_to_base_surf"))
    gravity = fill(read_band("iso_grav_anom"))
    gd, gg = gradient(depth, 3), gradient(gravity, 3)
    yield (
        NAMES[1],
        (
            np.sqrt(unit(magnitude(gd), foot) * unit(magnitude(gg), foot))
            * (1 - agreement(gd, gg) ** 2)
        ).astype(np.float32),
    )
    cond = fill(read_band("cond_surf"))
    mean = gaussian_filter(cond, 9)
    std = np.sqrt(np.maximum(gaussian_filter(cond * cond, 9) - mean * mean, 0))
    residual = (cond - mean) / (std + max(float(np.median(std[foot])), 1e-8))
    yield (
        NAMES[2],
        (
            unit(magnitude(gradient(residual, 1)), foot) * unit(magnitude(gd), foot)
        ).astype(np.float32),
    )
    grad = magnitude(gradient(elev, 2))
    lap = 4 * (
        gaussian_filter(elev, 2, order=(2, 0)) + gaussian_filter(elev, 2, order=(0, 2))
    )
    yield (
        NAMES[3],
        (
            unit(grad, foot)
            / (1 + unit(np.abs(lap), foot))
            * unit(magnitude(gs[0]), foot)
        ).astype(np.float32),
    )
