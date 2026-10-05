# Deployment configuration

GitHub Pages already exists at https://buffedlizard55-lab.github.io/GEMSDOE38/.
At audit time its source was main / (legacy Pages). The integration denied a
settings change to workflow mode with HTTP 403. This is a settings permission
limitation, not a data or model failure.

Both the existing legacy build and the new deployment workflow preserve
`/GEMSDOE38/docs/` paths, with a root redirect to docs/index.html. The workflow
stages only the public site, not raw data, virtual environments or Git metadata.
Its daily source refresh is fail-closed: on failed fetch it retains the dated
last known leaderboard observation. PR merge and deployment run status must be
verified on GitHub; this configuration note alone is not evidence of success.
