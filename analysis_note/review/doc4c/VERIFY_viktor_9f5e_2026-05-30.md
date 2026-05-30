# VERIFY viktor_9f5e 2026-05-30

Session: `viktor_9f5e`

## Commands Run

- `git status --short --branch`
- `git rev-parse --short HEAD`
- `pixi run p4c-all`
- `pixi run py phase4_inference/4c_observed/src/build_inference_artifact.py && pixi run py phase4_inference/4c_observed/src/update_commitments_phase4c.py`
- `pixi run tectonic --outdir analysis_note analysis_note/ANALYSIS_NOTE_doc4c_v1.tex`
- `pixi run lint-plots`
- `grep -n "\\tbd" analysis_note/ANALYSIS_NOTE_doc4c_v1.tex || true`
- `grep -n "mva_roc_bdt.pdf\\|mva_roc_bdt_tuned.pdf\\|mva_roc_logistic.pdf\\|mva_roc_small_nn.pdf" analysis_note/ANALYSIS_NOTE_doc4c_v1.tex || true`
- `grep -n "105 *<.*140\\|105<.*140" analysis_note/ANALYSIS_NOTE_doc4c_v1.tex || true`
- Python JSON/figure-reference consistency checks through `pixi run py`.

## Physics Values

- Active signal-strength fit window: `[70.0, 170.0]` GeV, including the Z peak.
- Observed signal strength: `mu = 2.4776040008517612 -0.7138966295430187 +0.8387787105161486`.
- Observed mass scan method: shifted M125 detector-level templates, `mu` profiled at each mass hypothesis.
- Coarse mass grid: `110-150` GeV in `2.5` GeV steps.
- Fine local mass grid: `122-128` GeV in `0.25` GeV steps around the coarse `125.0` GeV minimum.
- Refined reported center: `mH = 124.75` GeV.
- Diagnostic grid half-step/resolution style: `0.125` GeV half-step from the 0.25 GeV fine grid; not a stat/syst uncertainty.
- Diagnostic quadratic interpolation: `125.4239052495179` GeV, explicitly labeled diagnostic and not used as the reported center.
- Diagnostic grid interval: `[124.75, 125.5]` GeV by the grid-level `Delta(-2 ln L) <= 1` criterion.
- MVA training window: `80 < m4l < 170` GeV.
- Repaired best MVA: `bdt_mass_safe`, AUC `0.7929042332570392`.
- JHEP-like diagnostic BDT AUC: `0.9176181009228579`, diagnostic only because it includes mass-like variables.
- MVA precision-proxy relative improvement: `0.1902098976350023`.
- MVA promotion: `promote_s2 = false`; nominal result remains S1 final-state categories.

## Checks

- `pixi run p4c-all`: PASS after schema updates for `coarse_step` and `fine_step`.
- `pixi run tectonic --outdir analysis_note analysis_note/ANALYSIS_NOTE_doc4c_v1.tex`: PASS; PDF written to `analysis_note/ANALYSIS_NOTE_doc4c_v1.pdf`. Only underfull hbox warnings in dense tables.
- `pixi run lint-plots`: PASS, no plotting violations in 34 files.
- No `\tbd` remains in Doc 4c TeX.
- All `\includegraphics{figures/...}` references in Doc 4c exist on disk and are non-zero.
- Stale MVA filenames are absent from Doc 4c source: `mva_roc_bdt.pdf`, `mva_roc_bdt_tuned.pdf`, `mva_roc_logistic.pdf`, `mva_roc_small_nn.pdf`.
- Active 105-140 GeV current-fit claims: CLEAN. Remaining `105<m4l<140` mentions are explicitly user-request/reference-method/historical context.
- JSON consistency: PASS for refined `mH`, `mu`, fit window, MVA AUC, and `promote_s2=false`.
- Main-body comparison placement: PASS. `doc4c_reference_comparison` remains in the main Comparison section; `expected_reference_comparison` is explicitly secondary/continuity.
- Comparison uncertainty style: PASS. `doc4c_reference_comparison` shows CMS-HIG-16-041/JHEP mass as `125.26 +/- 0.20(stat) +/- 0.08(syst)` GeV with capped statistical and uncapped systematic component styling. This analysis is labeled with diagnostic fine-grid half-step only, not stat/syst.
- Dataset labels: PASS. Comparison figure labels include `13 TeV, 10 fb^-1` for this analysis and `13 TeV, 35.9 fb^-1` for CMS-HIG-16-041; PDG is labeled world average.

## Files Touched

- Phase 4c scan/schema/plot code:
  - `phase4_inference/4c_observed/src/run_observed_inference.py`
  - `phase4_inference/4c_observed/src/make_observed_plots.py`
  - `phase4_inference/4c_observed/src/build_inference_artifact.py`
- Regenerated Phase 4c JSON/artifact/figures:
  - `analysis_note/results/observed_*.json`
  - `phase4_inference/4c_observed/outputs/INFERENCE_OBSERVED.md`
  - `phase4_inference/4c_observed/outputs/FIGURES.json`
  - `phase4_inference/4c_observed/outputs/figures/observed_mass_scan.{pdf,png}`
- Doc 4c staged figures and note:
  - `analysis_note/figures/observed_*.{pdf,png}`
  - `analysis_note/figures/mva_roc_bdt_mass_safe.{pdf,png}`
  - `analysis_note/figures/mva_roc_bdt_jhep_like_diagnostic.{pdf,png}`
  - `analysis_note/figures/mva_roc_logistic_mass_safe.{pdf,png}`
  - `analysis_note/figures/mva_roc_logistic_jhep_like_diagnostic.{pdf,png}`
  - `analysis_note/figures/mva_best_score_datamc.{pdf,png}`
  - `analysis_note/figures/doc4c_reference_comparison.{pdf,png}`
  - `analysis_note/ANALYSIS_NOTE_doc4c_v1.tex`
  - `analysis_note/ANALYSIS_NOTE_doc4c_v1.pdf`

## Remaining Limitations

- The mass scan remains a shifted-template diagnostic based on available M125 signal MC. It is not a calibrated CMS-quality mass measurement and has no stat/syst split for this analysis.
- Several fine-grid mass hypotheses used visible fallback fits or failed after all fallback attempts; failed points are retained in `observed_mass_scan.json` rather than hidden.
