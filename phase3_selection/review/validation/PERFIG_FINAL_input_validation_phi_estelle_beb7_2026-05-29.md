# Per-Figure Validation: `input_validation_phi`

- Session: `estelle_beb7`
- Commit: `0bf8908`
- Figure: `phase3_selection/outputs/figures/input_validation_phi.png`
- Metadata source: `phase3_selection/outputs/FIGURES.json`

## Verdict

PASS

## Checks

- Visual quality: PASS. The figure is sharp, legible, and balanced at rendered size.
- Caption coherence: PASS. The plot content matches the metadata description of the `$\Phi$ [rad]` input-validation distribution in the broad `70 <= m4l <= 170 GeV` window.
- Legend completeness: PASS. Both entries are present: `MC prediction` and `Data`.
- Labels and units: PASS. The x-axis is labeled `$\Phi$ [rad]`; the main panel y-axis is `Events`; the pull panel is labeled `Pull`.
- CMS/open-data/open-simulation label compliance: PASS. The figure shows `CMS` with `Open Data and Open Simulation`, consistent with the project rules.
- No title-like broad/fit-window top text: PASS. The top-right `13 TeV, 10 fb$^{-1}$` label is a standard experiment annotation, not a plot title.
- Overlap/clipping: PASS. No visible overlap between legend, labels, data points, or panel elements; nothing is clipped.
- Ranges: PASS. The data and MC occupy the available range well; the pull panel is centered on zero with reasonable bounds.
- Error bars/pulls: PASS. Data error bars and pull uncertainties are present and visually consistent with the binned comparison.
- Number consistency: PASS. The plotted shape is consistent with the metadata values `chi2 = 3.9012194562542204`, `ndf = 5`, `p = 0.5637239206342102`, i.e. `chi2/ndf = 0.780243891250844`.

## Notes

No fixes required.
