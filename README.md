# GEMSDOE38 — measured-data fault discovery

## Download the new GeoTIFF

**[Download the unique all-finite TIF](docs/downloads/gems38-realdata-A-20261005-736488e5ab49-zero.tif)** · [ZIP](docs/downloads/gems38-realdata-A-20261005-736488e5ab49-zero.zip) · [NaN-outside twin](docs/downloads/gems38-realdata-A-20261005-736488e5ab49-nan.tif) · [format/provenance receipt](docs/downloads/submission-audit.json)

**RESEARCH ONLY — promotion gate failed. Do not spend a competition slot yet.** A real candidate exists; no higher leaderboard score is claimed and no competition upload was made.

- Name: `gems38-realdata-A-20261005-736488e5ab49`
- Note: `G38 measured 19 bands + low-relief multiscale magnetic edge; HGB120, d2.8 sparse. Research-only: holdout gate closed; no leaderboard score.`
- 1 band, float32, EPSG:32611, 3730 rows × 3292 columns, 100m; **41,339** positive cells.
- Primary has only finite values in `[0,1]`, zero outside the template footprint, no nodata tag. Official prose requests null/NaN outside; the alternate preserves that convention. Portal acceptance has not been tested.
- File SHA-256: `6e8486843141a826592324b39602524321abf6c0b6c12e3cb02cd054b216960e`.
- Pixel-content SHA-256: `736488e5ab49…`; **76,607 changed pixels vs H33**. Compared with **208** same-grid prior raster blobs across **254** public artifact paths in 36 supplied repositories: **no duplicates**. Two other blobs have different grids. See [audit scope](knowledge/uniqueness-audit.json); private/unlisted files are not covered.

**[Project website](https://buffedlizard55-lab.github.io/GEMSDOE38/)** · [Executive submission guide](docs/executive_summary.html) · [Scientific review](knowledge/research-review.md) · [Next-session priorities](knowledge/research-review.md#next-session-priorities)

## What changed / evidence

The inherited “MT/ASTER” generator used random faults and simulated fields. Its holdout forced positive deltas and its MINE results were synthetic demonstrations. These downloads are withdrawn, with hashes preserved in [the withdrawal record](knowledge/withdrawn-artifacts.json); original history is retained in Git. We do not represent them as geoscientific predictions.

The replacement recovered real 19-band data via a checksum-pinned owner mirror, built four label-free feature hypotheses, ran neural MINE on the complete available catalogue population, trained CPU models, measured spatially blocked results, and generated a genuinely new raster from measured features—not copied predictions.

|Evidence|Result|
|---|---|
|Official public leaderboard, checked 2026-10-05|**0.3262** leading, not 0.3195. H33's 0.2778 file attribution remains user-reported.|
|Full-label MINE evaluation|5,167,373 rows; 60,988 catalogue positives; H(Y)=0.06412918 nats; 4 features, 3 seeds, full-fit + OOF + null controls.|
|Spatial benchmark|19-band baseline **0.13143768**; 19+A **0.13370925**. These are catalogue-proxy scores, NOT competition scores.|
|Paired block uncertainty|Delta **+0.00227157**; 95% interval **[-0.00126337, +0.00705391]**; only 2/4 folds improved.|
|Promotion|**FAIL**; no independent comparable historical-best checkpoint and no hidden new-fault labels.|

Why the prior sparse H33 may work: DTI rewards maximum coverage of true faults while charging excess false-positive mass. Thinning and catalogue-flank pruning can reduce redundant mass. Exact attribution cannot be proven without hidden truth. The official known-fault mask is pixel-exact; 200m pruning is only a heuristic. See the [derivation, sources and limitations](knowledge/research-review.md).

MINE does not guarantee lower variance, does not measure incremental information conditional on existing features, and cannot rule out interactions from near-zero marginal estimates. A full-label screen must not leak feature selection into an allegedly untouched holdout. Our top hypothesis was fixed before these results.

## Reproduce without manual data placement

Python 3.11+, `gh` connected to GitHub, roughly 3GB RAM / 2GB working disk. CPU suffices. Dependencies tested are pinned in `requirements-lock.txt`; supported ranges are in `requirements.txt`.

```bash
python -m venv .venv
.venv/bin/pip install -r requirements-lock.txt
bash scripts/download_competition_data.sh
.venv/bin/python scripts/prepare_data.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python scripts/build_features.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python scripts/run_mine.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python scripts/run_validation.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python scripts/generate_submission.py
.venv/bin/python scripts/verify_uniqueness.py
.venv/bin/python scripts/build_site.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python -m pytest -q
```

The downloader also restores the H33 reference for comparison only. It fails on missing data/hash mismatch; it never substitutes random fields. Large source/intermediate rasters stay under ignored `data/`. GitHub Pages is static: it serves a precomputed artifact; it does not train in a browser. The research workflow regenerates files as downloadable Actions artifacts, without auto-uploading to DrivenData. The Pages workflow refreshes source status daily, preserving last known values and flagging fetch failures rather than inventing a live feed.

## Sources, constraints and next session

- [Competition task, metric and format](https://www.drivendata.org/competitions/306/competition-doe-gems/page/967/)
- [Staff mask clarification](https://community.drivendata.org/t/scoring-clarification-are-known-usgs-ingenious-faults-masked-when-scoring-and-are-they-in-the-final-round-label-set/11516/4)
- [Official rules PDF](https://docs.nlr.gov/docs/fy26osti/96647.pdf) — all parsed sections read; three submissions/week, one final selection, AI-use narrative disclosure and reproducible solution assets.
- [MINE, ICML 2018](https://proceedings.mlr.press/v80/belghazi18a.html), [MI bias/variance, ICML 2019](https://proceedings.mlr.press/v97/poole19a.html)
- [Source register](knowledge/source-register.json), [36 prior site snapshots](knowledge/site-review.json), [hypothesis preregistration](knowledge/hypotheses-preregistered.md).

Mirrors match owner SHA-256 receipts, not an independently authenticated organizer download. Known fault labels are incomplete; zero is unlabelled, not confirmed fault absence. No account login, hidden labels, private score, field confirmation or eligibility certification is available. Direct Dropbox shell downloads failed; the GitHub data bridge worked. No new GPU access is needed for this model.

Next: freeze a fresh nested spatial design for feature D; reproduce the strongest prior detector fold-locally; test 1m LiDAR and flight-line confounders; resolve ambiguous feature metadata; preserve spatial null structure in MI controls. Do not spend a slot because a single noisy delta is positive.

## Core values

**Maximize P(Win).** Prioritize truthful evidence, scarce-slot discipline and reproducible scientific improvement over a favorable-looking number.

**Own the Outcome.** Withdraw misleading inherited artifacts, repair the complete pipeline, report failed gates, and keep limitations visible.

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
