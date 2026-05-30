ITERATE

# Phase 4a Expected Inference Plot Validation

Session: `sabine_b3c5`  
Date: `2026-05-30`  
Scope: `phase4_inference/4a_expected`

## Final verdict

`ITERATE`

Blocking issues remain in the current Phase 4a expected-figure batch. The
registry, stale-file, and orphan-file checks passed, and `pixi run lint-plots`
returned PASS, but the focused code/visual review still finds Category A
violations in the current rendered set.

## Command evidence

- `pixi run lint-plots`
  - Result: `PASS`
  - Exact output:
    - `Pixi task (lint-plots): python conventions/lint_plots.py .`
    - `No plotting violations found in 25 file(s).`
- Registry/file smoke test:
  - `FIGURES.json` entries: `10`
  - Registered files: `20` (`10` PNG + `10` PDF)
  - Missing files: `0`
  - Zero-byte files: `0`
  - Orphan PNG/PDF files in `outputs/figures/`: `0`
- Stale-file check:
  - Plot script mtime: `2026-05-30 02:02:44.315156773 +0000`
  - `FIGURES.json` mtime: `2026-05-30 02:06:08.777405836 +0000`
  - All registered PNG/PDF mtimes are later than `make_expected_plots.py`
  - Verdict: no stale registered figures relative to the relevant plotting script

## Code-lint findings

1. [make_expected_plots.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase4_inference/4a_expected/src/make_expected_plots.py:121)
   - Failed check: missing mandatory `mh.label.exp_label(...)` call in `plot_expected_m4l`; custom `add_text(...)` text is used instead.
   - Category: `A`
   - Suggested fix: replace the hand-built label block with `mh.label.exp_label(...)` and follow the appendix template.

2. [make_expected_plots.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase4_inference/4a_expected/src/make_expected_plots.py:109)
   - Failed check: multi-panel figure with independent axes does not label each panel; only the first axes gets a label block.
   - Category: `A`
   - Suggested fix: apply `mh.label.exp_label(...)` to each independent panel, or redesign the figure so the labeling rule is satisfied explicitly.

3. [make_expected_plots.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase4_inference/4a_expected/src/make_expected_plots.py:122)
   - Failed check: `ax.legend(loc="upper right")` used without `mpl_magic(ax)` in a populated distribution panel.
   - Category: `B`
   - Suggested fix: either call `mpl_magic(ax)` after plotting or move the legend to a demonstrably empty region.

4. [make_expected_plots.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase4_inference/4a_expected/src/make_expected_plots.py:146)
   - Failed check: `ax.legend(loc="upper right")` without `mpl_magic(ax)` on the profile-scan figure; this matches the rendered overlap noted below.
   - Category: `A`
   - Suggested fix: move the legend away from the rising high-`mu` tail or use a placement that leaves the profile curve unobscured.

## Per-figure visual inspection

Every registered PNG was inspected directly.

1. `expected_m4l_final_state_templates` — `VIOLATION`
   - Failed check: independent lower panels are unlabeled; the required experiment/open-simulation label appears only on the top panel.
   - Category: `A`
   - Suggested fix: apply `mh.label.exp_label(...)` on each independent axes in the three-panel layout.

2. `expected_mu_profile_scan` — `VIOLATION`
   - Failed check: legend overlaps the physics content in the upper-right corner; the rising high-`mu` profile tail runs into the legend region.
   - Category: `A`
   - Suggested fix: relocate the legend to unused space or replace it with direct line annotations outside the curve envelope.

3. `expected_nuisance_impacts` — `PASS`
   - Readable and internally consistent with the registry entry.

4. `expected_uncertainty_breakdown` — `PASS`
   - Readable and internally consistent with the registry entry.

5. `expected_signal_injection_recovery` — `PASS`
   - Readable; no overlap or clipping seen.

6. `expected_low_count_validation` — `PASS`
   - Readable; threshold line, points, and legend remain distinct.

7. `expected_binning_stability` — `PASS`
   - Rechecked specifically because it failed earlier. The previous x-axis clipping issue is resolved on the current render.

8. `expected_binning_low_count_summary` — `PASS`
   - Readable and consistent with the registry metadata.

9. `expected_mass_profile_attempt` — `PASS`
   - Readable; no blocking overlap or clipping seen.

10. `expected_reference_comparison` — `PASS`
   - Rechecked specifically because it failed earlier. The publication-grade labels and reference-scope clarification are present on the current render.

## Residual notes

- The two previously fixed figures, `expected_binning_stability` and
  `expected_reference_comparison`, remain fixed on the current rendered batch.
- The repo-wide plotting linter did not flag the `plot_expected_m4l` labeling
  issue, so this needs to be handled in the executor fix cycle rather than
  assumed covered by `lint-plots`.

## Blocking summary

This review does **not** pass the Phase 4a blocking plot-validation gate yet.
The required next step is a focused rerender after:

1. replacing the custom label block in `expected_m4l_final_state_templates`
   with standards-compliant `exp_label` usage on each independent panel, and
2. moving the `expected_mu_profile_scan` legend so it no longer obscures the
   profile curve.
