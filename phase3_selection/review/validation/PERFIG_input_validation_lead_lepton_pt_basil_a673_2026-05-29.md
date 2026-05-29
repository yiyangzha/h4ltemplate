# Per-figure validation: `input_validation_lead_lepton_pt`

FAIL

## Checks

- Visual quality: fail. The figure is readable overall, but the visible plot title is not allowed and crowds the top margin.
- Caption-figure coherence: pass. The main panel shows the broad-window leading-lepton $p_T$ input-validation comparison with a pull panel, matching the registered caption and description.
- Legend completeness: pass. The legend contains both `MC prediction` and `Data`.
- Labels and units: pass. The x-axis is labeled `Leading lepton pT [GeV]`, the main y-axis is `Events`, and the lower panel is labeled `Pull`.
- Experiment label: pass. The `CMS Open Data+Sim` label is present on the main panel only and is not repeated on the pull panel.
- Text overlap/clipping: fail. The top-right title `13 TeV, broad window` is visible on the figure; it should not be present on a publication figure and it sits uncomfortably close to the top edge.
- Axis ranges: pass. The main panel range covers the populated bins without obvious wasted space; the pull panel spans the residuals cleanly around zero.
- Error bars/pulls: pass. The data error bars and pull points look consistent with the plotted counts and the stated shape-gate result.
- Number consistency: pass. The visible shape agreement/disagreement is consistent with the metadata values `chi2 = 16.22546152010662`, `ndf = 4`, `p_value = 0.0027310794648283346`, and `shape_normalization_scale_data_over_mc = 0.9649147146827438`.

## Fix instructions

1. Remove the visible title text `13 TeV, broad window` from the figure generation code.
2. Re-render the PNG and ensure the top margin is clean with no clipped or crowded text.
3. Keep the CMS/Open Data+Sim label on the main panel only, and do not add any title back into the plot.

