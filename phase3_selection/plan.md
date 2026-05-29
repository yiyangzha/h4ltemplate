# Phase 3 Selection Plan

Session: `magnus_d784`
Created: 2026-05-29T20:45:39Z

## Scope And Binding Inputs

Phase 3 implements the reviewed Phase 2 strategy without redesign. The
nominal inputs are the primary prompt paths from `paths.json`:
`/sandbox/work/jfc/analyses/h4ltemplate/data` and
`/sandbox/work/jfc/analyses/h4ltemplate/mc`. Local ROOT copies are used only
for branch/provenance comparison in the VBF recovery gate; they are not mixed
into nominal yields or templates.

The binding decisions are `[D1]`-`[D9]` in
`phase2_strategy/outputs/STRATEGY.md` and their proof requirements in
`COMMITMENTS.md`. Phase 3 must produce fit-ready detector-level template
inputs for downstream simultaneous `pyhf`/HistFactory-style inference, enforce
`105 < m4l < 140 GeV` for fit-region products, compare S1 and S2
quantitatively, and complete the VBF recovery/downscope, angular closure, MVA
input modeling, sideband/fake, TTBar, and category viability gates.

## Script Plan

All scripts will live under `phase3_selection/src/`. Analysis scripts write
machine-readable artifacts under `phase3_selection/outputs/`; plotting scripts
read only those artifacts and write `outputs/figures/`.

1. `selection_common.py`
   Shared constants, sample metadata, path handling, logging setup,
   final-state labels, MC process groups, binning, and JSON helpers. This is
   infrastructure used by Phase 3 scripts only.

2. `build_selection_table.py`
   Analysis script. Reads primary ROOT files with `uproot`, records
   provenance, generated-event denominators, nominal MC weights, branch
   inventories, trigger bit summaries, baseline object/ID/Z sanity masks,
   signal-window and broad-window masks, cutflows, sideband yields, TTBar/DY
   diagnostics, and binned `m4l` histograms for S1. Outputs:
   `selection_provenance.json`, `normalization.json`, `cutflow.json`,
   `sideband_fake_diagnostics.json`, `category_schema_s1.json`,
   `fit_inputs_s1.json`, and compact arrays in `selection_events.npz`.

3. `check_vbf_feasibility.py`
   Analysis/provenance script. Checks primary and local branch inventories for
   jet-like or VBF-like branches, records current `paths.json` allow-list
   limits, and tests whether any allowed event-key join target exists without
   reading disallowed sources. Outputs `vbf_recovery_downscope.json` and the
   evidence table used in `SELECTION.md`.

4. `compute_angles.py`
   Analysis script. Reconstructs four lepton four-vectors with `vector`,
   recomputes `m4l`, `mZ1`, and `mZ2`, calculates standard H->ZZ->4l
   rest-frame angular candidates, checks physical ranges, and writes
   `angular_closure.json` plus `angular_variables.npz`. If the stored-vs-
   recomputed mass closure fails, this script records the unit/pairing
   diagnostics and prevents angular inputs from being promoted.

5. `validate_inputs.py`
   Analysis script. Computes data/MC validation for every S1/S2 selection or
   classifier candidate variable using the predeclared broad and signal
   windows. For each variable it records bin counts, chi2, ndf, p-value,
   coherent ratio-trend metric, unphysical-tail checks, and the pass/discard
   verdict for `[D7]`. Outputs `input_validation.json`.

6. `train_mva.py`
   Analysis script. Runs only on variables passing `input_validation.json`.
   Trains a simple logistic/BDT baseline first, then a small NN attempt if the
   inputs and statistics support it. It excludes `m4l`, uses fixed seeds,
   records train/validation splits and software versions, checks overtraining,
   mass sculpting, category boundary stability, and low-stat bin viability.
   Outputs `mva_training_metadata.json`, `mva_metrics.json`,
   `prefit_category_counts.json`, `fit_inputs_s2.json`, and any model files
   under `outputs/models/`. If gates fail, it preserves diagnostics and marks
   S2 as rejected rather than silently promoting it.

7. `compare_approaches.py`
   Analysis script. Compares S1 and S2 using common expected metrics on the
   same MC/data inputs: Asimov counting/template precision proxy for `mu`,
   sideband/background closure, category/bin viability, low-stat fractions,
   and stability. Outputs `approach_comparison.json` and
   `selected_configuration.json`.

8. `make_input_plots.py`
   Plotting script. Reads `input_validation.json`, `angular_closure.json`, and
   saved histogram arrays to produce data/MC validation figures for all key
   variables, including angular and classifier inputs. Every figure is saved as
   PNG and PDF and registered in `outputs/FIGURES.json`; after each
   registration, the session log gets `FIGURE_READY: <path>`.

9. `make_selection_plots.py`
   Plotting script. Reads Phase 3 JSON/NPZ artifacts to produce the inclusive
   broad-window and signal-window `m4l` stacked data/MC plots, final-state
   category prefit `m4l` plots, cut motivation/N-1 or per-cut diagnostics,
   sideband fake diagnostics, approach comparison plots, ROC/score/overtraining
   plots if S2 is attempted, VBF downscope evidence plot/table, and category
   viability summaries. It never reads ROOT files.

10. `build_selection_artifact.py`
    Artifact script. Builds `outputs/SELECTION.md` from the machine-readable
    outputs. It includes object definitions, final selection, cutflow tables,
    S1/S2 comparison, MVA/input validation, VBF recovery/downscope evidence,
    angular reconstruction/NN gate, fake/sideband diagnostics, method health,
    proof artifact inventory, figure captions, and open issues for Phase 4.

11. `update_commitments_phase3.py`
    Markdown update script. Marks only Phase 3-resolved entries in
    `COMMITMENTS.md` as resolved or formally downscoped with proof paths.
    Phase 4-only commitments remain open.

## Figure Plan

Minimum Phase 3 figure set:

- Inclusive stacked `m4l` data/MC in `70 <= m4l <= 170 GeV` validation range.
- Inclusive stacked `m4l` data/MC in `105 < m4l < 140 GeV` fit range.
- Final-state category prefit `m4l` distributions for 4mu, 4e, and 2e2mu.
- Cut motivation plots for trigger, lepton ID/Z sanity, and fit-window stages.
- Input validation plots for `mZ1`, `mZ2`, `pt4l`, `eta4l`, `y4l`,
  leading/subleading lepton kinematics, and any angular variables attempted.
- Angular closure diagnostic plots for stored vs recomputed masses and
  physical angle ranges.
- Sideband fake diagnostics comparing DY and TTBar in low/high sidebands and
  the signal window.
- VBF recovery/downscope evidence figure/table, explicitly not using a VBF
  label for lepton-only proxy categories.
- S1 vs S2 approach comparison figure.
- ROC, score, train/validation, mass-sculpting, and boundary-stability figures
  if classifier training reaches those gates.

All figures use CMS Open Data/Open Simulation labels, square 10x10 mplhep
style, pull panels for data/MC, and explicit captions in `FIGURES.json` and
`SELECTION.md`.

## Artifact And Machine-Readable Output Structure

Expected outputs:

- `outputs/selection_provenance.json`
- `outputs/normalization.json`
- `outputs/cutflow.json`
- `outputs/sideband_fake_diagnostics.json`
- `outputs/vbf_recovery_downscope.json`
- `outputs/angular_closure.json`
- `outputs/angular_variables.npz`
- `outputs/input_validation.json`
- `outputs/mva_training_metadata.json` and `outputs/mva_metrics.json` if S2
  reaches training
- `outputs/prefit_category_counts.json`
- `outputs/approach_comparison.json`
- `outputs/selected_configuration.json`
- `outputs/fit_inputs_s1.json` and, if accepted or diagnostic, `fit_inputs_s2.json`
- `outputs/FIGURES.json`
- `outputs/SELECTION.md`

## Validation And Gates

- `[D1]/[VT1]`: provenance and local/primary non-mixing recorded before any
  nominal yields are interpreted.
- `[D2]/[D3]`: fit-ready histograms carry explicit `105 < m4l < 140 GeV`
  metadata, with broad sideband figures marked validation-only.
- `[D4]`: final states 4mu/4e/2e2mu are nominal; no VBF label appears unless
  real jet recovery passes.
- `[D6]`: DY+jets is the nominal reducible proxy; no data-integral hand scaling;
  TTBar promotion/omission follows the 10 percent signal-window or 20 percent
  sideband thresholds.
- `[D7]`: no MVA/NN input is used unless chi2/ndf <= 5, p-value is recorded,
  coherent ratio trend is <=20 percent, and tails are physical or calibrated.
- `[D8]`: angular/NN path is attempted only after stored-vs-recomputed mass/Z
  closure, physical ranges, overtraining, mass-sculpting, boundary stability,
  and expected precision improvement gates.
- `[D9]`: Phase 3 prepares category/bin counts and template metadata needed
  for downstream simultaneous `mu` and mass-extraction attempts.
- Closure alarm bands: any chi2/ndf < 0.1, chi2/ndf > 3, p <= 0.05, or pull
  above 5 sigma triggers investigation and either remediation or documented
  infeasibility with at least three attempts.

## Pixi And Commit Plan

The scaffold already contains Phase 3 task names, but `all` currently stops
after Phase 1. I will keep the existing task names, add missing scripts, add
`validate_inputs.py` to the task graph, and extend `all` to run Phase 1 then
`p3-all`.

Planned checkpoints:

1. Commit plan and baseline provenance/selection infrastructure.
2. Commit validation gates: VBF, angular closure, input validation, and
   fake/sideband diagnostics.
3. Commit S1/S2 comparison, figures, `SELECTION.md`, commitment updates, and
   final self-check fixes.

## Pre-Review Self-Check To Run Before Completion

- Re-read this plan line by line and mark every item DONE or explicitly
  infeasible with evidence.
- Run `pixi run p3-all`, `pixi run lint-plots`, and `pixi run all`.
- Verify `outputs/FIGURES.json` entries point to non-empty PNG/PDF files and
  no orphan PNGs exist under `outputs/figures/`.
- Grep Phase 3 scripts for forbidden plotting/code patterns, bare `print()`,
  and ROOT-reading inside plotting scripts.
- Confirm cutflow monotonicity, exact chi2/ndf and p-values, sideband counts,
  approach-comparison metrics, and category/bin viability values are present
  in machine-readable outputs and `SELECTION.md`.
