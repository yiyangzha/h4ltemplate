# Per-figure validation: input_validation_cos_theta2

Verdict: FAIL

Source metadata checked: `phase3_selection/outputs/FIGURES.json` entry `input_validation_cos_theta2`

Checklist assessment:
- Visual quality: PASS. The figure is clean, readable, and the ratio panel is legible.
- Caption-figure coherence: PASS. The rendered content matches the captioned observable `cos_theta2` in the broad `70 <= m4l <= 170 GeV` window.
- Legend completeness: PASS. Both `MC prediction` and `Data` are present.
- Labels/units: PASS with one exception below. The x-axis label `cos θ2` is present; the y-axis uses `Events`, which is appropriate for counts.
- Experiment label: PASS. `CMS` is visible on the main panel only.
- Text overlap/clipping: PASS. No obvious overlap or clipped annotations are visible.
- Axis ranges: PASS. The data and MC occupy the plotted range without obvious truncation.
- Error bars/pulls: PASS. Error bars and pull values are visible and qualitatively sensible.
- Number consistency between caption/metadata and figure: PASS. The figure structure is consistent with the metadata entry.

Failure reason:
- `input_validation_cos_theta2.png`: the experiment label text is `Open Data+Sim`, which does not follow the required open-data/open-simulation wording in `methodology/appendix-plotting.md`. For this project, open-data plots must use `Open Data` and open-simulation plots must use `Open Simulation`; a combined `Open Data+Sim` label is nonconforming and should be replaced with publication-quality labeling that matches the plot content.

Exact fix instructions:
1. Change the left label to a conforming open-data/open-simulation phrase that matches the figure content, e.g. `Open Data` for data or `Open Simulation` for MC, or a clearly documented combined label if the analysis explicitly requires a mixed label.
2. Regenerate `phase3_selection/outputs/figures/input_validation_cos_theta2.png` and the matching PDF from the source plotting script.
3. Re-check the rendered PNG to confirm the updated label is visible, unclipped, and still does not overlap the legend.
