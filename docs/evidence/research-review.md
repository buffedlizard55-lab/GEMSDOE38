# Scientific review and decision record — 2026-10-05

## Answer: why did H33-2-B2 reach the reported 0.2778?

**Evidence separation.** The user attributes 0.2778 to GEMSDOE32 H33-2-B2. The official leaderboard shows participant extradr19 at 0.2778, but does not expose the submitted filename or raster hash. The owner site still says “UNSCORED”. Thus the score-to-file mapping is **user-reported**, not independently organizer-verified. The live leaderboard leader is **0.3262**, ahead of 0.3222 and 0.3195, as checked on October 5.

**What we can verify.** We retrieved the H33 raster (SHA-256 in the submission manifest), reviewed its owner documentation and h33 source modules, and read the official metric and staff clarification. H33 retains sparse dots from a prior field and removes predictions within two pixels (200m) of the known catalogue. The official exclusion is **pixel-exact**, not a 200m buffer. Near-catalogue pixels are still penalized when far from new-fault truth; new truth may also occur near the catalogue. H33's wider buffer is an empirical heuristic, not an official rule.

**Plausible mechanism, not a proven causal explanation.** Sparse coverage avoids repeatedly paying false-positive mass where extra pixels give little additional maximum coverage of true faults. Removing catalogue-adjacent false positives can improve credit per prediction. It can also delete genuine splays and mapped-trace corrections. Hidden truth is unavailable, and the score sequence is not a randomized controlled comparison, so exact attribution to any geological feature is impossible.

For truth count G, weighted coverage T and weighted false-positive mass F:

`D = T / (T + 0.2 F + 0.8(G-T)) = T / (0.2 T + 0.2 F + 0.8 G)`.

A change improves D exactly when `(1 - 0.2 D) ΔT > 0.2 D ΔF` (fixed truth set and positive denominators). This is the correct coupled condition; the old “each dot breaks even at 0.2 D” is only an approximation under additional assumptions. For a new unit of *false-positive* mass at D=0.2778, required additional coverage is about 0.05883. Do not confuse per-dot coverage with probability of a true pixel: one dot can cover multiple truth pixels.

**Can we exceed 0.2778 / 0.3262?** It is possible in principle; it is not demonstrated here. The ratio 0.3262/0.2778 is about 1.174, but a 17.4% score gain is NOT a proven 17.4% required gain in detector information or accuracy. DTI is nonlinear and the hidden distribution differs from the catalogue. Improving geological discrimination, localization, and nonredundant coverage is a sound route. Tuning a count or filename for uniqueness is not.

## Scientific basis and distinct hypotheses

The four preregistered hypotheses, specific layers, signatures, missing-catalogue argument, falsifiers and qualitative opportunity/cost ranking are in [hypotheses-preregistered.md](hypotheses-preregistered.md). No numerical expected improvement was invented. All inputs are available in the measured 19-band mirror; no ASTER, InSAR or MT external volume was secretly simulated.

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
10. Official prose says null/NaN outside. The primary all-finite/zero encoding matches the user's reportedly accepted H33 style and avoids NaN range checks; a NaN-outside twin is also provided. Both pass their explicit local contracts. Portal acceptance is NOT certified.
11. Direct hidden labels, private-test scores, competition account access and geological field confirmation remain unavailable. CPU training worked; “GPU required” was false for this implementation.
12. The record includes historical user scores that cannot be tied to public file hashes independently; no invented forecasts or inferred hidden fault counts are used.

## Three review passes

- Pass 1: recover real data; withdraw synthetic claims; preregister hypotheses; implement/test actual features, MINE, spatial models, metric and new artifact.
- Pass 2: check derivative gradients, empty-truth metric behavior, absent data, sentinel/NaN/transform failures; verify finite artifact bytes; audit label-derived template, natural-prevalence MINE, selection leakage and geometry.
- Pass 3: independently compare raster content across prior public artifacts; check web download paths and archive membership; run CI; confirm closed promotion gate and no leaderboard promise; inspect PR and Pages deployment.

## Next session priorities

1. Freeze nested spatial splits BEFORE exploring D. Refit the strongest prior method fold-locally on exactly the same splits; use bootstrap of spatial blocks plus repeated model fits.
2. Use D's small but consistent marginal signal as a hypothesis, not as established incremental information. Compare joint/conditional information with interactions; add spatially preserved null controls and critic-capacity/step convergence checks.
3. Obtain genuine organizer feature metadata and the prior detector's exact raw-data recipe. Resolve `tc`/conductive-base semantics and template provenance.
4. Test flight-line orientation negatives, gravity/magnetic lithologic-contact confounders, and genuine 1m LiDAR on manageable blocks. Genuine structural specificity is more promising than arbitrary dot counts.
5. Calibrate an off-catalogue analogue using faults withheld from BOTH training and exclusion maps, with source-vector connected-component buffering; do not automatically equate this to hidden discoveries.
6. Only after a valid current-best comparison passes should the account holder authorize a weekly slot. Preserve final-round discovery value; no guaranteed prize or score is possible.

## Rules and AI disclosure

The complete parsed September 2026 official rules were read (all seven text chunks). Sections 3.2–3.5 specify three submissions per week, one final selection across both rounds, reproducible code/resources and disclosure of generative-AI assistance in the narrative. This project used an Arena.ai coding assistant for research synthesis, source review, code generation, testing and documentation. Raster predictions were computed by the documented measured-data statistical pipeline, not generated as imagined geological imagery. The original synthetic artifacts were withdrawn. The account holder must truthfully certify their own eligibility; this agent cannot certify citizenship, team status or legal rights on their behalf.
