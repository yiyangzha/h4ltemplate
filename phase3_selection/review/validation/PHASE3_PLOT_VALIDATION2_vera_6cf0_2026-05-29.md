# Phase 3 Level 3 Plot Validation

Session: `vera_6cf0`  
Date: 2026-05-29  
Scope: fresh Level 3 plot validation after review fixes for `phase3_selection`

## Verdict

PASS. I inspected all 30 registered PNG figures in `phase3_selection/outputs/FIGURES.json`, re-checked the plotting code under `phase3_selection/src/`, and compared the current outputs against the prior validation and fix-verification trail:

- `phase3_selection/review/validation/PERFIG_VALIDATION_SUMMARY_2026-05-29.md`
- `phase3_selection/review/validation/PHASE3_PLOT_VALIDATION_nora_76da_2026-05-29.md`
- `phase3_selection/review/arbiter/PHASE3_FIX_VERIFICATION_sally_2377_2026-05-29.md`

No remaining red flags or Category A/B plotting violations were found in the current committed figure set.

## Prior-Failure Recheck

All previously targeted failures are fixed in the current PNGs and code:

- Raw `DYJetsToLL` legend label: fixed. `sideband_dy_ttbar_diagnostics.png` now shows `DY+jets fake proxy`; the plotting path uses `sample_display_name(sample)` in [make_selection_plots.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase3_selection/src/make_selection_plots.py:218).
- Cutflow readability: fixed. `cutflow_summary.png` uses short horizontal-step labels and is readable at rendered size.
- Mass legend separation: fixed. `m4l_broad_window_inclusive.png`, `m4l_fit_window_inclusive.png`, `m4l_fit_4mu.png`, `m4l_fit_4e.png`, and `m4l_fit_2e2mu.png` keep the legend separated from the experiment label and plotted content.
- Presentation model labels: fixed. ROC figures show `BDT`, `logistic`, and `small NN`, not raw internal keys.
- Mixed data/simulation labeling: fixed. Mixed data/MC figures consistently show `Open Data and Open Simulation`; simulation-only figures show `Open Simulation`.

## Part 1: Code-Lint Review

Manual grep-style checks on the current plotting code found no violations.

### PASS checks

- `mh.style.use("CMS")` is applied in [plot_utils.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase3_selection/src/plot_utils.py:15).
- Ratio plots use `sharex=True` and `fig.subplots_adjust(hspace=0)` in [plot_utils.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase3_selection/src/plot_utils.py:67) and [plot_utils.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase3_selection/src/plot_utils.py:68).
- Save helpers write both PDF and PNG with `bbox_inches="tight"` and close figures in [plot_utils.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase3_selection/src/plot_utils.py:32), [plot_utils.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase3_selection/src/plot_utils.py:33), and [plot_utils.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase3_selection/src/plot_utils.py:34).
- No `ax.set_title()` calls found.
- No forbidden `tight_layout()` or `constrained_layout=True` found.
- No forbidden `plt.colorbar(...)` or `fig.colorbar(..., ax=...)` patterns found.
- No numeric hardcoded `fontsize=` usage found.
- No `data=False` plus `llabel=` stacking trap found.
- No derived-quantity errorbar trap from `.view()[:] =` paired with missing explicit `yerr` on derived values was found in the current plotting paths.
- Experiment labels are present in the plotting helpers and current selection plotting functions; no ratio-panel label duplication was seen in rendered outputs.

### Registry consistency

- `FIGURES.json` contains 30 entries.
- All 30 registered PNG files exist and are non-zero.
- All 30 registered PDF files exist and are non-zero.
- No duplicate PNG content hashes were found across the registered figure set.

## Part 2: Visual Validation

All current registered PNGs were visually inspected.

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
- `cut_motivation_efficiencies`: PASS
- `m4l_broad_window_inclusive`: PASS
- `m4l_fit_window_inclusive`: PASS
- `m4l_fit_4mu`: PASS
- `m4l_fit_4e`: PASS
- `m4l_fit_2e2mu`: PASS
- `sideband_dy_ttbar_diagnostics`: PASS
- `angular_closure_median_deltas`: PASS
- `vbf_downscope_evidence`: PASS
- `category_viability_s1`: PASS
- `approach_comparison_mu_proxy`: PASS
- `mva_roc_bdt`: PASS
- `mva_roc_logistic`: PASS
- `mva_roc_small_nn`: PASS
- `mva_best_score_datamc`: PASS

## Notes

- Readability is acceptable across the full set at the intended AN scale. Tick labels, legends, and experiment labels remain legible.
- No current legend overlaps with data points, stacks, or fit content in the inspected outputs.
- Ratio panels show no visible `Axis 0` artifact and no visible main/ratio gap.
- Labels use presentation text rather than raw dataset stems or underscored variable names in the rendered figures.

## Conclusion

The Phase 3 figure set passes fresh Level 3 validation after the applied fixes. I found no remaining plotting blockers in the current registered outputs.
