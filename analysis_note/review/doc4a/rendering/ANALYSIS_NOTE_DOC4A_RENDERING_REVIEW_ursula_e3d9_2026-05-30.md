VERDICT: ITERATE

# Doc 4a Rendering Review

Session: `ursula_e3d9`  
Date: 2026-05-30  
Artifact reviewed: `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex` and `analysis_note/ANALYSIS_NOTE_doc4a_v1.pdf`

## Summary

The note compiles successfully with `pixi run tectonic --keep-logs analysis_note/ANALYSIS_NOTE_doc4a_v1.tex`. The retained log reports 66 pages, no unresolved citations, no unresolved cross-references, and no overfull boxes. The review does find one blocking rendering/readability issue in a figure caption, plus a small set of non-blocking underfull-box warnings concentrated in narrow tables.

## Compile / Mechanical Checks

- Compile command: `pixi run tectonic --keep-logs analysis_note/ANALYSIS_NOTE_doc4a_v1.tex`
- Compile result: PASS
- Page count: 66 pages (`analysis_note/ANALYSIS_NOTE_doc4a_v1.log`, `Output written on ... (66 pages, ...)`)
- Unresolved citations: none found in log
- Unresolved cross-references: none found in log
- Overfull boxes: none found in log
- Underfull boxes: present at source lines 248-250, 549-555, 766, 837, 841-843 via log line mapping

## Findings

### A1. Figure caption contains a raw Python-dictionary dump and should be rewritten into prose

- Severity: A
- Evidence: [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:766)
- What the reader sees: the caption for `fig:sideband-dy-ttbar-diagnostics` includes a long literal mapping with braces, quoted keys, escaped underscores, and full-precision floats.
- Why this is a rendering/layout defect: captions are part of the rendered product. Dumping a Python literal into a caption makes the figure hard to read, encourages ugly line wrapping, and is exactly the kind of formatting defect a referee will notice even if TeX technically compiles it.
- Root cause: the source appears to have inserted serialized structured data directly into prose rather than converting it to a sentence or compact table.
- Required fix: rewrite the caption to plain prose with rounded values, e.g. describe the three region ratios inline without braces/quoted keys/full machine precision.

### B1. Underfull-box warnings in narrow longtable rows of the systematics inventory

- Severity: B
- Evidence: [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:248), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:249), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:250)
- Likely cause: column widths are tight relative to entries such as `grouped MC-stat downscope`, `per-sample prompt xsecs`, and `implemented prompt fallback`.
- Impact: likely loose interword spacing rather than overflow. Since there are no overfull boxes, this does not currently look blocking.

### B2. Underfull-box warnings in the comparison matrix

- Severity: B
- Evidence: [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:549), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:550), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:552), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:554), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:555)
- Likely cause: long reference strings and comparability text in fixed-width `p{...}` columns.
- Impact: likely visible spacing looseness. Not blocking on current evidence, but worth tightening if the table is revised anyway.

### B3. Underfull-box warnings in the limitation index

- Severity: B
- Evidence: [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:837), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:841), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:842), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:843)
- Likely cause: compact `p{...}` columns combined with long status/impact text.
- Impact: likely cosmetic only unless the rendered page shows visually distracting rivers of whitespace.

## Notes on PDF Inspection

I compiled the PDF and inspected the renderability evidence available locally: successful TeX/BibTeX passes, 66-page output, no unresolved refs/citations, and no overfull boxes. This environment does not provide a working local PDF rasterizer/viewer (`pdfinfo`, `pdftotext`, `pdftoppm`, `mutool`, Ghostscript, or a browser-based PDF path), so the review could not perform page-image inspection beyond source/log-backed rendering checks.

That limitation does not change the blocking verdict above: A1 is visible directly in the source and is a document-quality defect independent of viewer tooling.
