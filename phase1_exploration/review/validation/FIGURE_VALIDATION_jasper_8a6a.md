# Figure Validation: phase1_pt4l_small_slice_shapes

- Figure: `phase1_exploration/outputs/figures/pt4l_small_slice_shapes.png`
- Verdict: PASS

## Evidence

- The plot is square and fully framed; no axes, labels, or legend entries are clipped.
- All visible text is legible at rendered size: the CMS label, top-right energy note, axis labels, tick labels, and legend entries are readable without zooming.
- The legend is complete for the visible series: background ZZ, background ggZZ, background reducible, background top, data, signal VBF, signal VH, and signal ggH.
- The legend sits in an otherwise empty upper-right region and does not overlap data points or error bars.
- Axis labeling is consistent with the caption:
  - x-axis: `$p_T^{4\ell}$ [GeV]`
  - y-axis: `(1/N) dN/dp_T^{4\ell} [GeV^{-1}]`
- The visible experiment label is present on the main panel only, with no ratio-panel artifact or spurious text.
- The shape comparison is visually coherent with the caption’s stated purpose: area-normalized Phase 1 reconnaissance, not yield validation.

## Notes

- Refreshed by fixer session `petra_11e2` after regenerating the figure with a density-form y-axis label.
