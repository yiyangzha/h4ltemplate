# Phase 4b Partial-Data Inference Plan

Session: `yuki_9d50`
Date: 2026-05-30

## Scope

Run the Phase 4b 10% observed-data validation for the S1 final-state
template likelihood selected in Phase 3 and used in Phase 4a. The latest
user-requested Phase 4b override sets the fit window to
`70 < m4l < 170 GeV`, including the Z peak, replacing the earlier CMS-like
`105 < m4l < 140 GeV` Phase 4b instruction. MC is normalized to the effective 10% luminosity and is
not scaled to the observed data integral. VBF and MVA/NN categories remain
downscoped unless the existing Phase 3 gates support promotion; current
artifacts do not.

## Will Implement

1. Create `phase4_inference/4b_partial/src/partial_common.py` by adapting the
   Phase 4a path/session helpers for Phase 4b.
2. Create `run_partial_inference.py` to:
   - select a deterministic 10% observed-data subsample with fixed seed;
   - record seed, fraction, event counts, and effective luminosity;
   - scale MC templates to 10% luminosity;
   - fit the final-state and fallback merged/inclusive workspaces;
   - repeat low-count, toy, alternative-binning, channel-compatibility,
     nuisance-pull, impact, and corruption/stability checks;
   - run a deterministic split-proxy consistency check because true CMS run
     period metadata is unavailable in the Phase 3 event handoff;
   - write partial result JSONs under `analysis_note/results/` while
     preserving expected-result JSONs.
3. Create `make_partial_plots.py` to produce PNG/PDF figures for:
   - inclusive `70-170 GeV` 10% data/MC;
   - `70-170 GeV` category overlays;
   - partial-vs-expected `mu` and uncertainty comparison;
   - GoF and nuisance pulls/impacts;
   - low-count/binning stability;
   - deterministic split consistency.
   Every figure will be registered in `outputs/FIGURES.json`.
4. Create `build_inference_artifact.py` to write
   `outputs/INFERENCE_PARTIAL.md` with results, diagnostics, limitations,
   finding resolutions, and machine-readable output inventory.
5. Create/update a Phase 4b commitments helper or direct script logic to mark
   `[VT11]` as resolved with evidence for the fixed-seed 10% validation.
6. Update `pixi.toml` tasks if needed so `pixi run p4b-all` runs inference,
   plots, artifact, and commitment update.
7. Append to `experiment_log.md` and maintain
   `phase4_inference/4b_partial/logs/executor_yuki_9d50_2026-05-30.md`.

## Validation Checks

1. Run `pixi run p4b-all`.
2. Run `pixi run lint-plots`.
3. Run a figure-registry smoke test: registered PNG/PDF files exist and are
   nonzero, no orphan PNG/PDF files, and generated figures are newer than the
   plotting script.
4. Run JSON sanity checks for seed, 10% fraction, effective luminosity,
   expected-vs-partial metrics, fit/display windows, no data-integral
   normalization, and VT11 commitment update.
5. Run `git diff --check`.

## Decision Points

- If final-state observed fit or toy validation is unstable, merge/rebin to
  the first passing fallback and document the rejected attempts.
- If the deterministic split consistency check has low counts, report it as a
  split-proxy diagnostic with explicit low-stat limitations, not as a true
  CMS run-period validation.
- Do not tune fit inputs or MC normalization to match CMS references or the
  observed 10% data.
