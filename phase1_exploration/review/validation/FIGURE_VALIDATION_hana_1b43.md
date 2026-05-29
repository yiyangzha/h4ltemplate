# Figure Validation: `phase1_m4l_small_slice_shapes`

- PNG: `phase1_exploration/outputs/figures/m4l_small_slice_shapes.png`
- Result: PASS

## Evidence

- The figure is readable at rendered size: axis labels, tick labels, and legend text are all legible.
- The experiment label is present and correctly placed: `CMS Open Data+Sim` on the main panel.
- The x-axis label includes units: `$m_{4\ell}$ [GeV]`.
- The regenerated y-axis label is the correct density form: `(1/N) dN/dm_{4\ell} [GeV^{-1}]`.
- The figure matches the caption intent: it is a small-slice, area-normalized shape comparison with multiple physics categories overlaid for reconnaissance.
- The legend is complete for the plotted series: background ZZ, background ggZZ, background reducible, background top, data, signal VBF, signal VH, and signal ggH.
- No visible text-text collisions, clipped labels, or legend/data overlaps are present.
- The plot is effectively square in the rendered file (`1797 x 1829`), which is appropriate for the layout.
- Error bars appear visually reasonable for sparse small-slice distributions and do not look like a uniform or malformed artifact.

## Notes

- Refreshed by fixer session `petra_11e2` after regenerating the figure with a density-form y-axis label.
