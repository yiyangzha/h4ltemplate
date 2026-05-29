# Per-figure validation: `m4l_fit_4e`

**Result:** PASS

**Figure:** `phase3_selection/outputs/figures/m4l_fit_4e.png`

Checks against `TOGGLES.md`, `agents/plot_validator.md`, `methodology/appendix-plotting.md`, and `phase3_selection/outputs/FIGURES.json`:

- Stack/data readability: PASS. The main stacked distribution and the pull panel are both legible at rendered size.
- Pull panel: PASS. The pull points and error bars are visible, centered near zero, and do not look saturated or clipped.
- Label compliance: PASS. Axis labels are present with units on `m_{4\ell} [GeV]`; the y-axis is labeled `Events` and the pull panel is labeled `Pull`.
- No title-like text: PASS. There is no plot title inside the axes region.
- Legend overlap: PASS. The legend sits in open space at upper right and does not overlap the data or error bars.
- Axis units: PASS. The x-axis unit is explicit in GeV; the pull panel does not require a unit annotation.
- Caption/metadata coherence: PASS. The rendered content matches the registry entry for the `m4l_fit_4e` fit-window category, with the expected CMS open-data/open-simulation styling and the 4e final-state mass distribution.

No blocking visual or metadata issues were found in this figure.
