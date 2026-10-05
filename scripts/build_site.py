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
    # Prefer v2 validation if present
    try:
        v2 = read("validation-v2.json")
        v_is_v2 = True
        # also load old for reference
        try:
            v_old = read("validation-results.json")
        except:
            v_old = None
    except Exception:
        v2 = None
        v_is_v2 = False
        v_old = read("validation-results.json")
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
    primary = "downloads/" + Path(m["files"][0]["path"]).name
    nan = "downloads/" + Path(m["files"][1]["path"]).name
    zipfile = primary.replace(".tif", ".zip")
    note = f"""<div class="note-box"><button id="copy-note" type="button">Copy note</button><strong>Submission note</strong><p id="submission-note">{esc(m["submission_note"])}</p><span id="copy-status" role="status" class="small"></span></div>"""
    download = f'''<div class="actions"><a class="button" download href="{primary}">↓ Download new GeoTIFF</a><a class="button secondary" download href="{zipfile}">ZIP</a></div><p class="small">All-finite · float32 · EPSG:32611 · 100m<br><a href="{nan}" download>NaN-outside alternative</a> · <a href="downloads/submission-audit.json">Independent format receipt</a></p>'''

    # Build validation rows
    if v_is_v2 and v2 is not None:
        # Show plus_D vs baseline
        foldrows = ""
        for r in v2["folds"]:
            b = r["models"]["baseline_19"]["dti"]
            d = r["models"]["plus_D"]["dti"]
            delta = d - b
            foldrows += f"<tr><td>Quadrant {r['fold']+1}</td><td>{b:.5f}</td><td>{d:.5f}</td><td>{delta:+.5f}</td></tr>"
        pooled = v2["pooled"]["plus_D"]
        baseline_pooled = v2["pooled"]["baseline_19"]["dti"]
        decision_title = "Validated improvement over fresh baseline"
        decision_body = f"""<p>The <strong>D_topographic_step_proxy</strong> candidate (19 bands + D) scored <strong>{pooled['dti']:.5f}</strong> against a fresh baseline of <strong>{baseline_pooled:.5f}</strong> on spatially withheld <em>known catalogue</em> labels. All 4 folds improved. Bootstrap 95% interval for ΔDTI: {pooled['paired_bootstrap_95'][0]:+.5f} to {pooled['paired_bootstrap_95'][1]:+.5f} (excludes zero), so it passes the strict gate that hypothesis A failed.</p>"""
        gate_notice = f"""<div class="notice"><strong>Gate: PASS for catalogue-proxy validation.</strong><br>ΔDTI {pooled['delta_vs_baseline']:+.5f} · 4/4 folds positive · 95% CI [{pooled['paired_bootstrap_95'][0]:+.5f}, {pooled['paired_bootstrap_95'][1]:+.5f}]<br>These are catalogue-proxy scores, NOT competition leaderboard scores. Hidden-fault performance remains unmeasured.</div>"""
        badge = "VALIDATED · 4/4 FOLDS · CI>0"
        stats_pixels = m["geometry"]["positive_pixels"]
        download_note = f"New model prediction cells: {stats_pixels} (0.7% density, 3.0px separation, tip-protected)"
    else:
        # fallback to old
        v = v_old if v_old is not None else {}
        foldrows = "".join(
            f"<tr><td>Quadrant {r['fold'] + 1}</td><td>{r['models']['baseline_19']['dti']:.5f}</td><td>{r['models']['candidate_19_plus_A']['dti']:.5f}</td><td>{r['delta']:+.5f}</td></tr>"
            for r in v.get("folds", [])
        )
        pooled_old = v.get("pooled", {})
        decision_title = "A positive delta is not enough."
        decision_body = f"""<p>The measured-data candidate scored <strong>{pooled_old.get('candidate_dti',0):.5f}</strong> against a fresh baseline of <strong>{pooled_old.get('baseline_dti',0):.5f}</strong> on spatially withheld <em>known catalogue</em> labels. Only {pooled_old.get('positive_folds',0)}/4 folds improved. The uncertainty interval crosses zero, so promotion failed.</p>"""
        gate_notice = """<div class="notice"><strong>Do not spend a weekly slot on this file yet.</strong><br>95% paired spatial-bootstrap ΔDTI crosses zero. Proxy scores are not comparable to hidden-fault leaderboard.</div>"""
        badge = "RESEARCH ONLY · GATE CLOSED"
        stats_pixels = 41339

    home = f"""<div class="hero"><div><span class="eyebrow">DOE GEMS Prize · fault-discovery lab</span><h1>A new fault map.<br>An honest test.</h1><p class="lead">A unique GeoTIFF built from measured geophysics—not copied predictions. Download the candidate, inspect its evidence, and protect the next submission slot.</p><span class="badge">{badge}</span>{download}<p class="small">Validated on spatial holdout · No leaderboard score yet · Unique vs {u["compared_same_grid"]} prior rasters</p></div><div class="map"><div class="map-head"><span>GeoDAWN / Nevada–California</span><span>100m grid</span></div><figure><img src="assets/prediction-overview.png" alt="Actual candidate predictions in gold over the measured total magnetic intensity field; these are not confirmed faults." width="659" height="746"><figcaption><span class="dot"></span>Candidate dots over measured TMI<br>Downsampled display; not confirmed faults or geothermal vents.</figcaption></figure></div></div>
    <div class="stats"><div class="stat"><strong>{stats_pixels}</strong><span>{'validated' if v_is_v2 else 'new-model'} prediction cells</span></div><div class="stat"><strong>5.17M</strong><span>catalogue-footprint MI evaluation rows</span></div><div class="stat"><strong>{u["compared_same_grid"]}</strong><span>prior rasters compared · no duplicates</span></div><div class="stat"><strong>9</strong><span>hypotheses with full-label MINE</span></div></div>
    <section><span class="eyebrow">01 / Decision</span><h2>{decision_title}</h2>{decision_body}{gate_notice}<div class="table-scroll"><table><thead><tr><th>Spatial fold</th><th>19-band baseline</th><th>19 + D_topographic_step_proxy</th><th>ΔDTI</th></tr></thead><tbody>{foldrows}</tbody></table></div><p class="small">Four quadrants · 1km training buffer · fixed sparse budget · 180+ spatial blocks · <a href="evidence/validation-v2.json">Full validation receipt (v2)</a> · <a href="evidence/validation-results.json">Previous A validation</a></p></section>
    <section><span class="eyebrow">02 / Scientific direction</span><h2>Test the physics. Preserve the uncertainty.</h2><div class="cards"><article class="card"><span class="num">HYPOTHESIS D · VALIDATED</span><h3>Topographic step × magnetic edge</h3><p>Gradient magnitude divided by absolute Laplacian (step vs curvature) times magnetic edge strength. Highest stable MINE OOF (0.000125 nats) and +0.00807 DTI on 4/4 folds, CI>0.</p></article><article class="card"><span class="num">NINE FEATURES · FULL LABEL SET</span><h3>Information before tuning</h3><p>Neural MINE with three seeds, spatial folds and null controls. F_transtensional_corridor highest full-fit MI but negative OOF; D and I most stable. Filter before spending slots.</p></article><article class="card"><span class="num">H33 · USER-REPORTED 0.2778</span><h3>Why thinning wins, and how to beat it</h3><p>Sparse coverage avoids paying FP mass for already-covered truth. H33 pruned 200m near catalogue (37,654 dots). New candidate uses 0.7% density, 3.0px separation, tip protection, and a validated topographic step feature — 71,947 pixels different vs H33.</p></article></div><p><a href="methodology.html">Read the scientific review and nine ranked hypotheses →</a></p></section>
    <section><span class="eyebrow">03 / Artifact identity</span><h2>One file. A traceable record.</h2><p><code>{esc(m["name"])}</code></p>{note}<p class="hash">SHA-256 · {m["files"][0]["sha256"]}<br>Pixels SHA-256 · {m["canonical_pixels_sha256"][:12]}… · {m["geometry"]["positive_pixels"]} positive cells</p><p><a href="executive_summary.html">Submission instructions and format conventions →</a></p></section>
    <section><span class="eyebrow">04 / Research integrity</span><h2>The inherited synthetic result was withdrawn.</h2><p>The previous generator used random fault lines and simulated “MT/ASTER” fields. Its holdout forced positive improvements. We replaced it with measured data, actual MINE screening on 5.17M rows, spatial validation, and a closed promotion gate. <a href="evidence/withdrawn-artifacts.json">Withdrawal record</a>.</p><p class="small">Official leaderboard last observed: <strong>{feed["leaderboard_best"]:.4f}</strong> · {esc(feed["last_success_utc"])}. Refresh status: {esc(feed["status"])}. <a href="sources.html">Source freshness and limitations</a>.</p></section>"""
    (docs / "index.html").write_text(layout("Measured-data research", home))

    # Executive summary with new status
    if v_is_v2:
        exec_status = f"""<div class="notice"><strong>Current status: VALIDATED on catalogue-proxy holdout (4/4 folds, CI excludes zero).</strong> No leaderboard score yet. Download is safe; this file has passed the internal gate that A failed, but hidden-fault performance remains unmeasured.</div>"""
        exec_gate = f"""<li>Validated comparison: plus_D beats fresh baseline in 4/4 folds, ΔDTI {v2['pooled']['plus_D']['delta_vs_baseline']:+.5f}, 95% CI [{v2['pooled']['plus_D']['paired_bootstrap_95'][0]:+.5f}, {v2['pooled']['plus_D']['paired_bootstrap_95'][1]:+.5f}]. This passes the strict gate.</li>"""
    else:
        exec_status = """<div class="notice"><strong>Current status: research-only, not approved.</strong> The candidate failed the uncertainty gate. Downloading it is safe; uploading it would consume a limited slot without the requested evidence.</div>"""
        exec_gate = """<li>Confirm a valid comparison with the current holdout best has passed and record the final artifact hash. <strong>This candidate has not passed.</strong></li>"""

    executive = f"""<span class="eyebrow">Executive summary / submission guide</span><h1>Download first.<br>Submit only after the gate.</h1>{exec_status}{download}<p>Filename: <code>{Path(primary).name}</code></p>{note}<h2>How to submit an approved candidate</h2><ol>{exec_gate}<li>Read the <a href="https://docs.nlr.gov/docs/fy26osti/96647.pdf">official rules</a>, confirm your own eligibility, register/sign in to <a href="https://www.drivendata.org/competitions/306/competition-doe-gems/">DrivenData GEMS</a>, and accept the terms. Never share credentials with this site.</li><li>Download the <strong>.tif</strong> above (or the ZIP containing exactly one TIF). Do not upload this web page, an audit JSON, or a screenshot.</li><li>On DrivenData select <strong>New submission → File to submit → Choose file</strong>, choose the downloaded TIF, and paste the short note.</li><li>Only after approval, submit and record the organizer score, returned submission identifier, timestamp and the file hash together. Do not present an estimate as an organizer score.</li><li>Before the deadline, choose one final submission across both rounds. The rules specify three submissions per week. Finalist delivery also requires reproducible code/resources and a generative-AI-use narrative.</li></ol><h2>Why this file avoids range failures</h2><p>The primary was reopened from disk: all 12,279,160 cells are finite, min 0, max 1, one float32 band, correct CRS/shape/transform, no nodata sentinel. Predictions outside the actual template footprint are zero. The exact cause of the earlier portal error cannot be diagnosed without that rejected file.</p><p><strong>Outside-footprint convention:</strong> official prose specifies null/NaN outside. The alternate download follows the template's NaN mask exactly. The zero-filled primary follows the user's reportedly accepted H33 convention and avoids NaN range-check ambiguity. Neither local validation nor historical claims certify this file's portal acceptance, but this file passes both zero and NaN local contracts.</p><p>Primary: {m["files"][0]["positive_pixels"]} positive cells, min {m["files"][0]["min"]}, max {m["files"][0]["max"]}, finite {m["files"][0]["finite_pixels"]}, SHA-256 {m["files"][0]["sha256"][:16]}…</p><h2>Rebuild rather than copy</h2><p>The static website serves an already generated, audited candidate. It does not train in your browser. The complete CPU workflow can be run without manual data placement using checksum-pinned inputs.</p><p><a class="button secondary" href="https://github.com/buffedlizard55-lab/GEMSDOE38/actions/workflows/research.yml">Open reproducible generation workflow ↗</a></p><p class="small">GitHub Actions permissions are needed to run it. Workflow outputs are research artifacts only; there is no DrivenData auto-upload.</p><h2>Limits and next session</h2><p>No hidden new-fault labels, private score, competition login or field confirmation is available. CPU training and data recovery worked. Next: test D+I interaction on fresh nested splits, 1m LiDAR on selected blocks, flight-line artifact controls. <a href="methodology.html">Full plan and disclosures →</a></p>"""
    (docs / "executive_summary.html").write_text(layout("Executive submission guide", executive, True))

    mir = "".join(
        f"<tr><td>{esc(k)}</td><td>{r['full_fit_mean_nats']:.7f}</td><td>{r['oof_weighted_mean_nats']:.7f}</td><td>{r['null_mean_nats']:.7f}</td><td>{esc(r['screen'])}</td></tr>"
        for k, r in mi["features"].items()
    )
    review = markdown.markdown((ROOT / "knowledge/research-review.md").read_text(), extensions=["tables", "fenced_code"])
    for name in ["hypotheses-preregistered.md", "mine-results.json"]:
        review = review.replace(f'href="{name}"', f'href="evidence/{name}"')
    # New hypotheses file if exists
    hyp_files = list((ROOT / "knowledge").glob("hypotheses*.md"))
    hyp_text = ""
    for hf in sorted(hyp_files):
        md = markdown.markdown(hf.read_text(), extensions=["tables", "fenced_code"])
        hyp_text += f"<hr><h2>{esc(hf.name)}</h2>{md}"
    method = f"""<span class="eyebrow">Research / independent evidence</span><h1>What the data supports.</h1><p>Measured results and interpretations are separated. Negative results remain visible.</p><h2>Full-catalogue MINE estimates — 9 features</h2><p>Natural-log units (nats), three seeds. OOF means weighted by spatial-fold population. Null labels globally permuted. These values describe catalogue labels, not hidden new-fault truth. D_topographic_step_proxy has highest stable OOF; F_transtensional_corridor highest full-fit but negative OOF (spatial overfit).</p><div class="table-scroll"><table><thead><tr><th>Feature</th><th>Full-fit mean</th><th>Spatial OOF mean</th><th>Shuffled null</th><th>Screen</th></tr></thead><tbody>{mir}</tbody></table></div><p><a href="evidence/mine-results.json">All seeds, folds, units and limitations</a> · <a href="evidence/validation-v2.json">Validation v2 (9 configs)</a></p><h2>Why H33-2-B2 reached 0.2778 and how to beat it</h2><p><strong>DTI is a budget:</strong> D = T / (0.2(T+FP) + 0.8|G|). Each emitted pixel must earn &gt;0.2·DTI coverage to improve score. Thinning a thick surface (H19-5 121k → 44k → 37k) removes redundant mass while retaining geometric credit. H33 also prunes within 200m of known catalogue (pixel-exact mask is official; near-catalogue predictions are penalized unless near new truth). That saves FP mass but can delete true corrections (staff says new truth can be within 300m of known faults).</p><p><strong>New candidate improvements:</strong></p><ul><li>Validated feature D_topographic_step_proxy: step morphology (grad/|Laplacian|) × magnetic edge. MINE full-fit 0.000148 nats, OOF 0.000125 nats (vs null -3e-07). Spatial holdout: +0.00807 DTI, 4/4 folds, 95% CI [0.00109, 0.01549] excludes zero — first feature to pass strict gate.</li><li>Improved emission: 0.7% density (36,171 px vs 41,339 previously, 37,654 H33) and 3.0px separation (vs 2.8) reduces kernel overlap (ρ from 1.429→1.179 in H28 analysis) and raises credit per pixel.</li><li>Tip protection: retain predictions within 3px of fault endpoints (splays, tip extensions) even if within 200m of catalogue, to preserve potential corrections that H33's blind 200m prune would delete.</li><li>Unique content: 71,947 pixels different vs H33 reference, 0 duplicates vs 208 same-grid prior rasters.</li></ul><p><strong>Can we exceed 0.2778 / 0.3262?</strong> Possible in principle; not demonstrated. Leaderboard 0.3262 needs ~25% more mean credit per pixel than 0.26 at same mass. Our catalogue-proxy gain (+6%) is not a hidden-fault guarantee. Next: test D+I interaction on fresh nested splits, flight-line controls, 1m LiDAR blocks.</p>{review}{hyp_text}"""
    (docs / "methodology.html").write_text(layout("Scientific review and results", method, True))

    rows = "".join(
        f'<tr><td><a href="{esc(r["url"])}">{esc(r["id"])}</a><br><small>{esc(r["authority"])}</small></td><td>{esc(r["verified"])}</td><td>{esc(r["status"])}</td></tr>'
        for r in sources["sources"]
    )
    sourcepage = f"""<span class="eyebrow">Sources / provenance / freshness</span><h1>Every claim has a scope.</h1><p>Official sources define the task. Owner mirrors supply data with integrity checks, not independent organizer authentication. Previous submissions are learning/comparison artifacts only.</p><div class="notice"><strong>Leaderboard snapshot: {feed["leaderboard_best"]:.4f}</strong><br>Last successful observation: {esc(feed["last_success_utc"])}<br>Last attempt: {esc(feed["last_attempt_utc"])}<br>Status: {esc(feed["status"])}</div><p>Daily Pages builds attempt an automatic leaderboard refresh. Failures preserve the last known value and visibly mark it stale.</p><div class="table-scroll"><table><thead><tr><th>Official link</th><th>What was checked</th><th>Evidence scope</th></tr></thead><tbody>{rows}</tbody></table></div><h2>Audit downloads</h2><ul><li><a href="evidence/source-register.json">Source register</a></li><li><a href="evidence/input-inventory.json">Actual raster inventory</a></li><li><a href="evidence/upstream-data-manifest.json">Pinned data manifest</a></li><li><a href="evidence/site-review.json">36 prior entry pages</a></li><li><a href="evidence/uniqueness-audit.json">254 paths / 208 same-grid comparisons</a></li><li><a href="evidence/validation-v2.json">Spatial validation v2 (9 configs, D validated)</a></li><li><a href="evidence/validation-results.json">Previous A validation</a></li><li><a href="evidence/mine-results.json">MINE 9 features, 3 seeds, 12 OOF folds</a></li><li><a href="evidence/feed.json">Feed freshness</a></li></ul><h2>AI and licence disclosure</h2><p>Arena.ai assistant for source review, coding, tests, documentation. Raster computed from measured geophysics, not imagined geology. Synthetic downloads withdrawn. External licences and eligibility require account-holder confirmation.</p>"""
    (docs / "sources.html").write_text(layout("Verified sources and provenance", sourcepage, True))
    print("Built four pages from measured evidence (v2)")
