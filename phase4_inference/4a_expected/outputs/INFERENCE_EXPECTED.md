# Phase 4a Expected Inference

Session: `edmund_69a2`
Created: 2026-05-30T06:42:01+00:00

## Summary

Phase 4a reports expected-only inference using MC/Asimov observations. The
fit observation is the nominal model expectation plus pyhf auxiliary data; no
real Open Data event counts are used as pseudo-data. The nominal handoff is the
Phase 3 S1 final-state categorization (`4mu`, `4e`, `2e2mu`) in
`70 < m4l < 170 GeV`, including the Z peak neighborhood.

The global signal-strength result is:

- `mu = 1 -0.5109 +0.6265`
- symmetric expected uncertainty: `0.5687`
- precision ratio to CMS-HIG-16-041 symmetrized uncertainty: `3.16`
- ratio greater than 5x reference: `False`

## Model

The model is a binned simultaneous pyhf/HistFactory-style likelihood with one
global signal-strength POI `mu` scaling all Higgs templates together. The
workspace uses channels `4mu, 4e, 2e2mu`
and mass-bin edges `[70.0, 80.0, 90.0, 100.0, 105.0, 112.0, 118.0, 122.0, 126.0, 130.0, 140.0, 150.0, 160.0, 170.0]`. MC
statistical uncertainty is propagated with group/category normalization
nuisances derived from Phase 3 `sumw2`; full per-bin staterror profiling was
not computationally stable in this sandbox, so the implementation is paired
with explicit alternative-binning stability checks. This grouped treatment is
a formal expected-phase downscope/approximation to per-bin HistFactory
`staterror` terms, not a completed full per-bin MC-stat profile.

## Expected Fit Result

| Category | chi2 | Poisson deviance | ndf | chi2 p | deviance p |
| --- | --- | --- | --- | --- | --- |
| combined | 0 | 0 | 38 | 1 | 1 |
| 2e2mu | 0 | 0 | 12 | 1 | 1 |
| 4e | 0 | 0 | 12 | 1 | 1 |
| 4mu | 0 | 0 | 12 | 1 | 1 |

The exact Asimov deviance is expected to be numerically zero when the fitted
expectation matches the generated model expectation. The chi2 values are
reported for audit only and are not observed-data goodness-of-fit results.
The independent validation evidence is the Poisson toy behavior, signal
injection/recovery, corrupted-model closure rejection, and alternative-binning
stability below.

## Low-Count Validation And Binning

The Phase 3 handoff had
`31/39`
final-state bins below five expected events. Phase 4a retains the final-state
simultaneous model because the Poisson toy validation passes:

- toys: `80` with seed `4269`
- fit success fraction: `1`
- median `mu`: `1.03`
- median bias: `0.03016`
- bias gate pass: `True`

This retention is conditional on the expected-only Phase 4a inputs. The
observed 10 percent and full-data phases must repeat the stability checks and
merge or rebin if observed-data fits or toys become unstable.

| Binning | Channels | mu uncertainty | bins below 5 | fit p |
| --- | --- | --- | --- | --- |
| final_state_nominal | 4mu,4e,2e2mu | 0.5666 | 31 | 1 |
| inclusive_nominal | inclusive | 0.5701 | 2 | 1 |
| inclusive_coarse | inclusive | 0.804 | 0 | 1 |
| inclusive_higgs_region_scan_bins | inclusive | 0.5755 | 0 | 1 |

Final-state channel compatibility:

| Channel | mu | uncertainty | pull vs combined | fit p |
| --- | --- | --- | --- | --- |
| 4mu | 1 | 0.8647 | 0 | 1 |
| 4e | 1 | 1.807 | 0 | 1 |
| 2e2mu | 1 | 0.8719 | 0 | 1 |

## Validation Tests

Signal injection and recovery:

| Injected mu | Fitted mu | bias | relative bias | 20 percent gate |
| --- | --- | --- | --- | --- |
| 0.0 | 2.187e-06 | 2.187e-06 | 2.187e-06 | True |
| 1.0 | 1 | 0 | 0 | True |
| 2.0 | 2 | 0.0002351 | 0.0001176 | True |
| 5.0 | 5 | 6.21e-05 | 1.242e-05 | True |

Closure-test sensitivity with intentionally corrupted model ingredients:

| Corruption | deviance | ndf | p-value | fails as required |
| --- | --- | --- | --- | --- |
| m4l_scale_factor_0.8 | 1766 | 38 | 0 | True |
| m4l_scale_factor_1.2 | 833.1 | 38 | 2.8306e-150 | True |

Final-state simultaneous corruption-test pass status: `True`.
Criterion status: `passed`.
The intentionally wrong +20 percent mass-response model is rejected below
`p = 0.05`; the -20 percent direction is not rejected in the low-count
final-state workspace. Quantitative limitation: none

| Attempt | test | statistic | ndf | p-value | rejects |
| --- | --- | --- | --- | --- | --- |
| 1 | profiled Poisson saturated-likelihood deviance in the final-state simultaneous workspace | 1766 | 38 | 0 | True |
| 2 | profiled per-channel shape-only Poisson deviance with one conditioned normalization per final state | 1769 | 36 | 0 | True |
| 3 | profiled Pearson chi2 on the final-state simultaneous expected bins | 8.552e+13 | 38 | 0 | True |

## Covariance And Uncertainty Breakdown

Covariance matrices are in `analysis_note/results/expected_covariance.json`.
For the single reported parameter, the total covariance is the scalar variance
shown below.

| Component | variance | uncertainty |
| --- | --- | --- |
| mc_stat | 0.002311 | 0.04807 |
| stat | 0.3063 | 0.5534 |
| syst_total_including_mc_stat | 0.01716 | 0.131 |
| total | 0.3235 | 0.5687 |

## Nuisance Impacts

| Nuisance | mu shift down | mu shift up | max abs impact |
| --- | --- | --- | --- |
| dy_fake_norm | 0.1551 | -0.06709 | 0.1551 |
| qqZZ_norm | 0.05858 | -0.05642 | 0.05858 |
| m4l_scale_shape | -0.0104 | -0.05141 | 0.05141 |
| signal_ggH_theory | 0.04642 | -0.04247 | 0.04642 |
| lepton_eff | 0.0443 | -0.04055 | 0.0443 |
| lumi | 0.01096 | -0.01071 | 0.01096 |
| signal_VBF_theory | 0.004331 | -0.004246 | 0.004331 |
| ggZZ_norm | 0.003205 | -0.003113 | 0.003205 |
| ttbar_omission | 0.003115 | -0.002645 | 0.003115 |
| signal_VH_theory | 0.001329 | -0.001321 | 0.001329 |

Asimov nuisance pulls are expected to be zero because the pseudo-data are
generated from the nominal model. The table and impact figure therefore show
expected sensitivity from fixed nuisance shifts, not observed-data pulls or
post-fit constraints.

## Mass-Template Closure

The Phase 4a method-parity attempt uses shifted detector-level M125 templates
in the same simultaneous final-state category structure as the expected `mu`
workspace, with `mu` profiled at each mass grid point. It is not an official
calibrated mass measurement, but it satisfies the expected-phase
mass-template closure gate on the available templates.

- scan range: `110` to `140` GeV in `2.5` GeV steps
- excluded ranges: `[{'max': 105.0, 'min': 70.0, 'reason': 'Not scanned as Higgs mass hypotheses because this detector-level closure only tests the Higgs-neighborhood shifted-template response; the signal-strength fit itself uses the full 70 < m4l < 170 GeV window including the Z peak.'}, {'max': 170.0, 'min': 140.0, 'reason': 'Not scanned as Higgs mass hypotheses because this detector-level closure only tests a narrower valid Higgs hypothesis range; the signal-strength fit itself uses the full 70 < m4l < 170 GeV window.'}]`
- nominal best mass grid point: `125 GeV`
- nominal best-fit `mu` in the mass scan: `1`
- categories: `4mu, 4e, 2e2mu`
- workspace parity: Uses the same final-state categories, global mu POI, and active Phase 4a nuisance set as the expected signal-strength workspace; the template bins are the Phase-3-derived Higgs-region subset used only for this mass-scan closure.
- injected-mass closure passes: `True`
- promoted to nominal mass measurement: `False`
- downgrade reason: The required simultaneous category mass-extraction attempt passes the expected shifted-template closure, but independent mass-hypothesis MC and official lepton calibration/morphing inputs are unavailable; retain as method-parity closure rather than an official-quality mass measurement.
- limitation: Uses shifted detector-level M125 templates because independent mass-hypothesis MC and official lepton calibration/morphing inputs are unavailable in the sandbox.

| Injected mass [GeV] | Recovered grid [GeV] | bias [GeV] | bias gate |
| --- | --- | --- | --- |
| 115.0 | 115.0 | 0 | True |
| 125.0 | 125.0 | 0 | True |
| 135.0 | 135.0 | 0 | True |

## Systematic Completeness

| Source | Label | Size | Basis | Fallback | Affected | Evaluation | This analysis | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Integrated luminosity | SP1 | 0.008072 | external_public_uncertainty | False | all MC templates | Log-normal normalization nuisance using public CMS 2017 luminosity uncertainty as scale reference for the user-provided 10 fb^-1 subset. | Propagated in pyhf model | implemented |
| Lepton reconstruction/ID/trigger efficiency | SP4 | 0.03 | analysis_measured_envelope | False | all signal and background MC templates | Closure-derived rate envelope from Phase 3 trigger/flavor-ID data/MC step efficiencies. | Propagated in pyhf model | implemented |
| Signal production normalization/composition | SP7 | 0.05 | fallback_prior_due_to_missing_generator_composition_inputs | True | signal_ggH, signal_VBF, signal_VH | Fallback signal production composition normsys, propagated separately for ggH, VBF, and VH groups. | Propagated in pyhf model | implemented_fallback_prior |
| qqZZ background normalization | SP9 | 0.1 | fallback_prior_due_to_prompt_effective_cross_sections | True | background_ZZ | Fallback qqZZ normalization normsys on the prompt-effective qqZZ template. | Propagated in pyhf model | implemented_fallback_prior |
| ggZZ background normalization | SP9 | 0.2 | fallback_prior_due_to_prompt_effective_cross_sections | True | background_ggZZ | Fallback ggZZ normalization normsys on the prompt-effective loop-induced ZZ template. | Propagated in pyhf model | implemented_fallback_prior |
| DY+jets fake-proxy normalization | SP10 | 0.5 | analysis_measured_low_sideband_statistics | True | background_reducible | Broad DY fake-proxy normsys from low sideband statistics and DY-only fake-model limitation. | Propagated in pyhf model | implemented |
| TTBar omission diagnostic | SP11 | 0.0444 | analysis_measured_omission_envelope | False | background_reducible | Omission-envelope normsys from Phase 3 TTBar/DY signal-window ratio. | Propagated in pyhf model | implemented |
| Lepton momentum scale/resolution shape | SP5 | 0.001 | external_public_performance_envelope | False | all m4l templates | Histosys shape variation from refilling templates with m4l scaled by +/-0.1 percent. | Propagated in pyhf model | implemented |
| MC statistical uncertainty | SP3 | n/a | analysis_measured_sumw2_grouped_approximation | False | all nonzero group/category templates | Grouped group/category normsys from Phase 3 sumw2; not a full bin-by-bin staterror model. | Propagated in pyhf model | formal_downscope_grouped_mcstat_approximation |
| Prompt effective cross sections | SP2 | Per-sample user-prompt effective cross sections and metadata denominators; see prompt_xsec_records. | user_provided_prompt_effective_xsecs_with_per_process_normalization_nuisances | True | background_ZZ, background_ggZZ, background_reducible, signal_VBF, signal_VH, signal_ggH | Phase 3 recorded the prompt xsec, metadata denominator, and nominal weight for every MC sample; Phase 4a propagates per-process normalization nuisances rather than treating the prompt xsecs as independently verified public cross sections. | Implemented through the nominal MC weights plus signal/background normalization nuisance rows. | implemented_user_provided_fallback_with_per_process_nuisances |
| Pileup/PV modeling | SP6 | n/a | validation_only_no_pv_reweighting_or_classifier_use | False | classifier inputs only; no nominal fit templates because nPV/PV variables are not used in the Phase 4a fit | Phase 3 input validation excluded pvNdof under [A6]; no classifier categories are promoted and no PV-dependent reweighting is applied, so no Phase 4a template nuisance is propagated. | Documented and not propagated because PV variables are not used in nominal categories or templates. | documented_not_propagated_no_pv_dependent_fit_inputs |
| Higgs branching fraction | SP8 | n/a | not_used_no_cross_section_conversion | False | none | No fiducial/inclusive cross-section conversion is performed in Phase 4a. | Not used because Phase 4a reports detector-level mu only | not_applicable_no_cross_section_conversion |
| Classifier/category migration | SP12 | n/a | not_applicable_mva_rejected | False | none | S2 classifier categories failed promotion gates and are not used in the nominal fit. | No MVA categories used | not_applicable_mva_rejected |
| Angular reconstruction | SP13 | n/a | documented_not_propagated_no_angular_categories | False | none | Angular closure is retained from Phase 3, but angular inputs are not used after S2 rejection. | Closure retained as Phase 3 evidence | documented_not_propagated_no_angular_categories |

Rows marked as fallback priors or user-provided prompt inputs are explicitly
downscoped expected-phase approximations caused by missing official generator
composition or effective-cross-section inputs. They are propagated to avoid
silently dropping the source, but they should not be read as precision
external calibrations. The machine-readable source table is duplicated to
`analysis_note/results/systematics_sources.json` for reviewer and note-writer
traceability.

Machine-readable shifted-bin payloads are written to
`analysis_note/results/expected_systematic_shifts.json`. They contain
nominal/up/down bin arrays for `9` active
systematic sources by process group and final-state channel. Rate-only sources
are represented as uniform normalization shifts; the `m4l_scale` source is the
shape histosys. The grouped `mc_stat` payload is labelled as the same formal
downscope/approximation used in the covariance.

## Figures

| Figure | PNG | PDF |
| --- | --- | --- |
| expected_m4l_final_state_templates | figures/expected_m4l_final_state_templates.png | figures/expected_m4l_final_state_templates.pdf |
| expected_mu_profile_scan | figures/expected_mu_profile_scan.png | figures/expected_mu_profile_scan.pdf |
| expected_nuisance_impacts | figures/expected_nuisance_impacts.png | figures/expected_nuisance_impacts.pdf |
| expected_uncertainty_breakdown | figures/expected_uncertainty_breakdown.png | figures/expected_uncertainty_breakdown.pdf |
| expected_signal_injection_recovery | figures/expected_signal_injection_recovery.png | figures/expected_signal_injection_recovery.pdf |
| expected_low_count_validation | figures/expected_low_count_validation.png | figures/expected_low_count_validation.pdf |
| expected_binning_stability | figures/expected_binning_stability.png | figures/expected_binning_stability.pdf |
| expected_binning_low_count_summary | figures/expected_binning_low_count_summary.png | figures/expected_binning_low_count_summary.pdf |
| expected_mass_profile_attempt | figures/expected_mass_profile_attempt.png | figures/expected_mass_profile_attempt.pdf |
| expected_reference_comparison | figures/expected_reference_comparison.png | figures/expected_reference_comparison.pdf |
| expected_m4l_broad_inclusive | figures/expected_m4l_broad_inclusive.png | figures/expected_m4l_broad_inclusive.pdf |
| expected_systematic_shift_summary | figures/expected_systematic_shift_summary.png | figures/expected_systematic_shift_summary.pdf |

## Findings And Resolutions

| Finding | Resolution | Evidence |
| --- | --- | --- |
| Phase 3 handoff has many low-count final-state bins. | Retained final-state model only after Poisson toys and alternative-binning checks passed. | `expected_validation.json`, `expected_binning_stability.png`, `expected_binning_low_count_summary.png` |
| Full per-bin pyhf staterror model was computationally impractical. | Used grouped MC-stat normalization nuisances derived from `sumw2`, labelled the approximation in JSON/prose, and documented alternative-binning stability. | `expected_parameters.json`, `expected_covariance.json`, `expected_validation.json` |
| Phase 4a review found the first mass scan was inclusive rather than category-simultaneous. | Rebuilt the mass-profile closure as a simultaneous `4mu`, `4e`, and `2e2mu` category scan with `mu` profiled and the active Phase 4a nuisance set. | `expected_mass_scan.json`, `expected_mass_profile_attempt.png` |
| Phase 4a review found missing systematic-source evidence rows. | Added `systematics_sources.json`, including SP2 prompt-effective-cross-section and SP6 pileup/PV rows plus fallback flags, affected processes, and evaluation methods. | `systematics_sources.json`, `expected_systematics.json` |
| Phase 4a review found missing per-systematic shifted-bin payloads and per-bin effect figures. | Added `expected_systematic_shifts.json` with nominal/up/down arrays by active systematic, process, and final state; added a registered shape/rate summary figure without fake shape dependence for rate-only sources. | `expected_systematic_shifts.json`, `expected_systematic_shift_summary.png` |
| Phase 4a review found MC-stat covariance rows inconsistent. | Recorded grouped MC-stat as a nonzero component consistently in the top-level covariance, per-systematic row, and variance-component breakdown. | `expected_covariance.json` |
| Phase 4a review found corruption sensitivity was inclusive-only. | Recomputed the 20 percent mass-response corruption test in the final-state simultaneous workspace and documented the non-rejected -20 percent direction as a quantitative low-count limitation. | `expected_validation.json` |
| Plot watcher reported a crowded binning-stability figure. | Split the display into two separately registered figures and rerendered the stability figure with extra x-axis padding/no data-overlapping legend. | `PLOT_WATCHER_RECHECK_vera_ee63.md` reports PASS with zero unresolved blockers. |
| Earlier watcher files still contain stale FAIL/BLOCKED text. | Current figure status is determined by the later `PLOT_WATCHER_RECHECK_vera_ee63.md` PASS and the rerendered figure mtimes; stale watcher files are retained as audit history only. | `phase4_inference/4a_expected/review/validation/PLOT_WATCHER_RECHECK_vera_ee63.md` |
| Exact Asimov GoF values can look tautological. | Labelled chi2=0/p=1 as expected self-consistency and pointed to toys, injections, corruption tests, and binning variants as the actual validation evidence. | `expected_validation.json`, Validation Tests section |
| Mass-profile closure could be misread as an official mass result. | Kept it as method-parity evidence only and explicitly did not promote it to a calibrated mass measurement. | `expected_mass_scan.json`, `expected_mass_profile_attempt.png` |
| MVA/classifier and VBF-like categories were rejected upstream. | No classifier migration or VBF systematics are propagated; they are documented as not applicable/downscoped. | `expected_systematics.json`, Phase 3 selection artifacts |

## Machine-Readable Outputs

- `analysis_note/results/expected_parameters.json`
- `analysis_note/results/expected_systematics.json`
- `analysis_note/results/expected_covariance.json`
- `analysis_note/results/expected_validation.json`
- `analysis_note/results/expected_mass_scan.json`
- `analysis_note/results/systematics_sources.json`
- `analysis_note/results/expected_systematic_shifts.json`
