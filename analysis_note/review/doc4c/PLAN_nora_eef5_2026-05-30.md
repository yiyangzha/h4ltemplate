# Doc 4c Plan: nora_eef5

Date: 2026-05-30

## Scope

Finalize `analysis_note/ANALYSIS_NOTE_doc4c_v1.tex` from Doc 4b using the
current Phase 4c full-data JSON and broad-window artifacts. Do not run a
review panel and do not rerun Phase 3/4 inference unless a required artifact is
missing.

## Inputs Read

- `TOGGLES.md`
- `agents/note_writer.md`
- `analysis_note/review/doc4c/CLAUDE.md`
- `methodology/analysis-note.md`
- `SESSION_STATE.md`
- `COMMITMENTS.md`
- `experiment_log.md`
- `analysis_note/ANALYSIS_NOTE_doc4b_v1.tex`
- `analysis_note/results/*.json`
- `phase4_inference/4c_observed/outputs/INFERENCE_OBSERVED.md`
- Phase 3, Phase 4a, Phase 4b, and Phase 4c figure registries

## Edit Plan

1. Stage refreshed Phase 4a expected figures and Phase 4c observed figures in
   `analysis_note/figures/`, preserving existing Phase 1/3/4b staged figures.
2. Generate `doc4c_reference_comparison.{pdf,png}` if no full-data public
   comparison figure exists.
3. Copy Doc 4b to `ANALYSIS_NOTE_doc4c_v1.tex`.
4. Update abstract, title, change log, event-selection language, statistical
   method, results, cross-checks, comparison, conclusions, future directions,
   and limitations so full data is primary and the 10% result is a validation
   cross-check.
5. Replace stale active-fit-window language with `70 < m_{4\ell} < 170` GeV.
   Keep `105 < m_{4\ell} < 140` only for explicitly labeled CMS/reference or
   historical user-request context.
6. Add Phase 4c observed figures to Results/Cross-checks and the full-data
   reference-comparison figure to Comparison.
7. Compile with `tectonic` from `analysis_note/`, fix errors, and run focused
   checks: no `\tbd`, no stale current-window claims, all figures exist,
   JSON-number consistency, and `pixi run lint-plots`.
8. Write verification notes and append logs, then commit with
   `docs(doc4c): finalize full-data analysis note`.

## Key Numbers From JSON

- Observed signal strength: `mu = 2.4776040008517612
  -0.7138966295430187 +0.8387787105161486`
- Observed symmetric uncertainty: `0.7763376700295836`
- Fit window: `70-170 GeV`
- Full-data events: `203/203`; channel counts: `2e2mu=98`, `4e=24`,
  `4mu=81`
- GoF: `chi2/ndf = 47.325956020331446/38`, `p = 0.14274016366544112`
- Deviance/p-value: `48.685092616701326`, `p = 0.11477688817271811`
- Expected-vs-observed pull: `1.5353747369536923`
- Partial-vs-observed pull: `1.5866596142632463`
- Observed mass scan best grid point: `125.0 GeV`, with `mu` profiled and
  not promoted to an official calibrated mass measurement.
