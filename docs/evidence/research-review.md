# Scientific review and decision record — 2026-10-05 (latest status v3)

## Current decision (v3 — preregistered analysis and holdout audit)

**Submission gate: CLOSED.** Keep the unique D GeoTIFF as a research/download artifact, not a recommended weekly submission. The file passes the local disk-reread contract and public-artifact uniqueness comparison, but no portal acceptance or hidden-fault score exists. Its 0.7% / 3.0-pixel / catalogue-exclusion / tip-protected final emission was not tested against a comparable current-best holdout. The earlier v2 `+0.00807` result is a catalogue-proxy feature comparison, not proof that the final TIF beats H33 or hidden test truth.

**Why no current-best comparison is available.** At pinned GEMSDOE32 commit `b63ebab7dbcf9238422ebbc2dbc4addf84bed11b`, `src/gems32/holdout.py` sets `COLLAR_PX=15` and `DOMAIN_ERODE=12`; `evidence/h33_holdout.json` describes a 30-pixel collar and 20-pixel erosion. The holdout code requires `data/external/derived_sgmc_faults_100m_u8.tif`, which is absent from that tracked tree, along with the exact derived masks/checkpoints needed for reconstruction. `evidence/live_mirror_validation.json` reports only **2/6** historical score orderings reproduced (3/6 after its prevalence calibration). It also estimates hidden-truth prevalence from prior scores. This is interesting owner-reported research, not an independently reproduced hidden-label benchmark. The public leaderboard does not expose an artifact hash tying the user-reported 0.2778 to the H33 raster.

**v3 preregistration and results.** Hypotheses J/K/L were fixed in [the preregistration](hypotheses-v3-preregistered.md) before computing their features or MINE estimates; GeoDAWN raw flight-line candidate X is explicitly blocked because its official raw files were not obtained. J's full-label MINE mean is **4.66e-05 nats**, spatial OOF mean **1.95e-05** (three seeds; shuffled null mean -2.83e-07). K: full-fit 3.32e-05, OOF 7.02e-06. The stored L values (full-fit 1.72e-05, OOF 1.69e-05) are **exploratory only**: final code review found the implemented unsigned conductivity-gradient variant differs from preregistered L's signed opposing-side transform. See [the review amendment](hypotheses-v3-review-amendment.md). J/K's results and the J comparison are unaffected. MINE numbers are marginal catalogue-label dependence estimates, not conditional value or hidden-fault information. Feature normalization uses the full footprint without labels, so preprocessing is transductive rather than fold-local and the spatial folds are not strict independent-pipeline validation. The primary paired spatial test gives J+D vs D **+0.000712 DTI**, 2/4 folds positive, 20-km block-bootstrap 95% interval **[-0.004698, +0.006037]** — **FAIL**. J+D vs the 19-band baseline is +0.008785; that gain is mostly inherited from D and does not establish J's incremental value. See [MINE v3](mine-results-v3.json), [spatial validation v3](validation-v3.json), and [slot gate](slot-gate.json).

**Three-pass review outcome.** (1) Re-read the full README/user brief and AGENTS rules, inspected the existing generator, validator, holdout receipts and feature code. (2) Added fixed J/K/L transforms, synthetic unit tests, all-footprint MINE and locked four-quadrant comparisons; all inputs and output hashes were recorded. (3) Audited sibling holdout evidence against its code; found and logged an L implementation/preregistration mismatch instead of presenting its MINE row as confirmatory; corrected the generator so it cannot mark an artifact approved; and changed the site/README status to keep the slot gate visibly closed. No new TIF or portal submission was made, and no score is claimed.

## Historical v2 result — feature-proxy evidence only; not submission validation

**New MINE screen on 9 features (5.17M rows, 60,988 positives, H(Y)=0.064129 nats, 3 seeds, 12 OOF folds, shuffled nulls):** Full-fit mean nats — F_transtensional_corridor 0.00028387 (highest), D_topographic_step_proxy 0.00014835, I_drainage_deflection_curvature 0.00012835, E_basin_concealed_coedge 6.86e-05, G_quake_fabric_lineament 7.03e-05, H_rtp_tilt_basement_step 4.54e-05, A 1.70e-05, C 1.66e-05, B 1.20e-06. OOF weighted mean: D 0.00012556 (stable positive), I 0.00011102, H 3.54e-05, E 2.81e-05, G 1.17e-05, A 4.25e-06, C 9.09e-06, B -2.16e-05 (negative), F -7.31e-05 (negative, spatial overfit). Null means ~ -4e-07, so D and I are >300× null.

**Historical validation v2 (same 4 quadrants, 1km buffer, HGB120, 0.8% density, 2.8px separation, 200k negatives, 180+ 20km blocks, 1000 bootstraps):** Baseline 0.13144859. plus_D 0.13952240 Δ+0.00807381 4/4 folds positive, 95% CI [0.00109,0.01549] excludes zero under that internal catalogue-proxy design; this did not pass the current-best competition promotion gate. plus_I 0.13387 Δ+0.00242 3/4 CI crosses zero. plus_F 0.13491 Δ+0.00346 4/4 but CI crosses zero. plus_E -0.00040 1/4. plus_D_I 0.13864 Δ+0.00719 3/4 CI [-0.00074,0.01503] crosses zero slightly. plus_all_new 0.13642 Δ+0.00497 3/4.

**What the v2 MINE screen does and does not show:** B had a near-zero marginal estimate and was not independently model-tested, so no validation failure can be attributed to it. F had the highest full-fit estimate but negative spatial OOF; its model comparison CI crossed zero despite 4/4 positive folds, consistent with spatial instability but not proving MINE caused it. D had the highest stable OOF estimate in that screen and a positive v2 catalogue-proxy comparison. This is a useful prior internal result, not a controlled estimate of hidden-fault performance or evidence that the final emitted D raster beats the current-best H33 holdout.

**Historical research artifact:** Full-data HGB 19 + D_topographic_step_proxy, 0.7% density (36,171 px), 3.0px separation, 200m catalogue exclusion with tip protection, and no prior prediction as input. Pixel-content SHA ecfbf59e2b48; 71,947 pixels differ from the H33 reference; no duplicates against 208 same-grid public raster blobs. Both zero- and NaN-outside twins pass their local contracts. This does not validate the final emission policy against a comparable current-best holdout or certify portal acceptance. Do not upload based on this result.

**Scoring mechanics, not a win forecast:** DTI = T / (0.2 T + 0.2 F + 0.8 G). A change improves DTI exactly when `(1-0.2D)ΔT > 0.2DΔF` for a fixed truth set. At D=0.2778, one unit of additional false-positive mass needs about 0.05883 coverage to break even. A sibling H28 owner analysis reported that thinning reduced kernel overlap (ρ 1.429→1.179); sparse emission is therefore a plausible hypothesis, not a causal explanation of H33's reported score. The historical D-feature result was +0.00807 on an incomplete catalogue proxy, while the final 0.7% / 3.0px / tip-protected artifact policy has not been evaluated against a compatible current-best holdout. Lowering density and retaining endpoint-near pixels are heuristic tradeoffs, not demonstrated score improvements. The public 0.3262 leader remains untested here.

## Answer: why did H33-2-B2 reach the reported 0.2778?

**Evidence separation.** The user attributes 0.2778 to GEMSDOE32 H33-2-B2. The official leaderboard shows participant extradr19 at 0.2778, but does not expose the submitted filename or raster hash. The owner site still says “UNSCORED”. Thus the score-to-file mapping is **user-reported**, not independently organizer-verified. The live leaderboard leader is **0.3262**, ahead of 0.3222 and 0.3195, as checked on October 5.

**What we can verify.** We retrieved the H33 raster (SHA-256 in the submission manifest), reviewed its owner documentation and h33 source modules, and read the official metric and staff clarification. H33 retains sparse dots from a prior field and removes predictions within two pixels (200m) of the known catalogue. The official exclusion is **pixel-exact**, not a 200m buffer. Near-catalogue pixels are still penalized when far from new-fault truth; new truth may also occur near the catalogue. H33's wider buffer is an empirical heuristic, not an official rule.

**Plausible mechanism, not a proven causal explanation.** Sparse coverage avoids repeatedly paying false-positive mass where extra pixels give little additional maximum coverage of true faults. Removing catalogue-adjacent false positives can improve credit per prediction. It can also delete genuine splays and mapped-trace corrections. Hidden truth is unavailable, and the score sequence is not a randomized controlled comparison, so exact attribution to any geological feature is impossible.

For truth count G, weighted coverage T and weighted false-positive mass F:

`D = T / (T + 0.2 F + 0.8(G-T)) = T / (0.2 T + 0.2 F + 0.8 G)`.

A change improves D exactly when `(1 - 0.2 D) ΔT > 0.2 D ΔF` (fixed truth set and positive denominators). This is the correct coupled condition; the old “each dot breaks even at 0.2 D” is only an approximation under additional assumptions. For a new unit of *false-positive* mass at D=0.2778, required additional coverage is about 0.05883. Do not confuse per-dot coverage with probability of a true pixel: one dot can cover multiple truth pixels.

**Can we exceed 0.2778 / 0.3262?** It is possible in principle; it is not demonstrated here. The ratio 0.3262/0.2778 is about 1.174, but a 17.4% score gain is NOT a proven 17.4% required gain in detector information or accuracy. DTI is nonlinear and the hidden distribution differs from the catalogue. Improving geological discrimination, localization, and nonredundant coverage is a sound route. Tuning a count or filename for uniqueness is not.

## Scientific basis and distinct hypotheses

The v1 and v2 preregistrations are preserved as historical records. The newest pre-feature preregistration with exact J/K/L transforms, rank, falsifiers and the blocked X data request is [hypotheses-v3-preregistered.md](hypotheses-v3-preregistered.md). No numerical expected improvement was invented; GeoDAWN raw line data were not downloaded or used.

USGS describes GeoDAWN magnetics as information about subsurface structure/geology and radiometrics as information about surface geology/soil composition. It records 400m flight-line spacing for Area 2 and variable terrain clearance. Therefore interpolation onto 100m cells does **not** imply 100m resolving power; east-west flight-line artifacts are a key negative control for the next session. [USGS GeoDAWN](https://www.usgs.gov/data/geodawn-airborne-magnetic-and-radiometric-surveys-northwestern-great-basin-nevada-and).

A USGS Battle Mountain study jointly models gravity, magnetics and MT, and reports correspondence between gravity-derived basement and the base of shallow conductive anomalies. That supports testing multimodal structural constraints, but does not prove that every discordance or conductive edge is a fault. [1](https://pubs.usgs.gov/publication/70271418).

Fault intersections and stepovers can concentrate geothermal fluid pathways; detailed structural characterization matters beyond merely recognizing a line on a raster. This motivates future geometry-aware tests, not a claim that our predicted dots are geothermal vents. [3](https://www.osti.gov/servlets/purl/1110517).

### Official-source backlog, not implemented or assumed obtainable

|Source|Verified public description / licence|Obtained here?|Next decision|
|---|---|---|---|
|[USGS GeoDAWN](https://doi.org/10.5066/P93LGLVQ)|USGS release page identifies flight-line CSVs, grids, radiometric/magnetic data; CC0.|Core competition mirror only; full raw survey not downloaded.|Try line-level leveling/flight-height controls before treating narrow magnetic lineaments as faults.|
|[GDR 1391](https://gdr.openei.org/submissions/1391)|Official public CC BY 4.0 compilation lists 2m temperatures, paleo features, wells/springs, seismicity and geodetics.|Metadata inspected, external ZIP bytes not acquired in this run.|Test provenance, coverage and well sampling bias before a spatial feature is proposed as ready.|
|[GDR MT conductance](https://doi.org/10.5066/P9TWT2LU)|GDR describes five depth intervals from 2–200km.|Not acquired here.|Coarse depth conductance alone cannot resolve 100m surface fault traces. Do not call the surface band a new 3D MT survey.|
|[USGS 3DEP](https://www.usgs.gov/3d-elevation-program)|Referenced by official GeoDAWN page as overlapping LiDAR acquisition.|1m tiles not downloaded in this run.|Next session prioritize selected validation blocks, tile footprints and independent scarp interpretation before region-wide training.|

Direct shell HTTPS to Dropbox and several official/raw-content hosts failed in this sandbox; verified GitHub API mirrors were obtainable. A public metadata page does not prove sandbox binary download availability. We did not propose any external-data-only idea as implementation-ready.

## MINE: what was actually estimated

The original repository's five MI figures were synthetic examples, and its “bits (approx)” output used natural logs. They are withdrawn as geological evidence.

The replacement is a 24-hidden-unit neural DV estimator implemented in NumPy with analytically tested backpropagation, bounded critic, Adam ascent, EMA denominator correction, and exact binary-label product marginal. Stratified minibatches are importance-weighted to **natural** catalogue prevalence, not an artificial 50/50 target. Each feature has three full-fit runs, three shuffled-label null fits, and twelve spatial-fold fits (three seeds × four quadrants). Full-fit evaluation visits **all 5,167,373** footprint rows, with **60,988** catalogue positives. Finite-step stochastic optimization samples from the entire training population but does not guarantee every row is seen during fitting.

The catalogue entropy is about 0.064 nats; the exact value is recorded in [mine-results.json](mine-results.json). Estimates use nats throughout. Original [MINE](https://proceedings.mlr.press/v80/belghazi18a.html) and [Poole et al. on bias/variance tradeoffs](https://proceedings.mlr.press/v97/poole19a.html) justify caution: neural estimation is not a blanket promise of lower noise. These bounded, finite-capacity critics can miss real dependence. Negative DV estimates are optimization/generalization diagnostics, not negative true MI. Small marginal MI cannot exclude synergistic interactions (XOR is a standard counterexample), and a feature's MI does not quantify incremental information conditional on existing features.

Full-label feature screening followed by testing selected features on those same validation labels would leak information. Consequently A was preregistered before MINE results and was tested unchanged. Results for B–D are descriptive research only; D needs a fresh nested/locked validation design. Four spatial-fold estimates are not a confidence interval. Globally shuffled null labels destroy spatial autocorrelation; these controls detect fitting artifacts, not spatial significance. The estimator normalizes using training-only samples, but unlabeled feature transforms use full-region statistics (transductive).

## Real validation result and gate

Four geographic quadrants, 1km training-label buffer, fixed CPU HistGradientBoosting model, fixed 0.8% emission density and 2.8-cell spacing. Model: 19 measured bands vs 19 + A. All training positives plus up to 200,000 training negatives; no random geometric pseudo-labels. Class subsampling means model scores are ranks, not calibrated probabilities. The final output is a binary confidence decision.

Pooled catalogue-proxy DTI: **0.1314376800 → 0.1337092461**, delta **+0.0022715661**. Only **2/4** folds improved. Paired 20km spatial-block bootstrap 95% interval: **[-0.0012633735, +0.0070539140]**, 180 blocks, 1,000 draws. This interval is conditional on fitted models; it omits model-refit uncertainty and is not a guarantee of independent blocks. Features with 900m Gaussian scale can retain dependency across the 1km training buffer.

**FAIL. No slot promotion.** No compatible independent “current holdout best” checkpoint existed here. The historical H33 raster used the full catalogue, so testing it on that catalogue is not an honest out-of-fold baseline. It would be especially misleading to claim success because H33's catalogue exclusion makes its catalogue DTI low. We explicitly do not make that comparison. The fresh baseline is a reproducible benchmark, not a reconstruction of the group's holdout best.

The generated final candidate uses a full-data fit and a >200m catalogue-distance exclusion before sparse packing. That final exclusion is not validated on the catalogue proxy (it removes the very positives being evaluated), so the final file has **no validated hidden-fault score**. No upload or competition slot was used.

## Audit irregularities and limitations

1. Previous generator used random lines, a simulated catalogue and sine waves labeled “MT/ASTER”. Withdrawn downloads and hashes are recorded; history remains in Git.
2. Previous holdout explicitly forced positive deltas. Replaced with real predictions and measured bootstrap uncertainty.
3. Previous prepare script silently created a random footprint. Replaced with fail-closed template validation.
4. Previous validator accepted NaN interiors using a `True` placeholder. Removed; sentinel, interior NaN, range, CRS, transform and outside rules have regression tests.
5. The mirrored “example submission” contains all 60,988 catalogue positives; it is not the empty example described in official prose. Used ONLY for grid and footprint, never as model features. This is a provenance irregularity, not proof of organizer authenticity.
6. Mirror SHA-256 agreement proves integrity against owner receipts, NOT independent organizer authentication. No DrivenData login session was available.
7. Band descriptions are not an authoritative data dictionary: `tc` says “tilt angle or total curvature”; `depth_to_base_surf` says basement while official prose says conductive base. Baseline uses band numbers, but geological interpretation of ambiguous fields needs the original metadata. H38-B remains speculative for this reason.
8. Four hypotheses are novel relative to the original synthetic repo; related physics/transforms already exist in sibling work. We reviewed 36 entry pages plus selected H33 source modules, not every line of every sibling repository. No worldwide novelty claim.
9. Exact cause of the user's portal range error is unknown without the rejected file/log. Actual NaN, infinity, out-of-range values and feature nodata sentinels are checked here. A nodata tag alone was not proven to cause that error.
10. Official prose says null/NaN outside. The primary all-finite/zero encoding matches the H33 reference's zero-outside encoding and avoids non-finite values; whether the portal accepts it is untested. A NaN-outside twin is also provided. Both pass their explicit local contracts. Portal acceptance is NOT certified.
11. Direct hidden labels, private-test scores, competition account access and geological field confirmation remain unavailable. CPU training worked; “GPU required” was false for this implementation.
12. The record includes historical user scores that cannot be tied to public file hashes independently; no invented forecasts or inferred hidden fault counts are used.

## Three review passes

- Pass 1: recover real data; withdraw synthetic claims; preregister hypotheses; implement/test actual features, MINE, spatial models, metric and new artifact.
- Pass 2: check derivative gradients, empty-truth metric behavior, absent data, sentinel/NaN/transform failures; verify finite artifact bytes; audit label-derived template, natural-prevalence MINE, selection leakage and geometry.
- Pass 3: independently compare raster content across prior public artifacts; check web download paths and archive membership; run local tests; confirm the closed gate and no leaderboard promise; inspect the generated site. PR checks and Pages deployment must be verified after publication.

## Next session priorities

1. Freeze nested spatial splits BEFORE exploring D. Refit the strongest prior method fold-locally on exactly the same splits; use bootstrap of spatial blocks plus repeated model fits.
2. Use D's small but consistent marginal signal as a hypothesis, not as established incremental information. Compare joint/conditional information with interactions; add spatially preserved null controls and critic-capacity/step convergence checks.
3. Before any further L experiment, freeze an exact versioned side-contrast transform, sign convention and sampling distance; the existing L MINE values are exploratory only. See [the code-review amendment](hypotheses-v3-review-amendment.md).
4. Obtain genuine organizer feature metadata and the prior detector's exact raw-data recipe. Resolve `tc`/conductive-base semantics and template provenance.
5. Test flight-line orientation negatives, gravity/magnetic lithologic-contact confounders, and genuine 1m LiDAR on manageable blocks. Genuine structural specificity is more promising than arbitrary dot counts.
6. Calibrate an off-catalogue analogue using faults withheld from BOTH training and exclusion maps, with source-vector connected-component buffering; do not automatically equate this to hidden discoveries.
7. Only after a valid current-best comparison passes should the account holder authorize a weekly slot. Preserve final-round discovery value; no guaranteed prize or score is possible.

## Rules and AI disclosure

The complete parsed September 2026 official rules were read (all seven text chunks). Sections 3.2–3.5 specify three submissions per week, one final selection across both rounds, reproducible code/resources and disclosure of generative-AI assistance in the narrative. This project used an Arena.ai coding assistant for research synthesis, source review, code generation, testing and documentation. Raster predictions were computed by the documented measured-data statistical pipeline, not generated as imagined geological imagery. The original synthetic artifacts were withdrawn. The account holder must truthfully certify their own eligibility; this agent cannot certify citizenship, team status or legal rights on their behalf.
