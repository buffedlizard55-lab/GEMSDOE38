"""Build static, evidence-driven Pages. No prediction or score fabricated in the browser."""

import json, html, shutil
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / "knowledge" / name).read_text())


def esc(x):
    return html.escape(str(x))


def layout(title, body, article=False):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="GEMSDOE38 measured-data fault research, verified GeoTIFF downloads and transparent validation."><title>{esc(title)} · GEMSDOE38</title><link rel="stylesheet" href="assets/style.css"></head><body><a class="skip" href="#main">Skip to content</a><header><div class="wrap"><a class="brand" href="index.html">GEMS<span>DOE38</span></a><nav aria-label="Main navigation"><a href="index.html">Overview</a><a href="executive_summary.html">Submission guide</a><a href="methodology.html">Research &amp; results</a><a href="sources.html">Sources</a></nav></div></header><main id="main" class="wrap {"article" if article else ""}">{body}</main><footer><div class="wrap footer-row"><span>Maximize P(Win). Own the Outcome.<br>Evidence before a submission slot.</span><span>Research snapshot · 05 Oct 2026<br><a href="https://github.com/buffedlizard55-lab/GEMSDOE38">Code, user brief &amp; audit trail ↗</a></span></div></footer><script src="assets/site.js" defer></script></body></html>"""


if __name__ == "__main__":
    m = read("submission-manifest.json")
    v = read("validation-results.json")
    mi = read("mine-results.json")
    u = read("uniqueness-audit.json")
    feed = read("feed.json")
    sources = read("source-register.json")
    docs = ROOT / "docs"
    evidence = docs / "evidence"
    evidence.mkdir(exist_ok=True)
    for p in (ROOT / "knowledge").glob("*"):
        if p.suffix in [".json", ".md"] and p.is_file():
            shutil.copy2(p, evidence / p.name)
    # Historical synthetic demonstrations intentionally NOT exposed as active evidence.
    primary = "downloads/" + Path(m["files"][0]["path"]).name
    nan = "downloads/" + Path(m["files"][1]["path"]).name
    zipfile = primary.replace(".tif", ".zip")
    note = f"""<div class="note-box"><button id="copy-note" type="button">Copy note</button><strong>Submission note</strong><p id="submission-note">{esc(m["submission_note"])}</p><span id="copy-status" role="status" class="small"></span></div>"""
    download = f'''<div class="actions"><a class="button" download href="{primary}">↓ Download new GeoTIFF</a><a class="button secondary" download href="{zipfile}">ZIP</a></div><p class="small">All-finite · float32 · EPSG:32611 · 100m<br><a href="{nan}" download>NaN-outside alternative</a> · <a href="downloads/submission-audit.json">Independent format receipt</a></p>'''
    foldrows = "".join(
        f"<tr><td>Quadrant {r['fold'] + 1}</td><td>{r['models']['baseline_19']['dti']:.5f}</td><td>{r['models']['candidate_19_plus_A']['dti']:.5f}</td><td>{r['delta']:+.5f}</td></tr>"
        for r in v["folds"]
    )
    home = f"""<div class="hero"><div><span class="eyebrow">DOE GEMS Prize · fault-discovery lab</span><h1>A new fault map.<br>An honest test.</h1><p class="lead">A unique GeoTIFF built from measured geophysics—not copied predictions. Download the candidate, inspect its evidence, and protect the next submission slot.</p><span class="badge">RESEARCH ONLY · GATE CLOSED</span>{download}<p class="small">Not submitted. No leaderboard score. This candidate did not establish a reliable holdout improvement.</p></div><div class="map"><div class="map-head"><span>GeoDAWN / Nevada–California</span><span>100m grid</span></div><figure><img src="assets/prediction-overview.png" alt="Actual candidate predictions in gold over the measured total magnetic intensity field; these are not confirmed faults." width="659" height="746"><figcaption><span class="dot"></span>Candidate dots over measured TMI<br>Downsampled display; not confirmed faults or geothermal vents.</figcaption></figure></div></div>
    <div class="stats"><div class="stat"><strong>41,339</strong><span>new-model prediction cells</span></div><div class="stat"><strong>5.17M</strong><span>catalogue-footprint MI evaluation rows</span></div><div class="stat"><strong>{u["compared_same_grid"]}</strong><span>prior rasters compared · no duplicates</span></div><div class="stat"><strong>0 slots</strong><span>competition uploads used</span></div></div>
    <section><span class="eyebrow">01 / Decision</span><h2>A positive delta is not enough.</h2><p>The measured-data candidate scored <strong>0.13371</strong> against a fresh baseline of <strong>0.13144</strong> on spatially withheld <em>known catalogue</em> labels. Only 2 of 4 folds improved. The uncertainty interval crosses zero, so promotion failed.</p><div class="notice"><strong>Do not spend a weekly slot on this file yet.</strong><br>95% paired spatial-bootstrap ΔDTI: −0.00126 to +0.00705. These proxy scores are not comparable to the hidden-fault leaderboard or proof of beating H33.</div><div class="table-scroll"><table><thead><tr><th>Spatial fold</th><th>19-band baseline</th><th>19 + hypothesis A</th><th>ΔDTI</th></tr></thead><tbody>{foldrows}</tbody></table></div><p class="small">Four quadrants · 1km training buffer · fixed sparse budget · 180 spatial blocks · <a href="evidence/validation-results.json">Full validation receipt</a></p></section>
    <section><span class="eyebrow">02 / Scientific direction</span><h2>Test the physics. Preserve the uncertainty.</h2><div class="cards"><article class="card"><span class="num">HYPOTHESIS A · TESTED</span><h3>Quiet, persistent edges</h3><p>Magnetic gradient alignment across three scales, conditioned on low terrain relief. A candidate signature of concealed structure—not proof of a fault.</p></article><article class="card"><span class="num">FOUR FEATURES · FULL LABEL SET</span><h3>Information before tuning</h3><p>Neural MINE with three seeds, spatial folds and null controls. Step morphology is the strongest marginal signal; interactions still need independent tests.</p></article><article class="card"><span class="num">H33 · USER-REPORTED 0.2778</span><h3>Learn, don’t duplicate</h3><p>Thinning can reduce redundant false-positive mass. This candidate was trained afresh and changes 76,607 pixels versus H33. Higher hidden-test performance is unproven.</p></article></div><p><a href="methodology.html">Read the scientific review and four ranked hypotheses →</a></p></section>
    <section><span class="eyebrow">03 / Artifact identity</span><h2>One file. A traceable record.</h2><p><code>{esc(m["name"])}</code></p>{note}<p class="hash">SHA-256 · {m["files"][0]["sha256"]}</p><p><a href="executive_summary.html">Submission instructions and format conventions →</a></p></section>
    <section><span class="eyebrow">04 / Research integrity</span><h2>The inherited synthetic result was withdrawn.</h2><p>The previous generator used random fault lines and simulated “MT/ASTER” fields. Its holdout forced positive improvements. We replaced it with measured data, actual tests, and a closed submission gate. <a href="evidence/withdrawn-artifacts.json">Withdrawal record</a>.</p><p class="small">Official leaderboard last observed: <strong>{feed["leaderboard_best"]:.4f}</strong> · {esc(feed["last_success_utc"])}. Refresh status: {esc(feed["status"])}. <a href="sources.html">Source freshness and limitations</a>.</p></section>"""
    (docs / "index.html").write_text(layout("Measured-data research", home))
    executive = f"""<span class="eyebrow">Executive summary / submission guide</span><h1>Download first.<br>Submit only after the gate.</h1><div class="notice"><strong>Current status: research-only, not approved.</strong> The candidate failed the uncertainty gate. Downloading it is safe; uploading it would consume a limited slot without the requested evidence.</div>{download}<p>Filename: <code>{Path(primary).name}</code></p>{note}<h2>How to submit an approved candidate</h2><ol><li>Confirm a valid comparison with the current holdout best has passed and record the final artifact hash. <strong>This candidate has not passed.</strong></li><li>Read the <a href="https://docs.nlr.gov/docs/fy26osti/96647.pdf">official rules</a>, confirm your own eligibility, register/sign in to <a href="https://www.drivendata.org/competitions/306/competition-doe-gems/">DrivenData GEMS</a>, and accept the terms. Never share credentials with this site.</li><li>Download the <strong>.tif</strong> above (or the ZIP containing exactly one TIF). Do not upload this web page, an audit JSON, or a screenshot.</li><li>On DrivenData select <strong>New submission → File to submit → Choose file</strong>, choose the downloaded TIF, and paste the short note.</li><li>Only after approval, submit and record the organizer score, returned submission identifier, timestamp and the file hash together. Do not present an estimate as an organizer score.</li><li>Before the deadline, choose one final submission across both rounds. The rules specify three submissions per week. Finalist delivery also requires reproducible code/resources and a generative-AI-use narrative.</li></ol><h2>Why this file avoids range failures</h2><p>The primary was reopened from disk: all 12,279,160 cells are finite, min 0, max 1, one float32 band, correct CRS/shape/transform, no nodata sentinel. Predictions outside the actual template footprint are zero. The exact cause of the earlier portal error cannot be diagnosed without that rejected file.</p><p><strong>Outside-footprint convention:</strong> official prose specifies null/NaN outside. The alternate download follows the template's NaN mask exactly. The zero-filled primary follows the user's reportedly accepted H33 convention and avoids NaN range-check ambiguity. Neither local validation nor historical claims certify this file's portal acceptance.</p><h2>Rebuild rather than copy</h2><p>The static website serves an already generated, audited candidate. It does not train in your browser. The complete CPU workflow can be run without manual data placement using checksum-pinned inputs.</p><p><a class="button secondary" href="https://github.com/buffedlizard55-lab/GEMSDOE38/actions/workflows/research.yml">Open reproducible generation workflow ↗</a></p><p class="small">GitHub Actions permissions are needed to run it. Workflow outputs are research artifacts only; there is no DrivenData auto-upload.</p><h2>Limits and next session</h2><p>No hidden new-fault labels, verified holdout-best checkpoint, private score, competition login or field confirmation is available. CPU training and data recovery worked. The next experiment should use a newly locked nested spatial design for feature D and a fold-local reconstruction of the best prior detector. <a href="methodology.html">Full plan and disclosures →</a></p>"""
    (docs / "executive_summary.html").write_text(
        layout("Executive submission guide", executive, True)
    )
    mir = "".join(
        f"<tr><td>{esc(k)}</td><td>{r['full_fit_mean_nats']:.7f}</td><td>{r['oof_weighted_mean_nats']:.7f}</td><td>{r['null_mean_nats']:.7f}</td></tr>"
        for k, r in mi["features"].items()
    )
    review = markdown.markdown(
        (ROOT / "knowledge/research-review.md").read_text(),
        extensions=["tables", "fenced_code"],
    )
    # Local evidence links must resolve under Pages, not the repository root.
    for name in ["hypotheses-preregistered.md", "mine-results.json"]:
        review = review.replace(f'href="{name}"', f'href="evidence/{name}"')
    hypothesis = markdown.markdown(
        (ROOT / "knowledge/hypotheses-preregistered.md").read_text(),
        extensions=["tables", "fenced_code"],
    )
    method = f"""<span class="eyebrow">Research / independent evidence</span><h1>What the data supports.</h1><p>Measured results and interpretations are separated. Negative results remain visible.</p><h2>Full-catalogue MINE estimates</h2><p>Natural-log units (nats), three seeds. OOF means are weighted by spatial-fold population. Null labels are globally permuted, not spatially preserved. These values describe catalogue labels, not hidden new-fault truth.</p><div class="table-scroll"><table><thead><tr><th>Feature</th><th>Full-fit mean</th><th>Spatial OOF mean</th><th>Shuffled null</th></tr></thead><tbody>{mir}</tbody></table></div><p><a href="evidence/mine-results.json">All seeds, folds, units and limitations</a></p>{review}<hr>{hypothesis}"""
    (docs / "methodology.html").write_text(
        layout("Scientific review and results", method, True)
    )
    rows = "".join(
        f'<tr><td><a href="{esc(r["url"])}">{esc(r["id"])}</a><br><small>{esc(r["authority"])}</small></td><td>{esc(r["verified"])}</td><td>{esc(r["status"])}</td></tr>'
        for r in sources["sources"]
    )
    sourcepage = f"""<span class="eyebrow">Sources / provenance / freshness</span><h1>Every claim has a scope.</h1><p>Official sources define the task. Owner mirrors supply data with integrity checks, not independent organizer authentication. Previous submissions are learning/comparison artifacts only.</p><div class="notice"><strong>Leaderboard snapshot: {feed["leaderboard_best"]:.4f}</strong><br>Last successful observation: {esc(feed["last_success_utc"])}<br>Last attempt: {esc(feed["last_attempt_utc"])}<br>Status: {esc(feed["status"])}</div><p>Daily Pages builds attempt an automatic leaderboard refresh. Failures preserve the last known value and visibly mark it stale. This is not a real-time or guaranteed feed.</p><div class="table-scroll"><table><thead><tr><th>Official link</th><th>What was checked</th><th>Evidence scope</th></tr></thead><tbody>{rows}</tbody></table></div><h2>Audit downloads</h2><ul><li><a href="evidence/source-register.json">Source register</a></li><li><a href="evidence/input-inventory.json">Actual raster inventory, band names and checksums</a></li><li><a href="evidence/upstream-data-manifest.json">Pinned source data transport manifest</a></li><li><a href="evidence/site-review.json">36 prior entry pages, pinned commits and review scope</a></li><li><a href="evidence/uniqueness-audit.json">254 historical artifact paths / 208 same-grid content comparisons</a></li><li><a href="evidence/validation-results.json">Spatial validation and closed gate</a></li><li><a href="evidence/feed.json">Latest feed attempt and freshness</a></li></ul><h2>AI and licence disclosure</h2><p>An Arena.ai assistant supported source review, coding, tests and documentation. The new raster is computed from measured geophysics, not imagined geology. The original synthetic downloads are withdrawn. External resource licences and team eligibility require truthful account-holder confirmation; public accessibility alone is not a licence.</p>"""
    (docs / "sources.html").write_text(
        layout("Verified sources and provenance", sourcepage, True)
    )
    print("Built four pages from measured evidence")
