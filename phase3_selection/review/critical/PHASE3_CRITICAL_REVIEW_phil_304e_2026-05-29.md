# Phase 3 Critical Review

Session: `phil_304e`
Date: 2026-05-29
Role: Phase 3 Selection/Processing critical reviewer

## Verdict

ITERATE. I find no Category A physics showstopper in the selected S1 path, but there are three Category B issues that should be fixed before Phase 3 PASS. The main problem is not the choice of S1 itself; it is that the Phase 4 handoff claims/strongly implies category viability without carrying the actual low-stat bin evidence and the required conditional treatment.

## Findings

### B1. S1 category/bin viability is overstated relative to the selected fit binning

`approach_comparison.json` states `"category_viability": "passes final-state categories; see cutflow and fit_inputs_s1.json"` at line 5, and `SELECTION.md` hands off `fit_inputs_s1.json` as fit-ready with final-state categories `4mu`, `4e`, and `2e2mu` at lines 167-176. The strategy, however, warned that `m4l` bins below about five expected events are not accepted unless Phase 4 performs toy validation and stable MC-stat treatment (`STRATEGY.md` lines 205-207).

From `fit_inputs_s1.json`, summing signal plus background in the six selected `m4l` bins gives:

| Category | Total expected per bin | Bins below 5 |
| --- | --- | --- |
| `4mu` | `[2.563, 2.469, 3.098, 3.771, 2.515, 3.980]` | 6/6 |
| `4e` | `[1.884, 2.597, 2.696, 1.173, 0.688, 2.610]` | 6/6 |
| `2e2mu` | `[4.476, 2.616, 4.251, 3.975, 4.384, 6.865]` | 5/6 |

The inclusive diagnostic bins are all above 5 (`[8.922, 7.682, 10.045, 8.919, 7.587, 13.455]`), but `SELECTION.md` correctly says the inclusive category must not be fitted simultaneously with the mutually exclusive final-state categories (lines 172-175). Therefore the nominal final-state handoff is low-stat in 17/18 bins.

Required fix: either rebin/merge for the nominal Phase 4 handoff, or revise `SELECTION.md`, `approach_comparison.json`, and the Phase 4 handoff text to state explicitly that the selected final-state binning is conditional on Phase 4 low-count Poisson/toy validation and MC-stat stability. The current wording "passes final-state categories" is too strong for the evidence.

### B2. MVA machine-readable JSON contains non-standard `NaN` values

`mva_metrics.json` and `mva_training_metadata.json` contain literal `NaN` for logistic and small-NN score-gate `chi2`/`p_value`:

- `phase3_selection/outputs/mva_metrics.json:361950` and `:361952`
- `phase3_selection/outputs/mva_metrics.json:723311` and `:723313`
- same line positions in `mva_training_metadata.json`

These files are advertised as machine-readable Phase 3 outputs. Python's permissive JSON parser accepts `NaN`, but strict JSON readers do not. Since these diagnostics are intended for the note writer/review trail, use `null` plus an explicit reason such as `ndf = 0` instead of `NaN`.

Required fix: replace non-finite floating values in JSON serialization with `null` and add fields explaining why the statistic is undefined. Re-run the artifact builder so `SELECTION.md` continues to show `n/a` for those entries.

### B3. Major event-level cuts are not independently motivated by cut plots

`SELECTION.md` lists the effective event-level cuts at lines 49-56: finite core variables, `trigBits != 0`, final-state categorization, flavor-matched lepton ID, Z-pair sanity, broad validation window, and fit window. The cutflow shows the lepton-ID step is large, reducing data from 798 to 467 and MC weighted yield from 790 to 466 (`SELECTION.md` lines 64-67). The Phase 3 plan promised cut-motivation plots for trigger, lepton ID/Z sanity, and fit-window stages (`plan.md` lines 118-119), but the final figure registry in `SELECTION.md` lines 180-210 has only a cutflow summary, input validation plots, mass plots, sideband/MVA/VBF diagnostics, and no dedicated trigger/ID/Z-sanity motivation plot.

This is not a claim that the cuts are wrong. The implementation follows the Phase 2 object-handling instructions: trigger uses a bitmask (`build_selection_table.py` line 132), lepton ID is flavor-matched (`build_selection_table.py` lines 102-111), and Z sanity checks charge/flavor/Z membership (`build_selection_table.py` lines 114-127). The issue is reviewability: a 40% selection step needs a diagnostic beyond a cumulative count.

Required fix: add compact cut-motivation diagnostics or a machine-readable table/figure showing trigger, lepton-ID, and Z-sanity efficiencies by final state and process, with data/MC comparison where meaningful. If a plot is infeasible, document why and add the evidence to `SELECTION.md`.

## Verified Items

- MCP tools were not used; `TOGGLES.md` has `MCP_ALPHAXIV=false` and `MCP_LEP_CORPUS=false`.
- The governing convention is not `conventions/extraction.md`: `STRATEGY.md` lines 182-191 state this is a binned shape/profile-likelihood measurement, not a closed-form extraction.
- [D1] primary path freeze is satisfied for nominal Phase 3 processing: `selection_provenance.json` has `primary_paths_only_for_nominal = True`, 12 nominal files, roles only `primary_data`/`primary_mc`, and no local files.
- [D3] fit-window handling is satisfied: `SELECTION.md` lines 55-56 define `70 <= m4l <= 170 GeV` as validation and `105 < m4l < 140 GeV` for fit-ready templates; `fit_inputs_s1.json` records `fit_window: [105.0, 140.0]`.
- [D4]/VBF downscope is supported: `SELECTION.md` lines 73-79 reports 24 checked flat ntuples, zero jet/VBF-like branch files, zero allowed upstream join sources, `safe_event_key_join_possible = False`, and no lepton-only VBF label.
- [D6] DY/TTBar fake treatment is consistent with Phase 2: `SELECTION.md` lines 155-158 reports TTBar/DY ratios low `0.0954`, signal `0.0444`, high `0.1635`, all below the Phase 2 promotion thresholds.
- [D7] input gate was enforced before MVA use: `input_validation.json` passes only `lead_abs_eta` (`chi2/ndf = 0.4734`, `p = 0.7553`, max ratio deviation `0.193`) and `phi1` (`chi2/ndf = 0.1552`, `p = 0.9785`, max ratio deviation `0.0826`); `train_mva.py` uses only variables with `passes_d7_gate` at lines 120-122.
- [D8] angular closure passes before classifier training: `SELECTION.md` lines 88-101 shows all sample median mass differences below `0.1 GeV` and zero out-of-range angular counts.
- S1/S2 comparison was performed: `approach_comparison.json` gives S1 `mu` proxy `0.9730`, S2 best `small_nn` proxy `1.2025`, relative improvement `-0.2359`, and `promote_s2 = false`.
- Remaining Phase 4-only items are correctly left open in `COMMITMENTS.md`: [D2], [D5], [D9], pyhf workspace, global `mu`, systematics, GoF, pulls/impacts, injection tests, mass-template closure, reference comparisons, and final AN comparability rows remain unchecked.
- Level 2 plot validation is complete: `PERFIG_VALIDATION_SUMMARY_2026-05-29.md` lines 8-11 report 29 registry entries, 29 PNG + 29 PDF, no missing/empty/stale/orphan files, and `lint-plots` PASS; lines 32-35 state all 29 final figures passed after rechecks.

## Figure Sanity Spot Checks

I inspected the final Level 2 summary and key rendered figures directly:

- `m4l_fit_window_inclusive.png`: data/MC pulls are mostly within about ±1.5 with one upward bin near 123 GeV around 2 sigma; no global >20% normalization offset across the bulk is visible.
- `m4l_broad_window_inclusive.png`: the large continuum peak near the Z region is dominated by qqZZ and broadly follows data; sideband totals are not outside the `[0.5, 2.0]` data/MC sanity range.
- `input_validation_mZ1.png`: visually confirms a sharp Z1 peak and supports the D7 failure recorded in JSON (`chi2/ndf = 122.064`, `p = 6.22e-155`) as an input-modeling veto rather than an accepted classifier input.
- `mva_best_score_datamc.png`: score distribution is nearly degenerate and supports rejection of S2; the plot is diagnostic only and not part of the nominal fit.
- `category_viability_s1.png`: category totals are readable, but the figure does not expose the low-stat per-bin problem described in B1.

Physics sanity checks: all count/yield-like JSON values I scanned are non-negative; no negative yield/count-like values were found. The only non-finite values found are the MVA diagnostic `NaN` values in B2. Cutflow monotonicity is satisfied for all samples/channels in `cutflow.json`.

## Residual Risks For Phase 4

The selected S1 approach is defensible for the available flat ntuples, but Phase 4 must not treat the final-state binning as automatically robust. It needs explicit low-count treatment, MC-stat modifiers, toy/asymptotic validation, GoF per category, and alternative binning stability before any `mu` or mass result is accepted.
