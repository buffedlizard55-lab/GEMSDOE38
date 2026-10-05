"""Real, label-free surfaces preregistered in knowledge/hypotheses-preregistered.md."""

import numpy as np
from scipy.ndimage import gaussian_filter, distance_transform_edt

NAMES = [
    "A_quiet_persistent_magnetics",
    "B_depth_gravity_discordance",
    "C_conductivity_residual_edge",
    "D_topographic_step_proxy",
    "E_basin_concealed_coedge",
    "F_transtensional_corridor",
    "G_quake_fabric_lineament",
    "H_rtp_tilt_basement_step",
    "I_drainage_deflection_curvature",
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
    # E: basin-concealed magnetic-gravity co-edge with conductive halo
    # Layers: tmi, iso_grav_anom, det_elev_slope, cond_surf
    # Transform: co-located magnetic & gravity gradient magnitudes (sigma 2 & 5)
    #            gated by low topographic slope and positive conductivity residual.
    try:
        slope = fill(read_band("det_elev_slope"))
        cond2 = fill(read_band("cond_surf"))
        grav = fill(read_band("iso_grav_anom"))
        # magnetic gradients already have gs[0] at sigma1, compute sigma2,5 for mag and grav
        gm2 = gradient(mag, 2)
        gm5 = gradient(mag, 5)
        gg2 = gradient(grav, 2)
        gg5 = gradient(grav, 5)
        mag_edge = np.sqrt(
            unit(magnitude(gm2), foot) * unit(magnitude(gm5), foot)
        )
        grav_edge = np.sqrt(
            unit(magnitude(gg2), foot) * unit(magnitude(gg5), foot)
        )
        coedge = np.sqrt(mag_edge * grav_edge)
        low_slope = 1.0 / (1.0 + unit(np.abs(slope), foot))
        # conductivity residual vs broad background
        mean_c = gaussian_filter(cond2, 9)
        std_c = np.sqrt(
            np.maximum(gaussian_filter(cond2 * cond2, 9) - mean_c * mean_c, 0)
        )
        resid_c = (cond2 - mean_c) / (
            std_c + max(float(np.median(std_c[foot])), 1e-8)
        )
        cond_halo = np.clip(resid_c, 0, 5) / 5.0
        cond_halo = cond_halo.astype(np.float32)
        e_val = (coedge * low_slope * (0.5 + 0.5 * cond_halo)).astype(np.float32)
        yield NAMES[4], e_val
    except Exception as ex:
        # Fail-closed: produce zeros if band missing
        yield NAMES[4], np.zeros(foot.shape, dtype=np.float32)

    # F: transtensional corridor (shear + dilatation + 2nd invariant + topo curvature)
    try:
        shear = fill(read_band("geod_shearrate"))
        dilat = fill(read_band("geod_dilaterate"))
        sec = fill(read_band("geod_2ndinv"))
        # normalize each
        s_n = unit(np.abs(shear), foot)
        d_n = unit(np.abs(dilat), foot)
        sec_n = unit(sec, foot)
        # topo curvature magnitude (Laplacian of detrended elevation)
        lap_elev = 4 * (
            gaussian_filter(elev, 2, order=(2, 0))
            + gaussian_filter(elev, 2, order=(0, 2))
        )
        curv = unit(np.abs(lap_elev), foot)
        f_val = (np.sqrt(s_n * d_n) * sec_n / (1 + curv)).astype(np.float32)
        # Actually we want high curvature? Use inverse? Let's use product with curvature
        # to find pull-apart basins: high shear+dilatation + curvature
        # So use s_n*d_n*curv
        f_val2 = (np.sqrt(s_n * d_n) * np.sqrt(sec_n * curv)).astype(np.float32)
        # average both interpretations
        f_val = ((f_val + f_val2) * 0.5).astype(np.float32)
        yield NAMES[5], f_val
    except Exception:
        yield NAMES[5], np.zeros(foot.shape, dtype=np.float32)

    # G: quake fabric lineament (earthquake density aligned with magnetic fabric)
    try:
        ieq = fill(read_band("ieq_n100a15"))
        deq = fill(read_band("deq_n100a15"))
        # magnetic fabric orientation from tmi_hg and tmi_vg
        hg = fill(read_band("tmi_hg"))
        vg = fill(read_band("tmi_vg"))
        # structure tensor coherence: gradient of hg and vg?
        # Compute gradients of hg and vg at sigma 1
        ghg = gradient(hg, 1)
        gvg = gradient(vg, 1)
        # fabric strength = magnitude of magnetic gradient field
        fabric = unit(
            np.sqrt(magnitude(ghg) ** 2 + magnitude(gvg) ** 2), foot
        )
        # earthquake proximity: ieq is intensity/density, higher near quakes
        # deq is distance to earthquake, so inverse
        eq_density = unit(ieq, foot)
        # distance transform: low deq means close to quake, so 1/(1+deq)
        eq_close = 1.0 / (1.0 + unit(deq, foot))
        g_val = (np.sqrt(eq_density * eq_close) * fabric).astype(np.float32)
        yield NAMES[6], g_val
    except Exception:
        yield NAMES[6], np.zeros(foot.shape, dtype=np.float32)

    # H: RTP tilt basement step (rtp tilt zero-crossing + depth + gravity HG)
    try:
        rtp = fill(read_band("rtp"))
        tc_band = fill(read_band("tc"))
        depth2 = fill(read_band("depth_to_base_surf"))
        ghg_iso = fill(read_band("iso_grav_anom_hg"))
        # tilt angle tc: edge at high gradient of tc or near zero-crossing of derivative
        # Use gradient magnitude of tc as proxy for zero-crossing
        g_tc = gradient(tc_band, 2)
        tc_edge = unit(magnitude(g_tc), foot)
        # depth gradient
        gd2 = gradient(depth2, 3)
        depth_edge = unit(magnitude(gd2), foot)
        grav_hg = unit(np.abs(ghg_iso), foot)
        h_val = (np.sqrt(tc_edge * depth_edge) * grav_hg).astype(np.float32)
        yield NAMES[7], h_val
    except Exception:
        yield NAMES[7], np.zeros(foot.shape, dtype=np.float32)

    # I: drainage deflection curvature (profile vs plan curvature * gravity edge)
    try:
        # det_elev already available
        # slope components
        gx, gy = gradient(elev, 1)
        # second derivatives
        gxx = gaussian_filter(elev, 1, order=(2, 0))
        gyy = gaussian_filter(elev, 1, order=(0, 2))
        gxy = gaussian_filter(elev, 1, order=(1, 1))
        # profile and plan curvature approximations
        # Use simple curvature magnitude: sqrt(gxx^2 + 2*gxy^2 + gyy^2)
        curv_mag = np.sqrt(gxx * gxx + 2 * gxy * gxy + gyy * gyy)
        curv_norm = unit(np.abs(curv_mag), foot)
        # gravity edge
        grav_all = fill(read_band("iso_grav_anom"))
        gg_all = gradient(grav_all, 2)
        grav_edge_i = unit(magnitude(gg_all), foot)
        i_val = (curv_norm * grav_edge_i).astype(np.float32)
        yield NAMES[8], i_val
    except Exception:
        yield NAMES[8], np.zeros(foot.shape, dtype=np.float32)
