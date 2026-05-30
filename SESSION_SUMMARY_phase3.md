# Session Summary: Phase 3

Date: 2026-05-29
Phase: Phase 3 Selection

## Outcome

Phase 3 passed after one review iteration.

Key commits:

- `2219723` — initial Phase 3 selection processing
- `3f427e1`, `e248213`, `c3e7c8e` — VERIFY fixes
- `0bf8908`, `34155e3`, `63227ca`, `c7d6adf` — Level 2 plot-validation fixes
- `01b0066` — Phase 3 review-iteration fixes
- `570d36c` — targeted verification of review fixes

Final review evidence:

- `phase3_selection/review/critical/PHASE3_CRITICAL_REVIEW2_ursula_0b8b_2026-05-29.md`
- `phase3_selection/review/validation/PHASE3_PLOT_VALIDATION2_vera_6cf0_2026-05-29.md`
- `REGRESSION_CHECK_phase3.md`

## Selection Handoff

The selected nominal Phase 4 handoff is S1 final-state categories:
`4mu`, `4e`, and `2e2mu` in `105 < m4l < 140 GeV`.

This is a conditional low-count handoff, not an unconditional binning pass:
`17/18` final-state bins have `S+B < 5`, so Phase 4 must validate low-count
Poisson/toy behavior and MC-stat stability before reporting fit results. If
those checks fail, Phase 4 must rebin or merge categories.

## Key Phase 3 Results

- Primary prompt paths only; no local/primary mixing.
- VBF formally downscoped: no real jet/VBF branches and no allowed safe
  upstream event-key join source.
- DY+jets remains the nominal reducible fake proxy; TTBar remains diagnostic.
- Angular reconstruction closure passed with zero out-of-range angular values.
- D7 input gate passed only `lead_abs_eta` and `phi1`.
- S2 classifier approach was attempted but rejected; S1 has the better expected
  `mu` proxy and passes the documented handoff conditions.
- Figure registry contains 30 PNG/PDF pairs and passes fresh Level 3 plot
  validation.

## Phase 4a Obligations

- Build the `pyhf`/HistFactory-style workspace from `fit_inputs_s1.json`.
- Use one global `mu` and include MC-stat modifiers and systematic nuisance
  structure.
- Validate low-count final-state bins with Poisson/toy and MC-stat stability
  checks; rebin/merge if needed.
- Run expected signal-strength inference, GoF, pulls/impacts, injection tests,
  and the binding mass-extraction/method-parity attempt or documented
  infeasibility.

## Human Inputs

No new human decision was requested during Phase 3. The prior instruction to
pass the Doc 4b human gate directly remains pending for the Doc 4b gate.
