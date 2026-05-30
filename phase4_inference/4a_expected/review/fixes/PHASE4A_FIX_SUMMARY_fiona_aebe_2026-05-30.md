# Phase 4a Fix Summary

Session: `fiona_aebe`
Date: 2026-05-30

## Review Finding Map

### A1. D9 mass-extraction traceability

Resolution: implemented the required final-state simultaneous category
shifted-template mass scan instead of the previous inclusive scan.

Evidence:
- `analysis_note/results/expected_mass_scan.json` now reports method
  `simultaneous final-state category shifted-template mass-profile closure
  with mu profiled in each shifted-template fit`.
- The JSON records categories `4mu`, `4e`, `2e2mu`, profiled parameter `mu`,
  the active Phase 4a nuisance set, and the template-shift procedure.
- Injected-mass closure still passes for 124, 125, and 126 GeV with zero grid
  bias in this shifted-template closure.
- `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` and
  `COMMITMENTS.md` now describe the category-simultaneous implementation and
  its official-quality mass-measurement limitation.

### A2. Systematic variation-size evidence/completeness

Resolution: added a machine-readable systematic-source evidence table and
propagated it into the artifact.

Evidence:
- Added `analysis_note/results/systematics_sources.json`, duplicated in
  `expected_systematics.json` for the note-writer discovery path.
- The table has 14 rows and includes SP2 `prompt_effective_xsecs` and SP6
  `pileup_pv_modeling`.
- Each row contains source/commitment label, variation or nominal-size basis,
  citation/search trail, fallback flag, affected templates/processes,
  evaluation method, and Phase 4a status.
- Fallback priors for signal theory 5%, qqZZ 10%, ggZZ 20%, and DY 50% are
  explicitly flagged as expected-phase fallback/user-provided approximations,
  not external precision calibrations.
- `COMMITMENTS.md`, `INFERENCE_EXPECTED.md`, and `experiment_log.md` were
  regenerated/updated consistently.

### B1. MC-stat consistency

Resolution: kept the actual grouped MC-stat approximation and made the
machine-readable covariance representation internally consistent.

Evidence:
- `analysis_note/results/expected_covariance.json` now records
  `mc_stat_treatment = group_category_normsys_from_sumw2`.
- `mc_stat`, `per_systematic.mc_stat`, and
  `uncertainty_breakdown.variance_components.mc_stat` all report the same
  nonzero variance, `0.0029560843175981955`.
- `COMMITMENTS.md` now states the grouped approximation and no longer claims
  full bin-by-bin `staterror` profiling for Phase 4a.

### Plot Validator A/B Findings

Resolution: fixed the standards and overlap issues, then regenerated the full
Phase 4a expected figure set.

Evidence:
- `expected_m4l_final_state_templates` now uses
  `mh.label.exp_label(...)` on all three independent final-state panels.
- The final-state template figure retains a non-overlapping legend and the
  plotting source calls the `mpl_magic` autoscaling helper through
  `safe_mpl_magic`.
- `expected_mu_profile_scan` legend moved to upper center, away from the
  high-`mu` tail.
- The full figure registry was regenerated: 10 entries, 20 registered PNG/PDF
  files, no missing/empty/orphan/stale files.
- I visually inspected
  `outputs/figures/expected_m4l_final_state_templates.png` and
  `outputs/figures/expected_mu_profile_scan.png` after regeneration.

## Failed Attempts During Fixing

1. First `pixi run p4a-all` attempt after code edits:
   - Fit/JSON generation completed.
   - Plotting failed on `expected_signal_injection_recovery` because
     `mpl_magic` could not fit the lower-right legend after two scaling
     iterations.
   - Fix: moved that legend to upper center and used non-fatal autoscaling.

2. Second `pixi run p4a-all` attempt:
   - Fit/JSON generation completed.
   - Plotting failed on `expected_low_count_validation` because `mpl_magic`
     hit a Matplotlib log-scale transform error.
   - Fix: added `safe_mpl_magic` wrapper for legend-bearing plots.

3. Final `pixi run p4a-all` attempt:
   - Completed successfully.

## Verification

- `pixi run p4a-all`: PASS.
- `pixi run lint-plots`: PASS, exact result `No plotting violations found in
  25 file(s).`
- Figure registry smoke test: PASS,
  `entries=10 registered_files=20 missing=0 empty=0 orphans=0 stale=0`.
- JSON sanity check: PASS,
  category-simultaneous mass method present; categories are `4mu`, `4e`,
  `2e2mu`; mass closure passes; MC-stat covariance entries agree; SP2 and SP6
  rows present in `systematics_sources.json`.
- Output file listing: all expected result JSON, artifact, registry, and 20
  figure files have May 30 02:36 mtimes and nonzero sizes.

## Remaining Open Issues

- Full bin-by-bin HistFactory `staterror` profiling remains a documented
  Phase 4a downscope; the implemented treatment is the grouped
  group/category approximation from Phase 3 `sumw2`.
- The mass scan is category-simultaneous and passes shifted-template closure,
  but it remains detector-level method-parity evidence rather than an
  official-quality CMS mass measurement because independent mass-hypothesis MC
  and official calibration inputs are unavailable.
