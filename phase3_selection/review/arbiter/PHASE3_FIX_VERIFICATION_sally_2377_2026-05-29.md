# Phase 3 Fix Verification

Session: `sally_2377`  
Date: 2026-05-29  
Role: targeted fix-verification arbiter, using `agents/arbiter.md` as base role

## Scope

This is not a fresh Phase 3 review. I verified only the four prior findings from:

- `phase3_selection/review/validation/PHASE3_PLOT_VALIDATION_nora_76da_2026-05-29.md`
- `phase3_selection/review/critical/PHASE3_CRITICAL_REVIEW_phil_304e_2026-05-29.md`

Inputs read included `TOGGLES.md`, `agents/arbiter.md`, `methodology/06-review.md`, the current Phase 3 artifacts, relevant scripts under `phase3_selection/src/`, and the regenerated PNGs `sideband_dy_ttbar_diagnostics.png` and `cut_motivation_efficiencies.png`.

## Verification Results

| Finding | Status | Evidence |
| --- | --- | --- |
| A1 plot label: `sideband_dy_ttbar_diagnostics` must not show `DYJetsToLL` and should use presentation labels. | FIXED | Direct inspection of `phase3_selection/outputs/figures/sideband_dy_ttbar_diagnostics.png` shows legend labels `DY+jets fake proxy` and `TTBar diagnostic`; no visible `DYJetsToLL` raw file stem appears. The regenerated file mtime is `2026-05-29 23:45:37` and size is 129053 bytes. Source now calls `sample_display_name(sample)` for the sideband legend at `phase3_selection/src/make_selection_plots.py:218`; `sample_display_name` maps known samples to `SAMPLE_INFO[name]["stack"]` at `phase3_selection/src/selection_common.py:255-260`, with `DYJetsToLL.root` mapped to `DY+jets fake proxy` and `TTBar.root` mapped to `TTBar diagnostic` at `selection_common.py:99-110`. Pattern grep still finds raw sample keys in machine-readable sample names, provenance, and normalization tables, but not as the sideband legend label path; no `sample.replace(".root", "")` pattern remains in the plotting grep results. |
| B1 low-stat final-state bin viability must no longer be overstated; selected S1 must be conditional and carry 17/18 low-count-bin evidence plus Phase 4 Poisson/toy/MC-stat requirements. | FIXED | `SELECTION.md:8-13` states the S1 final-state handoff is conditional because `17/18` bins have `S+B < 5` and require Phase 4 low-count Poisson/toy validation plus MC-stat stability. `SELECTION.md:95-120` explicitly says this is not an unconditional viability pass and enumerates all 18 per-category per-bin `S+B` values: `4mu` has 6/6 bins below 5, `4e` has 6/6, and `2e2mu` has 5/6. `SELECTION.md:218-227` states Phase 4 may use the final-state categories only after low-count Poisson/toy validation and MC-stat stability checks, otherwise it must rebin or merge categories. `approach_comparison.json:5` now labels S1 viability as a conditional low-count handoff; `approach_comparison.json:28,74,120` record bins-below-5 counts by category; `approach_comparison.json:196-208` records required Phase 4 validation and the summary `17/18`. `selected_configuration.json:4-18` records `handoff_status = conditional_low_count_final_state_binning`, the `17/18` summary, and the required Poisson/toy, MC-stat, and rebin/merge fallback validations. |
| B2 strict JSON: MVA JSON files must not contain non-standard `NaN`/`Infinity`; undefined score-gate stats should be JSON `null` with a reason. | FIXED | I ran strict parsing with `json.loads(..., parse_constant=reject_constant)` via `pixi run py` on `mva_metrics.json`, `mva_training_metadata.json`, `approach_comparison.json`, `selected_configuration.json`, `cut_motivation_diagnostics.json`, and `FIGURES.json`; all parsed successfully and a recursive finite-value scan found `NONFINITE_COUNT 0` in each. `grep -RIn "NaN\\|Infinity\\|-Infinity" phase3_selection/outputs/mva_metrics.json phase3_selection/outputs/mva_training_metadata.json` returned no matches. The formerly undefined score gates are now serialized as `chi2: null`, `p_value: null`, `ndf: 0`, `passes: false`, `undefined_reason: "ndf=0"` in `mva_metrics.json:361950-361955` and `723312-723317`, with identical entries in `mva_training_metadata.json` at the same line ranges. `train_mva.py:69-88` initializes undefined statistics as `None` and sets `undefined_reason = "ndf=0"` when applicable. |
| B3 cut motivation: trigger, lepton-ID, and Z-sanity cuts need dedicated diagnostics/evidence and `SELECTION.md` explanation. | FIXED | `SELECTION.md:74-91` adds a `Cut Motivation Diagnostics` section with data and MC step efficiencies, pass counts, and denominators for trigger, flavor-matched lepton ID, and Z-pair sanity by final state. `cut_motivation_diagnostics.json:570-588` defines the three cuts and their denominator steps; `cut_motivation_diagnostics.json:590-752` records data and open-simulation efficiencies, numerators, denominators, and `undefined_reason` fields by final state. `FIGURES.json:276-309` registers the new `cut_motivation_efficiencies` figure sourced from `cut_motivation_diagnostics.json`, and `SELECTION.md:247-248` lists the PNG/PDF in the figure table. Direct inspection of `phase3_selection/outputs/figures/cut_motivation_efficiencies.png` shows the expected trigger, lepton-ID, and Z-pairing efficiency rows for `4mu`, `4e`, and `2e2mu`, with separate Open data and Open simulation markers. |

## Pattern Checks

- Raw sideband-label pattern: `grep -RIn "DYJetsToLL\\|TTBar\\|sample.replace\\|\\.root.*label\\|replace(.*root" phase3_selection/src phase3_selection/outputs/FIGURES.json phase3_selection/outputs/SELECTION.md phase3_selection/outputs/*.json` finds raw sample keys in sample dictionaries, normalization/provenance tables, and machine-readable sample payloads. The relevant visible sideband legend path is fixed: `make_selection_plots.py:215-218` still iterates over raw keys for lookup, but labels with `sample_display_name(sample)`, which resolves to presentation stack names.
- MVA non-finite pattern: `grep -RIn "NaN\\|Infinity\\|-Infinity" phase3_selection/outputs/mva_metrics.json phase3_selection/outputs/mva_training_metadata.json` returned no matches; strict JSON parsing also passed.
- Cut-motivation registry pattern: `grep -RIn "cut_motivation\\|Cut Motivation\\|Trigger bitmask\\|Flavor-matched\\|Z-pair\\|cut_motivation_efficiencies" ...` finds the new diagnostics in `build_selection_table.py`, plotting in `make_selection_plots.py`, prose in `SELECTION.md`, registration in `FIGURES.json`, and machine-readable output in `cut_motivation_diagnostics.json`.

## Verdict

All four targeted findings are fixed. This verification does not replace the required fresh Phase 3 review; it only confirms that the previous A/B findings were specifically addressed.

ALL FIXED — proceed to fresh Phase 3 review
