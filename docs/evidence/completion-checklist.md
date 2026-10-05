# Requirement coverage — audit of the actual outcome

|Requirement|Status / evidence|
|---|---|
|Review repository before implementation|Done. Inherited random-geology and forced-positive validation identified and replaced; archive and Git history retained.|
|Review previous results/sites|36 supplied entry pages retrieved at pinned commits; selected H33 source modules reviewed. User scores preserved and not relabeled as organizer-verified file scores.|
|Official problem, metric, forum, rules|Read task + both chunks, full parsed rules PDF (all seven chunks), staff clarification, leaderboard, about page and data login redirect; source register.|
|3–5 ranked hypotheses before implementing|Four recorded before feature computation; qualitative expected opportunity/cost, layers, physical signatures, confounders and differences. No fabricated score gains.|
|Full-label MINE|Four features, all 5,167,373 catalogue footprint rows evaluated, 60,988 positives, three seeds, spatial OOF and null controls. Hidden true new-fault labels unavailable; catalogue zeros are unlabelled.|
|Avoid noisy single-number ablation|Paired spatial bootstrap, four-fold outcomes and MINE diagnostics reported; no blanket low-variance claim.|
|Train own model with real data|Done on CPU using measured 19-band inputs and new multiscale feature; exact provenance hashes.|
|Complete data placement autonomously|Done through checksum-pinned GitHub bridge; direct Dropbox failed. No synthetic fallback.|
|Beat current independent holdout best before spending slot|NOT met: no compatible prior-best checkpoint. Fresh baseline experiment also fails uncertainty gate. No competition slot used.|
|Unique new TIF|Done: actual newly computed raster; no duplicates among 208 same-grid historical blobs at 254 artifact paths. Two other blobs use different grids. Global/private uniqueness cannot be proven.|
|Easy download, unique name, short note|Done in README, home page and executive guide; ZIP contains exactly one TIF.|
|Range/format verification|Done from disk, min 0/max 1/all finite, exact template grid. NaN-outside alternative provided. Portal acceptance remains untested.|
|Scientific discovery / higher leaderboard score|Not established. Candidate is a fault-ranking hypothesis, not a confirmed fault/vent map. No competition score or promised gain.|
|Auditable source/data tables|Source register, hypothesis table, input inventory, source snapshots, hash-pinned data manifest and limitations.|
|Current feed automation|Workflow attempts daily leaderboard parse, keeps last known result on failure and shows freshness. Successful deployed automation must be checked, not assumed.|
|Keep prompt and values as starting point|README preserves complete operating brief with malformed links normalized/repetition consolidated; AGENTS.md directs future sessions to it.|
|Three review passes|Pass 1 real implementation; pass 2 metric/gradient/format/leakage tests; pass 3 historical-content uniqueness, source scope, site-link and archive checks. 26 local tests passed; lint F checks and compile succeeded.|
|PR, merge, Pages|Tracked separately through GitHub receipts; do not treat a created workflow as proof of deployment.|
|Next steps and limitations|Detailed in research-review.md and executive guide; no request for credentials or manual data placement.|
