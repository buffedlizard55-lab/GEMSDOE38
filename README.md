# GEMSDOE38 — Unique TIF Submission for DOE GEMS Prize

## Prompt (Must Read Every Time)

Review the repo.

THE FOLLOWING IS THE HIGHEST URGENCY AND MUST BE FOLLOWED!

MUST GENERATE A UNIQUE TIF SUBMISSION FOR THE COMPETITION.  DO NOT COPY A PREVIOUS SUBMISSION UNLESS IT'S FOR LEARNING AND EDUCATION.  BUT WE MUST GENERATE A UNIQUE TIF SUBMISSION.

There should be an easy to download submission tif file as described by the prompt.

Quantify what a feature adds with an information-theoretic estimator, not a noisy single-number ablation. With faults covering roughly 1% of the area, a holdout ablation — add a feature, rerun, see if DTI moves — runs on so few positive examples that the resulting delta is itself noisy, easily mistaken for signal or for nothing. Mutual information directly measures how much a feature's value reduces uncertainty about the true label, independent of whether any particular model exploits that relationship well, and Belghazi, Baratin, Rajeswar, Ozair, Bengio, Courville, and Hjelm's MINE estimator (ICML, 2018) makes this computable for exactly this kind of high-dimensional, continuous feature. Compute MINE-estimated mutual information between each candidate feature and the true label on the full label set, not only the small ablation holdout, and use it as a far-less-noisy first-pass filter — a feature with near-zero estimated mutual information is unlikely to earn back a submission slot no matter how the model is tuned around it, and this tells you before spending the compute to find out the hard way.

## Core Values

Maximize P(Win) — “Maximize the Probability of Winning”: our decision making framework. In every decision, we weigh tradeoffs, assess risk, and choose the path that maximizes the probability that Arena succeeds. We set aside our emotions and make tough decisions in order to maximize P(Win). “Maximize P(Win)” frees us from constraints and clarifies that we must put Arena first.

Own the Outcome — We own results end to end — not just our individual slice of the work. When problems arise and we have the means to act, we do so without waiting for permission or assignment. We treat failure and success as signals and use them to improve. At Arena, we stay accountable to the final outcome.

## Competition Overview

- **Competition**: DOE GEMS Prize (DrivenData #306) - https://www.drivendata.org/competitions/306/competition-doe-gems/
- **Problem**: Predict geothermal-indicative faults in GeoDAWN region, NW Nevada
- **Metric**: Distance-weighted Tversky Index (DTI) with alpha=0.2, beta=0.8, triangular kernel R=300m (3px at 100m)
  - Formula: DTI = TPw / (TPw + 0.2*FPw + 0.8*FNw + eps)
  - TPw = sum_g max_x:p(x)*k(d(x,g)), FPw = sum_x p(x)[1-max_g k(d)], FNw = sum_g [1-max_x p(x)k(d)]
  - k(d) = max(1-d/R, 0)
- **Submission format**: Single-band float32 GeoTIFF, EPSG:32611, 100m, 3292x3730, values in [0,1], NaN or 0 outside footprint, transform (100,0,243350,0,-100,4508550)
- **Scoring nuance**: Known USGS/INGENIOUS faults are masked/excluded from evaluation (forum 11516) — mass on catalogue is waste, not penalty, but still waste of budget. Hidden new faults are ~0.24% of cells (~12.6k px). Best to emit sparse dotted predictions off-catalogue.
- **Highest known scores**: Public leaderboard #1 0.3262 (nchuzhoy, 2026-10-04), group best 0.2778 (GEMSDOE32 H33-2-B2), 0.2708 anchor, 0.2600 D2.8 dotted H19-5
- **Goal**: Generate unique submission scoring >0.2778, ideally >0.3195-0.3262

## Why Dotted Wins

Metric is a budget: every emitted pixel costs 0.2*FPw, earns at most 1*TPw. Thinning thick surface while keeping geometry removes mass already covered — raises credit per emitted pixel. Break-even credit per dot ≈0.2*DTI ≈0.052 at 0.26 operating point. Empirical break-even measured at 0.0548.

## Executive Summary

See docs/index.html and docs/executive_summary.html for one-click download and step-by-step upload guide. The primary file is all-finite (no NaN, no nodata tag) to avoid "Predicted values must be in range [0, 1]" error, which has two root causes:
1. Float32 sentinel -3.4028234663852886e+38 from training_features.tif inside footprint (3,061 pixels)
2. Feature raster valid mask smaller than template (5,165,852 vs 5,167,373)

Fix: footprint only from np.isfinite(sample_submission.tif), clip to [0,1], write with nodata=None, re-read and assert all finite.

## Data Sources (Verified)

- Competition overview: https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/
- Rules PDF: https://docs.nlr.gov/docs/fy26osti/96647.pdf (sha256 50d854b1e0239fe6...)
- Reference solution: https://github.com/drivendataorg/gems-prize-reference-solution
- GDR 1391 INGENIOUS: https://gdr.openei.org/submissions/1391 (DOI 10.15121/1881483)
- GeoDAWN area: https://www.sciencebase.gov/catalog/item/657e1d85d34e23d3533209f7
- Forum clarifications:
  - Known faults masked: https://community.drivendata.org/t/scoring-clarification-are-known-usgs-ingenious-faults-masked-when-scoring-and-are-they-in-the-final-round-label-set/11516/4
  - Pooled Tversky: https://community.drivendata.org/t/leaderboard-aggregation-pooled-over-public-test-pixels-or-mean-of-per-chunk-scores/11550

## Limitations & Needs

- No DrivenData auth → cannot auto-download training_features.tif, labels.tif, sample_submission.tif, 1m_DEM_links.csv from data tab (verified redirect to login)
- Single remaining blocker to training is data placement: run bash scripts/download_competition_data.sh on unrestricted machine into data/, then python scripts/prepare_data.py — after that full train→inference→validate pipeline ready (GPU needed for training; metric/losses/validation verified working on CPU)
- External data needed for new hypotheses: ASTER L1T (NASA LP DAAC), Landsat 8/9 (USGS EarthExplorer), Sentinel-1 InSAR (ASF DAAC), MT conductance (GDR), paleo geothermal (GDR), 1m DEM (USGS 3DEP via competition CSV)

## Structure

- docs/: GitHub Pages site with one-click download
- scripts/: generation, validation, MINE estimator
- src/: core logic
