# Phase 4c Full-Data Inference Plan

Session: `zoran_44a0`
Date: 2026-05-30

## Governing Instruction

Use the current full-data fit window `70 < m4l < 170 GeV`, including the Z
peak. Keep S1 final-state categories nominal unless observed full-data
stability gates fail. Do not tune any parameter to agree with CMS/JHEP
references; comparisons are context only. Preserve DY+jets as the reducible
fake proxy, VBF/NN as downscoped, and the grouped MC-stat approximation as a
documented limitation.

## Scripts To Write

1. `src/observed_common.py`
   - Mirror Phase 4b common utilities with Phase 4c session/log paths.
   - Define full-data luminosity `10 fb^-1`, broad/fit binning
     `[70, 80, 90, 100, 105, 112, 118, 122, 126, 130, 140, 150, 160, 170]`,
     final-state channels, result/output directories, JSON helpers, and log
     append helpers.

2. `src/run_observed_inference.py`
   - Reuse Phase 4b pyhf model construction and diagnostics.
   - Use all 203 selected data events from `selection_events.npz`.
   - Keep MC at full `10 fb^-1` normalization with no data-integral scaling.
   - Produce:
     - `analysis_note/results/observed_parameters.json`
     - `analysis_note/results/observed_validation.json`
     - `analysis_note/results/observed_covariance.json`
     - `analysis_note/results/observed_systematics.json`
     - `analysis_note/results/observed_systematic_shifts.json`
   - Include expected and partial compatibility pulls, >2 sigma flags, GoF,
     boundary/triviality/viability checks, low-count and category stability,
     deterministic split proxy, and data-sensitive systematic diagnostics
     where supported by available inputs.

3. `src/make_observed_plots.py`
   - Produce and register final Phase 4c figures:
     - full-data `m4l` data/MC over `70-170 GeV`
     - final-state category `m4l` plots
     - observed-vs-expected-vs-partial `mu` comparison
     - nuisance pulls
     - nuisance impacts
     - low-count/category/binning stability
     - deterministic split proxy
     - uncertainty/viability diagnostic
   - Write `outputs/FIGURES.json` with nonzero PNG/PDF files.

4. `src/build_inference_artifact.py`
   - Write `outputs/INFERENCE_OBSERVED.md` from the JSON payloads and figure
     registry.
   - Include headline numbers, full event count, fit window, normalization
     policy, comparison pulls, GoF, boundary/triviality/viability verdicts,
     and finding Resolution/Evidence rows.

5. `src/update_commitments_phase4c.py`
   - Resolve remaining feasible commitments or mark downscopes `[D]` with
     Phase 4c evidence.
   - Preserve existing resolved items and avoid weakening prior evidence.

## Checks

Run:

- `pixi run p4c-all`
- `pixi run lint-plots`
- figure registry smoke test for registered/nonzero/no-orphan/non-stale
  PNG/PDF files
- JSON sanity check for fit window `70-170`, full event count `203`,
  luminosity `10 fb^-1`, expected/partial comparisons, no data-integral
  normalization, and explicit boundary/GoF/viability statuses
- `git diff --check`

Commit on passing checks with message:

`feat(phase4c): run full data inference`
