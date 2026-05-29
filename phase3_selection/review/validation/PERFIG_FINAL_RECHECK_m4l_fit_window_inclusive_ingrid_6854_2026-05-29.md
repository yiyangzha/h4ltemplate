# Per-Figure Final Recheck

Figure: `m4l_fit_window_inclusive`

Verdict: PASS

Checks:

- Legend and experiment-label separation: PASS. The legend sits on the right side of the main panel and does not overlap the `CMS Open Data and Open Simulation` label block in the upper left.
- No title-like text: PASS. There is no plot title; the only large header text is the experiment label and the integrated-luminosity annotation, both consistent with the plotting standard.
- Pull panel: PASS. The lower panel is present, labeled `Pull`, and the points and error bars are visible and aligned with the shared mass axis.
- Axis units: PASS. The x-axis is labeled `m4l [GeV]` and the main-panel y-axis is labeled `Events`, both with appropriate units/quantity labeling for this figure type.
- Caption coherence: PASS. The FIGURES.json entry describes an inclusive four-lepton mass distribution in the fit window with a lower pull panel, which matches the rendered figure.

Notes:

- The figure visually matches the `m4l_fit_window_inclusive` entry in `phase3_selection/outputs/FIGURES.json`.
- No label collisions, clipping, or panel-layout regressions are visible after the mass-legend commit `63227ca`.
