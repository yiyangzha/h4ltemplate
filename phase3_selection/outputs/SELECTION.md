# Phase 3 Selection And Processing

Session: `magnus_d784`
Created from machine-readable Phase 3 outputs.

## Summary

Phase 3 implements the reviewed Phase 2 strategy using the primary prompt
ROOT paths only. The nominal Phase 4 handoff is `S1_reference_like_final_state_categories` with final-state
categories `4mu`, `4e`, and `2e2mu`, but this binning is conditional:
17/18
final-state fit bins have `S+B < 5` and require Phase 4 low-count Poisson/toy
validation plus MC-stat stability checks before a result is reported. No VBF
category is used because the recovery gate found no real jet/VBF information in
the allowed flat ntuples. The S2 angular/kinematic classifier was attempted and
rejected by the input, score-shape, low-stat, and expected-precision gates.

## Data Source Freeze And Provenance

Nominal processing used the primary prompt data and MC paths recorded in
`paths.json`, not local copies. `selection_provenance.json` records file size,
tree entries, metadata denominators, branch counts, and jet-like branch
matches for every nominal input. `primary_paths_only_for_nominal` is
`True`.

## MC Normalization

The MC normalization is `weight = sigma_eff_pb * L_pb / sum_Metadata_nEvents`
with `L = 10000 pb^-1`, as specified in Phase 2. No MC component is hand-scaled
to the data integral for fit inputs or yield plots.

| Sample | Group | Metadata nEvents | xsec [pb] | nominal weight |
| --- | --- | --- | --- | --- |
| DYJetsToLL.root | background_reducible | 8.24e+07 | 5396 | 0.654469 |
| GGZZ2E2Mu.root | background_ggZZ | 4.99e+05 | 0.003185 | 6.38277e-05 |
| GGZZ4E.root | background_ggZZ | 9.93e+05 | 0.001619 | 1.63106e-05 |
| GGZZ4Mu.root | background_ggZZ | 9.97e+05 | 0.001575 | 1.57903e-05 |
| GluGluToHToZZ.root | signal_ggH | 9.84e+05 | 0.006024 | 6.12249e-05 |
| TTBar.root | background_top | 1.48e+07 | 52.7 | 0.0356647 |
| VBF_HToZZ.root | signal_VBF | 4.98e+05 | 0.00048794 | 9.79799e-06 |
| WMHToZZ.root | signal_VH | 1.93e+05 | 6.706e-05 | 3.47303e-06 |
| WPHToZZ.root | signal_VH | 2.95e+05 | 0.000107235 | 3.63825e-06 |
| ZHToZZ.root | signal_VH | 4.86e+05 | 9.8394e-05 | 2.0234e-06 |
| ZZTo4L.root | background_ZZ | 5.21e+07 | 1.325 | 0.000254299 |

## Object Definitions And Final Selection

The ntuples already contain the best four-lepton candidate selected by the
ntuplizer. Phase 3 applies only event-level checks that can be audited from
retained branches:

- finite core four-lepton, Z-mass, and lepton variables;
- trigger bitmask requirement `trigBits != 0`, not equality to one integer;
- final-state categories inferred from retained lepton PDG IDs;
- flavor-matched lepton ID checks, using electron cut-based IDs only for
  electrons and muon PF+medium IDs only for muons;
- Z-pair sanity using retained `zId`, charge, flavor, `mZ1`, and `mZ2`;
- broad validation window `70 <= m4l <= 170 GeV` for sidebands and diagnostics;
- fit window `105 < m4l < 140 GeV` for fit-ready templates.

## Cutflow

| Step | Data events | MC raw entries | MC weighted yield | Monotonic |
| --- | --- | --- | --- | --- |
| all | 854 | 3517238 | 842 | True |
| finite_core | 854 | 3517238 | 842 | True |
| trigger_bitmask_nonzero | 798 | 3442802 | 790 | True |
| valid_final_state | 798 | 3442802 | 790 | True |
| flavor_matched_lepton_id | 467 | 2986053 | 466 | True |
| z_pair_sanity | 467 | 2986053 | 466 | True |
| broad_validation_window_70_170 | 203 | 1058285 | 210 | True |
| fit_window_105_140 | 69 | 405145 | 56.6 | True |

## Cut Motivation Diagnostics

Trigger, flavor-matched lepton-ID, and Z-pair sanity efficiencies are recorded
as step-to-previous-step ratios by final state. Data uses raw event counts, and
MC uses prompt-normalized weighted yields. The dedicated machine-readable source
is `cut_motivation_diagnostics.json`.

| Cut | Final state | Data eff. | MC eff. | Data pass | Data denom. | MC pass | MC denom. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Trigger bitmask | 4mu | 1 | 0.9946 | 162 | 162 | 178 | 179 |
| Trigger bitmask | 4e | 0.8939 | 0.9032 | 236 | 264 | 228 | 252 |
| Trigger bitmask | 2e2mu | 0.9346 | 0.9358 | 400 | 428 | 385 | 411 |
| Flavor-matched lepton ID | 4mu | 0.9444 | 0.9434 | 153 | 162 | 168 | 178 |
| Flavor-matched lepton ID | 4e | 0.3644 | 0.3542 | 86 | 236 | 80.7 | 228 |
| Flavor-matched lepton ID | 2e2mu | 0.57 | 0.5671 | 228 | 400 | 218 | 385 |
| Z-pair sanity | 4mu | 1 | 1 | 153 | 153 | 168 | 168 |
| Z-pair sanity | 4e | 1 | 1 | 86 | 86 | 80.7 | 80.7 |
| Z-pair sanity | 2e2mu | 1 | 1 | 228 | 228 | 218 | 218 |

## Categories And VBF Recovery/Downscope

The nominal categories are the final states `4mu`, `4e`, and `2e2mu`, retained
because the S2 classifier split fails and no real VBF category is available.
This is not an unconditional category/bin viability pass: the selected
final-state binning is a conditional Phase 4 handoff. The per-bin expected
`S+B` evidence is:

| Category | m4l bin [GeV] | Signal | Background | S+B | S+B < 5 |
| --- | --- | --- | --- | --- | --- |
| 4mu | 105-112 | 0.0443 | 2.52 | 2.56 | yes |
| 4mu | 112-118 | 0.104 | 2.37 | 2.47 | yes |
| 4mu | 118-122 | 0.235 | 2.86 | 3.1 | yes |
| 4mu | 122-126 | 2.21 | 1.56 | 3.77 | yes |
| 4mu | 126-130 | 0.375 | 2.14 | 2.51 | yes |
| 4mu | 130-140 | 0.00661 | 3.97 | 3.98 | yes |
| 4e | 105-112 | 0.0201 | 1.86 | 1.88 | yes |
| 4e | 112-118 | 0.0736 | 2.52 | 2.6 | yes |
| 4e | 118-122 | 0.255 | 2.44 | 2.7 | yes |
| 4e | 122-126 | 0.706 | 0.467 | 1.17 | yes |
| 4e | 126-130 | 0.198 | 0.49 | 0.688 | yes |
| 4e | 130-140 | 0.0137 | 2.6 | 2.61 | yes |
| 2e2mu | 105-112 | 0.0544 | 4.42 | 4.48 | yes |
| 2e2mu | 112-118 | 0.155 | 2.46 | 2.62 | yes |
| 2e2mu | 118-122 | 0.511 | 3.74 | 4.25 | yes |
| 2e2mu | 122-126 | 2.21 | 1.77 | 3.97 | yes |
| 2e2mu | 126-130 | 0.544 | 3.84 | 4.38 | yes |
| 2e2mu | 130-140 | 0.0233 | 6.84 | 6.87 | no |

The VBF recovery gate checked primary and local branch inventories, the current
allow-list, event-key join feasibility, and `h4l_ntuplize.py` provenance.
It found 24 checked flat ntuples,
zero files with jet/VBF-like branches, zero allowed upstream join sources, and
`safe_event_key_join_possible = False`.
Decision: Formal downscope: no real jet or VBF discriminator branches are available in allowed flat ntuples. No lepton-only category is labeled VBF.

## Angular Reconstruction And NN Gate

Four-vector closure passed before angular variables were considered. The
computed angular candidates have physical ranges in every checked selected
event. The angle definitions are detector-level candidates derived from the
retained lepton four-vectors and the Phase 2-cited H->4l angular references.

| Sample | Broad entries | median dm4l [GeV] | median dmZ1 [GeV] | median dmZ2 [GeV] | 0.1 GeV gate | out-of-range angles |
| --- | --- | --- | --- | --- | --- | --- |
| cms_10fb_13TeV.root | 203 | 7.629e-06 | 7.629e-06 | 3.815e-06 | True | 0 |
| DYJetsToLL.root | 38 | 1.526e-05 | 7.629e-06 | 3.815e-06 | True | 0 |
| GGZZ2E2Mu.root | 17694 | 7.629e-06 | 7.629e-06 | 5.722e-06 | True | 0 |
| GGZZ4E.root | 25309 | 7.629e-06 | 7.629e-06 | 3.815e-06 | True | 0 |
| GGZZ4Mu.root | 72541 | 7.629e-06 | 7.629e-06 | 3.815e-06 | True | 0 |
| GluGluToHToZZ.root | 113819 | 7.629e-06 | 7.629e-06 | 3.815e-06 | True | 0 |
| TTBar.root | 50 | 1.526e-05 | 7.629e-06 | 3.815e-06 | True | 0 |
| VBF_HToZZ.root | 68867 | 1.526e-05 | 7.629e-06 | 3.815e-06 | True | 0 |
| WMHToZZ.root | 22475 | 1.526e-05 | 7.629e-06 | 3.815e-06 | True | 0 |
| WPHToZZ.root | 30423 | 1.526e-05 | 7.629e-06 | 3.815e-06 | True | 0 |
| ZHToZZ.root | 29427 | 1.526e-05 | 7.629e-06 | 3.815e-06 | True | 0 |
| ZZTo4L.root | 677642 | 7.629e-06 | 7.629e-06 | 3.815e-06 | True | 0 |

## Input-Variable Modeling Gate

D7 was applied before classifier training. Shape comparisons use a data-area
normalization only for input-modeling diagnostics; nominal yields remain
prompt-luminosity normalized. Only variables passing `chi2/ndf <= 5` and no
coherent shape-ratio trend above 20 percent were eligible for S2 training.

| Variable | chi2/ndf | ndf | p | max shape ratio deviation | D7 pass |
| --- | --- | --- | --- | --- | --- |
| cos_theta1 | 1.6 | 5 | 0.1562 | 0.557 | False |
| cos_theta2 | 1.29 | 5 | 0.2655 | 0.459 | False |
| cos_theta_star | 1.01 | 5 | 0.4115 | 0.364 | False |
| eta4l | 0.404 | 5 | 0.8464 | 0.22 | False |
| lead_abs_eta | 0.473 | 4 | 0.7553 | 0.193 | True |
| lead_lepton_pt | 4.06 | 4 | 0.002731 | 1 | False |
| mZ1 | 122 | 6 | 6.222e-155 | 1 | False |
| mZ2 | 32.1 | 6 | 7.491e-39 | 1 | False |
| phi | 0.78 | 5 | 0.5637 | 0.251 | False |
| phi1 | 0.155 | 5 | 0.9785 | 0.0826 | True |
| pt4l | 0.333 | 5 | 0.8934 | 0.348 | False |
| sublead_abs_eta | 1.08 | 4 | 0.3664 | 0.243 | False |
| sublead_lepton_pt | 849 | 4 | 0 | 1 | False |
| y4l | 997 | 5 | 0 | 1 | False |

Variables explicitly not promoted: `m4l` is excluded to avoid mass sculpting;
`pvNdof` and isolation-tail variables remain excluded under Phase 2 [A6].

## S1 Versus S2 Approach Comparison

| Approach | Metric/result |
| --- | --- |
| S1 reference-like final-state fit | mu uncertainty proxy = 0.973; conditional low-count handoff |
| S2 classifier categories | best model = small NN, relative improvement = -0.236 |
| Nominal selection | S1_reference_like_final_state_categories |

S2 was not promoted. The best classifier is
small NN with a relative proxy change of
-0.236; this is worse
than S1, not a >10 percent improvement. The detailed S2 gate table is:

| Model | AUC | overtrain gap | score chi2 | score ndf | score p | score gate | low-stat bin fraction | category gate | all S2 gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BDT | 0.548 | 2.726e-05 | 4.945 | 2 | 0.08436 | True | 1 | False | False |
| logistic | 0.5496 | 1.516e-05 | n/a | 0 | n/a | False | 0.9722 | False | False |
| small NN | 0.5505 | 1.216e-05 | n/a | 0 | n/a | False | 1 | False | False |

The BDT score-shape gate passes, but its category-viability gate fails; the
logistic and small NN score-shape and category-viability gates both fail. No
trained classifier variant satisfies all S2 promotion gates.

## Fake And Sideband Diagnostics

DY+jets remains the nominal reducible fake proxy. The signal region is excluded
from sideband constraints. The TTBar diagnostic is not promoted to a nominal
component because the TTBar diagnostic / DY+jets fake-proxy ratios are below
the Phase 2 thresholds:
{'high_sideband_140_170': 0.16348247967166454, 'low_sideband_70_105': 0.09536477980847097, 'signal_window_105_140': 0.04440264879971137}.

| Sample | 70 <= m4l < 105 | 105 < m4l < 140 | 140 < m4l <= 170 |
| --- | --- | --- | --- |
| DY+jets fake proxy | 2.62 | 17.7 | 4.58 |
| TTBar diagnostic | 0.25 | 0.785 | 0.749 |
| Open data | 115 | 69 | 19 |
| qqZZ | 123 | 29.5 | 20.3 |

## Fit-Ready Handoff

The fit-ready handoff for Phase 4 is `fit_inputs_s1.json`. It contains
prompt-normalized `m4l` templates in `105 < m4l < 140 GeV`, bin edges
`[105, 112, 118, 122, 126, 130, 140]`, sumw2 arrays for MC-stat terms, and
final-state categories plus an inclusive diagnostic category. Phase 4 may use
the `4mu`, `4e`, and `2e2mu` categories for the simultaneous fit only after
low-count Poisson/toy validation and MC-stat stability checks. If those checks
fail, Phase 4 must rebin or merge categories before reporting a result. The
inclusive category is a diagnostic cross-check only and must not be fitted
simultaneously with the mutually exclusive final-state categories. The
broad-window templates are explicitly validation-only.

## Figures

| Figure id | PNG | PDF |
| --- | --- | --- |
| input_validation_cos_theta1 | figures/input_validation_cos_theta1.png | figures/input_validation_cos_theta1.pdf |
| input_validation_cos_theta2 | figures/input_validation_cos_theta2.png | figures/input_validation_cos_theta2.pdf |
| input_validation_cos_theta_star | figures/input_validation_cos_theta_star.png | figures/input_validation_cos_theta_star.pdf |
| input_validation_eta4l | figures/input_validation_eta4l.png | figures/input_validation_eta4l.pdf |
| input_validation_lead_abs_eta | figures/input_validation_lead_abs_eta.png | figures/input_validation_lead_abs_eta.pdf |
| input_validation_lead_lepton_pt | figures/input_validation_lead_lepton_pt.png | figures/input_validation_lead_lepton_pt.pdf |
| input_validation_mZ1 | figures/input_validation_mZ1.png | figures/input_validation_mZ1.pdf |
| input_validation_mZ2 | figures/input_validation_mZ2.png | figures/input_validation_mZ2.pdf |
| input_validation_phi | figures/input_validation_phi.png | figures/input_validation_phi.pdf |
| input_validation_phi1 | figures/input_validation_phi1.png | figures/input_validation_phi1.pdf |
| input_validation_pt4l | figures/input_validation_pt4l.png | figures/input_validation_pt4l.pdf |
| input_validation_sublead_abs_eta | figures/input_validation_sublead_abs_eta.png | figures/input_validation_sublead_abs_eta.pdf |
| input_validation_sublead_lepton_pt | figures/input_validation_sublead_lepton_pt.png | figures/input_validation_sublead_lepton_pt.pdf |
| input_validation_y4l | figures/input_validation_y4l.png | figures/input_validation_y4l.pdf |
| cutflow_summary | figures/cutflow_summary.png | figures/cutflow_summary.pdf |
| cut_motivation_efficiencies | figures/cut_motivation_efficiencies.png | figures/cut_motivation_efficiencies.pdf |
| m4l_broad_window_inclusive | figures/m4l_broad_window_inclusive.png | figures/m4l_broad_window_inclusive.pdf |
| m4l_fit_window_inclusive | figures/m4l_fit_window_inclusive.png | figures/m4l_fit_window_inclusive.pdf |
| m4l_fit_4mu | figures/m4l_fit_4mu.png | figures/m4l_fit_4mu.pdf |
| m4l_fit_4e | figures/m4l_fit_4e.png | figures/m4l_fit_4e.pdf |
| m4l_fit_2e2mu | figures/m4l_fit_2e2mu.png | figures/m4l_fit_2e2mu.pdf |
| sideband_dy_ttbar_diagnostics | figures/sideband_dy_ttbar_diagnostics.png | figures/sideband_dy_ttbar_diagnostics.pdf |
| angular_closure_median_deltas | figures/angular_closure_median_deltas.png | figures/angular_closure_median_deltas.pdf |
| vbf_downscope_evidence | figures/vbf_downscope_evidence.png | figures/vbf_downscope_evidence.pdf |
| category_viability_s1 | figures/category_viability_s1.png | figures/category_viability_s1.pdf |
| approach_comparison_mu_proxy | figures/approach_comparison_mu_proxy.png | figures/approach_comparison_mu_proxy.pdf |
| mva_roc_bdt | figures/mva_roc_bdt.png | figures/mva_roc_bdt.pdf |
| mva_roc_logistic | figures/mva_roc_logistic.png | figures/mva_roc_logistic.pdf |
| mva_roc_small_nn | figures/mva_roc_small_nn.png | figures/mva_roc_small_nn.pdf |
| mva_best_score_datamc | figures/mva_best_score_datamc.png | figures/mva_best_score_datamc.pdf |

## Method Health And Open Issues

- Cutflow monotonicity: all sample/channel cumulative cutflows are monotonic.
- Cut motivation: trigger, lepton-ID, and Z-pair sanity efficiency diagnostics
  are recorded in `cut_motivation_diagnostics.json` and the registered
  `cut_motivation_efficiencies` figure.
- S1 binning: conditional handoff; low-count final-state bins must be validated
  in Phase 4 with toys/Poisson treatment and MC-stat stability.
- Angular closure: passed with median mass differences far below `0.1 GeV`.
- Classifier/NN: attempted and rejected; S2 diagnostics are preserved for the
  analysis note appendix as a serious rejected approach.
- VBF: formally downscoped for current flat ntuples; production-sensitive VBF
  comparisons are non-comparable unless future allowed inputs expose real jets.
- Reducible background: DY+jets MC is retained as the nominal fake proxy per
  user request and Phase 2 [D6]; this remains a comparability limitation versus
  CMS data-driven Z+X.
- Phase 4 must build the actual `pyhf`/HistFactory workspace, nuisance model,
  injection tests, GoF, pulls/impacts, and simultaneous mass-extraction attempt
  from these fit-ready inputs.

## Code Reference

Run the Phase 3 chain with `pixi run p3-all`. The full analysis chain through
Phase 3 is `pixi run all`.
