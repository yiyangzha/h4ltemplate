# Phase 4a Expected Inference

Session: `edmund_69a2`
Created: 2026-05-30T01:26:57+00:00

## Summary

Phase 4a reports expected-only inference using MC/Asimov observations. The
fit observation is the nominal model expectation plus pyhf auxiliary data; no
real Open Data event counts are used as pseudo-data. The nominal handoff is the
Phase 3 S1 final-state categorization (`4mu`, `4e`, `2e2mu`) in
`105 < m4l < 140 GeV`.

The global signal-strength result is:

- `mu = 1 -0.5167 +0.6327`
- symmetric expected uncertainty: `0.5747`
- precision ratio to CMS-HIG-16-041 symmetrized uncertainty: `3.193`
- ratio greater than 5x reference: `False`

## Model

The model is a binned simultaneous pyhf/HistFactory-style likelihood with one
global signal-strength POI `mu` scaling all Higgs templates together. The
workspace uses channels `4mu, 4e, 2e2mu`
and mass-bin edges `[105.0, 112.0, 118.0, 122.0, 126.0, 130.0, 140.0]`. MC
statistical uncertainty is propagated with group/category normalization
nuisances derived from Phase 3 `sumw2`; full per-bin staterror profiling was
not computationally stable in this sandbox, so the implementation is paired
with explicit alternative-binning stability checks.

## Expected Fit Result

| Category | chi2 | Poisson deviance | ndf | chi2 p | deviance p |
| --- | --- | --- | --- | --- | --- |
| combined | 0 | 0 | 17 | 1 | 1 |
| 2e2mu | 0 | 0 | 5 | 1 | 1 |
| 4e | 0 | 0 | 5 | 1 | 1 |
| 4mu | 0 | 0 | 5 | 1 | 1 |

The exact Asimov deviance is expected to be numerically zero when the fitted
expectation matches the generated model expectation. The chi2 values are
reported for audit only and are not observed-data goodness-of-fit results.

## Low-Count Validation And Binning

The Phase 3 handoff had
`17/18`
final-state bins below five expected events. Phase 4a retains the final-state
simultaneous model because the Poisson toy validation passes:

- toys: `80` with seed `4269`
- fit success fraction: `1`
- median `mu`: `0.9394`
- median bias: `-0.06065`
- bias gate pass: `True`

| Binning | Channels | mu uncertainty | bins below 5 | fit p |
| --- | --- | --- | --- | --- |
| final_state_nominal | 4mu,4e,2e2mu | 0.5724 | 17 | 1 |
| inclusive_nominal | inclusive | 0.5755 | 0 | 1 |
| inclusive_coarse | inclusive | 0.5868 | 0 | 1 |
| inclusive_peak_side | inclusive | 0.5895 | 0 | 1 |

Final-state channel compatibility:

| Channel | mu | uncertainty | pull vs combined | fit p |
| --- | --- | --- | --- | --- |
| 4mu | 1 | 0.8669 | 0 | 1 |
| 4e | 1 | 1.811 | 0 | 1 |
| 2e2mu | 1 | 0.8771 | 0 | 1 |

## Validation Tests

Signal injection and recovery:

| Injected mu | Fitted mu | bias | relative bias | 20 percent gate |
| --- | --- | --- | --- | --- |
| 0.0 | 5.391e-21 | 5.391e-21 | 5.391e-21 | True |
| 1.0 | 1 | 0 | 0 | True |
| 2.0 | 2 | -4.472e-06 | 2.236e-06 | True |
| 5.0 | 5 | -7.576e-05 | 1.515e-05 | True |

Closure-test sensitivity with intentionally corrupted model ingredients:

| Corruption | deviance | ndf | p-value | fails as required |
| --- | --- | --- | --- | --- |
| m4l_scale_factor_0.8 | 13.47 | 5 | 0.01934 | True |
| m4l_scale_factor_1.2 | 91.6 | 5 | 3.1049e-18 | True |

The corruption tests pass the sensitivity requirement because the intentionally
wrong models are rejected below `p = 0.05`.

## Covariance And Uncertainty Breakdown

Covariance matrices are in `analysis_note/results/expected_covariance.json`.
For the single reported parameter, the total covariance is the scalar variance
shown below.

| Component | variance | uncertainty |
| --- | --- | --- |
| mc_stat | 0.002956 | 0.05437 |
| stat | 0.3064 | 0.5535 |
| syst_total_including_mc_stat | 0.02396 | 0.1548 |
| total | 0.3303 | 0.5747 |

## Nuisance Impacts

| Nuisance | mu shift down | mu shift up | max abs impact |
| --- | --- | --- | --- |
| dy_fake_norm | 0.1427 | -0.06093 | 0.1427 |
| qqZZ_norm | 0.08392 | -0.08207 | 0.08392 |
| lepton_eff | 0.05804 | -0.05382 | 0.05804 |
| m4l_scale_shape | -0.009583 | -0.05273 | 0.05273 |
| signal_ggH_theory | 0.0462 | -0.04237 | 0.0462 |
| lumi | 0.01497 | -0.01476 | 0.01497 |
| ggZZ_norm | 0.004351 | -0.004283 | 0.004351 |
| signal_VBF_theory | 0.004308 | -0.004223 | 0.004308 |
| ttbar_omission | 0.003187 | -0.002649 | 0.003187 |
| signal_VH_theory | 0.001326 | -0.001318 | 0.001326 |

## Mass-Template Closure

The Phase 4a method-parity attempt uses shifted detector-level M125 templates
with `mu` profiled at each mass grid point. It is not an official calibrated
mass measurement, but it satisfies the expected-phase mass-template closure
gate on the available templates.

- nominal best mass grid point: `125 GeV`
- nominal best-fit `mu` in the mass scan: `1`
- injected-mass closure passes: `True`
- promoted to nominal mass measurement: `False`
- downgrade reason: Detector-level shifted-template closure passes, but independent mass-hypothesis MC and official lepton calibration/morphing inputs are unavailable; retain as method-parity closure rather than a nominal mass measurement.
- limitation: Uses shifted detector-level M125 templates because independent mass-hypothesis MC and official lepton calibration/morphing inputs are unavailable in the sandbox.

| Injected mass [GeV] | Recovered grid [GeV] | bias [GeV] | bias gate |
| --- | --- | --- | --- |
| 124.0 | 124.0 | 0 | True |
| 125.0 | 125.0 | 0 | True |
| 126.0 | 126.0 | 0 | True |

## Systematic Completeness

| Source | Conventions | Ref 1 | Ref 2 | This analysis | Status |
| --- | --- | --- | --- | --- | --- |
| Integrated luminosity | SP1 | https://cms-results.web.cern.ch/cms-results/public-results/preliminary-results/LUM-20-001/ | CMS-PAS-LUM-20-001 public summary, 2017 full-year luminosity 42.12 +/- 0.34 fb^-1; used as a scale reference for the user-provided 10 fb^-1 subset. | Propagated in pyhf model | implemented |
| Lepton reconstruction/ID/trigger efficiency | SP4 | phase3_selection/outputs/cut_motivation_diagnostics.json | Phase 3 cut-motivation closure: largest final-state lepton-ID data/MC step-efficiency discrepancy is about 3 percent; propagated as a rate envelope. | Propagated in pyhf model | implemented |
| Signal production normalization/composition | SP7 | https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-16-041/ | CMS-HIG-16-041 and CMS-HIG-19-001 normalize H(125) signal to SM expectations; prompt effective signal cross sections are user-provided, so a 5 percent composition prior is scanned and marked fallback. | Propagated in pyhf model | implemented |
| qqZZ background normalization | SP9 | https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-19-001/ | Open-data fallback for prompt effective ZZ cross section; CMS references estimate ZZ from simulation and treat background normalization as a systematic source. | Propagated in pyhf model | implemented |
| ggZZ background normalization | SP9 | https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-19-001/ | Open-data fallback for small loop-induced ggZZ component; prior is wider than qqZZ because only prompt effective cross sections are available in this sandbox. | Propagated in pyhf model | implemented |
| DY+jets fake-proxy normalization | SP10 | phase3_selection/outputs/sideband_fake_diagnostics.json | Phase 3 sideband fake diagnostics show only 11 DY+jets raw entries in the two sidebands after selection, so the DY fake proxy is weakly constrained and assigned a broad fallback prior. | Propagated in pyhf model | implemented |
| TTBar omission diagnostic | SP11 | phase3_selection/outputs/sideband_fake_diagnostics.json | Phase 3 TTBar/DY weighted-yield diagnostic in the signal window; TTBar is below promotion threshold and propagated as an omission envelope on reducible background. | Propagated in pyhf model | implemented |
| Lepton momentum scale/resolution shape | SP5 | https://cds.cern.ch/record/1279137 | CMS momentum-scale public performance context reports per-mille-level deviations; propagated by shifting m4l templates by +/-0.1 percent. | Propagated in pyhf model | implemented |
| MC statistical uncertainty | SP3 | phase3_selection/outputs/fit_inputs_s1.json | Derived from Phase 3 per-bin sumw2 templates. Implemented as group/category normalization nuisances and tested with alternative-bin stability because full per-bin staterror profiling is computationally impractical in this sandbox. | Propagated in pyhf model | implemented |
| Higgs branching fraction | SP8 | https://pdg.lbl.gov/2024/tables/rpp2024-sum-gauge-higgs-bosons.pdf | PDG H->ZZ* fraction retained for cross-section conversions | Not used because Phase 4a reports detector-level mu only | not_applicable_no_cross_section_conversion |
| Classifier/category migration | SP12 | phase3_selection/outputs/approach_comparison.json | S2 classifier categories rejected | No MVA categories used | not_applicable_mva_rejected |
| Angular reconstruction | SP13 | phase3_selection/outputs/angular_closure.json | Angular inputs not used in nominal fit after S2 rejection | Closure retained as Phase 3 evidence | documented_not_propagated_no_angular_categories |

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

## Findings And Resolutions

| Finding | Resolution | Evidence |
| --- | --- | --- |
| Phase 3 handoff has many low-count final-state bins. | Retained final-state model only after Poisson toys and alternative-binning checks passed. | `expected_validation.json`, `expected_binning_stability.png`, `expected_binning_low_count_summary.png` |
| Full per-bin pyhf staterror model was computationally impractical. | Used grouped MC-stat normalization nuisances derived from `sumw2` and documented alternative-binning stability. | `expected_parameters.json`, `expected_covariance.json`, `expected_validation.json` |
| Plot watcher reported a crowded binning-stability figure. | Split the display into two separately registered figures. | `PLOT_WATCHER_RECHECK_vera_ee63.md` reports PASS with zero unresolved blockers. |
| MVA/classifier and VBF-like categories were rejected upstream. | No classifier migration or VBF systematics are propagated; they are documented as not applicable/downscoped. | `expected_systematics.json`, Phase 3 selection artifacts |

## Machine-Readable Outputs

- `analysis_note/results/expected_parameters.json`
- `analysis_note/results/expected_systematics.json`
- `analysis_note/results/expected_covariance.json`
- `analysis_note/results/expected_validation.json`
- `analysis_note/results/expected_mass_scan.json`
