# Per-Figure Validation: `m4l_fit_4mu`

- Session: `hana_d5d8`
- Commit under review: `34155e3`
- Figure: `phase3_selection/outputs/figures/m4l_fit_4mu.png`
- Metadata source: `phase3_selection/outputs/FIGURES.json`

## Verdict: FAIL

The figure is broadly readable and the axis/unit labeling is correct, but the rendered layout has a label collision risk in the upper-right region: the experiment label text (`Open Data and Open Simulation`) runs into the space occupied by the legend, so the branding text is partially crowded/obscured by the legend block. That fails the plot-validator overlap/readability check for a publication figure.

## Checks

- Stack/data readability: PASS. The stacked components and the data points are visible and distinguishable in the main panel.
- Pull panel readability: PASS. The residual/pull points and zero line are visible, and the panel is legible.
- Label compliance: PASS. Axis labels are publication-style and the x-axis includes units (`m4l [GeV]`).
- No title-like text: PASS. There is no explicit plot title; the top text is experiment/luminosity labeling.
- Legend overlap: FAIL. The legend occupies the same upper-right region as the experiment label text, creating visual crowding/overlap risk.
- Axis units: PASS. The x-axis has `GeV`; the y-axis uses event counts, which is appropriate here.
- Caption/metadata coherence: PASS. `FIGURES.json` describes a four-lepton mass distribution for the `4mu` final-state category in the fit window, which matches the rendered figure.

## Notes

- The figure otherwise appears consistent with the expected `m4l_fit_4mu` content.
- The issue is layout-level and should be fixed by moving either the legend or the experiment label to preserve clear separation.
