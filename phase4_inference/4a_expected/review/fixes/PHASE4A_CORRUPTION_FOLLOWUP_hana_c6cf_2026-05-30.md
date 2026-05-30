# Phase 4a Corruption Follow-Up

Session: `hana_c6cf`
Date: 2026-05-30

## Scope

This follow-up addresses the remaining Phase 4a closure issue: the final-state
simultaneous `m4l_scale_factor_0.8` corruption sensitivity test must either
reject at `p < 0.05` with a defensible nominal-workspace-aligned test, or be
documented as infeasible after concrete remediation attempts.

## Result

The `m4l_scale_factor_0.8` corruption still does not reject in the nominal
final-state simultaneous workspace. The criterion is therefore marked as
`documented_low_count_infeasible`, not passed.

The `m4l_scale_factor_1.2` corruption rejects as before with profiled Poisson
deviance `99.9107 / 17`, `p = 9.2424e-14`.

## Attempts For `m4l_scale_factor_0.8`

| Attempt | Test | Statistic | ndf | p-value | Rejects at 0.05 |
|---:|---|---:|---:|---:|---|
| 1 | Profiled Poisson saturated-likelihood deviance in the final-state simultaneous workspace | 16.9238 | 17 | 0.45954 | False |
| 2 | Profiled per-channel shape-only Poisson deviance with one conditioned normalization per final state | 12.9668 | 15 | 0.60486 | False |
| 3 | Profiled Pearson chi2 on the final-state simultaneous expected bins | 22.7243 | 17 | 0.15844 | False |

The raw unprofiled Pearson diagnostic gives `p = 0.026715`, but I did not use
it to pass the gate because it drops the nominal profiled workspace treatment
and is less reliable for the low-count bins. This would be a diagnostic alarm,
not a defensible replacement for the final-state simultaneous closure gate.

## File Updates

- `analysis_note/results/expected_validation.json` now contains
  `criterion_status: documented_low_count_infeasible`, per-row diagnostics,
  and the three remediation attempts.
- `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` now states that
  the +/-20 percent corruption sensitivity criterion is not passed and shows
  the three failed attempts.
- `COMMITMENTS.md` now matches `analysis_note/results/expected_mass_scan.json`:
  VT12 injected masses are `115, 125, 135 GeV`.
- `phase4_inference/4a_expected/src/update_commitments_phase4a.py` was updated
  so rerunning the commitments task preserves the corrected VT12 wording.

## Verification

- `pixi run p4a-fit`
- `pixi run p4a-plots`
- `pixi run p4a-artifact`
- `pixi run p4a-update-commitments`
- `pixi run lint-plots`
- Registry smoke check: all 24 registered plot files exist, are nonzero, have
  no orphan PNG/PDF files, and are newer than `make_expected_plots.py`.
- JSON sanity check:
  - final-state corruption workspace present
  - `m4l_scale_factor_0.8` has `p = 0.459538098019478` and does not pass
  - `criterion_status` is `documented_low_count_infeasible`
  - at least three remediation attempts are recorded and none rejects
  - mass-closure injected masses are `[115.0, 125.0, 135.0]`
  - `COMMITMENTS.md` contains `115, 125, and 135 GeV` and no stale
    `124, 125, and 126 GeV` wording
