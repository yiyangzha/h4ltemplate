# Phase 4a Fix Verification Arbiter

Session: `albert_54c1`  
Date: 2026-05-30  
Scope: targeted verification of fixes after commit `ddcf18e085975f0cad8a6414a4ed6b6448025065`

Verdict: `ALL FIXED`

This is not a full fresh review. I verified only the previous review-cycle
findings listed in the prompt, plus the requested lint and figure-registry
smoke checks.

## Finding Verification Table

| Original finding | Status | Evidence |
|---|---:|---|
| Critical A1 [D9]: prior implementation was inclusive rather than simultaneous final-state category mass extraction with `mu` profiled. | `FIXED` | `analysis_note/results/expected_mass_scan.json` reports method `simultaneous final-state category shifted-template mass-profile closure with mu profiled in each shifted-template fit`, categories `["4mu", "4e", "2e2mu"]`, `profiled_parameter: "mu"`, no `inclusive` string hits, and closure rows for injected 124, 125, and 126 GeV all have `passes_bias_gate: true`. Source evidence: `phase4_inference/4a_expected/src/run_expected_inference.py:582-651` builds `nominal_templates = shifted_category_templates(...)`, passes `CHANNELS` to `model_spec(...)`, records `categories: list(CHANNELS)`, and records `profiled_parameter: "mu"`. `model_spec` defines the signal `mu` normfactor at line 136. `INFERENCE_EXPECTED.md:139-150` reports the same category-simultaneous mass-template closure and limitation. |
| Critical A2: systematic evidence lacked `systematics_sources.json`, SP2, SP6, variation-size evidence, and fallback flags; `COMMITMENTS.md` overclaimed unsupported evidence. | `FIXED` | `analysis_note/results/systematics_sources.json` exists and was read in full, with 14 rows. The SP2 row `prompt_effective_xsecs` includes `commitment_label: "SP2"`, `variation_basis: "user_provided_prompt_effective_xsecs_with_per_process_normalization_nuisances"`, `fallback_flag: true`, `citation_or_search_trail`, affected processes, evaluation method, status, and per-sample prompt cross-section records. The SP6 row `pileup_pv_modeling` includes `commitment_label: "SP6"`, `variation_basis: "validation_only_no_pv_reweighting_or_classifier_use"`, `fallback_flag: false`, citation/search trail to Phase 3 validation outputs, affected-template statement, evaluation method, and status. `INFERENCE_EXPECTED.md:171-175` includes SP3, SP2, and SP6 rows in the systematic-source table. `COMMITMENTS.md:55-59` states SP2 is user-provided fallback with per-process nuisances and SP3 is grouped approximation; `COMMITMENTS.md:66-67` states SP6 is documented as excluded from nominal fit nuisance propagation, not externally calibrated. I found no remaining overclaim that public/campaign cross sections or a propagated PV nuisance were available. |
| Critical B1: MC-stat covariance had contradictory zero and nonzero MC-stat entries; commitments implied full bin-by-bin staterror. | `FIXED` | `analysis_note/results/expected_covariance.json` now has `mc_stat_treatment: "group_category_normsys_from_sumw2; not full bin-by-bin HistFactory staterror profiling"`. The top-level `mc_stat`, `per_systematic.mc_stat`, `uncertainty_breakdown.per_systematic.mc_stat.variance_increment_over_stat`, and `uncertainty_breakdown.variance_components.mc_stat` all report `0.0029560843175981955`. Source evidence: `run_expected_inference.py:443-450` special-cases `mc_stat` in the per-systematic loop and records the grouped treatment and nonzero variance rather than fitting it with `include_staterror=False`. `COMMITMENTS.md:58-59` explicitly says this is the grouped group/category MC-stat approximation and that full bin-by-bin `staterror` remains a documented expected-phase downscope. |
| Plot A/B: `expected_m4l_final_state_templates` missing `mh.label.exp_label(...)` on all independent panels and had unacceptable legend handling. | `FIXED` | Source evidence: `make_expected_plots.py:119-140` loops over all three `CHANNELS`, calls `mh.label.exp_label(...)` inside the loop for each `ax`, labels each panel as `Open Simulation ({channel})`, places the legend only on the first panel, and calls `safe_mpl_magic(ax)` for each panel. Visual evidence from regenerated `outputs/figures/expected_m4l_final_state_templates.png`: all three panels visibly show CMS/Open Simulation labels for `4mu`, `4e`, and `2e2mu`; the legend is confined to the upper right of the first panel and does not obscure the plotted markers. |
| Plot A/B: `expected_mu_profile_scan` legend overlapped the profile curve. | `FIXED` | Source evidence: `make_expected_plots.py:155-163` draws the profile and sigma lines, moves the legend to `loc="upper center"`, calls `safe_mpl_magic(ax)`, and adds the standard label. Visual evidence from regenerated `outputs/figures/expected_mu_profile_scan.png`: the legend is centered at the top in empty whitespace; the rising high-`mu` profile curve on the right is unobscured. |

## Requested Non-Mutating Checks

### `pixi run lint-plots`

Result: PASS

```text
Pixi task (lint-plots): python conventions/lint_plots.py .
No plotting violations found in 25 file(s).
```

### Figure Registry Smoke Test

Result: PASS

```text
entries=10
registered_files=20
missing=0
zero_byte=0
orphan_png_pdf=0
stale_relative_to_make_expected_plots=0
make_expected_plots_mtime=1780108482933928243
FIGURES_json_mtime=1780108571975291249
REGISTERED_DETAIL phase4_inference/4a_expected/outputs/figures/expected_m4l_final_state_templates.png size=160319 mtime_ns=1780108567752368886
REGISTERED_DETAIL phase4_inference/4a_expected/outputs/figures/expected_m4l_final_state_templates.pdf size=28209 mtime_ns=1780108567402375321
REGISTERED_DETAIL phase4_inference/4a_expected/outputs/figures/expected_mu_profile_scan.png size=105916 mtime_ns=1780108568376357414
REGISTERED_DETAIL phase4_inference/4a_expected/outputs/figures/expected_mu_profile_scan.pdf size=21301 mtime_ns=1780108568160361385
```

## Conclusion

All targeted findings from the previous Phase 4a review cycle are fixed.
The orchestrator should proceed to a full fresh Phase 4a blocking review.
