# Phase 4a Expected Inference Critical Review

Session: `dmitri_46e5`  
Date: 2026-05-30  
Scope: fresh blocking critical review after fix commit `ddcf18e` and targeted verification commit `0cbd76c`.

## Verdict: ITERATE

The prior critical-review blockers are materially improved: the mass-profile attempt is now category-simultaneous with `mu` profiled, `SP2` and `SP6` have explicit source rows, the MC-stat covariance entries are internally consistent, and exact Asimov `chi2=0`/`p=1` is labelled as a self-consistency audit rather than independent GoF. However, Phase 4a is not complete because the mandatory machine-readable per-systematic shift payloads and per-systematic shift figures are absent.

## Findings

### A1. Missing per-systematic up/down shift outputs and per-systematic impact figures

Category: A, must resolve before Doc 4a.

The Phase 4a template requires "Per-systematic shifts (bin edges + up/down shifts)" in `analysis_note/results/*.json` and also lists "Per-systematic impact figures (bin-dependent shifts)" among the work this phase must do. The current result files do not contain those payloads. `analysis_note/results/expected_systematics.json` has only top-level keys `created_utc`, `phase`, and `sources`; each of its 14 source entries contains traceability fields such as `relative_variation`, `affected_templates_processes`, `evaluation_method`, and `status`, but no `bin_edges`, `nominal`, `up`, `down`, `delta`, or per-channel/per-process shifted-bin arrays.

Concrete evidence:

- `phase4_inference/4a_expected/CLAUDE.md` requires machine-readable per-systematic shifts and covariance outputs in the "Machine-readable outputs" section, and its "What this phase does" list includes per-systematic impact figures.
- `analysis_note/results/expected_systematics.json` contains 14 `sources` rows and no shift arrays; I checked the schema of every source row.
- `phase4_inference/4a_expected/src/run_expected_inference.py:662-775` constructs `systematic_table_payload()` as a source table only. The code records labels, variation bases, affected templates, and citations, but it never writes shifted template arrays or binned up/down effects to JSON.
- The registered figure list has 10 figures: templates, `mu` scan, nuisance ranking, uncertainty breakdown, injection, low-count validation, binning stability, mass-profile attempt, and reference comparison. There is no registered per-systematic shifted-template or per-bin systematic-impact figure. The only systematic figure, `expected_nuisance_impacts`, ranks maximum `mu` shifts and does not show bin-dependent template shifts.

This is not a request to tune values toward published references. The issue is traceability: a note writer or reviewer cannot inspect how, for example, `m4l_scale`, `dy_norm`, `zz_norm`, `lepton_eff`, or grouped `mc_stat` changes the actual binned templates. The artifact claims propagation, but the required binned evidence is unavailable.

Required fix:

- Add machine-readable per-systematic shift payloads with bin edges and nominal/up/down arrays, at least by channel and process group for all active nuisances.
- Add registered figure(s) that show the per-bin effects for shape sources and a clear rate-impact representation for pure normalization sources.
- Keep pure normalization sources labelled as normalization-only; do not manufacture fake shape dependence for them.

### B1. MC-stat downscope is documented but still marked as completed rather than formally downscoped

Category: B, should address before PASS unless the orchestrator accepts the existing arbiter decision as sufficient.

The current implementation honestly records grouped MC-stat normalization nuisances, and the covariance is now internally consistent: `expected_covariance.json` reports `mc_stat_treatment = group_category_normsys_from_sumw2; not full bin-by-bin HistFactory staterror profiling`, `mc_stat` variance `0.0029560843`, stat variance `0.3063689402`, syst variance `0.0239551084`, and total variance `0.3303240485`, with `stat + syst = total`.

The residual issue is status traceability. Phase 2 strategy row `[SP3]` says MC statistical uncertainty will be implemented as "Bin-by-bin template statistical terms"; `run_expected_inference.py:169-180` implements one `normsys` per group/category from summed `sumw2`, not per-bin `staterror` terms. `COMMITMENTS.md` marks `[D2][SP3]` as `[x]` while the proof text says full bin-by-bin profiling "remains a documented expected-phase downscope." That is better than the prior state, but the status marker still reads as completed implementation of the original commitment rather than formal downscope/approximation.

This does not invalidate the expected result by itself because the artifact labels the approximation and validates low-count behavior with toys and alternative binnings. It should be cleaned up so downstream reviewers do not mistake grouped MC stat for the original bin-by-bin commitment.

### B2. Corruption sensitivity is inclusive-only while the nominal fit is final-state simultaneous

Category: B, should address if feasible.

The corruption test now gives nontrivial failures: `m4l_scale_factor_0.8` has deviance `13.4714` with `ndf=5`, `p=0.01934`, and `m4l_scale_factor_1.2` has deviance `91.5956`, `p=3.10e-18`, so the test does catch a 20% mass-response corruption. The limitation is that `run_expected_inference.py:540-556` builds the corruption test by merging channels into an `inclusive` model and fitting with `active_systematics - {"m4l_scale"}`. The nominal result, low-count concern, and mass-profile closure are all final-state simultaneous (`4mu`, `4e`, `2e2mu`).

The current inclusive test is valid evidence that the broad mass-response alarm is not tautological. It is weaker evidence for the actual nominal workspace, especially because final-state bins are the low-count part of the model. A final-state version of the same corruption test, or an explicit quantitative reason why the inclusive alarm is sufficient, would close this residual risk.

## Resolved Prior Findings Checked

- Prior mass-scan blocker: resolved. `expected_mass_scan.json` now lists categories `4mu`, `4e`, `2e2mu`, active nuisance metadata, and injected-mass closures at 124, 125, and 126 GeV, all recovered on-grid with `bias_GeV = 0.0`.
- Prior missing `SP2`/`SP6` source rows: resolved. `systematics_sources.json` and `expected_systematics.json` now contain `prompt_effective_xsecs` and `pileup_pv_modeling` rows with fallback/status fields.
- Prior MC-stat covariance contradiction: resolved numerically. The top-level `mc_stat`, `per_systematic.mc_stat`, and variance-component entries all use `0.0029560843`.
- Prior Asimov circularity wording: materially improved. `expected_validation.json` states that nominal Asimov `chi2=0` and `p=1` are self-consistency/audit quantities, and the artifact points to toys, injections, corruption tests, and binning variants as the validation evidence.

## Completion-Criteria Verdicts

- Expected results computed on MC/Asimov pseudo-data only: PASS. `expected_common.py:180` excludes `is_data` events when filling event-level templates, and `fit_configuration()` uses `model.expected_data(...)` as pseudo-data.
- All systematic variations with citations for variation size: PARTIAL. Each source row has a citation/search trail, but several are fallback priors or analysis-measured envelopes. That is acceptable if kept honestly labelled; A1 remains because shifted-bin outputs are missing.
- Closure test passes and demonstrated sensitivity: PARTIAL. Signal injection passes for `mu = 0, 1, 2, 5`; corrupted mass-response tests fail as required. B2 remains because the corruption test is inclusive-only.
- Precision comparison vs reference documented in validation JSON: PASS. `expected_validation.json` reports ratio `3.192990241669998`, reference uncertainty `0.18`, and `ratio_gt_5x = false`.
- Covariance matrices in results: PASS for the single reported parameter. `stat`, `mc_stat`, `syst`, `total`, and `per_systematic` entries exist and are internally consistent.
- All figures saved and registered in `FIGURES.json`: PASS for the 10 registered figures, but the required per-systematic shift figure class is missing under A1.
- `COMMITMENTS.md` updated: PASS with B1 status-cleanup risk.
- Every finding has a Resolution + Evidence section: PASS for the artifact's own listed findings.

## Residual Risks

- The repository has a `conventions/` directory with `search.md`, `extraction.md`, and `unfolding.md`, but `conventions/fitting.md` referenced by `phase4_inference/4a_expected/CLAUDE.md` is absent. Phase 2 explicitly adapts `conventions/search.md` to this measurement, so this did not block the review, but the missing fitting convention should not be cited as read or satisfied.
- The expected uncertainty is dominated by low statistics: total expected uncertainty is `0.5747` on `mu`, compared with `0.18` for the CMS-HIG-16-041 reference used in the precision comparison. The ratio `3.19` is below the >5x investigation gate and is honestly documented.
- The mass scan is appropriately not promoted to an official-quality mass measurement. It uses shifted detector-level M125 templates because independent mass-hypothesis MC and official calibration inputs are unavailable.
