# Phase 3 Critical Review 2

Session: `ursula_0b8b`  
Date: 2026-05-29  
Role: fresh Phase 3 critical reviewer after first review-iteration fixes

## Verdict

PASS.

I find no remaining Category A or Category B issues in the current Phase 3
selection artifact or machine-readable outputs. The prior plot-label and
critical-review findings are fixed, and I did not find a new physics or
handoff regression introduced by the fixes.

## Prior Finding Closure

| Prior finding | Current status | Evidence |
| --- | --- | --- |
| Plot A1: `sideband_dy_ttbar_diagnostics` exposed raw `DYJetsToLL`/dataset-style labels. | FIXED | `PHASE3_FIX_VERIFICATION_sally_2377_2026-05-29.md:20` records direct inspection of final labels `DY+jets fake proxy` and `TTBar diagnostic`. I re-opened `phase3_selection/outputs/figures/sideband_dy_ttbar_diagnostics.png`; the legend shows those presentation labels and no `DYJetsToLL` stem. Source now labels the sideband series through `sample_display_name(sample)` in `phase3_selection/src/make_selection_plots.py:218`. |
| Critical B1: S1 category/bin viability overstated despite low-count final-state bins. | FIXED | `SELECTION.md:8-13` states the S1 final-state handoff is conditional because `17/18` bins have `S+B < 5`; `SELECTION.md:95-120` enumerates the per-bin S+B evidence. `selected_configuration.json:4-18` records `handoff_status = conditional_low_count_final_state_binning` and requires Phase 4 low-count Poisson/toy validation, MC-stat stability, and rebin/merge fallback. `approach_comparison.json:201-208` records `17/18` final-state bins below 5 expected events and zero inclusive diagnostic bins below 5. |
| Critical B2: MVA JSON contained non-standard `NaN`. | FIXED | Strict JSON parsing with `parse_constant` rejection succeeded for `FIGURES.json`, `mva_metrics.json`, `mva_training_metadata.json`, `approach_comparison.json`, `selected_configuration.json`, `fit_inputs_s1.json`, and other Phase 3 JSON outputs; recursive scan found `nonfinite=0` in each. `grep -RIn "NaN\|Infinity\|-Infinity" phase3_selection/outputs/*.json` returned no matches. The undefined logistic and small-NN score gates are now JSON `null` with `undefined_reason: "ndf=0"` in `mva_metrics.json:361950-361955` and `mva_metrics.json:723312-723317`. |
| Critical B3: trigger, lepton-ID, and Z-pair cuts lacked dedicated motivation diagnostics. | FIXED | `SELECTION.md:74-91` adds a cut-motivation section with data/MC efficiencies, pass counts, and denominators. `cut_motivation_diagnostics.json:163-240` and `:243-320` record Open Data and Open Simulation efficiencies by final state; e.g. 4e lepton-ID efficiency is `0.3644` in data and `0.3542` in simulation. `FIGURES.json:279-308` registers `cut_motivation_efficiencies`, and I directly inspected the PNG: it shows trigger, lepton-ID, and Z-pair rows for `4mu`, `4e`, and `2e2mu` with separate Open data/simulation markers. |

## Fresh Review Checks

### Phase 2 Commitment Traceability

- [D1] Primary paths are respected: `selection_provenance.json:185` has `primary_paths_only_for_nominal = true`; all listed roles are `primary_data`/`primary_mc` (`selection_provenance.json:11-178`). This matches the Phase 2 requirement to use prompt paths (`STRATEGY.md:99-100`, `:562-570`).
- [D3] Fit-window handling is consistent: `SELECTION.md:58-59` defines `70 <= m4l <= 170 GeV` for validation and `105 < m4l < 140 GeV` for fit-ready templates; `fit_inputs_s1.json` records `fit_window = [105.0, 140.0]`.
- [D4]/[A3] VBF is correctly downscoped: `vbf_recovery_downscope.json:7-13` records formal downscope, no allowed upstream join sources, and `safe_event_key_join_possible = false`; `vbf_recovery_downscope.json:66-180` begins the 24 branch checks, all with empty `jet_or_vbf_like_branches`; `selected_configuration.json:19` records `vbf_label_used = false`.
- [D6] DY+jets fake proxy and TTBar diagnostic treatment match the strategy: `sideband_fake_diagnostics.json` gives TTBar/DY ratios `0.0954` low sideband, `0.0444` signal window, and `0.1635` high sideband, below the Phase 2 promotion thresholds. `SELECTION.md:201-215` states the same and keeps DY+jets as the nominal fake proxy.
- [D7]/[D8] Angular inputs and classifier gating are enforced. `angular_closure.json:4` has `overall_pass = true`, and `angular_closure.json:8-266` records zero out-of-range angular values per sample. `input_validation.json:194-232` passes only `lead_abs_eta` (`chi2/ndf = 0.4734`, `p = 0.7553`, max deviation `0.1931`); `input_validation.json:428-470` passes only `phi1` (`chi2/ndf = 0.1552`, `p = 0.9785`, max deviation `0.0826`). Other candidate variables are rejected by the D7 trend/chi2 gates, and `input_validation.json:3-6` explicitly keeps `m4l`, isolation tails, SIP3D, and `pvNdof` out of the classifier path.

The still-open [D2], [D5], and [D9] commitments in `COMMITMENTS.md:20-35` and `:46-50` are correctly Phase 4 obligations: pyhf/HistFactory workspace, one global `mu`, and simultaneous/profiled mass-extraction attempt or documented infeasibility. They are not Phase 3 blockers because Phase 3 has produced fit inputs and the conditional handoff needed for those Phase 4 tests.

### Cutflow, Normalization, And Handoff

- MC normalization uses the Phase 2 formula: `normalization.json:3` has `lumi_pb_user_prompt = 10000.0`, and each MC record uses `weight_formula = sigma_eff_pb * L_pb / sum_Metadata_nEvents` (examples at `normalization.json:20-24`, `:64-68`, `:130-134`). No data-integral scaling is claimed in the artifact (`SELECTION.md:26-30`).
- The cumulative cutflow is monotonic and numerically consistent with the artifact: `SELECTION.md:61-72` gives final fit-window data `69`, MC raw `405145`, MC weighted yield `56.6`, and monotonic `True`. My JSON aggregation of `cutflow.json` reproduced the same endpoint: data `69`, MC raw `405145`, MC weighted `56.6098`, all cumulative sample/channel cutflows monotonic.
- The selected fit handoff is honest about low counts. `approach_comparison.json:47-54`, `:93-100`, and `:139-146` list final-state S+B bin totals; `approach_comparison.json:201-208` summarizes `17/18` final-state bins below 5 expected events. This is now a valid conditional Phase 4 handoff, not an unconditional viability claim.

### S1/S2 Approach Comparison

The mandatory >=2 approach comparison is present and quantitative. `approach_comparison.json:4-7` gives S1 expected signal `7.7324`, background `48.8774`, and `mu` uncertainty proxy `0.9730`. `approach_comparison.json:212-218` gives S2 best model `small_nn`, proxy `1.2025`, relative improvement `-0.2359`, and `promote_s2 = false`. The MVA output supports rejection: BDT score-shape gate passes (`mva_metrics.json:1472-1477`) but its category viability fails with low-stat fraction `1.0` (`mva_metrics.json:248-249`); logistic and small NN have undefined score-gate chi2 due `ndf=0` and fail promotion (`mva_metrics.json:361950-361955`, `:723312-723317`, `:723372-723378`).

This is consistent with Phase 2: the classifier was attempted, alternative architectures were trained, the NN was not promoted without a >10% improvement and gate pass, and S1 was retained for robustness.

### Figures And Plot-Related Physics Sanity

Current registry smoke test: `FIGURES.json` has 30 entries, 60 registered PNG/PDF files, 60 actual files in `outputs/figures`, no missing files, no zero-byte files, and no orphan PNG/PDF files. The apparent count difference relative to `PERFIG_VALIDATION_SUMMARY_2026-05-29.md:8-11` is explained by the later B3 fix adding `cut_motivation_efficiencies`; that new figure was inspected in `PHASE3_FIX_VERIFICATION_sally_2377_2026-05-29.md:23` and by me during this review.

I visually spot-checked the current post-fix figures most relevant to the prior findings and physics handoff:

- `sideband_dy_ttbar_diagnostics.png`: sideband labels are publication-style; expected DY+jets dominates TTBar in all three regions, matching the ratios in `sideband_fake_diagnostics.json`.
- `cut_motivation_efficiencies.png`: the large 4e and 2e2mu lepton-ID efficiency steps are now visible and agree between Open Data and Open Simulation at the few-percent level shown in `SELECTION.md:81-91`.
- `m4l_fit_window_inclusive.png`: no global >20% data/MC offset is visible across the bulk; pulls are within roughly ±2.5 in the six fit-window bins, consistent with a low-stat prefit validation plot rather than a fitted result.
- `category_viability_s1.png`: the figure summarizes final-state totals, while the artifact/JSON now carry the more important per-bin low-count warning.

The old plot-validation report `PHASE3_PLOT_VALIDATION_nora_76da_2026-05-29.md` remains useful for the 29-figure pre-fix set and its single A finding; the targeted verifier plus this review cover the two changed figures. A separate fresh plot-validator PASS on the 30-entry registry would be audit-clean, but I do not classify the stale 29-count summary as a Phase 3 critical-review blocker because the changed figures have direct post-fix inspection evidence and the registry itself is internally consistent.

## Correctly Deferred Phase 4 Items

The following are correctly left unresolved for Phase 4, not Phase 3:

- pyhf/HistFactory workspace, Poisson terms, nuisances, MC-stat modifiers, GoF, pulls, impacts, and global `mu`: open in `COMMITMENTS.md:20-35`, `:54-89`, and `:121-127`.
- Signal injection/recovery, alternative binning stability, channel compatibility fits, and simultaneous mass-template closure: open in `COMMITMENTS.md:117-131` and `:176-178`.
- Reference-result comparison and final AN comparability matrix: open in `COMMITMENTS.md:180-202`, with comparison targets recorded in `COMMITMENTS.md:204-245`.
- VBF categories are explicitly unavailable unless real jet recovery becomes possible; no lepton-only category is mislabeled VBF (`selected_configuration.json:19`, `SELECTION.md:122-127`).

## Findings

No Category A findings.  
No Category B findings.

Category C / audit hygiene:

- C1. The old per-figure validation summary still says 29 figures (`PERFIG_VALIDATION_SUMMARY_2026-05-29.md:8-11`) while the current registry has 30 entries after the cut-motivation fix. This is non-blocking because `cut_motivation_efficiencies` was directly inspected during fix verification and this review, but updating or superseding the summary would make the audit trail cleaner.

## Residual Risks

The main residual risk is deliberately deferred to Phase 4: the final-state category binning is statistically sparse (`17/18` bins below 5 expected events). Phase 4 must either validate low-count Poisson/toy behavior and MC-stat stability or merge/rebin before reporting `mu` or mass results. A Phase 4 result that ignores this conditional handoff would be a new Category A issue, but Phase 3 now documents the risk clearly and hands it off with machine-readable evidence.
