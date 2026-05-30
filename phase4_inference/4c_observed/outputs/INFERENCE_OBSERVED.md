# Phase 4c Observed-Data Inference

Session: `zoran_44a0`
Created: 2026-05-30T07:47:12+00:00

## Summary

Phase 4c runs the reviewed Phase 4a final-state template likelihood on the full
observed dataset. Per the latest user instruction, the observed-data fit window
is `70 < m4l < 170 GeV`, including the Z peak. MC templates use the full
`10 fb^-1` normalization; no template is
normalized to the observed data integral.

The full-data observed result is:

- `mu = 2.478 -0.7139 +0.8388`
- symmetric uncertainty: `0.7763`
- expected-vs-observed pull: `1.535`
- partial-vs-observed pull: `1.587`
- compatibility with Phase 4a expected within 2 sigma: `True`
- compatibility with Phase 4b 10% result within 2 sigma: `True`
- viability verdict: `PASS`
- observed shifted-template mass fine-grid best: `124.8 GeV`
- diagnostic grid half-step: `0.125 GeV`

## Full Dataset

- seed: `None`
- selection method: all selected data events from the Phase 3 handoff are retained for Phase 4c; the seed is used only for the deterministic split proxy
- selected data events kept: `203` of `203` (`1`)
- fit-window event counts by channel: `{'2e2mu': 98, '4e': 24, '4mu': 81}`
- broad-window event counts by channel: `{'2e2mu': 98, '4e': 24, '4mu': 81}`
- normalization policy: All Phase 3 MC template weights are used at the full 10 fb^-1 normalization; no MC template is normalized to the observed data integral.

## Observed Fit And GoF

| quantity | value |
| --- | --- |
| mu | 2.478 |
| uncertainty minus | 0.7139 |
| uncertainty plus | 0.8388 |
| chi2 | 47.33 |
| ndf | 38 |
| chi2 p-value | 0.1427 |
| Poisson deviance | 48.69 |
| deviance p-value | 0.1148 |
| fit triviality gate | PASS |
| mu at boundary | False |
| relative total uncertainty | 0.3133 |
| viability verdict | PASS |

This is an observed-data GoF against the post-fit model, not an Asimov
self-consistency check. The `zero_chi2_warning` flag is
`False`.

## Expected-Vs-Observed Compatibility

| quantity | value |
| --- | --- |
| Phase 4a expected mu | 1 |
| Phase 4a expected uncertainty | 0.5687 |
| Phase 4b partial mu | 0 |
| Phase 4b partial uncertainty | 1.355 |
| Phase 4c observed mu | 2.478 |
| Phase 4c observed uncertainty | 0.7763 |
| pull vs expected | 1.535 |
| pull vs partial | 1.587 |
| any comparison over 2 sigma | False |

## Low-Count And Binning Stability

| configuration | channels | mu | uncertainty | observed zero bins | GoF p |
| --- | --- | --- | --- | --- | --- |
| final_state_nominal | 4mu, 4e, 2e2mu | 2.477 | 0.7762 | 3 | 0.1427 |
| inclusive_nominal | inclusive | 2.537 | 0.7808 | 0 | 0.9132 |
| inclusive_coarse | inclusive | 2.559 | 0.8133 | 0 | 0.7704 |
| inclusive_peak_side | inclusive | 2.56 | 0.8137 | 0 | 0.7282 |

Nominal final-state model retained:
`True`.
Decision: `retain_final_state_nominal_for_full`.

Toy validation repeats the Phase 4a low-count stability check on the full-data
luminosity model:

| quantity | value |
| --- | --- |
| toys | 80 |
| seed | 4269 |
| fit success fraction | 1 |
| median mu | 1.03 |
| median bias vs mu=1 | 0.03016 |

## Per-Category Compatibility

| channel | observed events | mu | uncertainty | pull vs combined | GoF p |
| --- | --- | --- | --- | --- | --- |
| 4mu | 81 | 2.476 | 1.153 | -0.001475 | 0.6966 |
| 4e | 24 | 1.106 | 1.899 | -0.6686 | 0.9787 |
| 2e2mu | 98 | 3.1 | 1.281 | 0.4152 | 0.7308 |

## Deterministic Split Proxy

True CMS run-period metadata is unavailable in the Phase 3 event handoff, so
Phase 4c uses a documented deterministic random half-split proxy.

| split | events | effective lumi fb^-1 | mu | uncertainty | GoF p |
| --- | --- | --- | --- | --- | --- |
| split_a | 103 | 5 | 2.35 | 1.108 | 0.161 |
| split_b | 100 | 5 | 2.612 | 1.064 | 0.4074 |

Split pull: `-0.1706`.

## Nuisance Pulls And Impacts

Top nuisance impacts:

| nuisance | mu shift down | mu shift up | max abs impact |
| --- | --- | --- | --- |
| dy_fake_norm | 0.2102 | -0.1708 | 0.2102 |
| signal_ggH_theory | 0.1149 | -0.1054 | 0.1149 |
| lepton_eff | 0.07755 | -0.09355 | 0.09355 |
| qqZZ_norm | 0.02051 | -0.04704 | 0.04704 |
| m4l_scale_shape | -0.02516 | 0.03684 | 0.03684 |
| lumi | 0.02148 | -0.02256 | 0.02256 |
| signal_VBF_theory | 0.01063 | -0.01054 | 0.01063 |
| ttbar_omission | 0.004211 | -0.004059 | 0.004211 |
| signal_VH_theory | 0.003349 | -0.003342 | 0.003349 |
| ggZZ_norm | 0.002742 | -0.002661 | 0.002742 |

Full pull and impact payloads are in
`analysis_note/results/observed_parameters.json`.

## Uncertainty Breakdown

| component | variance | uncertainty |
| --- | --- | --- |
| stat | 0.534 | 0.7307 |
| mc_stat | 0 | 0 |
| syst incl mc_stat | 0.06873 | 0.2622 |
| total | 0.6027 | 0.7763 |

The grouped MC-stat treatment remains the reviewed Phase 4a approximation, not
a full bin-by-bin HistFactory staterror profile.

## Observed Mass Scan

The full-data follow-up does not assume the observed Higgs candidate peak is at
125 GeV. It scans shifted M125 detector-level templates with `mu` profiled at
each mass hypothesis. The likelihood still uses the broad `70 < m4l < 170 GeV`
fit bins, but the Z peak region is excluded from the Higgs mass-hypothesis grid.

| quantity | value |
| --- | --- |
| scan min GeV | 110 |
| scan max GeV | 150 |
| coarse scan step GeV | 2.5 |
| fine scan min GeV | 122 |
| fine scan max GeV | 128 |
| fine scan step GeV | 0.25 |
| coarse best mass grid GeV | 125 |
| fine-grid best mass GeV | 124.8 |
| diagnostic grid half-step GeV | 0.125 |
| diagnostic parabolic best GeV | 125.4 |
| best profiled mu | 2.403 |
| uncertainty meaningful | True |
| grid interval GeV | [124.75, 125.5] |
| promoted to nominal mass measurement | False |

| mH hypothesis GeV | grid | profiled mu | delta -2lnL | GoF p | fit status |
| --- | --- | --- | --- | --- | --- |
| 110 | coarse | n/a | n/a | n/a | failed_after_all_fallbacks_FailedMinimization |
| 112.5 | coarse | n/a | n/a | n/a | failed_after_all_fallbacks_FailedMinimization |
| 115 | coarse | n/a | n/a | n/a | failed_after_all_fallbacks_FailedMinimization |
| 117.5 | coarse | n/a | n/a | n/a | failed_after_all_fallbacks_FailedMinimization |
| 120 | coarse | 1.743 | 140.6 | 1e-30 | full_nuisance_fit |
| 122.5 | coarse | 2.99 | 40.42 | 3.576e-06 | full_nuisance_fit |
| 125 | coarse | 2.478 | 0.2386 | 0.1427 | full_nuisance_fit |
| 127.5 | coarse | 1.81 | 19.99 | 0.000926 | full_nuisance_fit |
| 130 | coarse | 1.287 | 51.13 | 3.365e-11 | full_nuisance_fit |
| 132.5 | coarse | 0.97 | 95.68 | 1.532e-26 | full_nuisance_fit |
| 135 | coarse | 0.5096 | 129.1 | 1.981e-38 | full_nuisance_fit |
| 137.5 | coarse | 0.2085 | 185.5 | 4.741e-53 | full_nuisance_fit |
| 140 | coarse | 0 | 272.7 | 1.987e-84 | full_nuisance_fit |
| 142.5 | coarse | 0 | 357.4 | 4.075e-174 | full_nuisance_fit |
| 145 | coarse | n/a | n/a | n/a | failed_after_all_fallbacks_FailedMinimization |
| 147.5 | coarse | n/a | n/a | n/a | failed_after_all_fallbacks_FailedMinimization |
| 150 | coarse | n/a | n/a | n/a | failed_after_all_fallbacks_FailedMinimization |
| 122 | fine | 2.942 | 57.51 | 8.586e-09 | full_nuisance_fit |
| 122.2 | fine | 2.991 | 47.49 | 3.913e-07 | full_nuisance_fit |
| 122.8 | fine | 3 | 34.47 | 1.733e-05 | full_nuisance_fit |
| 123 | fine | 2.94 | 29.05 | 9.007e-05 | full_nuisance_fit |
| 123.2 | fine | 2.569 | 21.33 | 0.001532 | full_nuisance_fit |
| 123.5 | fine | 2.492 | 16.86 | 0.004199 | full_nuisance_fit |
| 123.8 | fine | 2.286 | 10.36 | 0.03019 | full_nuisance_fit |
| 124 | fine | 2.276 | 7.031 | 0.05714 | full_nuisance_fit |
| 124.2 | fine | 2.29 | 4.867 | 0.07972 | full_nuisance_fit |
| 124.5 | fine | 2.294 | 1.123 | 0.1424 | full_nuisance_fit |
| 124.8 | fine | 2.403 | 0 | 0.1645 | full_nuisance_fit |
| 125.2 | fine | 2.542 | 0.769 | 0.1275 | full_nuisance_fit |
| 125.5 | fine | 2.705 | 0.4624 | 0.132 | full_nuisance_fit |
| 125.8 | fine | 2.729 | 1.157 | 0.1203 | full_nuisance_fit |
| 126 | fine | 2.722 | 2.561 | 0.09188 | full_nuisance_fit |
| 126.2 | fine | 2.727 | 4.588 | 0.06459 | full_nuisance_fit |
| 126.5 | fine | 2.688 | 7.271 | 0.04177 | full_nuisance_fit |
| 126.8 | fine | 2.646 | 11.46 | 0.0112 | full_nuisance_fit |
| 127 | fine | 2.54 | 14.09 | 0.004766 | full_nuisance_fit |
| 127.2 | fine | 2.384 | 17.76 | 0.001129 | full_nuisance_fit |
| 127.8 | fine | 1.556 | 22.91 | 0.0003276 | full_nuisance_fit |
| 128 | fine | 1.47 | 26.48 | 0.0001564 | full_nuisance_fit |

Limitations: The scan is grid-level and model-limited: only M125 signal MC is available, the Z-peak region is excluded from Higgs mass hypotheses, and any interval or interpolation is a shifted-template diagnostic rather than a calibrated mass uncertainty.

## Figures

| figure | PNG | PDF |
| --- | --- | --- |
| observed_m4l_broad_inclusive | figures/observed_m4l_broad_inclusive.png | figures/observed_m4l_broad_inclusive.pdf |
| observed_m4l_70_170_categories | figures/observed_m4l_70_170_categories.png | figures/observed_m4l_70_170_categories.pdf |
| observed_expected_mu_comparison | figures/observed_expected_mu_comparison.png | figures/observed_expected_mu_comparison.pdf |
| observed_nuisance_pulls | figures/observed_nuisance_pulls.png | figures/observed_nuisance_pulls.pdf |
| observed_nuisance_impacts | figures/observed_nuisance_impacts.png | figures/observed_nuisance_impacts.pdf |
| observed_binning_stability | figures/observed_binning_stability.png | figures/observed_binning_stability.pdf |
| observed_split_consistency | figures/observed_split_consistency.png | figures/observed_split_consistency.pdf |
| observed_uncertainty_viability | figures/observed_uncertainty_viability.png | figures/observed_uncertainty_viability.pdf |
| observed_mass_scan | figures/observed_mass_scan.png | figures/observed_mass_scan.pdf |

## Findings And Resolutions

| Finding | Resolution | Evidence |
| --- | --- | --- |
| Phase 4a final-state workspace was sparse and required repeated observed-data stability checks. | Repeated toy validation, alternative inclusive/coarse binnings, category compatibility, and deterministic split checks on all selected full-data events. | `observed_validation.json`, `observed_binning_stability.png`, `observed_split_consistency.png` |
| True CMS run-period information is unavailable in the Phase 3 handoff. | Used a deterministic random half-split proxy and labelled it as a limitation, not a run-period validation. | `observed_validation.json` deterministic split section |
| Reducible background remains a DY+jets MC fake proxy rather than a full data-driven fake-rate estimate. | Preserved the Phase 2/3 scope and propagated the broad DY fake-proxy nuisance; no hand scaling to observed data integral was applied. | `observed_systematics.json`, `observed_m4l_broad_inclusive.png` |
| VBF and MVA/NN categories are not nominal categories. | Retained S1 final-state categories only; no VBF or classifier labels are used in the fit. | Phase 3 `selected_configuration.json`, `observed_parameters.json` |
| Full-data viability must be checked honestly. | Evaluated the boundary, fit-triviality, and total-uncertainty gates; if the result is not competitive the verdict remains `LIMITED_NOT_COMPETITIVE` rather than being tuned. | `observed_validation.json`, `observed_uncertainty_viability.png` |
| Data-sensitive systematics must be re-evaluated where possible. | Recomputed observed-data nuisance pulls, impacts, GoF, category compatibility, alternative binnings, and deterministic split diagnostics; external/fallback priors remain transferred because no new calibration or fake-rate inputs are available. | `observed_parameters.json`, `observed_systematics.json` |
| Full-data mass must not be assumed to be 125 GeV. | Added an observed shifted-template mass scan with `mu` profiled at each mass hypothesis; classified as approximate detector-level evidence rather than an official calibrated mass measurement. | `observed_mass_scan.json`, `observed_mass_scan.png` |

## Machine-Readable Outputs

- `analysis_note/results/observed_parameters.json`
- `analysis_note/results/observed_validation.json`
- `analysis_note/results/observed_covariance.json`
- `analysis_note/results/observed_mass_scan.json`
- `analysis_note/results/observed_systematics.json`
- `analysis_note/results/observed_systematic_shifts.json`
- `analysis_note/results/systematics_sources.json`
