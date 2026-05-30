# Phase 4a Regression Summary

Session: hana_c6cf
Date: 2026-05-30

## Changes Made

- Phase 3 MVA metadata now explicitly records broad `70 < m4l < 170 GeV` training/evaluation and the policy excluding `m4l` from classifier inputs.
- Added a tuned BDT variant as the targeted MVA improvement attempt. It did not satisfy all promotion gates, so S1 remains the nominal Phase 4 handoff.
- Phase 4a retains the `105 < m4l < 140 GeV` signal-strength fit window.
- Added a broad expected `m4l` figure over `70 < m4l < 170 GeV`.
- Broadened the shifted-template mass scan to `110-140 GeV` in `2.5 GeV` steps and documented the excluded `70-105 GeV` sideband/Z-peak-adjacent range.
- Added `analysis_note/results/expected_systematic_shifts.json` with nominal/up/down shifted-bin arrays by active systematic, process group, and final state.
- Added `expected_systematic_shift_summary` figure showing the actual `m4l_scale` shape-source bin shifts and rate-only source impacts without fake shape dependence.
- Marked grouped MC-stat as a formal Phase 4a downscope/approximation in JSON, artifact prose, and `COMMITMENTS.md`, rather than completed full bin-by-bin profiling.
- Re-ran the corruption sensitivity in the final-state simultaneous workspace.

## Important Limitation

The final-state simultaneous corruption test does not fully pass: the `m4l_scale_factor_1.2` corruption is rejected, but `m4l_scale_factor_0.8` is not rejected with the 18-bin final-state deviance test (`p = 0.4595`). This is documented in `expected_validation.json` as a quantitative low-count limitation, not hidden as a pass.

## Verification

- `pixi run p3-all`: passed.
- `pixi run p4a-all`: passed after code updates; then `p4a-fit`, `p4a-plots`, `p4a-artifact`, and `p4a-update-commitments` were rerun after wording/layout fixes.
- `pixi run lint-plots`: passed, no violations.
- Registry smoke tests: Phase 3 has 31 entries and Phase 4a has 12 entries; no missing, zero-byte, stale, or orphan PNG/PDF files.
- JSON sanity: fit window `105-140`, broad figure metadata `70-170`, MVA training window `70-170`, tuned BDT present, systematic-shift payload present, broadened mass grid documented, final-state corruption limitation documented.

## Files Added

- `analysis_note/results/expected_systematic_shifts.json`
- `phase4_inference/4a_expected/outputs/figures/expected_m4l_broad_inclusive.{png,pdf}`
- `phase4_inference/4a_expected/outputs/figures/expected_systematic_shift_summary.{png,pdf}`
- `phase4_inference/4a_expected/review/REGRESSION_TICKET_PHASE3_PHASE4A_hana_c6cf_2026-05-30.md`
- `phase4_inference/4a_expected/review/fixes/PHASE4A_REGRESSION_PLAN_hana_c6cf_2026-05-30.md`
