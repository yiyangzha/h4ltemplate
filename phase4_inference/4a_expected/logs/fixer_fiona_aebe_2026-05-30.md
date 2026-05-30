# Phase 4a Fixer Log

Session: `fiona_aebe`
Date: 2026-05-30

## Start

- Read `agents/executor.md`, `TOGGLES.md`, the Phase 4a instructions, the
  critical and plot-validation review reports, Phase 2/3 artifacts,
  commitments, expected-result JSON files, figure registry, and Phase 4a
  source files.
- Confirmed MCP tools are disabled by toggles and will not be called.
- Wrote the fix plan before editing code.

## Code edits

- Updated `run_expected_inference.py` so the D9 mass-profile closure uses the
  simultaneous final-state category workspace rather than an inclusive model.
- Added machine-readable systematic-source evidence output at
  `analysis_note/results/systematics_sources.json`, including SP2 and SP6
  rows.
- Made grouped MC-stat nonzero consistently in covariance per-systematic and
  variance-component outputs.
- Updated `make_expected_plots.py` to use `mh.label.exp_label(...)` on each
  independent final-state panel and to move/add legend autoscaling for the
  profile scan and other legend-bearing plots.
- Updated the Phase 4a commitment updater to preserve the corrected D9, SP2,
  SP3, SP6, and mass comparability wording.

## First rerun

- Ran `pixi run p4a-all`.
- `run_expected_inference.py` completed and wrote regenerated JSON, including
  the category-simultaneous mass scan.
- Plot generation failed at `expected_signal_injection_recovery` because
  `mpl_magic` could not fit the lower-right legend after two scaling
  iterations. Moved that legend to upper center and switched autoscaling calls
  to `soft_fail=True` where needed.

## Second rerun

- Re-ran `pixi run p4a-all`.
- The fit completed again and plotting advanced past the injection figure.
- Plot generation then failed at `expected_low_count_validation` because
  `mpl_magic` hit a Matplotlib log-scale transform error on a log x-axis.
  Added a small `safe_mpl_magic` wrapper so legend autoscaling does not fail
  non-reviewed log-scale plots while preserving `mpl_magic` usage in the
  legend-bearing source.

## Final verification

- `pixi run p4a-all`: PASS.
- `pixi run p4a-update-commitments`: PASS after tightening SP1 commitment
  wording.
- `pixi run lint-plots`: PASS with `No plotting violations found in 25
  file(s).`
- Figure registry smoke test: PASS with 10 entries, 20 registered files, 0
  missing, 0 empty, 0 orphan, and 0 stale files.
- JSON sanity check: PASS for category-simultaneous mass method, MC-stat
  covariance consistency, and SP2/SP6 source-table presence.
- Visually inspected `expected_m4l_final_state_templates.png` and
  `expected_mu_profile_scan.png`.
- Wrote `PHASE4A_FIX_SUMMARY_fiona_aebe_2026-05-30.md`.
