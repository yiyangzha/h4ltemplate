# Per-Figure Validation

Figure: `m4l_fit_2e2mu`

Verdict: PASS

Checks:
- Stack/data readability: PASS. The stacked components, data markers, and error bars are distinguishable at render size.
- Pull panel: PASS. The pull points and zero line are visible, with readable tick labels and no clipping.
- Label compliance: PASS. Axis labels include units where applicable, and the experiment label is present in open-data style.
- No title-like text: PASS. There is no plot title; the visible CMS/open-data labeling is consistent with the plotting convention.
- Legend overlap: PASS. The legend sits in the upper-right open region and does not obscure the plotted content.
- Axis units: PASS. The main x-axis is labeled `m4l [GeV]`; the y-axis is labeled `Events`, and the pull panel is labeled `Pull`.
- Caption/metadata coherence: PASS. `FIGURES.json` entry `m4l_fit_2e2mu` describes a four-lepton mass distribution for the `2e2mu` category in `105 < m4l < 140 GeV`, matching the rendered figure.

Evidence:
- PNG inspected: `phase3_selection/outputs/figures/m4l_fit_2e2mu.png`
- Metadata inspected: `phase3_selection/outputs/FIGURES.json` entry `m4l_fit_2e2mu`
