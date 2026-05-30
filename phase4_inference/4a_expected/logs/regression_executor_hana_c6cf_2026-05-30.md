# Regression Executor Log

Session: hana_c6cf
Date: 2026-05-30

## Milestones

- Read `TOGGLES.md`, `agents/executor.md`, Phase 3/4a instructions, strategy/selection artifacts, Dmitri critical review, Celeste plot validation, relevant source, and current JSON outputs.
- Wrote regression ticket and plan before code edits.
- Updated Phase 3 MVA code to record broad-window training/evaluation metadata, preserve `m4l` exclusion, and add a tuned BDT trial.
- Regenerated Phase 3 with `pixi run p3-all`; S1 remains nominal because S2 still fails promotion gates.
- Updated Phase 4a expected inference to add broadened mass scan metadata, final-state corruption sensitivity, per-systematic shifted-bin payloads, and formal MC-stat downscope labeling.
- Added broad expected `m4l` and systematic-shift summary figures.
- Regenerated Phase 4a with pixi tasks and repeated plotting/artifact updates after documenting the final-state corruption limitation.
- Ran `pixi run lint-plots`, registry smoke tests, and JSON sanity checks.

## Open Issue

The final-state simultaneous 20 percent corruption test is not fully sensitive in both directions. The `+20%` mass-response corruption fails as required; the `-20%` direction does not (`p = 0.4595`). This is recorded as a quantitative limitation in `expected_validation.json` and `INFERENCE_EXPECTED.md`.

## 2026-05-30 Corruption Follow-Up

Narrow follow-up requested by the user before Phase 4a closure.

Actions:
- Tested defensible final-state-aligned alternatives for the non-rejecting
  `m4l_scale_factor_0.8` corruption.
- Kept the nominal final-state simultaneous profiled Poisson deviance as the
  binding gate: `16.9238 / 17`, `p = 0.45954`, no rejection.
- Added a profiled per-channel shape-only Poisson deviance attempt:
  `12.9668 / 15`, `p = 0.60486`, no rejection.
- Added a profiled Pearson chi2 attempt: `22.7243 / 17`, `p = 0.15844`, no
  rejection.
- Recorded the raw unprofiled Pearson diagnostic (`p = 0.026715`) but did not
  use it for the gate because it is not the nominal profiled workspace
  treatment and is less reliable in low-count bins.
- Marked the corruption criterion as `documented_low_count_infeasible`, not
  passed, in `expected_validation.json` and `INFERENCE_EXPECTED.md`.
- Fixed stale VT12 injected-mass wording in `COMMITMENTS.md` and the
  commitment updater to match `expected_mass_scan.json`: `115, 125, 135 GeV`.

Verification:
- `pixi run p4a-fit`
- `pixi run p4a-plots`
- `pixi run p4a-artifact`
- `pixi run p4a-update-commitments`
- `pixi run lint-plots`
- JSON sanity confirmed `m4l_scale_factor_0.8` remains non-rejecting with
  `p = 0.459538098019478`, three remediation attempts are present, and VT12
  commitment wording matches the mass-scan JSON.
