# Per-Figure Final Recheck: `m4l_broad_window_inclusive`

- Session: `hugo_97f3`
- Date: `2026-05-29`
- Figure: `phase3_selection/outputs/figures/m4l_broad_window_inclusive.png`
- Matching metadata: `phase3_selection/outputs/FIGURES.json`

## Verdict

PASS

## Evidence

- Legend and experiment-label separation is clean: the `CMS` open-data label sits in the upper-left annotation area, while the legend is placed on the right and does not collide with the data or the exp label.
- No title-like text is present on the figure. There is no plot title, only the experiment label, luminosity/energy annotation, axis labels, legend, and the pull-panel label.
- The pull panel is present and readable. The zero line is visible, the points have sensible uncertainties, and there is no visible gap or panel overlap problem.
- Axis units are correct and visible: the x-axis is labeled `m4l [GeV]`, and the y-axis labels are `Events` for the main panel and `Pull` for the lower panel.
- Caption coherence is good. The FIGURES.json caption matches the rendered figure: inclusive four-lepton mass distribution in the broad validation window, with MC normalization and pull-panel description consistent with the image.

## Notes

- The legend entries are publication-quality and readable.
- The figure layout remains stable after the mass-legend commit `63227ca`.
