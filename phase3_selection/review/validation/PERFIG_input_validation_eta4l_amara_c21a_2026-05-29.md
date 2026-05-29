# Per-Figure Plot Validation

Session: `amara_c21a`
Figure: `input_validation_eta4l`
Decision: **PASS**

## Scope

Validated only `phase3_selection/outputs/figures/input_validation_eta4l.png` against the corresponding entry in `phase3_selection/outputs/FIGURES.json`.

## Checks

- Visual quality: PASS. The figure is sharp, legible, and properly framed.
- Caption-figure coherence: PASS. The visible content matches the metadata description of the `eta_{4l}` input-validation distribution in the broad `70 <= m4l <= 170 GeV` window.
- Legend completeness: PASS. The legend contains both `MC prediction` and `Data`, and both correspond to visible plotted elements.
- Labels/units: PASS. `Events` and `Pull` are labeled clearly; `eta_{4l}` is presented as a dimensionless variable, so no unit label is needed.
- Experiment label: PASS. `CMS` branding is present on the main panel only, as expected for a ratio plot.
- Text overlap/clipping: PASS. No visible text collisions, clipping, or ratio-panel artifacts.
- Axis ranges: PASS. The displayed ranges encompass the data and MC without excessive wasted space.
- Error bars/pulls: PASS. Data error bars and pull values are visible and look numerically reasonable for the plotted counts.
- Number consistency: PASS. The visible event counts and pull pattern are consistent with the metadata values in `FIGURES.json` (`chi2 = 2.019533351774123`, `ndf = 5`, `p_value = 0.846435676737652`, `passes_d7_gate = false`).

## Notes

- The top-right annotation `13 TeV, broad window` is consistent with the figure description and does not interfere with readability.
- The plot uses `MC prediction` rather than a raw code identifier, which is appropriate.
