# Plot Validation: input_validation_cos_theta_star

Verdict: FAIL

Scope: exact one figure `phase3_selection/outputs/figures/input_validation_cos_theta_star.png`

Checks:
- Visual quality: PASS. The main distribution and ratio panel are clean, readable, and not clipped.
- Caption-figure coherence: PASS. The figure matches the captioned observable `\cos\theta^*` in the broad `70 <= m4l <= 170 GeV` window, and the visible ratio panel is consistent with the stated data/MC comparison.
- Legend completeness: PASS. Both `MC prediction` and `Data` are present.
- Labels/units: PASS. The x-axis label `cos θ*` is present; the figure is otherwise numerically consistent with a dimensionless angular observable.
- Experiment label: FAIL. The rendered label is `CMS Open Data+Sim`, which does not match the required open-data/open-simulation wording in the plotting standards. The project convention requires explicit `Open Data` or `Open Simulation`, not a combined `Data+Sim` label.
- Text overlap/clipping: PASS. No visible overlap or clipping.
- Axis ranges: PASS. The histogram and ratio panel ranges are sensible for the displayed content.
- Error bars/pulls: PASS. Data error bars and pull magnitudes look reasonable, with the ratio panel centered near zero except for the expected positive excursions in the last bins.
- Number consistency between caption/metadata and visible figure: PASS. The visible shape is consistent with the metadata values in `FIGURES.json` (`chi2/ndf = 1.007137...`, `p = 0.411540...`, `passes_d7_gate = false`).

Fix instructions:
1. Replace the experiment label `CMS Open Data+Sim` with the standards-compliant wording used elsewhere in the analysis, either `CMS Open Data` or `CMS Open Simulation` as appropriate for this figure.
2. Regenerate the PNG and keep the ratio-panel layout unchanged.
3. Re-run this figure through validation after the relabeling.
