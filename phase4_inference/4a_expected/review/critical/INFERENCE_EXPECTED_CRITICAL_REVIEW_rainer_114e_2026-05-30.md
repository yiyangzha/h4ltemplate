# Phase 4a Expected Inference Critical Review

Verdict: `ITERATE`

Doc 4a must not begin yet. I found two Category A blockers and one Category B blocker. The expected `mu` fit itself is numerically consistent with the reported JSON, and the Asimov-only boundary is respected, but binding traceability and systematic/covariance requirements are not satisfied.

## Findings

### A1. [D9] binding mass-extraction attempt is not satisfied

Category: A

The Phase 2 strategy requires Phase 4a to attempt a simultaneous category mass extraction with the same category workspace used for the `mu` fit, or document three concrete infeasibility attempts before downgrading. Evidence:

- Strategy [D9] requires “simultaneous category mass extraction” with `mu` profiled: `phase2_strategy/outputs/STRATEGY.md:126`.
- The binding attempt specifically requires the same simultaneous category workspace with final-state categories: `phase2_strategy/outputs/STRATEGY.md:137`.
- Downgrade is allowed only after closure failure with attempted fix or three concrete infeasibility attempts: `phase2_strategy/outputs/STRATEGY.md:158`.
- `COMMITMENTS.md` marks this as resolved and requires either mass workspace/scan JSON or an infeasibility log: `COMMITMENTS.md:46` and `COMMITMENTS.md:117`.
- The implementation uses an inclusive model: `mass_scan()` converts channel templates with `inclusive_from_channels(...)` and builds `model_spec(..., ("inclusive",), ...)` at `phase4_inference/4a_expected/src/run_expected_inference.py:559` and `phase4_inference/4a_expected/src/run_expected_inference.py:560`.
- The output JSON states the method is “inclusive shifted-template mass-profile closure”: `analysis_note/results/expected_mass_scan.json:177`.
- No `MASS_EXTRACTION_INFEASIBILITY.md` or `systematic` infeasibility log exists; `find . -name 'systematics_sources.json' -print` also returned no systematic-source file, and the only “three concrete” hits were in the plan/strategy/commitments text, not executed evidence.

Impact: the analysis currently claims [D9] is resolved while doing a different, weaker mass-profile exercise. The artifact properly says this is not an official mass measurement, but the binding commitment was to first attempt the simultaneous category extraction or document why it cannot be done. That traceability failure blocks advancement.

Required fix: implement the final-state simultaneous mass scan/closure with `mu` profiled, or write a concrete infeasibility artifact with three failed attempts including filenames, commands, failure modes, and why no supported implementation remains. Update `COMMITMENTS.md` and `expected_mass_scan.json` accordingly.

### A2. Systematic completeness and variation-size evidence are incomplete

Category: A

Phase 4a requires every systematic variation to be justified by a measurement or published uncertainty, with no arbitrary flat borrowed systematics unless the documented exception is met. Evidence:

- Phase 4a completion criterion requires “All systematic variations with citations for variation size”: `phase4_inference/4a_expected/CLAUDE.md:102`.
- Key requirements prohibit arbitrary or flat borrowed systematics without the documented exception: `phase4_inference/4a_expected/CLAUDE.md:64`.
- Strategy requires an equivalent `systematics_sources.json` table with source name, nominal value, uncertainty, citation/search trail, closure metric, fallback flag, and affected templates: `phase2_strategy/outputs/STRATEGY.md:423`.
- Strategy [SP2] requires every prompt effective cross section to have public/campaign search trail and yield-closure comparison, or be marked user-provided with per-process normalization nuisance: `phase2_strategy/outputs/STRATEGY.md:438`.
- `COMMITMENTS.md` marks [SP2] resolved with proof requiring public/campaign search trail, yield-closure comparison, and per-process nuisance: `COMMITMENTS.md:57`.
- There is no `systematics_sources.json` on disk (`find . -name 'systematics_sources.json' -print` returned nothing).
- `expected_systematics.json` has no SP2 row. The only prompt-cross-section hits are generic prose in SP7/SP9 fallback rows: `analysis_note/results/expected_systematics.json:31`, `analysis_note/results/expected_systematics.json:42`, and `analysis_note/results/expected_systematics.json:53`.
- The hard-coded prior values are in source, not derived from a cited numeric table: signal theory `0.050`, qqZZ `0.100`, ggZZ `0.200`, DY `0.50` at `phase4_inference/4a_expected/src/run_expected_inference.py:60`, `phase4_inference/4a_expected/src/run_expected_inference.py:68`, `phase4_inference/4a_expected/src/run_expected_inference.py:76`, and `phase4_inference/4a_expected/src/run_expected_inference.py:84`.
- The systematic completeness table omits [SP6] pileup/PV modeling entirely, even though [SP6] is a committed source in `phase2_strategy/outputs/STRATEGY.md:383` and marked resolved in `COMMITMENTS.md:69`.

Impact: the fit includes propagated nuisance parameters, but several variation sizes are not traceable to the required evidence hierarchy. The fallback rows may be acceptable after a proper documented fallback table and prior-width scans, but they are not acceptable as currently evidenced. This also means `COMMITMENTS.md` overstates [SP2]/[SP6] completion.

Required fix: add the required systematic-source evidence table or equivalent JSON, include SP2 and SP6 rows, document exact variation-size provenance or closure-derived envelope for each fallback prior, include affected templates/processes, and update `COMMITMENTS.md` statuses if any source remains a formal downscope.

### B1. MC-stat treatment is documented as approximate, but commitments/covariance are internally inconsistent

Category: B

The grouped MC-stat approximation is acknowledged, but the commitments and covariance representation still imply the full requirement was met.

Evidence:

- Strategy [SP3] requires “Bin-by-bin template statistical terms”: `phase2_strategy/outputs/STRATEGY.md:380`.
- `COMMITMENTS.md` claims the workspace includes bin-by-bin MC-stat modifiers: `COMMITMENTS.md:61`.
- The artifact instead states grouped category normalization nuisances are used and are not a drop-in replacement for full per-bin staterror profiling: `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md:28`.
- Source implements MC stat as one normsys per group/channel using total `sqrt(sumw2)/yield`: `phase4_inference/4a_expected/src/run_expected_inference.py:168`.
- `expected_covariance.json` top-level MC-stat variance is nonzero, `0.0029560843175981955`, at `analysis_note/results/expected_covariance.json:3`.
- The same file reports `per_systematic.mc_stat = 0.0` at `analysis_note/results/expected_covariance.json:37`; the detailed uncertainty row also has `variance_increment_over_stat = 0.0` at `analysis_note/results/expected_covariance.json:104`, while `variance_components.mc_stat` is nonzero at `analysis_note/results/expected_covariance.json:138`.
- The source cause is the per-systematic loop fitting `{syst}` with `include_staterror=False`, so `mc_stat` cannot contribute in that row: `phase4_inference/4a_expected/src/run_expected_inference.py:445`.

Impact: a note writer could quote either zero MC-stat as a per-systematic contribution or nonzero MC-stat as a variance component. The approximation may be defensible for expected Phase 4a if formally downscoped, but the current machine-readable output is internally contradictory and `COMMITMENTS.md` overclaims the implementation.

Required fix: make the covariance JSON internally consistent, either by moving MC stat out of `per_systematic` entirely or recording the nonzero value consistently, and update `COMMITMENTS.md` to say grouped approximation rather than bin-by-bin profiling unless the full staterror model is implemented.

### C1. `expected_m4l_final_state_templates` is cramped for a three-panel figure

Category: C

The figure is not a physics blocker, and the plot-validation summary passed after fixes, but the rendered image uses three independent panels in a single 10x10 canvas (`phase4_inference/4a_expected/src/make_expected_plots.py:109`). The labels and data are legible, but the panels are compressed and the y-axis typography dominates the content. If this figure goes into the AN, prefer three separate registered panels composed in LaTeX or a larger per-panel layout.

## Completion-Criteria Verdicts

- Expected results computed on MC/Asimov pseudo-data only: PASS. JSON states no observed Open Data counts are used (`analysis_note/results/expected_parameters.json:3`), and source template building excludes `is_data` in `event_group_templates`.
- All systematic variations with citations for variation size: FAIL. See A2.
- Closure test passes and ±20% corruption test fails: PASS. JSON gives corruption p-values `0.01934008970762087` and `3.1049330873040137e-18`, both below 0.05 (`analysis_note/results/expected_validation.json:97`).
- Precision comparison vs reference documented in validation JSON: PASS. `ratio_this_over_reference = 3.192990241669998`, `ratio_gt_5x = false` (`analysis_note/results/expected_validation.json:184`).
- Covariance matrices in results: PARTIAL/FAIL. Required files exist, but MC-stat covariance is internally inconsistent; see B1.
- All figures saved and registered in `FIGURES.json`: PASS. Independent smoke check: `entries 10 missing 0 empty 0 orphans 0`.
- `COMMITMENTS.md` updated: FAIL. It is updated, but it marks [D9], [SP2], and [SP3] resolved beyond the evidence currently on disk.
- Every finding has a Resolution + Evidence section: PARTIAL. The artifact has a findings table, but A1/A2/B1 above are unresolved.

## Open Questions / Assumptions

- MCP tools were disabled by toggles, so I did not call them. I did not perform new web literature checks because the blockers are internal traceability and implementation issues.
- `conventions/fitting.md` is absent; I used the Phase 4a template, Phase 2 strategy, `COMMITMENTS.md`, and methodology as the governing source.
- The expected `mu` numbers are internally consistent with JSON: `mu = 1.0 -0.51674064615437 +0.6327358408468291`, symmetric uncertainty `0.5747382435005995`.

## Residual Risks After Fixes

- Low-count final-state retention remains Phase-4a-only. The 4b/4c agents must repeat stability checks and merge/rebin if observed toys or fits become unstable.
- Asimov GoF `chi2=0, p=1` is correctly labeled as self-consistency only; it should not be promoted to independent validation in Doc 4a.
- The mass-profile result must remain method-parity or detector-level evidence unless the [D9] simultaneous category extraction is actually implemented and passes closure.
