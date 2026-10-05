# GEMSDOE38 — measured-data fault-discovery research

## Current status — 2026-10-05

> **Slot gate: CLOSED. The GeoTIFF below is a unique, locally format-checked research artifact, not an approved competition submission.** Its portal acceptance is untested; hidden-fault performance is unknown; and it has not beaten a reproducible current-best holdout. Do not spend a weekly slot on it.

### Download the unique research GeoTIFF

**[Download all-finite GeoTIFF](docs/downloads/gems38-D-step-3p0-07pct-tipProt-20261005-ecfbf59e2b48-zero.tif)** · [ZIP containing that one TIF](docs/downloads/gems38-D-step-3p0-07pct-tipProt-20261005-ecfbf59e2b48-zero.zip) · [NaN-outside alternative](docs/downloads/gems38-D-step-3p0-07pct-tipProt-20261005-ecfbf59e2b48-nan.tif) · [local format/provenance receipt](docs/downloads/submission-audit.json)

- **Distinct name:** `gems38-D-step-3p0-07pct-tipProt-20261005-ecfbf59e2b48`
- **Short distinction note:** `G38 D-step 19+D HGB120; 0.7%, 3.0px, tip-protected; local format-check only`
- 1 band, float32, EPSG:32611, 3730 × 3292 cells, 100m transform. The all-finite file has 36,171 binary positive cells; every pixel is in `[0,1]`, outside-footprint cells are zero, and no nodata tag is set.
- Local disk-reread checks passed for dtype, shape, CRS, transform, inside-footprint finiteness/range, outside policy and nodata convention. The NaN-outside twin has the same canonical in-footprint pixels. **Neither encoding is portal-certified.**
- All-finite file SHA-256: `8e0876bbe844ee118489993bc3fe67c3120181ffef9a0dc144c083fbb5a1f5cd`; canonical pixel hash: `ecfbf59e2b487400bd6a180ab745f1914619cff88afda3a2bbcdc54f4336e0d2`.
- No content duplicate was found among the 208 retrievable same-grid raster blobs across 36 pinned sibling repositories. This is a scoped public-artifact comparison, not a claim about private or unobserved submissions.
- This is the existing v2 raster, retained for traceability. No new raster was generated in v3 because the primary candidate failed its incremental proxy gate and no reproducible current-best holdout is available.

**[Project website](https://buffedlizard55-lab.github.io/GEMSDOE38/)** · [Executive submission guide](docs/executive_summary.html) · [Scientific review](knowledge/research-review.md) · [v3 preregistered hypotheses](knowledge/hypotheses-v3-preregistered.md) · [v3 MINE results](knowledge/mine-results-v3.json) · [v3 validation](knowledge/validation-v3.json) · [slot gate](knowledge/slot-gate.json)

## Decision record: evidence, not optimism

### Current-best evidence is not reproducible yet

The user-reported mapping of GEMSDOE32 `h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros` to **0.2778** is not tied to an organizer-published raster hash. The public leaderboard snapshot on 2026-10-05 showed a best score of **0.3262**; it identifies a participant score, not the underlying artifact filename.

At pinned GEMSDOE32 commit `b63ebab7dbcf9238422ebbc2dbc4addf84bed11b`, the holdout implementation uses a 15-pixel collar and 12-pixel domain erosion, while its `h33_holdout.json` describes 30 and 20 pixels. The required `data/external/derived_sgmc_faults_100m_u8.tif` is absent from that tracked tree. Its own live-mirror receipt reproduced just **2/6** historical score orderings (3/6 after the receipt's calibration). These are useful owner-reported proxy results, not a reproducible hidden-label benchmark. No candidate is claimed to have beaten H33 or the current leaderboard best.

### Historical v2 result — limited scope

The earlier D-feature experiment reported `19+D` versus a fresh 19-band baseline at catalogue-proxy DTI **0.139522 vs 0.131449** (Δ **+0.008074**; 4/4 quadrants; conditional paired 20km-block 95% interval **[+0.001093, +0.015498]**). This is a positive internal result against the incomplete public catalogue, whose zero pixels are unlabelled. It is **not** an evaluation against the reported H33 holdout best, and it did not validate the final raster's separate 0.7% emission, 3.0px thinning, 200m exclusion and endpoint protection. It does not open the submission gate.

### v3 preregistration, full-label MINE and locked spatial comparison

Three local feature hypotheses (J/K/L) and one blocked external-data hypothesis (X) were documented before building v3 features. J was selected as the primary on physical rationale before MINE results. The full-footprint MINE screen evaluated all **5,167,373** public-label cells (60,988 positives; entropy 0.064129 nats), with three seeds, four spatial OOF folds and shuffled-label controls. MINE estimates marginal association with the public catalogue; they are not incremental conditional information, hidden-fault truth or guarantees of model value. Upstream feature quantile scaling uses the full footprint without labels, so folds have label-free transductive preprocessing rather than a completely fold-local pipeline.

|Feature|Full-fit MINE mean (nats)|Spatial OOF mean (nats)|Shuffled-null mean (nats)|Interpretation|
|---|---:|---:|---:|---|
|J — asymmetric magnetic flank|4.661e-05|1.950e-05|-2.835e-07|Predeclared primary; marginal signal above null, but not incremental model value|
|K — multiscale cross-field junction|3.324e-05|7.019e-06|-5.580e-07|Weak OOF signal; no individual spatial model comparison run|
|L — unsigned as-coded variant|1.719e-05|1.691e-05|-9.060e-08|Exploratory only: implementation differed from registered signed side contrast; no individual spatial model comparison|

**Implementation review amendment:** a final code audit found that L's code used positive depth/gravity gradient agreement with an *unsigned* projected conductivity-residual gradient, not the registered signed opposing-side contrasts. Its MINE row is exploratory for that as-coded variant, not evidence for registered L. J/K definitions and the primary J comparison are unaffected; see [the amendment record](knowledge/hypotheses-v3-review-amendment.md). The locked, equal-budget spatial comparison was 19 bands vs 19+D vs 19+D+J, with four geographic quadrants, 1km training exclusion, fixed HGB settings, 0.8% emission and 2.8-cell spacing. J+D compared with D yielded **ΔDTI +0.000712**, only **2/4** folds positive, paired 20km-block 95% interval **[-0.004698, +0.006037]**: **FAIL**. J+D did beat the 19-band baseline by +0.008785, but that does not establish J's added value; D supplies most of the improvement. No new submission file or competition slot was used.

### Ranked hypotheses and external-source status

|Rank|Candidate and layers|Signature / missing-fault rationale|Qualitative expected DTI opportunity / cost / status|
|---|---|---|---|
|1|J — `tmi`, `iso_grav_anom`, `cond_surf`, `det_elev_slope`|Two-scale magnetic flank-slope asymmetry, corroborated by gravity edge and positive local conductivity residual; a buried damage/alteration boundary may persist with weak relief.|**Moderate, unquantified prior**; low–medium compute, local data. Not present in D or A–I definitions; related topographic asymmetry exists in sibling work. **Incremental spatial gate failed.**|
|2|K — `tmi`, `iso_grav_anom`|Cross-field gradient strength gated by structure-tensor junctionness that persists at two scales; transfer/intersection structures could focus permeability.|**Moderate opportunity, ranked below J** after sibling-overlap penalty; medium compute. Different from scalar co-edge because it tests local multidirectional persistence. No solo spatial validation.|
|3|L — `depth_to_base_surf`, `iso_grav_anom`, `cond_surf`, `det_elev_slope`|Registered concept: signed co-polarized basement-depth/gravity side-step with a conductivity-residual side response; concealed basin throw may lack a scarp.|**Low–moderate qualitative opportunity**; low compute. Different from edge-amplitude or gradient-discordance features; metadata says basement while organizer prose says conductive base. **Implementation drift found:** current MINE is for an unsigned variant, not this hypothesis; no solo spatial validation.|
|4 (blocked)|X — official GeoDAWN Area-2 magnetic/radiometric flight-line CSVs and flight paths|Test whether candidate lineaments reproduce across adjacent traverses and are not survey-parallel residuals.|Potentially **moderate precision gain if a line residual is measured**, but very high data/processing cost. USGS lists raw Area-2 magnetic CSV ZIP (3.74 GB) and radiometric CSV ZIP (427.33 MB); shell TLS failed earlier and raw bytes are absent. Metadata is readable, but X is **not implementable or MINE-tested** until official bytes/schema are obtained.|

Sources: [DrivenData problem and data contract](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/), [staff clarification that near-catalogue new truth can exist](https://community.drivendata.org/t/scoring-clarification-are-known-usgs-ingenious-faults-masked-when-scoring-and-are-they-in-the-final-round-label-set/11516/4), [USGS GeoDAWN DOI 10.5066/P93LGLVQ](https://doi.org/10.5066/P93LGLVQ), [USGS ScienceBase raw-file list](https://www.sciencebase.gov/catalog/item/657e1d85d34e23d3533209f7), and the [USGS blind-geothermal integrated-study abstract](https://pubs.usgs.gov/publication/70221765). A published blind system motivates testing structural intersections; it does not validate J/K or these pixel predictions. The USGS describes GeoDAWN Area-2 traverse lines at 400m spacing and magnetic tie-line/micro-leveling; interpolation to 100m does not confer 100m source resolving power.

## Promotion gate and next steps

**Keep `knowledge/slot-gate.json` closed.** Reopen only after (1) the exact current-best input, code, splits and checkpoints are restored or regenerated and hash-verified; (2) the current-best and proposed artifact are evaluated under the same frozen spatial test design with paired uncertainty; (3) a candidate beats that benchmark without post-hoc budget/threshold changes; and (4) portal acceptance is separately tested. Do not treat public label zeros as confirmed negatives or the sibling's calibrated SGMC proxy as expert hidden truth.

Next work: reconcile GEMSDOE32 code/evidence/input mismatches; retrieve exact current-best raster and holdout sources; independently rebuild its detector fold-locally on the same splits; test flight-line residuals only if official data bytes can be obtained; add spatially preserved MINE nulls and conditional/incremental information checks; then consider another preregistration. Preserve the final-round discovery opportunity and do not auto-upload.

## Reproduce v3 research

Python 3.11+, pinned dependencies in `requirements-lock.txt`, about 3GB RAM and CPU are sufficient. Data are restored by the checksum-pinned owner-mirror downloader; the mirror is not independently organizer-authenticated.

```bash
python -m venv .venv
.venv/bin/pip install -r requirements-lock.txt
bash scripts/download_competition_data.sh
.venv/bin/python scripts/prepare_data.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python scripts/build_features_v3.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python scripts/run_mine_v3.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python scripts/run_validation_v3.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python -m pytest -q
.venv/bin/python scripts/build_site.py
```

`data/` is ignored. A static site serves a previously generated research file; it does not train in a browser. The feed is a timestamped organizer leaderboard observation, not a continuous API guarantee. No automatic competition upload exists.

## Limitations and integrity

- Labels are incomplete positive-unlabelled traces. Zero is not verified absence; public-label metrics can penalize unlabelled real faults.
- MINE is a bounded, finite-capacity DV estimator; small marginal values can miss interactions and do not equal conditional information or test-set performance. Full-fit estimates are optimistic; OOF folds and global-shuffle nulls are diagnostic, not independent truth.
- No private labels, current-best reproducible holdout, account session, portal acceptance, field validation or independent organizer data download is available.
- Core bands are owner-mirrored with hash receipts. Hash agreement proves mirror integrity against owner receipts, not organizer authentication.
- The generated D raster's endpoint protection and catalogue exclusion are heuristics; staff says nearby hidden labels can exist.
- GeoDAWN/3DEP data are not assumed obtained just because an official metadata page is public. External content must be licensed and reproducibly shared per contest rules.
- We cannot promise a leaderboard score or prize. The public leading score was 0.3262 at the recorded snapshot; the observed user-reported H33 mapping remains unverified by artifact hash.

## Core values

**Maximize P(Win).** Prioritize truthful evidence, scarce-slot discipline and reproducible scientific improvement over a favorable-looking number.

**Own the Outcome.** Withdraw misleading inherited artifacts, repair the complete pipeline, report failed gates, and keep limitations visible.

---

## User project prompt — read at the start of every session

The complete operating brief is preserved below with malformed duplicate Markdown links normalized and repeated paragraphs consolidated for readability. Historical scores/assumptions in the brief are requests and user reports, **not automatically verified facts**. The corrected evidence above takes precedence as the current research record.

<details>
<summary>Expand the project brief, historical results, requirements and supplied data links</summary>

Review the repo.

THE FOLLOWING IS THE HIGHEST URGENCY AND MUST BE FOLLOWED!

MUST GENERATE A UNIQUE TIF SUBMISSION FOR THE COMPETITION. DO NOT COPY A PREVIOUS SUBMISSION UNLESS IT'S FOR LEARNING AND EDUCATION. BUT WE MUST GENERATE A UNIQUE TIF SUBMISSION.

There should be an easy to download submission tif file as described by the prompt. Read the entire prompt.

Quantify what a feature adds with an information-theoretic estimator, not a noisy single-number ablation. With faults covering roughly 1% of the area, a holdout ablation — add a feature, rerun, see if DTI moves — runs on so few positive examples that the resulting delta is itself noisy, easily mistaken for signal or for nothing. Mutual information directly measures how much a feature's value reduces uncertainty about the true label, independent of whether any particular model exploits that relationship well, and Belghazi, Baratin, Rajeswar, Ozair, Bengio, Courville, and Hjelm's MINE estimator (ICML, 2018) makes this computable for exactly this kind of high-dimensional, continuous feature. Compute MINE-estimated mutual information between each candidate feature and the true label on the full label set, not only the small ablation holdout, and use it as a far-less-noisy first-pass filter — a feature with near-zero estimated mutual information is unlikely to earn back a submission slot no matter how the model is tuned around it, and this tells you before spending the compute to find out the hard way.

The following sites should serve as a starting point for understanding how to generate TIF submissions. These websites are researched, and tested and have generated TIF submissions. But we need to generate high scoring submissions. Here are the user-reported results; blank scores were not supplied:

|Site|Submission and reported score|
|---|---|
|[GEMSDOE](https://buffedlizard55-lab.github.io/GEMSDOE/docs/index.html)|gems-submission-20260925T001403Z-7f00890a: 0.1563|
|[6GEMSDOE](https://buffedlizard55-lab.github.io/6GEMSDOE/)|gems6_hgb88-topk03_33cec71ff0: 0.0286|
|[GEMSDOE3](https://buffedlizard55-lab.github.io/GEMSDOE3/docs/index.html)|pindrop-v4-nodes-20260925T152420Z-f347b70daa: 0.1193; pindrop-v4-discovery-20260925T152423Z-37f9d5b855: 0.0830; pindrop-v4-ridge-20260925T152422Z-4e03fc9705: 0.1152|
|[GEMSDOE2](https://buffedlizard55-lab.github.io/GEMSDOE2/docs/index.html)|gemsdoe2-dual-family-union-20260925T160406Z-f68e590f: 0.1560|
|[GEMSDOE4](https://buffedlizard55-lab.github.io/GEMSDOE4/)|gems-submission-20260926T163915Z-237f0063: 0.0343|
|[5GEMSDOE](https://buffedlizard55-lab.github.io/5GEMSDOE/docs/index.html)|gems-submission-20260926T175114Z-7f00890a: 0.1563|
|[7GEMSDOE](https://buffedlizard55-lab.github.io/7GEMSDOE/)|lidarscarp-ridge-top2pct-36c3a3f341c8: 0.1461|
|[8GEMSDOE](https://buffedlizard55-lab.github.io/8GEMSDOE/)|Hedge-v2_submission: 0.1563|
|[GEMSDOE9](https://buffedlizard55-lab.github.io/GEMSDOE9/docs/index.html)|2314b599: 0.0107|
|[11GEMSDOE](https://buffedlizard55-lab.github.io/11GEMSDOE/docs/index.html)|gems-structural-area06-v1: 0.0202|
|[12GEMSDOE](https://buffedlizard55-lab.github.io/12GEMSDOE/docs/index.html)|r7-nms3-dem10-scarp_0c9199f14e62: 0.1294; r7-nms3-dem10-scarp_0c9199f14e62_allfinite: 0.1294|
|[15GEMSDOE](https://buffedlizard55-lab.github.io/15GEMSDOE/docs/index.html)|gems-tso1-20260929T005627Z-conj_alteration_mag: 0.0782|
|[14GEMSDOE](https://buffedlizard55-lab.github.io/14GEMSDOE/docs/index.html)|GEMS_r5-geom-horse-ensemble_20260929T154852Z_ccbe1de0_site_e96e942f: 0.0020|
|[17GEMSDOE](https://buffedlizard55-lab.github.io/17GEMSDOE/)|17GEMSDOE_F-ensemble-2pct_20260930T050626Z: 0.0187|
|[18GEMSDOE](https://buffedlizard55-lab.github.io/18GEMSDOE/)|H19-C_20260930T212401Z_c11e495e: 0.0297|
|[19GEMSDOE](https://buffedlizard55-lab.github.io/19GEMSDOE/docs/index.html)|h19-4-multiline-corroborated-openness-thermal-pop-20260930-691e4dfa-nan: 0.1894; h19-5-powerlaw-budget-multiline-corroborated-20260930-e27054cf-nan: 0.1922|
|[GEMSDOE10](https://buffedlizard55-lab.github.io/GEMSDOE10/)|h16-continuation-20260927T065521077735Z-3431b83c7c: 0.0461; h20-dem10-scarp-thin-20260927T155223039488Z-ffc91a1686: 0.0921; H25-ctx-ridge-20260927T232947704150Z-6452ae1d00: 0.1280; h28-dotted-ridge-20260928T020256236880Z-6452ae1d00: 0.1839|
|[13GEMSDOE](https://buffedlizard55-lab.github.io/13GEMSDOE/)|20261001_r13-lattice-s5_v2_nan-outside: 0.0904|
|[16GEMSDOE](https://buffedlizard55-lab.github.io/16GEMSDOE/docs/index.html)|h16-1-topo-geophys-baseline-ridges-20260930-df20f65e-nan: 0.1855; h18-3a-topo-geophys-x-complexity-prior-20260930-c502dfab-nan: 0.0976; h18-4-usgs-geologic-map-faults-gap-20260930-aef8f42c-nan: 0.0360|
|[GEMSDOE21](https://buffedlizard55-lab.github.io/GEMSDOE21/)|h19-4-reference-20260930-691e4dfa: 0.1894|
|[20GEMSDOE](https://buffedlizard55-lab.github.io/20GEMSDOE/docs/index.html)|h20-1-sarnnpu-powerlaw-pi0363-tilt-wingcrack-20260930-be0e8f6b-nan: 0.1890; h20-5-continuous-pu-proxy-unverified-20260930-824ce73a-nan: 0.1859|
|[GEMSDOE22](https://buffedlizard55-lab.github.io/GEMSDOE22/docs/index.html)|h23-a-dti-optimal-emission-6pct-20261002-e2ec4b49-nan: 0.1002; h23-b-dti-optimal-emission-10pct-20261002-86176698-nan: 0.0748|
|[GEMSDOE23](https://buffedlizard55-lab.github.io/GEMSDOE23/)|h30-arrangement-matched-habitat-20261002-0d4e02e8-nan: 0.1352|
|[GEMSDOE24](https://buffedlizard55-lab.github.io/GEMSDOE24/)|h25-1-dotted-h19-5-d1-5-20261002-989f59505db1-nan: 0.2477|
|[GEMSDOE25](https://buffedlizard55-lab.github.io/GEMSDOE25/)|dotted-h19-5-d2-8-20261002-e56ea318af89-nan: 0.2600|
|[GEMSDOE26](https://buffedlizard55-lab.github.io/GEMSDOE26/)|dilcond-oof-v1-20261003-47629f496133-nan: 0.1223|
|[GEMSDOE27](https://buffedlizard55-lab.github.io/GEMSDOE27/)|topo-gap-closure-t-v2-on-d1-5-20261002-5512495c6bd1-nan: 0.2449|
|[GEMSDOE28](https://buffedlizard55-lab.github.io/GEMSDOE28/)|h27-4-r1-solo-d2-8-20261003-8acb75e1f2cc-nan: 0.2708; h32-1-prethin-tip-euler-d2-8-20261003-31e35eee884e-nan: —; h36-1-rung30-blind-r1-20261003-b531dae0a36f-nan: —; h38-1-hf-euler-r30-r1-20261003-56a9f473edc7-nan: —|
|[GEMSDOE29](https://buffedlizard55-lab.github.io/GEMSDOE29/docs/index.html)|efd28-repro-20261003-1cc7dc534d51-nan: 0.2600; repo-c0-habitat-emission-20261003-a4d439b07426-nan: —; sgmc-off-catalogue-44k-20261003-c8dcd780e3fd-nan: —; wormrank-d28-20261003-59dcaf6dd11d-zeros: —; wormsurv-filter-20261003-921f10960d6e-zeros: —; xfit-c0-habitat-20261003-ca879db0089a-zeros: —; xfit-h41-union-qfaults-20261003-9edb34b99e3a-zeros: —|
|[GEMSDOE30](https://buffedlizard55-lab.github.io/GEMSDOE30/)|d28-poisson300m-offcat-44090-20261003T233156Z-91eae1ca: 0.2600|
|[GEMSDOE31](https://buffedlizard55-lab.github.io/GEMSDOE31/docs/)|h27-4-solo-d28-20261004-8acb75e1-nan: 0.2708|
|[GEMSDOE32](https://buffedlizard55-lab.github.io/GEMSDOE32/docs/index.html)|h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros: 0.2778|
|[GEMSDOE33](https://buffedlizard55-lab.github.io/GEMSDOE33/)|h33d-analog-tip-stepover-r30-20261004-cb490425926e: —|
|[GEMSDOE34](https://buffedlizard55-lab.github.io/GEMSDOE34/docs/index.html)|h34-scatter-q50-arr-matched-20261004T223317Z: —|
|[GEMSDOE35](https://buffedlizard55-lab.github.io/GEMSDOE35/docs/index.html)|h35-06-aaa86efb25-20261004T225420098147Z-candidate: —|
|[GEMSDOE36](https://buffedlizard55-lab.github.io/GEMSDOE36/docs/)|anderson-geothermal-pinn-38854-20261004T230000Z-9b9ea4e6-zeros: —|
|37GEMSDOE / 38GEMSDOE / 39GEMSDOE / 40GEMSDOE|No URLs or scores supplied for these placeholder names.|

WE NEED TO STUDY, ANALYZE, AND UNDERSTAND THE HIGHEST SCORE FROM THE GEMDOE SITE WHERE THE SUBMISSION TIF IS DOWNLOADED FROM WHICH IS GEMSDOE32, h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros: 0.2778. Why and how did this get the highest score and are we able to generate a submission that scores higher than 0.2778?

Answer the question using Phd level experience, knowledge, and judgement. Then use the answer to generate a unique TIF submission into the competition. Must be unique submission unlike any within the GEMSDOE sites above. Verify working line by line no hallucinations.

The leaderboard: https://www.drivendata.org/competitions/306/competition-doe-gems/leaderboard/

We need to quickly look at the results and results from the GEMSDOE websites above.

Before implementing, generate 3–5 candidate geological hypotheses we haven't tried yet, each naming: the specific layer(s) involved, the physical signature being targeted (e.g., an edge-detection or curvature transform), why it should catch a fault missing from the USGS/INGENIOUS catalogue rather than one already in it, and how it differs from anything already implemented in this repo. Rank them by expected DTI improvement and implementation cost. Validate the top candidate on our spatially-blocked holdout set before touching a weekly submission slot — do not spend a submission slot on an idea that hasn't beaten the current holdout best. If a candidate can't be validated without new external data, name the specific free, official source needed and check it's obtainable before proposing the idea as viable.

Work line by line verifying from official verified trusted sources, provide links for manual review. There should be no manual input, work on your own to complete tasks. Flag any irregularities for review. No hallucinations. Verify no hallucinations. The goal of this project is to get a full list that follow our requirements. Verify line by line.

We have a good understanding of how our hypothesis, methodology, calculations, analysis are done so we should be able to figure out a way to score higher on the leaderboard using previous results and scoring that we have across the sites listed above. We need to come up with distinct and unique strategies to score higher in this competition leaderboard. We need to start doing heavy and deep research into the part of the project that matters the most, which is the scientific discovery of geothermal vents. We should store all of our information and knowledge that we can gather from official verified sources. This will serve as a starting point for other projects as well. We need to think outside the box but still be grounded in proper scientific research, we are ultimately aiming for a top prize that many others are competing for. So it's important to be contrarian but be smart about it. We need to find sources of data that others are over looking or areas of the project when it comes to geothermal vents. We need to do deep research and critical thinking and come up with new hypothesis to test.

0.3195 is the highest score right now so we need to design a new strategy, research, testing, analyzing, and generating submission system than the current website. It should be unique, take unique approaches to generating a submission that can score higher than 0.3195.

Put this prompt into the repo readme and read it everytime we work on the project as a starting point to make sure we are building what we are aiming for and have a strong base to continue building and improving on making something useful for everyday use. It should solve the problem of having to manually check everything ourselves and having an up to date current feed.

Review the repo. The following is taken from the Arena AI team and I think it makes a good point on building a successful project, so let's keep the Core Values and Own the Outcome as a focal point when building, developing, researching, suggesting upgrades, and implementing the work.

Our Core Values — Maximize P(Win): “Maximize the Probability of Winning”: our decision making framework. In every decision, we weigh tradeoffs, assess risk, and choose the path that maximizes the probability that Arena succeeds. We set aside our emotions and make tough decisions in order to maximize P(Win). “Maximize P(Win)” frees us from constraints and clarifies that we must put Arena first.

Own the Outcome: We own results end to end — not just our individual slice of the work. When problems arise and we have the means to act, we do so without waiting for permission or assignment. We treat failure and success as signals and use them to improve. At Arena, we stay accountable to the final outcome.

We need to focus on being able to generate a submission into the competition. The site should be able to generate a TIF file that is required for submission. It should be as easy as download to click a File to submit into the competition. This needs to be in the executive summary or the very beginning of the site. It should be obvious when you visit the site.

I tried to submit the document that i downloaded from the site but it returned this error on the submission form: "Predicted values must be in range [0, 1]".

Also we need to give it a unique name and A short comment to help you or your team tell submissions apart later e.g. clustering with k=25.

Submission page: New submission. File to submit / No file chosen. You can submit a single-band GeoTIFF (.tif) file, or a .zip file containing a single GeoTIFF, with your predictions. It must match the submission format's CRS, shape, and geotransform. You may wish to review the competition rules first. Note (optional): A short comment to help you or your team tell submissions apart later e.g. clustering with k=25.

Create a executive summary subpage that explains exactly how to make a submission into the contest. Work on the next steps from the previous sessions first.

The goal of this project is to place top of the leaderboard in this competition. Competition problem: https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/

We need to create a project that can compete and place top of the leaderboard. We need to understand the problem, collect all the data and organize it into a clean easily auditable table with official verified links for manual verification. Guidelines: https://www.drivendata.org/competitions/306/competition-doe-gems/

Get familiar with the problem through the overview and problem description. Additional resources: https://www.drivendata.org/competitions/306/competition-doe-gems/page/968/

Download the data: https://www.drivendata.org/competitions/306/competition-doe-gems/data/

Create and train your own model. Reference solution: https://github.com/drivendataorg/gems-prize-reference-solution

Use your model to generate predictions that match the submission format. Tell me what are you limitations and what you need access to during this project. We will need to find free publicly available sources and data from official and verified sources if we are to use 3rd party or external data.

Rules PDF: https://docs.nlr.gov/docs/fy26osti/96647.pdf

You must be able to do your own research, deep research, scientific literature research and organize the knowledge so that we can critically think through the problem and generate a solution through scientific and free publicly available information. This must be done autonomously and must be constantly reviewed and improved upon. Provide suggestions and improvements and implement them.

User-reported prior blocker: ❌ No DrivenData auth → cannot auto-download training_features.tif, labels.tif, sample_submission.tif, 1m_DEM_links.csv from the data tab (verified redirect to login).

See below for links from the above site. See attached files for links from the above site.

https://gdr.openei.org/submissions/1391

Download competition data from DrivenData (requires login) to data/.

Supplied mirror links:
- https://www.dropbox.com/scl/fi/aemhtutjgcp6tr3tint94/GEMS_96647.pdf?rlkey=rek210cj2smnmzb8n0sla1vmd&st=wz4kofki&dl=0
- https://www.dropbox.com/scl/fi/6rgvnuady818ol8yqgis4/example_submission.tif?rlkey=kbykilvau066xuogoosbf4cq8&st=8junzdyw&dl=0
- https://www.dropbox.com/scl/fi/t7fyt03qdh9egyme0itwo/existing_faults.tif?rlkey=yiao96uluqdkipf0h5vju71jf&st=rnino7ya&dl=0
- https://www.dropbox.com/scl/fi/3vz9o0wwavi26xaeoxlwr/gems-geodawn-numerical-features.tif?rlkey=je8d8fepqfbst9lnwsq9rkplu&st=zj1lag1r&dl=0
- https://www.dropbox.com/scl/fi/ig0mban712ns1atphgphe/Digital-elevation-model-links-JSON.pdf?rlkey=zm77f1vbtt2if8hlruymptnu3&st=srhhir10&dl=0

Site creation: Create a github page for this repo that has clean ui, user friendly, simple and easy to use. It should be organized and clean. It should include all relevant information in an easy to read format with official verified links as sources for review.

User-reported prior next step: **The single remaining blocker to training is data placement**: run `bash scripts/download_competition_data.sh` on any unrestricted machine into `data/`, then `python scripts/prepare_data.py` — after that the full train→inference→validate pipeline is ready to run (GPU needed for training; metric/losses/validation all verified working here on CPU). You need to complete the above task by yourself.

Run this task through multiple passes.

Pass 1: Implement the task completely and verify the result.

Pass 2: Review your work for bugs, missing requirements, incorrect assumptions, and edge cases. Fix everything you find.

Pass 3: Re-check the entire implementation against the original request. Improve accuracy, reliability, completeness, and code quality. Fix any remaining issues.

Do not stop after the first pass. Each pass must build on the previous one. Before finishing, verify that the final result fully satisfies the original request. Work line by line verify everything no hallucinations.

Go ahead and create a pull request and then merge the pull request onto the main. Make suggestions for what work still needs to be done and any limitations that is in the way of a successful project. It should be worked on in this next session or the next session. Work line by line verify everything no hallucinations.

</details>
