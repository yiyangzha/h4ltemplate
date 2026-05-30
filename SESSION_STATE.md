# Session State

Last updated: 2026-05-30T06:29:07Z
Current phase: Phase 4c — Full Data Inference / 70-170 fit-window regression
Step in loop: ITERATE — regression rerun complete; awaiting orchestrator VERIFY/review decision
Iteration count: 0

## Completed phases (commit hashes)

- Phase 1 checkpoint before fixes: `17d87dc`
- Phase 1 review fixes: `68a1505`
- Phase 1 PASS boundary: `e4b6cee`
- Phase 2 initial strategy checkpoint: `79620cc`
- Phase 2 review verdict checkpoint: `47b3de5`
- Phase 2 first fixes: `8e93f30`
- Phase 2 re-review checkpoint: `ca006ab`
- Phase 2 traceability fix: `fcdf1d9`
- Phase 2 PASS boundary: `0d45723`
- Phase 3 initial implementation: `2219723`
- Phase 3 VERIFY fixes: `3f427e1`, `e248213`, `c3e7c8e`
- Phase 3 Level 2 plot fixes: `0bf8908`, `34155e3`, `63227ca`, `c7d6adf`
- Phase 3 VERIFY/plot evidence checkpoint: `af51379`
- Phase 3 initial review findings: `0ac5236`
- Phase 3 review fixes: `01b0066`
- Phase 3 targeted fix verification: `570d36c`
- Phase 3 PASS boundary: `6940760`
- Phase 4a expected inference initial execution and VERIFY: `5351db4`
- Phase 4a per-figure validation: `8d19166`
- Phase 4a initial review findings: `6b1a514`
- Phase 4a review fixes: `ddcf18e`
- Phase 4a targeted verification: `0cbd76c`
- Phase 4a regression update: `be3a796`
- Phase 4a regression gate: `f7c3dff`
- Phase 4a corruption follow-up: `f214807`
- Phase 4a PASS boundary: `e72746d`
- Doc 4a draft note: `15ae12f`
- Doc 4a VERIFY exchange: `0ef5388`
- Doc 4a review findings: `435fdd4`
- Doc 4a review fixes: `8e7dd78`
- Doc 4a fix verification: `c33a925`
- Doc 4a PASS boundary: `829e1a9`
- Phase 4b broad-window partial inference: `6b6d88f`
- Phase 4b override summary: `130a316`
- Doc 4b note update: `b497d73`
- Doc 4b VERIFY exchange: `d631824`
- Doc 4b compact gate: `c6ce817`

## Current Work

Phase 3 passed after one review iteration. Regression worker `viktor_56ca`
kept the analysis in Phase 4c, removed the active narrow fit-window handoff,
and reran Phase 3 plus Phase 4c with `70 < m4l < 170 GeV` fit templates,
matching the Phase 4c observed fit window including the Z peak. No Doc 4c work
is active.

This handoff is conditional because many final-state bins have low expected
counts. Phase 4a/4c must run low-count Poisson/toy validation and MC-stat
stability checks before reporting fit results; otherwise it must rebin or
merge categories.

Key Phase 3 artifacts:

- `phase3_selection/outputs/SELECTION.md`
- `phase3_selection/outputs/fit_inputs_s1.json` with `fit_window = [70, 170]`
- `phase3_selection/outputs/selected_configuration.json`
- `phase3_selection/outputs/approach_comparison.json`
- `phase3_selection/outputs/FIGURES.json`
- `REGRESSION_CHECK_phase3.md`
- `SESSION_SUMMARY_phase3.md`

Phase 4a expected inference has passed its blocking gate with a documented
low-count limitation. Phase 3 MVA training/evaluation metadata now records the
broad `80 < m4l < 170 GeV` training window and a repaired BDT trial; S1 remains nominal.
Phase 4a includes broad `m4l` display metadata, a broadened `110-140 GeV`
shifted-template mass scan, per-systematic shifted-bin payloads, a
systematic-shift summary figure, and formal grouped-MC-stat downscope labeling.

The final-state simultaneous corruption sensitivity was run. `+20%` is
rejected, while `-20%` is not (`p = 0.45954`) after three documented attempts.
This is marked `documented_low_count_infeasible`, not passed. Phase 4b/4c must
repeat stability checks on observed subsets and merge/rebin if needed.

Doc 4a passed after review and fix verification. The expected-results analysis
note is `analysis_note/ANALYSIS_NOTE_doc4a_v1.pdf` (66 pages). Next step:
start Doc 4b from the current Phase 4b 10% results.

Phase 4b produced a user-requested broad-window partial fit over
`70 < m4l < 170 GeV`, including the Z peak. The fixed-seed 10% result is
`mu = 0.0 +1.3548619813595435`, with the lower interval at the physical
boundary; GoF `chi2/ndf = 31.755141641709276 / 38`, `p = 0.752432307059706`.
No fresh Phase 4b review was run after this override, per the user instruction.

Doc 4b updated the analysis note with the fixed-seed 10% result and passed the
compact gate. The human gate was auto-approved per the user's directive and
archived. Next step: run Phase 4c full-data inference using the current
`70 < m4l < 170 GeV` fit-window instruction unless superseded.

Phase 4c full-data inference is committed through `bee3081`, with observed
`mu = 2.4776 -0.7139 +0.8388` and an observed shifted-template mass scan whose
best grid point is `125.0 GeV`. The user then requested a fast targeted MVA
training audit because the previous classifier behaved nearly randomly.

The targeted MVA regression found the root cause: the D7 gate was used as a hard
feature whitelist, leaving only `lead_abs_eta` and `phi1`. The repaired MVA now
trains weighted models in `80 < m4l < 170 GeV`, excludes `m4l`, and uses a
curated mass-safe angular/kinematic feature set. Best nominal model is
`bdt_mass_safe` with AUC `0.7929` and broad-window proxy improvement `0.1902`,
but S2 remains rejected because score-shape, low-stat/category, and/or
mass-sculpting gates fail. The active Phase 4c result remains S1 because the
MVA is not promoted.

## Pending Decisions For Human

The user explicitly directed this run to pass the Phase 4b human gate without
asking. Archive that directive verbatim at the Doc 4b human gate and proceed
after Doc 4b review PASS.

## Key Results So Far

- Phase 4a expected-only result before blocking review: expected `mu = 1.0`
  with symmetric expected uncertainty `0.5747382435005995`.
- Phase 1 established the data/MC inventory, input inventory, literature
  survey, six reconnaissance figures, and key Phase 2 constraints.
- Phase 2 established the binding detector-level template-fit strategy,
  commitments, validation gates, mass-extraction attempt, VBF/NN downscope
  gates, and comparison plan.
- Phase 3 selected S1 final-state categories as the conditional Phase 4 handoff.
  VBF is formally downscoped; DY+jets remains the nominal reducible fake proxy;
  TTBar remains diagnostic; angular closure passed; D7 input modeling passed
  only `lead_abs_eta` and `phi1`; S2 classifier/NN was attempted and rejected.
- Phase 4a expected inference retained final-state categories after low-count
  toy validation: 80 toys, success fraction `1.0`, median bias
  `-0.06064996537909362`.
- Phase 4a regression update added `expected_systematic_shifts.json`,
  `expected_m4l_broad_inclusive`, and `expected_systematic_shift_summary`.
- Phase 4a PASS evidence is in `REGRESSION_CHECK_phase4a.md` and
  `SESSION_SUMMARY_phase4a.md`.
- Doc 4a PASS evidence is in `SESSION_SUMMARY_doc4a.md` and
  `analysis_note/review/doc4a/arbiter/DOC4A_FIX_VERIFICATION_ARBITER_alfred_5984_2026-05-30.md`.
- Phase 4b evidence is in `SESSION_SUMMARY_phase4b.md` and
  `phase4_inference/4b_partial/outputs/INFERENCE_PARTIAL.md`.
- Doc 4b evidence is in `SESSION_SUMMARY_doc4b.md`,
  `analysis_note/review/doc4b/arbiter/DOC4B_COMPACT_GATE_tomoko_c890_2026-05-30.md`,
  and `analysis_note/review/HUMAN_GATE_doc4b_2026-05-30.md`.
