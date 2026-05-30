PASS

# Phase 4a Expected Inference Plot Validation

Session: `celeste_62e7`
Date: `2026-05-30`
Scope: `phase4_inference/4a_expected`
Reference commit: `ddcf18e`

## Final verdict

`PASS`

The Phase 4a expected figure set passes the blocking plot-validation gate after
the `ddcf18e` fix commit. `pixi run lint-plots` passes, the figure registry
smoke test is clean, the plotting source follows the required mechanical
patterns, and direct inspection of every registered PNG finds no remaining
blocking readability, overlap, clipping, or labeling defect.

## Command evidence

1. `pixi run lint-plots`
   - Result: `PASS`
   - Exact output:
     - `Pixi task (lint-plots): python conventions/lint_plots.py .`
     - `No plotting violations found in 25 file(s).`

2. Registry / file smoke test
   - `FIGURES.json` entries: `10`
   - Registered files: `20` (`10` PNG + `10` PDF)
   - Missing files: `0`
   - Zero-byte files: `0`
   - Orphan PNG/PDF files in `outputs/figures/`: `0`
   - Stale registered PNG/PDF relative to `make_expected_plots.py`: `0`
   - `make_expected_plots.py` mtime ns: `1780108482933928243`
   - `FIGURES.json` mtime ns: `1780108571975291249`

3. Mechanical source checks
   - Positive pattern evidence from [make_expected_plots.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase4_inference/4a_expected/src/make_expected_plots.py:32):
     - `mh.style.use("CMS")` at line `32`
     - PDF/PNG save with `bbox_inches="tight"` and `plt.close(fig)` at lines `74-76`
     - ratio-style multi-panel spacing `fig.subplots_adjust(hspace=0)` at line `118`
     - `mh.label.exp_label(...)` on the repaired multi-panel final-state template figure at lines `129-137`
     - repaired `expected_mu_profile_scan` legend placement and label at lines `155-163`
   - Negative grep checks found no forbidden `set_title(`, `tight_layout`,
     `constrained_layout`, `plt.colorbar`, `fig.colorbar(..., ax=...)`,
     numeric `fontsize=`, `data=False`, or derived-quantity `.view()[:] =`
     error-bar trap patterns in `phase4_inference/4a_expected/src/`.

## Focused fix verification

1. `expected_m4l_final_state_templates`
   - Prior issue: missing `exp_label` on lower independent panels.
   - Source evidence: [make_expected_plots.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase4_inference/4a_expected/src/make_expected_plots.py:117) builds the three-panel figure and applies `mh.label.exp_label(...)` inside the per-channel loop at lines `129-137`.
   - Visual result: all three panels now show `CMS Open Simulation (<channel>)`; legend remains confined to the top panel and does not obscure points.
   - Verdict: `FIXED`

2. `expected_mu_profile_scan`
   - Prior issue: legend overlapped the rising high-`mu` tail.
   - Source evidence: [make_expected_plots.py](/sandbox/work/jfc/analyses/higgs_4lep_mass/phase4_inference/4a_expected/src/make_expected_plots.py:154) places the legend at `loc="upper center"` at line `161`, then applies `safe_mpl_magic(ax)` and the standard experiment label.
   - Visual result: the legend sits in empty top whitespace; the right-hand profile tail is unobscured.
   - Verdict: `FIXED`

## Per-figure visual inspection

Every registered PNG in `phase4_inference/4a_expected/outputs/figures/` was
inspected directly.

1. `expected_m4l_final_state_templates` — `PASS`
   - Three independent panels are labeled correctly (`4mu`, `4e`, `2e2mu`).
   - No legend/data overlap; x-axis and y-axis text remain legible.

2. `expected_mu_profile_scan` — `PASS`
   - The legend no longer overlaps the profile curve.
   - `1 sigma` and `2 sigma` guide lines are readable and do not collide with the label block.

3. `expected_nuisance_impacts` — `PASS`
   - Label text is readable and uses publication-quality names.
   - Marker placement is clear; no clipping or offset-text artifact.

4. `expected_uncertainty_breakdown` — `PASS`
   - Sparse point layout is readable and uncluttered.
   - Axis labels and category labels are legible with no collision.

5. `expected_signal_injection_recovery` — `PASS`
   - Legend sits in empty space and the exact-recovery diagonal remains visible.
   - All four injection points are readable and consistent with the registry metadata.

6. `expected_low_count_validation` — `PASS`
   - Log-scale x-axis is readable; threshold marker at `p = 0.05` is visible.
   - No overlap between the lower-right legend and plotted points.

7. `expected_binning_stability` — `PASS`
   - Left padding fix holds: long y-axis labels are readable and no longer clipped.
   - The x-range leaves enough space around the points for easy comparison.

8. `expected_binning_low_count_summary` — `PASS`
   - Long y-axis labels remain readable.
   - The nominal low-count point and three zero-count points are clearly separated.

9. `expected_mass_profile_attempt` — `PASS`
   - Legend sits in empty upper-right space.
   - Mass-hypothesis axis labels are readable and the minimum is visually clear.

10. `expected_reference_comparison` — `PASS`
    - Publication-quality labels and the scope clarification `Open Simulation and public references` are present.
    - Reference intervals, the SM expectation line, and the large uncertainty on the expected result remain readable without a blocking collision.

## Conclusion

The current Phase 4a expected figure batch passes both the mechanical and
visual validation checks. No Category A or B plotting issue remains open in
this review cycle.
