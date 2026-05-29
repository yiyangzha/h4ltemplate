# Phase 3 Pre-Review Self-Check

Session: `magnus_d784`
Date: 2026-05-29

## Plan Check

- DONE: `selection_common.py` and analysis/plotting script split implemented under `phase3_selection/src/`.
- DONE: baseline provenance, normalization, cutflow, sideband diagnostics, and S1 fit inputs produced.
- DONE: VBF recovery/downscope gate completed with branch, provenance, allow-list, and join evidence.
- DONE: four-vector and angular closure produced before classifier use.
- DONE: D7 input validation produced before MVA training.
- DONE: logistic, BDT, and small NN alternatives attempted; S2 rejected by gates.
- DONE: S1/S2 comparison produced and S1 selected.
- DONE: input, selection, sideband, MVA, and comparison figures produced and registered.
- DONE: `SELECTION.md` and `COMMITMENTS.md` updates produced.
- DONE: `pixi.toml` Phase 3 tasks and root `all` task updated.

## Completion Criteria

- Cutflow table in artifact with data and MC counts: DONE, see `SELECTION.md` and `cutflow.json`.
- At least two selection approaches compared: DONE, S1 versus S2 in `approach_comparison.json`.
- Closure tests pass or have remediation evidence: DONE for angular closure; S2 failed promotion gates and was rejected rather than used.
- All figures saved and registered: DONE, 25 registry entries with non-empty PNG/PDF files and no orphan PNGs.
- Data/MC comparisons for all key variables: DONE, 14 input-validation figures and JSON gate table.
- `COMMITMENTS.md` updated: DONE for Phase 3-resolved and formally downscoped items.
- Experiment log updated: DONE with Phase 3 plan, processing, validation, figures, artifact, and commitment entries.
- `plot_utils.py` created: DONE with `data_mc_comparison`, `save_and_register`, and standard setup.

## Key Validation Values

- Final fit-window cutflow: data 69 events; MC weighted yield 56.6.
- S1 expected signal/background in fit window: S = 7.732, B = 48.877.
- S1 expected `mu` uncertainty proxy: 0.973.
- Angular closure: overall pass; per-sample median mass differences are below `0.1 GeV`; out-of-range angular counts are zero.
- D7 input gate passed variables: `lead_abs_eta`, `phi1`.
- Best S2 model: `small_nn`; relative expected-proxy change = -0.236; S2 not promoted.
- VBF gate: formally downscoped because no real jet/VBF branches or allowed upstream join source exists.
- TTBar/DY ratios: low sideband 0.095, signal window 0.044, high sideband 0.163; TTBar not promoted.

## Commands Run

- `pixi run p3-all`: passed.
- `pixi run all`: passed; Phase 1 regeneration side effects were restored to respect Phase 3 ownership.
- `pixi run lint-plots`: passed.
- `pixi run py -m py_compile phase3_selection/src/*.py`: passed.
- Figure registry smoke test: passed with 25 entries, no missing/empty files, no orphan PNGs.
- `git diff --check`: passed.
- `grep -R "print(" -n phase3_selection/src`: no bare print calls.

## Open Issues For Phase 4

- Phase 4 must build the actual `pyhf` workspace, one global `mu`, MC-stat modifiers, GoF, pulls/impacts, injection tests, and the binding simultaneous mass-extraction attempt.
- VBF remains formally non-comparable unless allowed inputs are expanded to real jet information.
- DY+jets-only reducible modeling remains a deliberate comparability limitation versus CMS data-driven Z+X.
