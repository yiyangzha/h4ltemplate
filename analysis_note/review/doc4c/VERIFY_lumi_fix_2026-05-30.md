# Doc 4c Reference-Comparison Lumi Fix Verification

## Scope

Targeted fix for `analysis_note/figures/doc4c_reference_comparison.{pdf,png}` only. The physics numbers and `ANALYSIS_NOTE_doc4c_v1.tex` source were not changed.

## User-Requested Checks

- Main-body placement: PASS. `analysis_note/ANALYSIS_NOTE_doc4c_v1.tex` has `\section{Comparison to Prior Results and Theory}` at line 681 and includes `figures/doc4c_reference_comparison.pdf` at line 714.
- Luminosity labels: PASS by visual inspection of the regenerated PNG.
  - This analysis: `13 TeV, 10 fb^{-1}`.
  - CMS-HIG-16-041: `13 TeV, 35.9 fb^{-1}`.
  - CMS-HIG-19-001: `13 TeV, 137 fb^{-1}`.
  - PDG 2024: `world average` with no dataset luminosity.
- Legend removal: PASS. The regenerated figure has no legend blocks.
- Marker style: PASS. All measurement points use black square markers.
- Error-bar style: PASS. Total/diagnostic bars are horizontal black bars; entries with statistical components use an inner capped statistical bar and an outer uncapped total/stat+syst bar.
- Axis range/readability: PASS by visual inspection; all uncertainty bars are inside the visible x-axis ranges.

## Commands

- `pixi run py - <<'PY' ...` regenerated `analysis_note/figures/doc4c_reference_comparison.pdf` and `.png`.
- `pixi run tectonic --outdir analysis_note analysis_note/ANALYSIS_NOTE_doc4c_v1.tex` completed successfully, with underfull-box warnings only.
- `pixi run lint-plots` passed with no plotting violations.
- `grep -n "Comparison to Prior Results and Theory\|doc4c_reference_comparison" analysis_note/ANALYSIS_NOTE_doc4c_v1.tex` confirmed main-body placement.

## Result

The previously incorrect `2.7 fb^{-1}` labels were replaced with the correct luminosities. The compiled Doc 4c PDF was regenerated after replacing the figure.
