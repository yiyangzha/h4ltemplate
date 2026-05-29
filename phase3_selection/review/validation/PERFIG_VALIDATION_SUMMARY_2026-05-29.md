# Phase 3 Per-Figure Validation Summary

Date: 2026-05-29
Scope: Level 2 VERIFY plot validation for `phase3_selection/outputs/FIGURES.json`

## Registry

- Final registry entries: 29
- Final registered files: 29 PNG + 29 PDF
- Final smoke test: no missing files, no zero-byte files, no stale PNGs, no orphan PNGs
- Final `pixi run lint-plots`: PASS, no plotting violations in 20 files

## Initial Findings And Fixes

- Mixed data/MC label used `Open Data+Sim`, which was not compliant with the
  required open-data/open-simulation wording. Fixed in `0bf8908`
  (`fix(phase3): address level 2 plot labels`) by using
  `Open Data and Open Simulation` and removing title-like window text.
- `cutflow_summary` had dense multi-line x tick labels. Fixed in `34155e3`
  (`fix(phase3): improve cutflow readability`) by redesigning it as a
  horizontal log-yield cutflow with short step labels and full mapping in
  metadata.
- `m4l_fit_4mu` had legend/experiment-label crowding. Fixed in `63227ca`
  (`fix(phase3): separate mass plot legends`) by moving mass-plot legends to a
  clean region and regenerating all mass stack plots.
- `mva_roc_bdt` exposed code-style presentation text (`bdt AUC=...`). Fixed in
  `c7d6adf` (`fix(phase3): use presentation model labels`) by adding display
  names (`BDT`, `small NN`, `logistic`) while preserving machine-readable keys.

## Final PASS Coverage

All 29 final registry figures have PASS validation on the final committed image
set. Some older `PERFIG_FINAL_*` files record pre-fix FAIL verdicts; those are
superseded by the corresponding `PERFIG_FINAL_RECHECK_*` PASS files listed
below.

Final direct PASS reports:

- `input_validation_cos_theta1`
- `input_validation_cos_theta2`
- `input_validation_cos_theta_star`
- `input_validation_eta4l`
- `input_validation_lead_abs_eta`
- `input_validation_lead_lepton_pt`
- `input_validation_mZ1`
- `input_validation_mZ2`
- `input_validation_phi`
- `input_validation_phi1`
- `input_validation_pt4l`
- `input_validation_sublead_abs_eta`
- `input_validation_sublead_lepton_pt`
- `input_validation_y4l`
- `angular_closure_median_deltas`
- `vbf_downscope_evidence`
- `category_viability_s1`
- `approach_comparison_mu_proxy`
- `sideband_dy_ttbar_diagnostics`

Final recheck PASS reports after fixes:

- `cutflow_summary`:
  `PERFIG_FINAL_cutflow_summary_RECHECK_gertrude_acf4_2026-05-29.md`
- `m4l_broad_window_inclusive`:
  `PERFIG_FINAL_RECHECK_m4l_broad_window_inclusive_hugo_97f3_2026-05-29.md`
- `m4l_fit_window_inclusive`:
  `PERFIG_FINAL_RECHECK_m4l_fit_window_inclusive_ingrid_6854_2026-05-29.md`
- `m4l_fit_4mu`:
  `PERFIG_FINAL_RECHECK_m4l_fit_4mu_isolde_59ff_2026-05-29.md`
- `m4l_fit_4e`:
  `PERFIG_FINAL_RECHECK_m4l_fit_4e_ivan_1a66_2026-05-29.md`
- `m4l_fit_2e2mu`:
  `PERFIG_FINAL_RECHECK_m4l_fit_2e2mu_jasper_7f59_2026-05-29.md`
- `mva_roc_bdt`:
  `PERFIG_FINAL_RECHECK_mva_roc_bdt_margaret_675b_2026-05-29.md`
- `mva_roc_logistic`:
  `PERFIG_FINAL_RECHECK_mva_roc_logistic_nadia_2a87_2026-05-29.md`
- `mva_roc_small_nn`:
  `PERFIG_FINAL_RECHECK_mva_roc_small_nn_nora_5b28_2026-05-29.md`
- `mva_best_score_datamc`:
  `PERFIG_FINAL_RECHECK_mva_best_score_datamc_odette_732f_2026-05-29.md`

## Review Gate Status

Level 2 per-figure validation is complete. Phase 3 can proceed to the
independent Phase 3 critical review and Level 3 plot-validation review.
