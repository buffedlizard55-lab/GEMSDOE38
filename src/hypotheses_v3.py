"""Label-free v3 candidate features J/K and the exploratory unsigned L variant.

A final review found that the as-coded L variant does not implement the signed
opposing-side transform in the L preregistration; see the review amendment.
All transforms use measured input bands and footprint-only normalization. No
labels, catalogue distances, prior candidate rasters, or hidden labels enter.
The simple Gaussian derivatives and sampling operate on the 100 m grid; they
must not be interpreted as 100 m resolving power for the source surveys.
"""

import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates

from src.hypotheses import agreement, fill, gradient, magnitude, unit

V3_NAMES = [
    "J_asymmetric_magnetic_flank",
    "K_multiscale_crossfield_junction",
    "L_unsigned_basin_depth_gravity_conductivity_gradient",
]


def _positive_local_residual(a, foot, sigma=9.0):
    """Bounded positive departure from a broad local mean, in [0, 1]."""
    mean = gaussian_filter(a, sigma)
    std = np.sqrt(np.maximum(gaussian_filter(a * a, sigma) - mean * mean, 0))
    scale = max(float(np.median(std[foot])), 1e-8)
    z = (a - mean) / (std + scale)
    return (np.clip(z, 0, 5) / 5.0).astype(np.float32)


def _relief_gate(slope, foot):
    """Weak, label-free downweighting of steep terrain: 1/(1+unit(|slope|))."""
    return (1.0 / (1.0 + unit(np.abs(slope), foot))).astype(np.float32)


def _profile_asymmetry(a, sigma, foot, offset=2.0, chunk_rows=128):
    """Absolute flank-slope contrast along smoothed-field gradient normals.

    At every pixel, sample the Gaussian-smoothed scalar field at +/- ``offset``
    cells along its gradient normal. Compare the two absolute one-sided slopes.
    The result is in [0, 1]. Row chunks bound coordinate-array memory.
    """
    smoothed = gaussian_filter(a, sigma)
    gy = gaussian_filter(a, sigma, order=(1, 0)) * sigma
    gx = gaussian_filter(a, sigma, order=(0, 1)) * sigma
    norm = np.hypot(gy, gx)
    ny = np.divide(gy, norm, out=np.zeros_like(gy), where=norm > 1e-10)
    nx = np.divide(gx, norm, out=np.zeros_like(gx), where=norm > 1e-10)
    h, w = a.shape
    cols = np.arange(w, dtype=np.float32)[None, :]
    out = np.zeros((h, w), dtype=np.float32)
    for start in range(0, h, chunk_rows):
        stop = min(start + chunk_rows, h)
        rows = np.arange(start, stop, dtype=np.float32)[:, None]
        ny0 = ny[start:stop]
        nx0 = nx[start:stop]
        plus = map_coordinates(
            smoothed,
            [rows + offset * ny0, cols + offset * nx0],
            order=1,
            mode="nearest",
            prefilter=False,
        )
        minus = map_coordinates(
            smoothed,
            [rows - offset * ny0, cols - offset * nx0],
            order=1,
            mode="nearest",
            prefilter=False,
        )
        center = smoothed[start:stop]
        slope_plus = np.abs(plus - center) / offset
        slope_minus = np.abs(center - minus) / offset
        asym = np.abs(slope_plus - slope_minus) / (
            slope_plus + slope_minus + 1e-8
        )
        out[start:stop] = np.clip(asym, 0, 1).astype(np.float32)
    out[~foot] = 0
    return out


def _junctionness(a, sigma):
    """Low-eigenvalue fraction of a local 2-D gradient structure tensor."""
    gy, gx = gradient(a, sigma)
    jxx = gaussian_filter(gx * gx, sigma)
    jyy = gaussian_filter(gy * gy, sigma)
    jxy = gaussian_filter(gx * gy, sigma)
    trace = jxx + jyy
    discriminant = np.sqrt(np.maximum((jxx - jyy) ** 2 + 4 * jxy * jxy, 0))
    low = np.maximum((trace - discriminant) * 0.5, 0)
    high = np.maximum((trace + discriminant) * 0.5, 0)
    return np.clip(2 * low / (low + high + 1e-12), 0, 1).astype(np.float32)


def _projected_magnitude(g, normal):
    """Absolute gradient component along a vector normal; sign is discarded."""
    return np.abs(g[0] * normal[0] + g[1] * normal[1])


def build_v3(read_band, foot):
    """Yield fixed-order J/K and exploratory unsigned L; errors fail rather than zero-fill."""
    if foot.ndim != 2 or not foot.any():
        raise ValueError("A nonempty 2-D footprint is required")

    tmi = fill(read_band("tmi"))
    gravity = fill(read_band("iso_grav_anom"))
    conductivity = fill(read_band("cond_surf"))
    slope = fill(read_band("det_elev_slope"))
    depth = fill(read_band("depth_to_base_surf"))
    relief = _relief_gate(slope, foot)
    halo = _positive_local_residual(conductivity, foot)

    # J: asymmetric magnetic flank profile, corroborated by a gravity edge and
    # a bounded positive conductivity residual; weak relief gate is fixed.
    gm2, gm5 = gradient(tmi, 2), gradient(tmi, 5)
    mag_edge2 = unit(magnitude(gm2), foot)
    mag_edge5 = unit(magnitude(gm5), foot)
    asym2 = _profile_asymmetry(tmi, 2, foot)
    asym5 = _profile_asymmetry(tmi, 5, foot)
    grav_edge3 = unit(magnitude(gradient(gravity, 3)), foot)
    j = (
        np.sqrt(mag_edge2 * mag_edge5)
        * np.sqrt(asym2 * asym5)
        * np.sqrt(grav_edge3)
        * (0.5 + 0.5 * halo)
        * relief
    ).astype(np.float32)
    j[~foot] = 0
    yield V3_NAMES[0], j

    # K: edge strength gated by junctionness that persists in magnetic and
    # gravity structure tensors at both preregistered scales.
    gg2, gg5 = gradient(gravity, 2), gradient(gravity, 5)
    grav_edge2 = unit(magnitude(gg2), foot)
    grav_edge5 = unit(magnitude(gg5), foot)
    mag_coedge = np.sqrt(mag_edge2 * mag_edge5)
    grav_coedge = np.sqrt(grav_edge2 * grav_edge5)
    junc = [
        _junctionness(tmi, 2),
        _junctionness(tmi, 5),
        _junctionness(gravity, 2),
        _junctionness(gravity, 5),
    ]
    k = (
        np.sqrt(mag_coedge * grav_coedge)
        * np.power(np.maximum(junc[0] * junc[1] * junc[2] * junc[3], 0), 0.25)
    ).astype(np.float32)
    k[~foot] = 0
    yield V3_NAMES[1], k

    # Exploratory L as coded: co-polarized basement-depth/gravity gradients;
    # unsigned conductivity-residual gradient magnitude projected on the
    # basement normal. This is not the preregistered signed opposing-side L.
    gd = gradient(depth, 3)
    gg = gradient(gravity, 3)
    depth_mag = magnitude(gd)
    normal = (
        np.divide(gd[0], depth_mag + 1e-10),
        np.divide(gd[1], depth_mag + 1e-10),
    )
    cond_mean = gaussian_filter(conductivity, 9)
    cond_residual = conductivity - cond_mean
    cond_grad = gradient(cond_residual, 3)
    cond_side = unit(_projected_magnitude(cond_grad, normal), foot)
    polarity = np.maximum(agreement(gd, gg), 0)
    coedge = np.sqrt(unit(depth_mag, foot) * unit(magnitude(gg), foot))
    l = (coedge * polarity * (0.5 + 0.5 * cond_side) * relief).astype(np.float32)
    l[~foot] = 0
    yield V3_NAMES[2], l
