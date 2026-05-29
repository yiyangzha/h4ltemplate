# Phase 3 Level 3 Plot Validation

Session: `nora_76da`  
Date: 2026-05-29  
Scope: confirmatory Level 3 validation for `phase3_selection`

## Verdict

FAIL. I inspected all 29 registered PNG figures and the plotting code under
`phase3_selection/src/`. The previously reported Level 2 issues are fixed in
the final image set, but one Category A label-quality violation remains in
`sideband_dy_ttbar_diagnostics`.

## Level 2 Fix Confirmation

- `Open Data+Sim` label removed from final figures: confirmed.
- No title-like broad-window / fit-window top text on the mass plots: confirmed.
- `cutflow_summary` readability fix: confirmed.
- Mass-plot legend separation from the CMS label: confirmed.
- `BDT` / `small NN` presentation names on ROC outputs: confirmed.

## Part 1: Code-Lint Review

Reference: `pixi run lint-plots` previously reported PASS in
`PERFIG_VALIDATION_SUMMARY_2026-05-29.md`. I still performed a manual grep-style
check of the Phase 3 plotting code.

### PASS checks

- `mh.style.use("CMS")` applied in [plot_utils.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase3_selection/src/plot_utils.py:15)
- ratio plots use `sharex=True` and `fig.subplots_adjust(hspace=0)` in [plot_utils.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase3_selection/src/plot_utils.py:67)
- no `ax.set_title()` calls found in Phase 3 plotting scripts
- no numeric hardcoded `fontsize=` values found
- save path writes both PDF and PNG with `bbox_inches="tight"` and `plt.close(fig)` in [plot_utils.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase3_selection/src/plot_utils.py:32)
- no forbidden `colorbar(...)` patterns found
- no `.view()[:] =` plus derived-errorbar misuse found in plotting scripts
- no ratio-panel experiment-label duplication seen in rendered outputs

### Finding A1

- File: [make_selection_plots.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase3_selection/src/make_selection_plots.py:151)
- Check failed: publication-quality legend text
- Category: A
- Evidence: the sideband plot legend is built from raw ROOT filenames via
  `sample.replace(".root", "")`, which renders `DYJetsToLL` and `TTBar` in the
  final figure. `DYJetsToLL` is a dataset/file stem, not publication-quality
  prose.
- Required fix: replace raw sample stems with presentation labels, e.g.
  `DY+jets` and `t\bar{t}` or `TTBar diagnostic`, then regenerate
  `sideband_dy_ttbar_diagnostics.{png,pdf}`.

## Part 2: Visual Validation

All 29 final PNGs were inspected directly.

- `input_validation_cos_theta1`: PASS
- `input_validation_cos_theta2`: PASS
- `input_validation_cos_theta_star`: PASS
- `input_validation_eta4l`: PASS
- `input_validation_lead_abs_eta`: PASS
- `input_validation_lead_lepton_pt`: PASS
- `input_validation_mZ1`: PASS
- `input_validation_mZ2`: PASS
- `input_validation_phi`: PASS
- `input_validation_phi1`: PASS
- `input_validation_pt4l`: PASS
- `input_validation_sublead_abs_eta`: PASS
- `input_validation_sublead_lepton_pt`: PASS
- `input_validation_y4l`: PASS
- `cutflow_summary`: PASS
- `angular_closure_median_deltas`: PASS
- `vbf_downscope_evidence`: PASS
- `category_viability_s1`: PASS
- `approach_comparison_mu_proxy`: PASS
- `sideband_dy_ttbar_diagnostics`: VIOLATION A1
  - visible legend text uses `DYJetsToLL` and `TTBar`; `DYJetsToLL` remains a
    raw dataset/file label rather than publication-quality text
  - fix: use polished legend labels and regenerate
- `m4l_broad_window_inclusive`: PASS
- `m4l_fit_window_inclusive`: PASS
- `m4l_fit_4mu`: PASS
- `m4l_fit_4e`: PASS
- `m4l_fit_2e2mu`: PASS
- `mva_best_score_datamc`: PASS
- `mva_roc_bdt`: PASS
- `mva_roc_logistic`: PASS
- `mva_roc_small_nn`: PASS

## Summary

The final figure set is close to review-ready. The earlier Level 2 mechanical
and layout failures are fixed. The only remaining blocker is the raw
dataset-style legend text in `sideband_dy_ttbar_diagnostics`, which is a
Category A label-quality violation under `agents/plot_validator.md` and
`methodology/appendix-plotting.md`.
