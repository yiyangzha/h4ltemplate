# Phase 4a Per-Figure Validation Summary

Date: 2026-05-30  
Scope: Level 2 VERIFY per-figure validation for `phase4_inference/4a_expected/outputs/FIGURES.json`

## Registry

- Final registry entries: 10
- Final registered files: 10 PNG + 10 PDF
- Final smoke test after plot refresh commit `5edd995`: no missing files, no zero-byte files, no orphan files, and no stale registered files relative to `phase4_inference/4a_expected/src/make_expected_plots.py`
- Final `pixi run lint-plots`: PASS, no plotting violations in 25 files

## Final Verdict

PASS after two scoped plot fixes.

All 10 Phase 4a expected-inference figures have final PASS evidence on the
current rendered image set. Two figures initially failed per-figure validation:

- `expected_binning_stability`: initial FAIL from `anselm_770a` because the
  x-axis label was clipped at the right edge. Fixed in commit `1213c39`
  (`fix: prevent Phase 4a binning plot label clipping`) and rechecked PASS by
  `brigitte_ea36`.
- `expected_reference_comparison`: initial FAIL from `cosima_6a51` because
  on-figure reference labels were not publication-grade and the `3.19`
  precision-ratio scope was not explicit. Fixed in commit `23f3001`
  (`fix: improve expected reference comparison labels`) and rechecked PASS by
  `dagmar_2a00`.

Because `23f3001` modified the shared plotting script while regenerating only
one target figure, a full Phase 4a figure refresh was required. Commit
`5edd995` (`fix: refresh phase 4a expected figures`) regenerated the full
figure set and verified no stale files remained.

## Final PASS Coverage

Final direct PASS reports:

- `expected_m4l_final_state_templates`:
  `PERFIG4A_expected_m4l_final_state_templates_ada_c6bf.md`
- `expected_mu_profile_scan`:
  `PERFIG4A_expected_mu_profile_scan_agnes_d754.md`
- `expected_nuisance_impacts`:
  `PERFIG4A_expected_nuisance_impacts_albert_5619.md`
- `expected_uncertainty_breakdown`:
  `PERFIG4A_expected_uncertainty_breakdown_alfred_46f0.md`
- `expected_signal_injection_recovery`:
  `PERFIG4A_expected_signal_injection_recovery_amara_cbb0.md`
- `expected_low_count_validation`:
  `PERFIG4A_expected_low_count_validation_andrzej_6b03.md`
- `expected_binning_low_count_summary`:
  `PERFIG4A_expected_binning_low_count_summary_basil_6cfb.md`
- `expected_mass_profile_attempt`:
  `PERFIG4A_expected_mass_profile_attempt_claude_41cd.md`

Final recheck PASS reports after fixes:

- `expected_binning_stability`:
  `PERFIG4A_RECHECK_expected_binning_stability_brigitte_ea36.md`
- `expected_reference_comparison`:
  `PERFIG4A_RECHECK_expected_reference_comparison_dagmar_2a00.md`

Superseded FAIL reports retained for audit:

- `PERFIG4A_expected_binning_stability_anselm_770a.md`
- `PERFIG4A_expected_reference_comparison_cosima_6a51.md`

## Notes For Blocking Review

- The watcher reports `PLOT_WATCHER_FEEDBACK_celeste_1743.md` and
  `PLOT_WATCHER_FEEDBACK_nora_2930.md` contain earlier no-figure or FAIL
  states. They are superseded by `PLOT_WATCHER_RECHECK_vera_ee63.md`, the
  focused per-figure rechecks listed above, and the final full plot refresh
  in commit `5edd995`.
- No per-figure validator reported unresolved physics-content failures after
  the two layout/label fixes.
