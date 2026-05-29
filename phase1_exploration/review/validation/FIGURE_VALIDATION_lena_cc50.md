# Figure Validation: `phase1_eta4l_small_slice_shapes`

- Session: `lena_cc50`
- PNG: `phase1_exploration/outputs/figures/eta4l_small_slice_shapes.png`

## Verdict

PASS

## Evidence

- The figure renders cleanly at `1763 x 1824` pixels and is effectively square, which fits the small-slice comparison layout.
- All visible text is legible at rendered size: the CMS open-data/simulation label, the `13 TeV, small slices` annotation, axis tick labels, and legend entries are readable.
- The experiment label is present and correctly placed on the main panel: `CMS Open Data+Sim`.
- The x-axis label is appropriate for the observable and does not require units: `\eta_{4\ell}`.
- The regenerated y-axis label is the correct unitless-density form: `(1/N) dN/d\eta_{4\ell}`.
- The legend is complete for the plotted series: background ZZ, background ggZZ, background reducible, background top, data, signal VBF, signal VH, and signal ggH.
- The legend sits in an open region of the plot and does not overlap the points or error bars.
- There are no visible text collisions, clipped labels, or spurious artifacts.
- The plot does not appear misleading: the caption’s caution that this is reconnaissance-only, not yield validation, matches the visual presentation of the overlaid normalized shapes.
- Refreshed by fixer session `petra_11e2` after regenerating the figure with a density-form y-axis label.
