# Preregistration v2 — 2026-10-05 (expanded after first MINE screen)

Evidence status: hypotheses, not geological discoveries. Ranking below combines expert judgement, MINE full-label screening (5.17M rows, 60,988 positives, H(Y)=0.064129 nats), and spatial holdout validation (4 quadrants, 1km buffer, HGB120, 0.8% density, 2.8px separation). No new external data required: all layers are in the 19-band checksum-restored mirror. GEMSDOE32 already implements multiscale Hessians, orientation consensus, drainage collinearity, conductive boundaries and clay-cap breach; distinctions below are narrower than claiming these physics were never tried anywhere in the 36 sibling repos.

## New candidates E–I (not in original 4)

| Rank / ID | Layers & exact transform | Physical signature | Why potentially unmapped; falsifier | Difference vs this repo & cost | Expected ΔDTI (catalogue-proxy) & MINE |
|---|---|---|---|---|---|
| 1 / E_basin_concealed_coedge | tmi, iso_grav_anom, det_elev_slope, cond_surf. Gaussian gradients sigma 2 & 5 for mag and gravity; co-edge = sqrt(unit(|∇mag2|)*unit(|∇mag5|)*unit(|∇grav2|)*unit(|∇grav5|))^(1/2); low-slope gate = 1/(1+unit(|slope|)); cond residual = (cond - Gauss9(cond))/std9 clipped to positive halo; final = coedge * lowSlope * (0.5+0.5*halo) | Co-located magnetic & gravity edges in low relief with conductive halo — buried basin fault with fluid alteration, no surface scarp | Basin fill hides scarps; USGS mapping focuses on range fronts. Lithologic contacts and radiometric soil changes mimic. Fails if improvement only on rugged fronts or cond halo is saline clay not fault. | A tests magnetic persistence alone; B tests discordance not agreement; C tests cond edge * depth edge not mag+grav. E tests mag+grav *agreement* gated by low relief + cond halo. Low cost (minutes CPU, Gaussian filters). | MINE full-fit mean 6.86e-05 nats, OOF 2.81e-05 nats (positive but small). Validation: -0.00040 ΔDTI, 1/4 folds positive, CI crosses zero. Not validated. |
| 2 / F_transtensional_corridor | geod_shearrate, geod_dilaterate, geod_2ndinv, det_elev. s=unit(|shear|), d=unit(|dilat|), sec=unit(2ndinv); curv=unit(|Laplacian(elev, sigma2)|); product sqrt(s*d)*sec/(1+curv) and sqrt(s*d*sec*curv) averaged | Transtensional pull-apart: high shear + dilatation + second invariant + curvature — transfer fault / accommodation zone in Walker Lane | Strike-slip with small vertical component missed in DEM-only mapping, but active strain from GPS/InSAR. Non-tectonic subsidence and landslide curvature are confounders. | Previous factorial (GEMSDOE25) found strain family inert alone (-0.0109) but did not test interaction with curvature. This tests interaction. Low cost. | MINE full-fit mean 2.84e-04 nats (highest), OOF -7.31e-05 (negative, spatial overfit). Validation: +0.00347 ΔDTI, 4/4 folds positive but CI [-0.00217,0.00947] crosses zero. Promising but not robust. |
| 3 / G_quake_fabric_lineament | ieq_n100a15 (earthquake intensity), deq_n100a15 (distance to quake), tmi_hg, tmi_vg. Fabric = unit(sqrt(|∇hg|^2+|∇vg|^2)); eq_density=unit(ieq), eq_close=1/(1+unit(deq)); final = sqrt(eq_density*eq_close)*fabric | Microseismic lineament aligned with magnetic fabric — blind fault with small-magnitude seismicity | Blind faults may have microseismicity but no surface scarp; USGS catalogue may miss them due to cover. Location uncertainty and aftershock clustering mimic. | Earthquake density not used in original 4; previous strain family included seismicity but not oriented with magnetic fabric. Medium cost (structure tensor). | MINE 7.03e-05 full-fit, OOF 1.17e-05. Not yet validated in v2 (but included in all_new). |
| 4 / H_rtp_tilt_basement_step | rtp, tc (tilt angle), depth_to_base_surf, iso_grav_anom_hg. tc_edge = unit(|∇tc sigma2|); depth_edge = unit(|∇depth sigma3|); grav_hg = unit(|iso_grav_hg|); final = sqrt(tc_edge*depth_edge)*grav_hg | RTP tilt zero-crossing + basement step + gravity HG — deep basement contact with sharp magnetic contact | Deep basement faults with no surface expression but sharp magnetic contact; detrended elevation may be flat. Tilt derivative can also mark intrusive contacts, not faults. | A uses TMI gradient agreement across scales, not RTP tilt zero-crossing. H uses tilt derivative edge. Low cost. | MINE 4.54e-05 full-fit, OOF 3.55e-05. Included in all_new, not solo validated. |
| 5 / I_drainage_deflection_curvature | det_elev, iso_grav_anom. Second derivatives gxx,gyy,gxy sigma1; curvature mag sqrt(gxx^2+2gxy^2+gyy^2); curv_norm=unit(|curv|); grav_edge=unit(|∇grav sigma2|); final=curv_norm*grav_edge | Curvature-controlled drainage deflection × gravity edge — subtle geomorphic offset in alluvial fans | Alluvial fan drainage deflected by fault, missed in 100m DEM. Roads and lithologic benches mimic. 100m grid limits resolution; 1m LiDAR would be better (USGS 3DEP, free but not downloaded here). | D is step proxy (grad/|Laplacian|) × mag edge; I is curvature magnitude × grav edge, different physics (gravity not mag) and different morphology (curvature not step). Medium cost (second derivatives). | MINE full-fit 1.28e-04 nats, OOF 1.11e-04 nats (second highest stable). Validation: +0.00242 ΔDTI, 3/4 folds, CI crosses zero. Second best after D. |

## Ranking by expected DTI improvement (catalogue-proxy) and implementation cost

Feasibility-adjusted ranking (expert + MINE OOF + validation):

1. **D_topographic_step_proxy** (original) — MINE OOF 0.000125 nats, validation +0.00807 ΔDTI, 4/4 folds, CI [0.00109,0.01549] excludes zero. **VALIDATED**. Low cost. Top.
2. **I_drainage_deflection_curvature** — OOF 0.000111 nats, validation +0.00242, 3/4 folds, CI crosses zero. Medium cost, second.
3. **F_transtensional_corridor** — full-fit highest (0.000283) but OOF negative, validation +0.00347 4/4 but CI crosses zero. Low cost, third (needs spatial regularization).
4. **E_basin_concealed_coedge** — OOF positive small, validation negative. Low cost, fourth.
5. **G, H** — smaller MI, not solo validated, medium/low cost, lower expected.

## Locked experiment v2

- Compute all nine surfaces, no catalogue or prior submission as feature inputs.
- MINE: same protocol as v1 (DV bound, natural prevalence, exact binary product marginal, EMA, 3 seeds, 4 spatial folds, 1 shuffled null per feature).
- Validation v2: test baseline_19 vs plus_D, plus_I, plus_E, plus_F, plus_D_I, plus_D_E_I, plus_all_new (6 new features) using same 4 quadrants, 1km buffer, HGB120, 0.8% density, 2.8px separation. No tuning after seeing results.
- Result: D alone is best and passes strict gate (4/4 folds, CI>0). D+I is second but CI crosses zero.
- Generate new submission: full-data HGB 19+D, 0.7% density, 3.0px separation, 200m catalogue exclusion with tip protection (retain within 3px of fault endpoints). No prior prediction as input. Second candidate D+I 0.65% density.
- Uniqueness: pixel-content digest, byte digest, compare against 208 same-grid prior rasters.

## External data check

- USGS 3DEP 1m LiDAR (https://www.usgs.gov/3d-elevation-program) — free, official, could improve D and I (100m grid limits scarp resolution). Not downloaded in this run due to tile volume; next session prioritize selected validation blocks.
- USGS GeoDAWN raw flight-line CSVs (https://doi.org/10.5066/P93LGLVQ) — CC0, could test east-west acquisition artifacts. Not downloaded; core mirror only used.
- GDR 1391 (https://gdr.openei.org/submissions/1391) — CC BY 4.0, 2m temps, wells, seismicity. Metadata inspected, ZIP not acquired; sampling bias needs check before use.

All ideas use only 19-band mirror; no invented ASTER/MT fields.

## Limitations

- MINE full-fit can be optimistic; OOF is diagnostic not unbiased MI; globally shuffled null destroys spatial autocorrelation.
- Catalogue labels are incomplete positive/unlabelled; zero is not confirmed absence; hidden new-fault truth unavailable.
- D's step proxy uses gradient/|Laplacian| ratio, not explicit asymmetric signed profile; name corrected.
- Tip protection uses 8-neighbor count for endpoints, approximate; true fault topology from vector data (NBMG QFaults REST) could be better but not used here.
- Final submission has no validated hidden-fault score; catalogue-proxy improvement does not guarantee leaderboard gain.
