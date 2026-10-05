"""Build static, evidence-driven Pages. A local proxy result never opens the slot gate."""

import html
import json
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / "knowledge" / name).read_text())


def esc(value):
    return html.escape(str(value))


def layout(title, body, article=False):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="GEMSDOE38 measured-data fault research, unique GeoTIFF research artifact, and transparent validation."><title>{esc(title)} · GEMSDOE38</title><link rel="stylesheet" href="assets/style.css"></head><body><a class="skip" href="#main">Skip to content</a><header><div class="wrap"><a class="brand" href="index.html">GEMS<span>DOE38</span></a><nav aria-label="Main navigation"><a href="index.html">Overview</a><a href="executive_summary.html">Submission guide</a><a href="methodology.html">Research &amp; results</a><a href="sources.html">Sources</a></nav></div></header><main id="main" class="wrap {"article" if article else ""}">{body}</main><footer><div class="wrap footer-row"><span>Maximize P(Win). Own the Outcome.<br>Evidence before a submission slot.</span><span>Research snapshot · 05 Oct 2026<br><a href="https://github.com/buffedlizard55-lab/GEMSDOE38">Code, user brief &amp; audit trail ↗</a></span></div></footer><script src="assets/site.js" defer></script></body></html>"""


def note_box(note):
    return f'''<div class="note-box"><button id="copy-note" type="button">Copy note</button><strong>Artifact distinction note (not submission approval)</strong><p id="submission-note">{esc(note)}</p><span id="copy-status" role="status" class="small"></span></div>'''


def main():
    manifest = read("submission-manifest.json")
    gate = read("slot-gate.json")
    mine = read("mine-results-v3.json")
    validation = read("validation-v3.json")
    feed = read("feed.json")
    sources = read("source-register.json")
    uniqueness = read("uniqueness-audit.json")

    docs = ROOT / "docs"
    evidence = docs / "evidence"
    evidence.mkdir(exist_ok=True)
    for path in (ROOT / "knowledge").glob("*"):
        if path.is_file() and path.suffix in {".json", ".md"}:
            shutil.copy2(path, evidence / path.name)
    downloads = docs / "downloads"
    downloads.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "knowledge/submission-manifest.json", downloads / "submission-audit.json")

    primary_receipt = manifest["files"][0]
    nan_receipt = manifest["files"][1]
    primary = "downloads/" + Path(primary_receipt["path"]).name
    nan = "downloads/" + Path(nan_receipt["path"]).name
    zip_path = primary.replace(".tif", ".zip")
    note = manifest["submission_note"]
    download = f'''<div class="actions"><a class="button" download href="{primary}">↓ Download unique research GeoTIFF</a><a class="button secondary" download href="{zip_path}">ZIP</a></div><p class="small">Local format checks passed · portal acceptance untested<br><a href="{nan}" download>NaN-outside alternative</a> · <a href="downloads/submission-audit.json">Local format/provenance receipt</a></p>'''

    # Display v3 MINE without labelling it as conditional information or truth.
    mine_rows = []
    for name, row in mine["features"].items():
        mine_rows.append(
            f"<tr><td>{esc(name)}</td><td>{row['full_fit_mean_nats']:.7g}</td>"
            f"<td>{row['oof_weighted_mean_nats']:.7g}</td><td>{row['null_mean_nats']:.7g}</td>"
            f"<td>{esc(row['screen'])}</td></tr>"
        )
    mine_table = "".join(mine_rows)

    fold_rows = []
    for fold in validation["folds"]:
        models = fold["models"]
        delta = models["plus_D_J"]["dti"] - models["plus_D"]["dti"]
        fold_rows.append(
            f"<tr><td>Quadrant {fold['fold'] + 1}</td>"
            f"<td>{models['baseline_19']['dti']:.5f}</td>"
            f"<td>{models['plus_D']['dti']:.5f}</td>"
            f"<td>{models['plus_D_J']['dti']:.5f}</td>"
            f"<td>{delta:+.5f}</td></tr>"
        )
    delta_j = validation["comparisons"]["plus_D_J_vs_plus_D"]
    gate_reasons = "".join(f"<li>{esc(reason)}</li>" for reason in gate["reasons_closed"])

    badge = "RESEARCH ONLY · SLOT GATE CLOSED"
    hero = f"""<div class="hero"><div><span class="eyebrow">DOE GEMS Prize · measured-data research</span><h1>A unique map.<br>An honest gate.</h1><p class="lead">A distinct GeoTIFF derived from measured geophysics. It passes local file checks; no hidden-fault score or comparable current-best holdout is available.</p><span class="badge">{badge}</span>{download}<p class="small">Do not submit this file from the current evidence. Leaderboard snapshot: {feed['leaderboard_best']:.4f} on {esc(feed['last_success_utc'])}; no score is claimed for this candidate.</p></div><div class="map"><div class="map-head"><span>GeoDAWN / Nevada–California</span><span>100m grid</span></div><figure><img src="assets/prediction-overview.png" alt="Candidate research pixels in gold over measured total magnetic intensity; pixels are not confirmed faults." width="659" height="746"><figcaption><span class="dot"></span>Candidate pixels over measured TMI<br>Downsampled display; not confirmed faults or geothermal vents.</figcaption></figure></div></div>
    <div class="stats"><div class="stat"><strong>{manifest['geometry']['positive_pixels']:,}</strong><span>candidate cells · research only</span></div><div class="stat"><strong>{mine['population']:,}</strong><span>all-pixel MINE evaluation population</span></div><div class="stat"><strong>{uniqueness['compared_same_grid']}</strong><span>prior same-grid public rasters checked</span></div><div class="stat"><strong>3</strong><span>v3 feature arrays MINE-screened</span></div></div>
    <section><span class="eyebrow">01 / Decision</span><h2>Why the weekly slot remains protected</h2><div class="notice"><strong>Gate: CLOSED.</strong> The unique raster has local disk-reread format checks only. Neither portal acceptance nor an artifact-level win over a reproducible current-best holdout has been demonstrated.</div><ul>{gate_reasons}</ul><p><a href="evidence/slot-gate.json">Full gate requirements and evidence</a></p></section>
    <section><span class="eyebrow">02 / Preregistered test</span><h2>J did not add a reliable gain over D</h2><p>The primary asymmetric magnetic-flank hypothesis was selected before feature computation. In four spatial catalogue-proxy folds, 19+D+J vs 19+D was <strong>{delta_j['delta_dti']:+.6f} DTI</strong>, {delta_j['positive_folds']}/4 folds positive; paired 20km-block 95% interval [{delta_j['paired_block_bootstrap_95'][0]:+.6f}, {delta_j['paired_block_bootstrap_95'][1]:+.6f}]. This fails the preregistered incremental gate. The proxy uses incomplete public labels, where zero is unlabelled.</p><div class="table-scroll"><table><thead><tr><th>Spatial fold</th><th>19-band baseline</th><th>19 + D</th><th>19 + D + J</th><th>J increment vs D</th></tr></thead><tbody>{''.join(fold_rows)}</tbody></table></div><p class="small">Four geographic quadrants · 1km training exclusion · fixed HGB settings · equal 0.8% budget · 2.8-cell spacing · 180 paired 20km blocks · <a href="evidence/validation-v3.json">full v3 receipt</a>. A positive total D+J vs baseline does not prove J adds information beyond D.</p></section>
    <section><span class="eyebrow">03 / Information screen</span><h2>Full-label MINE is a filter, not an approval</h2><p>DV-MINE estimates marginal association with the public known-fault catalogue, not conditional gain over the 19 bands, hidden truth, or leaderboard score. Full-fit estimates can be optimistic; spatial OOF and global shuffled-label nulls are diagnostics.</p><div class="table-scroll"><table><thead><tr><th>Feature</th><th>Full-fit mean (nats)</th><th>Spatial OOF mean (nats)</th><th>Null mean (nats)</th><th>Screen</th></tr></thead><tbody>{mine_table}</tbody></table></div><p><a href="evidence/mine-results-v3.json">All seeds, folds and estimator limitations</a> · <a href="evidence/hypotheses-v3-preregistered.md">Pre-feature hypotheses and formulas</a> · <a href="evidence/hypotheses-v3-review-amendment.md">L implementation review amendment</a></p></section>
    <section><span class="eyebrow">04 / Artifact identity</span><h2>Unique raster, clear scope</h2><p><code>{esc(manifest['name'])}</code></p>{note_box(note)}<p class="hash">File SHA-256 · {primary_receipt['sha256']}<br>Canonical pixel SHA-256 · {manifest['canonical_pixels_sha256']}<br>{primary_receipt['positive_pixels']:,} binary positive cells · values [0,1]</p><p>No duplicate among {uniqueness['compared_same_grid']} retrievable same-grid blobs in 36 pinned sibling repositories; scope is not exhaustive beyond observed public artifacts.</p><p><a href="executive_summary.html">Executive guide: local format vs. submission readiness →</a></p></section>
    <section><span class="eyebrow">05 / Research integrity</span><h2>Unknowns stay visible</h2><p>The reported H33 score-to-file mapping is user-reported and has no organizer-exposed raster hash. Its sibling holdout recipe is not reproducible from the tracked tree, and its mirror receipt reproduced only 2/6 logged orderings (3/6 after calibration). No new candidate is claimed to beat it. The historical v2 D proxy result remains in the audit record but does not validate this final emitted raster.</p><p><a href="methodology.html">Read the complete scientific review, limitations and next steps →</a></p><p class="small">Leaderboard observation: <strong>{feed['leaderboard_best']:.4f}</strong> · {esc(feed['last_success_utc'])} · {esc(feed['status'])}. <a href="sources.html">Source register and freshness</a>.</p></section>"""
    (docs / "index.html").write_text(layout("Measured-data research", hero))

    executive = f"""<span class="eyebrow">Executive summary / submission guide</span><h1>Download for review.<br>Do not submit yet.</h1><div class="notice"><strong>Current status: research-only. Competition slot gate is CLOSED.</strong> The local format contract passes; portal acceptance, hidden-fault performance, and a comparable current-best holdout win are untested/unavailable.</div>{download}<p>Artifact: <code>{Path(primary).name}</code></p>{note_box(note)}<h2>Before any competition upload</h2><ol><li><strong>Do not use this artifact as a competition submission yet.</strong> First resolve the current-best holdout and pass the gate in <a href="evidence/slot-gate.json">the decision record</a>.</li><li>After the gate is open, review the <a href="https://docs.nlr.gov/docs/fy26osti/96647.pdf">official rules</a>, independently confirm eligibility, and sign in to <a href="https://www.drivendata.org/competitions/306/competition-doe-gems/">DrivenData GEMS</a>. Never share credentials with this site.</li><li>For an approved artifact only, download the <strong>.tif</strong> above (or its ZIP, which contains exactly one TIF). Do not upload this page, a JSON receipt, or a screenshot.</li><li>On DrivenData use <strong>New submission → File to submit → Choose file</strong>, then paste the approved artifact's short distinction note.</li><li>Record the organizer-returned submission ID, score, timestamp and exact file hash together. Do not present a local metric as an organizer score.</li><li>Preserve the final-round choice; rules specify three submissions per week and a single final selection across both rounds.</li></ol><h2>Local file checks (not portal certification)</h2><ul><li>Primary: single-band float32, EPSG:32611, shape 3730 × 3292, correct transform, all 12,279,160 cells finite, min {primary_receipt['min']}, max {primary_receipt['max']}, 36,171 positive cells, outside-footprint zero, no nodata tag.</li><li>NaN alternative: same canonical pixels inside footprint; NaN outside with NaN nodata. The competition prose specifies null/NaN outside; neither local encoding has been portal-tested.</li><li>SHA-256: <code>{primary_receipt['sha256']}</code>.</li></ul><p>The exact cause of the earlier portal range error cannot be diagnosed without the rejected raster/log. This file passes local range checks only; do not infer portal acceptance.</p><h2>What would reopen the gate?</h2><p>Recreate/hash the current-best holdout inputs and code; compare the current-best and candidate on identical frozen spatial test cells; show a robust incremental win without post-hoc tuning; and separately verify portal acceptance. Hidden expert labels remain unavailable here.</p><h2>Rebuild the research artifact</h2><p>The static website serves an existing audited file and does not train in the browser. See the <a href="https://github.com/buffedlizard55-lab/GEMSDOE38/actions/workflows/research.yml">research workflow</a> and local reproducibility commands in the README. There is no automatic DrivenData upload.</p><p class="small">AI-use disclosure and official rule interpretation are in the <a href="methodology.html">scientific review</a>. Account-holder eligibility and external-content rights must be verified by the account holder.</p>"""
    (docs / "executive_summary.html").write_text(layout("Executive submission guide", executive, True))

    review = markdown.markdown(
        (ROOT / "knowledge/research-review.md").read_text(),
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    hypotheses = markdown.markdown(
        (ROOT / "knowledge/hypotheses-v3-preregistered.md").read_text(),
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    for filename in [
        "hypotheses-v3-preregistered.md",
        "hypotheses-v3-review-amendment.md",
        "hypotheses-preregistered.md",
        "mine-results.json",
        "mine-results-v3.json",
        "validation-v3.json",
        "slot-gate.json",
    ]:
        review = review.replace(f'href="{filename}"', f'href="evidence/{filename}"')
        hypotheses = hypotheses.replace(f'href="{filename}"', f'href="evidence/{filename}"')
    method = f"""<span class="eyebrow">Research / independent evidence</span><h1>What the data supports.</h1><p>Measured results, proxy evaluations and interpretations are separated. Failed gates and uncertainty remain visible.</p><h2>Current decision</h2><p><strong>SLOT GATE CLOSED. Do not submit the current artifact. No current-best compatible reproducible holdout is available, and no claim to beat H33 or the leaderboard is made.</strong> The v3 J incremental comparison fails against D on the public catalogue proxy. See the <a href="evidence/slot-gate.json">gate record</a>.</p><h2>v3 preregistration</h2>{hypotheses}<h2>Complete review, historical context and next steps</h2>{review}<p><a href="evidence/mine-results.json">Historical v2 MINE receipt (nine features)</a> · <a href="evidence/validation-v2.json">Historical v2 proxy receipt</a> · <a href="evidence/submission-manifest.json">Research-artifact manifest</a></p>"""
    (docs / "methodology.html").write_text(layout("Scientific review and results", method, True))

    source_rows = "".join(
        f"<tr><td><a href=\"{esc(source['url'])}\">{esc(source['id'])}</a><br><small>{esc(source['authority'])}</small></td><td>{esc(source['verified'])}</td><td>{esc(source['status'])}</td></tr>"
        for source in sources["sources"]
    )
    sourcepage = f"""<span class="eyebrow">Sources / provenance / freshness</span><h1>Every claim has a scope.</h1><p>Official sources define the competition and geological context. Owner mirrors provide hash-checked inputs but not independent organizer authentication. Prior sites and score mappings are research context only.</p><div class="notice"><strong>Public leaderboard snapshot: {feed['leaderboard_best']:.4f}</strong><br>Last successful observation: {esc(feed['last_success_utc'])}<br>Last attempt: {esc(feed['last_attempt_utc'])}<br>Status: {esc(feed['status'])}</div><p>Refresh snapshots may fail or be stale. A public participant score is not linked to a file hash unless the organizer supplies one.</p><div class="table-scroll"><table><thead><tr><th>Review link</th><th>What was checked</th><th>Scope / result</th></tr></thead><tbody>{source_rows}</tbody></table></div><h2>Audit downloads</h2><ul><li><a href="evidence/source-register.json">Source register</a></li><li><a href="evidence/input-inventory.json">Raster inventory and hashes</a></li><li><a href="evidence/upstream-data-manifest.json">Pinned owner-mirror manifest</a></li><li><a href="evidence/site-review.json">36 prior entry-page snapshots</a></li><li><a href="evidence/uniqueness-audit.json">Public-artifact uniqueness audit</a></li><li><a href="evidence/hypotheses-v3-features.json">Feature hashes and diagnostics</a></li><li><a href="evidence/mine-results-v3.json">Full-label MINE v3</a></li><li><a href="evidence/validation-v3.json">Spatial validation v3</a></li><li><a href="evidence/slot-gate.json">Submission gate</a></li><li><a href="downloads/submission-audit.json">GeoTIFF local format receipt</a></li><li><a href="evidence/feed.json">Leaderboard snapshot receipt</a></li></ul><h2>AI and licence disclosure</h2><p>An Arena.ai assistant supported source review, coding, tests and documentation. The raster was computed by the measured-data pipeline, not generated as an imagined geological image. Synthetic inherited artifacts were withdrawn. The account holder must confirm eligibility and rights for any additional source data.</p>"""
    (docs / "sources.html").write_text(layout("Verified sources and provenance", sourcepage, True))
    print("Built four pages with gate-closed, catalogue-proxy-only status")


if __name__ == "__main__":
    main()
