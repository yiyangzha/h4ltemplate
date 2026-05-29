# Per-Figure Validation: `input_validation_cos_theta2`

Result: **PASS**

Checked figure: `phase3_selection/outputs/figures/input_validation_cos_theta2.png`

Metadata source: `phase3_selection/outputs/FIGURES.json` entry `input_validation_cos_theta2`

## Checks

- Visual quality: PASS. The histogram and ratio panel are cleanly rendered, with no visible clipping or layout collapse.
- Caption-figure coherence: PASS. The plot matches an input-validation distribution for `\cos\theta_2` in the broad `70 <= m4l <= 170 GeV` window, with a pull panel as described in the metadata.
- Legend completeness: PASS. Both `MC prediction` and `Data` are present.
- Labels/units: PASS. The x-axis is labeled `cos \theta_2`, the y-axis is `Events`, and the pull panel is labeled `Pull`.
- CMS/open-data/open-simulation label compliance: PASS. The figure shows `CMS` and `Open Data and Open Simulation` in the expected style.
- No title-like broad/fit-window top text: PASS. No separate title appears; the only top text is the standard experiment/energy annotation.
- Text overlap/clipping: PASS. No visible overlaps between the CMS label, the open-data label, the energy annotation, or the legend.
- Axis ranges: PASS. The x-range covers the full `[-1, 1]` cosine domain, and the y-ranges are appropriate for the displayed yields and pulls.
- Error bars/pulls: PASS. The data points and pull panel both show sensible uncertainties; nothing suggests the sqrt(N) trap or missing pull uncertainties.
- Number consistency with metadata: PASS. The rendered figure is consistent with the metadata values `chi2 = 6.443113394442091`, `ndf = 5`, `p = 0.26545662085295785`, and `shape_normalization_scale_data_over_mc = 0.968714740485773`.

## Conclusion

The figure is suitable for review and needs no fix.
