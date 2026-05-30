# Phase 4a Expected-Inference Plan

Session: `edmund_69a2`
Created: 2026-05-30T00:24:13Z

## Context Read Before Planning

- [x] Runtime/process context: `CLAUDE.md`, `TOGGLES.md`, `mcp_manifest.json`, `prompt.md`, `paths.json`, `pixi.toml`, `SESSION_STATE.md`, `experiment_log.md`, `COMMITMENTS.md`, `agents/executor.md`, and `phase4_inference/4a_expected/CLAUDE.md`.
- [x] Methodology context: `methodology/03-phases.md` Phase 4a section, `methodology/04-blinding.md`, `methodology/05-artifacts.md`, `methodology/06-review.md`, `methodology/07-tools.md`, `methodology/11-coding.md`, `methodology/appendix-plotting.md`, `methodology/appendix-sessions.md`, and `conventions/extraction.md`.
- [x] Upstream artifacts: Phase 1 input/literature/reconnaissance artifacts, Phase 2 strategy/regression/session summary, and Phase 3 selection JSON/markdown handoff artifacts listed in the executor prompt.
- [x] Noted context issue: `phase4_inference/4a_expected/CLAUDE.md` references `conventions/fitting.md`, but that file is absent. I will use the reviewed Phase 2 shape-fit strategy, `conventions/search.md` where needed, and pyhf/HistFactory requirements as the fit authority.
- [x] MCP status: `MCP_ALPHAXIV=false` and `MCP_LEP_CORPUS=false`; no MCP tools will be called.

## Scope And Guardrails

- [x] Use only MC/Asimov pseudo-data in Phase 4a. Real data counts in `fit_inputs_s1.json` may be read only as Phase 3 handoff metadata, not as fit observations or pseudo-data.
- [x] Build the nominal expected observations from the nominal model expectation.
- [x] Use the Phase 3 S1 handoff: final states `4mu`, `4e`, `2e2mu`, `105 < m4l < 140 GeV`, with the inclusive category used only as a diagnostic or fallback if low-count validation forces a formally documented merge.
- [x] Preserve the Phase 2/3 downscopes: no VBF label without real jet information; no S2 classifier categories; DY+jets remains the nominal reducible fake proxy; TTBar remains a diagnostic/omission systematic.

## Implementation Milestones

1. **Workspace and model builder**
   - [x] Create `phase4_inference/4a_expected/src/expected_common.py` for paths, JSON I/O, logging with `RichHandler`, figure registry helpers, and fit-input loading.
   - [x] Create `phase4_inference/4a_expected/src/run_expected_inference.py`.
   - [x] Build a pyhf HistFactory-style model from `phase3_selection/outputs/fit_inputs_s1.json` with one global `mu` POI scaling all Higgs signal samples.
   - [x] Include bin-by-bin MC statistical uncertainties using per-sample `sumw2` and sample-level statistical modifiers where pyhf supports them.
   - [x] Encode rate/shape nuisances for luminosity, prompt effective cross sections, lepton efficiency, lepton momentum scale/resolution, signal composition, qqZZ/ggZZ, DY fake proxy, TTBar omission, and applicable downscoped/not-applicable sources in `expected_systematics.json`.
   - [x] Commit after the workspace/model code and initial JSON outputs are reproducible.

2. **Low-count validation and binning decision**
   - [x] Validate the Phase 3 final-state handoff with Asimov toys and MC-stat stability checks before reporting a fit.
   - [x] If final-state binning fails the low-count/MC-stat gate, formally merge to an inclusive or coarser validated model, document the reason, and retain final-state fits as channel-compatibility diagnostics only.
   - [x] Run alternative-binning stability checks, including the original final-state bins and a merged/inclusive binning.
   - [x] Write exact chi2/ndf/p-values, toy p-values, low-count verdicts, and binning decisions to `analysis_note/results/expected_validation.json`.
   - [x] Commit after validation tests and any binning decision are in place.

3. **Expected inference, pulls, impacts, covariance**
   - [x] Fit expected Asimov observations, report `mu`, uncertainties, fit convergence, and boundary checks in `analysis_note/results/expected_parameters.json`.
   - [x] Compute combined and per-category goodness-of-fit with chi2/ndf and p-values; include toy-based or Poisson deviance validation for low-count cases.
   - [x] Compute nuisance pulls/constraints and impact ranking on `mu` by fixing/shifting nuisance parameters where feasible.
   - [x] Compute stat, per-systematic, systematic-total, and total covariance matrices for the reported parameters in `analysis_note/results/expected_covariance.json`.
   - [x] Run signal injection/recovery at `mu = 0`, `1`, `2`, and `5`; any bias above 20% triggers investigation before completion.
   - [x] Demonstrate closure-test sensitivity by corrupting relevant corrections/model ingredients by `+20%` and `-20%` and verifying the closure/GoF test fails. If not, redesign and rerun.

4. **Mass-extraction/method-parity attempt**
   - [x] Attempt the binding simultaneous/profiled mass extraction or mass-template closure required by [D9].
   - [x] Preferred path: construct shifted signal templates from M125 samples, scan mass hypotheses with `mu` profiled, and run injected-mass closure at nominal and shifted hypotheses.
   - [x] If this cannot be validated, document three concrete attempts with filenames, commands, exact failure modes, and downgrade to a detector-level peak-position cross-check only.
   - [x] Write mass-scan or infeasibility evidence to `analysis_note/results/expected_mass_scan.json` and/or `phase4_inference/4a_expected/outputs/MASS_EXTRACTION_INFEASIBILITY.md`.

5. **Figures and plot watcher protocol**
   - [x] Create `phase4_inference/4a_expected/src/make_expected_plots.py`.
   - [x] Produce PNG/PDF pairs under `phase4_inference/4a_expected/outputs/figures/` and register all figures in `outputs/FIGURES.json`.
   - [x] Required figures: expected prefit/postfit `m4l` model in fitted categories or validated merged category, `mu` likelihood scan, mass scan or downgrade/peak diagnostic, nuisance impact ranking, uncertainty breakdown, injection-recovery summary, GoF/toy validation, low-count/binning stability, and comparison summary vs CMS/PDG references.
   - [x] After every save/register step, append `FIGURE_READY: phase4_inference/4a_expected/outputs/figures/<name>.png` to the session log and check `phase4_inference/4a_expected/review/validation/` for watcher feedback from `celeste_1743`.
   - [x] Commit after figures and registry smoke checks pass.

6. **Artifact and commitment update**
   - [x] Create `phase4_inference/4a_expected/src/build_inference_artifact.py` to generate `outputs/INFERENCE_EXPECTED.md` from the machine-readable outputs.
   - [x] Include the mandatory systematic completeness table: `| Source | Conventions | Ref 1 | Ref 2 | This analysis | Status |`.
   - [x] Include source citations for every external numeric systematic/input value, and mark fallback/downscope rows explicitly.
   - [x] Create `phase4_inference/4a_expected/src/update_commitments_phase4a.py` to mark Phase 4a-resolved `COMMITMENTS.md` items and leave genuine downstream items open.
   - [x] Append material decisions/results to `experiment_log.md` and keep `logs/executor_edmund_69a2_*.md` current.

7. **Reproducibility and completion checks**
   - [x] Update `pixi.toml` if needed so `p4a-fit`, `p4a-plots`, `p4a-artifact`, `p4a-update-commitments`, and `p4a-all` match the scripts, and extend the root `all` task through Phase 4a.
   - [x] Run `pixi run p4a-all`.
   - [x] Run `pixi run lint-plots`.
   - [x] Run the relevant `pixi run all` chain if feasible.
   - [x] Verify `outputs/FIGURES.json`: all registered PNG/PDF files exist, are non-zero, and there are no orphan PNG/PDF files under `outputs/figures/`.
   - [x] Verify all required JSON files exist in `analysis_note/results/` and include phase fields, chi2/ndf/p-values, covariance matrices, fitted parameters, pulls/impacts, injection results, and precision comparison.
   - [x] Re-read this plan line by line and mark every item DONE or formally infeasible with evidence before declaring completion.

## Expected Output Files

- `phase4_inference/4a_expected/src/expected_common.py`
- `phase4_inference/4a_expected/src/run_expected_inference.py`
- `phase4_inference/4a_expected/src/make_expected_plots.py`
- `phase4_inference/4a_expected/src/build_inference_artifact.py`
- `phase4_inference/4a_expected/src/update_commitments_phase4a.py`
- `analysis_note/results/expected_parameters.json`
- `analysis_note/results/expected_systematics.json`
- `analysis_note/results/expected_covariance.json`
- `analysis_note/results/expected_validation.json`
- `analysis_note/results/expected_mass_scan.json` or `phase4_inference/4a_expected/outputs/MASS_EXTRACTION_INFEASIBILITY.md`
- `phase4_inference/4a_expected/outputs/figures/*.png`
- `phase4_inference/4a_expected/outputs/figures/*.pdf`
- `phase4_inference/4a_expected/outputs/FIGURES.json`
- `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md`
