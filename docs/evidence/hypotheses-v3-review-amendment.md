# v3 implementation review amendment — 2026-10-05

## Finding

A line-by-line final review found that the implementation named `L_signed_basin_side_step` did **not** implement the L transform in the pre-feature preregistration. The preregistered L called for signed opposing-side contrasts of gravity and conductivity residuals along the basement-depth normal. The code instead used positive gradient agreement between basement depth and gravity, multiplied by the **absolute** conductivity-residual gradient component projected onto the depth normal. It did not sample opposing sides and did not retain conductivity polarity.

The mismatch was discovered after the v3 feature build and MINE run. Therefore, the recorded L MINE values are **exploratory results for the as-coded unsigned variant**, not confirmatory evidence for the preregistered L hypothesis. No solo spatial model comparison was run for either version of L. The initial code/feature output is preserved by its content hashes below; the pre-feature protocol itself remains unchanged in `hypotheses-v3-preregistered.md`.

## Scope and consequence

- **J:** code matches the locked primary definition; its MINE and spatial comparison are unaffected.
- **K:** code matches the registered multiscale junction definition; its MINE estimate remains a marginal screen only, with no solo spatial model comparison.
- **L:** do not use its exploratory MINE value to rank, validate, promote, or describe the registered signed-side transform. Any corrected L work needs a new exact formula, including the sign convention and side-sampling distance, fixed before recomputation.
- The closed slot decision does not change. J failed its preregistered incremental comparison, and there is still no reproducible current-best holdout. No new GeoTIFF or portal action resulted from this code review.

## Archived as-coded L evidence

Before the review amendment, the L-named array had SHA-256 `600b4d37c7b2cccf2fe7d3e820c156b5888ebc21f3d7ed263d42a0ef4b006768`; the row-major `X_v3.npy` matrix had SHA-256 `54291ede6222b3da5d9ea9b78996aedeeed0494e1b1d806f40edd805aa83d2db`. Its as-coded MINE values were full-fit mean **1.7185886e-05 nats**, spatial OOF mean **1.6910283e-05 nats**, and shuffled-null mean **-9.0604929e-08 nats**. Those numbers remain useful only as a record of the unsigned variant's marginal association with the incomplete public catalogue; they are not a test of the registered L transform, conditional information, hidden-fault truth, or model value.

## Before any further L experiment

Write and timestamp a separate preregistered amendment with an exact signed side-contrast formula, rationale for its polarity, side offset and scale; then implement it without using these exploratory L results to tune it. Recompute full-label MINE and use a separately frozen spatial model comparison only if it remains scientifically justified. Keep the original result and this deviation record intact.
