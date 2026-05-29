# Figure Validation: `phase1_leading_lepton_pt_small_slice_shapes`

- Session: `magnus_b4f3`
- PNG: `phase1_exploration/outputs/figures/leading_lepton_pt_small_slice_shapes.png`
- Rendered size: `1830 x 1829`
- Result: PASS

## Evidence

- The plot renders cleanly at near-square size, which matches the intended single-panel comparison layout.
- Axis labels are legible and use appropriate units: `Leading lepton p_T [GeV]` on x and the density label `(1/N) dN/dp_T^lead [GeV^{-1}]` on y.
- The CMS open-data/simulation experiment label is present and readable at the top left, with the energy note `13 TeV, small slices` placed cleanly at the top right.
- The legend is complete for the plotted series: background ZZ, background ggZZ, background reducible, background top, data, signal VBF, signal VH, and signal ggH.
- Legend placement is acceptable for this peaked distribution; it sits in an essentially empty upper-right region and does not visibly cover data points or error bars.
- Tick labels are readable, the plot is not clipped, and there are no visible text collisions or spurious artifacts.
- The caption intent matches the render: a Phase 1 shape-reconnaissance comparison with area-normalized small slices, explicitly not a yield-validation plot.

## Notes

- The many overlaid error-bar series are visually busy, but still readable; no series appears to have malformed or suspiciously uniform error bars.
- Refreshed by fixer session `petra_11e2` after regenerating the figure with a density-form y-axis label.
