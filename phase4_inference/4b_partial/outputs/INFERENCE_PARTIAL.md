# Phase 4b Partial-Data Inference

Session: `yuki_9d50`
Created: 2026-05-30T04:41:25+00:00

## Summary

Phase 4b runs the reviewed Phase 4a final-state template likelihood on a
fixed-seed 10% observed-data subsample. Per the latest user-requested Phase 4b
override, the partial-data fit window is `70 < m4l < 170 GeV`, including the Z
peak. This replaces the earlier CMS-like `105 < m4l < 140 GeV` Phase 4b
instruction for this quick rerun only. MC templates are scaled by `0.10` to an effective
luminosity of `1 fb^-1`; no template
is normalized to the observed data integral.

The 10% observed result is:

- `mu = 0 -n/a +1.355`
- symmetric uncertainty: `1.355`
- expected-vs-partial pull: `-0.6795`
- compatibility with Phase 4a expected within 2 sigma: `True`

## Fixed-Seed Subsample

- seed: `9417`
- selection method: numpy default_rng(seed) permutation of selected data events from Phase 3 handoff; first round(0.10*N) events retained
- selected data events kept: `20` of `203` (`0.09852`)
- fit-window event counts by channel: `{'2e2mu': 10, '4e': 3, '4mu': 7}`
- broad-window event counts by channel: `{'2e2mu': 10, '4e': 3, '4mu': 7}`
- normalization policy: All Phase 3 MC template weights are multiplied by 0.10 to represent the 10% effective luminosity; no MC template is normalized to the observed data integral.

## Observed Fit And GoF

| quantity | value |
| --- | --- |
| mu | 0 |
| uncertainty minus | n/a |
| uncertainty plus | 1.355 |
| chi2 | 31.76 |
| ndf | 38 |
| chi2 p-value | 0.7524 |
| Poisson deviance | 26.77 |
| deviance p-value | 0.9138 |

This is an observed-data GoF against the post-fit model, not an Asimov
self-consistency check. The `zero_chi2_warning` flag is
`False`.

## Expected-Vs-Partial Compatibility

| quantity | value |
| --- | --- |
| Phase 4a expected mu | 1 |
| Phase 4a expected uncertainty | 0.5747 |
| Phase 4b partial mu | 0 |
| Phase 4b partial uncertainty | 1.355 |
| pull | -0.6795 |

## Low-Count And Binning Stability

| configuration | channels | mu | uncertainty | observed zero bins | GoF p |
| --- | --- | --- | --- | --- | --- |
| final_state_nominal | 4mu, 4e, 2e2mu | 7.312e-16 | 1.358 | 24 | 0.7511 |
| inclusive_nominal | inclusive | 1.22e-15 | 1.418 | 2 | 0.9349 |
| inclusive_coarse | inclusive | 4.225e-14 | 1.011 | 1 | 0.8667 |
| inclusive_peak_side | inclusive | 0 | 1.011 | 1 | 0.7792 |

Nominal final-state model retained:
`True`.
Decision: `retain_final_state_nominal_for_10pct`.

Toy validation repeats the Phase 4a low-count stability check on the 10%
luminosity model:

| quantity | value |
| --- | --- |
| toys | 80 |
| seed | 4269 |
| fit success fraction | 1 |
| median mu | 0.809 |
| median bias vs mu=1 | -0.191 |

## Per-Category Compatibility

| channel | observed events | mu | uncertainty | pull vs combined | GoF p |
| --- | --- | --- | --- | --- | --- |
| 4mu | 7 | 1.225e-16 | 4.056 | 2.865e-17 | 0.7939 |
| 4e | 3 | 0 | 9.277 | 0 | 0.7971 |
| 2e2mu | 10 | 0 | 2.436 | 0 | 0.2778 |

## Deterministic Split Proxy

True CMS run-period metadata is unavailable in the Phase 3 event handoff, so
Phase 4b uses a documented deterministic random half-split proxy.

| split | events | effective lumi fb^-1 | mu | uncertainty | GoF p |
| --- | --- | --- | --- | --- | --- |
| split_a | 11 | 0.5 | 0 | 2.898 | 0.4625 |
| split_b | 9 | 0.5 | 2.216e-16 | 2.207 | 0.4295 |

Split pull: `-6.083e-17`.

## Nuisance Pulls And Impacts

Top nuisance impacts:

| nuisance | mu shift down | mu shift up | max abs impact |
| --- | --- | --- | --- |
| dy_fake_norm | 1.996e-15 | 3.064e-15 | 3.064e-15 |
| lumi | 0 | 1.5e-15 | 1.5e-15 |
| lepton_eff | 9.8e-16 | 1.44e-15 | 1.44e-15 |
| signal_VH_theory | 1.433e-15 | 3.22e-16 | 1.433e-15 |
| ttbar_omission | 0 | 1.397e-15 | 1.397e-15 |
| ggZZ_norm | 0 | 7.486e-16 | 7.486e-16 |
| m4l_scale_shape | 6.315e-16 | 0 | 6.315e-16 |
| qqZZ_norm | 8.598e-17 | 0 | 8.598e-17 |
| signal_VBF_theory | 0 | 0 | 0 |
| signal_ggH_theory | 0 | 0 | 0 |

Full pull and impact payloads are in
`analysis_note/results/partial_parameters.json`.

## Uncertainty Breakdown

| component | variance | uncertainty |
| --- | --- | --- |
| stat | 1.766 | 1.329 |
| mc_stat | 0 | 0 |
| syst incl mc_stat | 0.06948 | 0.2636 |
| total | 1.836 | 1.355 |

The grouped MC-stat treatment remains the reviewed Phase 4a approximation, not
a full bin-by-bin HistFactory staterror profile.

## Figures

| figure | PNG | PDF |
| --- | --- | --- |
| partial_m4l_broad_inclusive | figures/partial_m4l_broad_inclusive.png | figures/partial_m4l_broad_inclusive.pdf |
| partial_m4l_70_170_categories | figures/partial_m4l_70_170_categories.png | figures/partial_m4l_70_170_categories.pdf |
| partial_expected_mu_comparison | figures/partial_expected_mu_comparison.png | figures/partial_expected_mu_comparison.pdf |
| partial_nuisance_pulls | figures/partial_nuisance_pulls.png | figures/partial_nuisance_pulls.pdf |
| partial_nuisance_impacts | figures/partial_nuisance_impacts.png | figures/partial_nuisance_impacts.pdf |
| partial_binning_stability | figures/partial_binning_stability.png | figures/partial_binning_stability.pdf |
| partial_split_consistency | figures/partial_split_consistency.png | figures/partial_split_consistency.pdf |

## Findings And Resolutions

| Finding | Resolution | Evidence |
| --- | --- | --- |
| Phase 4a final-state workspace was sparse and required repeated observed-data stability checks. | Repeated toy validation, alternative inclusive/coarse binnings, category compatibility, and deterministic split checks on the fixed-seed 10% data. | `partial_validation.json`, `partial_binning_stability.png`, `partial_split_consistency.png` |
| True CMS run-period information is unavailable in the Phase 3 handoff. | Used a deterministic random half-split proxy and labelled it as a limitation, not a run-period validation. | `partial_validation.json` deterministic split section |
| Reducible background remains a DY+jets MC fake proxy rather than a full data-driven fake-rate estimate. | Preserved the Phase 2/3 scope and propagated the broad DY fake-proxy nuisance; no hand scaling to observed data integral was applied. | `partial_systematics.json`, `partial_m4l_broad_inclusive.png` |
| VBF and MVA/NN categories are not nominal categories. | Retained S1 final-state categories only; no VBF or classifier labels are used in the fit. | Phase 3 `selected_configuration.json`, `partial_parameters.json` |
| Phase 4b must update VT11. | Marked VT11 resolved with seed, event counts, effective luminosity, expected comparison, and stability evidence. | `COMMITMENTS.md`, `partial_validation.json` |

## Machine-Readable Outputs

- `analysis_note/results/partial_parameters.json`
- `analysis_note/results/partial_validation.json`
- `analysis_note/results/partial_covariance.json`
- `analysis_note/results/partial_systematics.json`
- `analysis_note/results/partial_systematic_shifts.json`
- `analysis_note/results/systematics_sources.json`
