# Doc 4c Verification: nora_eef5

Date: 2026-05-30

## Artifacts

- `analysis_note/ANALYSIS_NOTE_doc4c_v1.tex`
- `analysis_note/ANALYSIS_NOTE_doc4c_v1.pdf`
- `analysis_note/figures/doc4c_reference_comparison.pdf`
- `analysis_note/figures/doc4c_reference_comparison.png`
- Refreshed staged Phase 4a expected figures in `analysis_note/figures/`
- Staged Phase 4c observed figures in `analysis_note/figures/`

## Commands Run

- `/sandbox/fake_home/.pixi/bin/pixi run py - <<'PY' ...` to read JSON values
  and generate `doc4c_reference_comparison.{pdf,png}`
- `/sandbox/fake_home/.pixi/bin/pixi run tectonic --outdir analysis_note analysis_note/ANALYSIS_NOTE_doc4c_v1.tex`
- `grep -R "\\tbd" analysis_note/ANALYSIS_NOTE_doc4c_v1.tex`
- `grep -n "105 < m4l < 140\\|105 < m_{4\\ell} < 140\\|105<m_{4\\ell}<140\\|105--140\\|fit window 105" analysis_note/ANALYSIS_NOTE_doc4c_v1.tex`
- `/sandbox/fake_home/.pixi/bin/pixi run lint-plots`
- `/sandbox/fake_home/.pixi/bin/pixi run py - <<'PY' ...` for figure
  existence, JSON-number consistency, and page-count extraction from aux

## Results

- Compile: PASS, PDF written to `analysis_note/ANALYSIS_NOTE_doc4c_v1.pdf`
- Page count: 73 pages from `\@abspage@last`
- `\tbd` grep: clean (`grep_exit=1`)
- Active-result narrow-window grep: clean. Remaining `105<m4l<140`
  references are absent from active-result body text; CMS/reference-method
  context is retained only in explicitly labeled prose.
- Figure references: 58 total, 58 unique, 0 missing
- Plot lint: PASS, no plotting violations in 34 checked files
- Key JSON-number consistency checks present in the note:
  - observed `mu = 2.4776 -0.7139 +0.8388`
  - symmetric uncertainty `0.7763`
  - GoF `47.326/38`, `p = 0.1427`
  - deviance `48.685`, `p = 0.1148`
  - expected-vs-observed pull `1.535`
  - partial-vs-observed pull `1.587`
  - mass best grid point `125.0 GeV`
  - active fit window `70 < m_{4\ell} < 170`

## User Correction Applied

The full-data reference comparison now includes center-of-mass energy and
luminosity labels. The mass panel uses:

- This analysis: `13 TeV, 10 fb^-1`, `mH = 125.0 GeV` shown with a visual
  coarse-grid half-step of `1.25 GeV`, explicitly not a stat/syst uncertainty.
- CMS-HIG-16-041 / JHEP 11 (2017) 047: `13 TeV, 35.9 fb^-1`,
  `mH = 125.26 +/- 0.20(stat) +/- 0.08(syst) GeV`; total plotted as
  `sqrt(0.20^2 + 0.08^2) = 0.215 GeV`.
- CMS-HIG-19-001 signal-strength line: `13 TeV, 137 fb^-1`.
- PDG 2024 mass: world average, not dataset-specific, with total
  uncertainty `0.11 GeV`.

The AN prose, comparison table, and figure caption now state that a calibrated
stat/syst mass uncertainty is unavailable for the detector-level shifted-template
scan.

## Remaining Limitations

- The result remains detector-level and not a fiducial cross-section
  measurement.
- Reducible background remains a DY+jets MC fake proxy rather than a CMS-style
  data-driven Z+X estimate.
- Grouped MC-stat treatment remains an approximation, not full bin-by-bin
  `staterror`.
- The mass scan is a shifted-template diagnostic, not an official calibrated
  Higgs mass measurement.
