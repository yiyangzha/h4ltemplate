# Per-Figure Validation: `input_validation_eta4l`

Session: `dorothea_9c83`
Date: 2026-05-29
Commit: `0bf8908`

Verdict: PASS

Checks performed against `TOGGLES.md`, `agents/plot_validator.md`, `methodology/appendix-plotting.md`, `phase3_selection/outputs/FIGURES.json`, and `phase3_selection/outputs/figures/input_validation_eta4l.png`.

Findings:
- Visual quality is good: the main panel and pull panel are clean, legible, and not clipped.
- Caption-figure coherence is good: the plot matches the metadata for the `eta4l` input-validation distribution in the broad `70 <= m4l <= 170 GeV` window.
- Legend is complete: MC prediction and Data are both present and clearly distinguished.
- Labels and units are appropriate: `Events`, `Pull`, and the dimensionless `n_{4\ell}` axis are readable and correctly styled.
- CMS/open-data/open-simulation labeling is compliant: the figure shows `CMS` with `Open Data and Open Simulation`, and the luminosity tag `13 TeV, 10 fb^{-1}` is present.
- No title-like broad/fit-window text appears as an on-plot title; the descriptive text is part of the experiment label block.
- No text overlap, clipping, or legend collision is visible.
- Axis ranges are appropriate: the data occupy the plotted range well, and the pull panel is centered near zero with no obvious saturation.
- Error bars and pull magnitudes are reasonable for the stated `chi2 = 2.019533351774123`, `ndf = 5`, and `p = 0.846435676737652` in `FIGURES.json`.
- Number consistency matches the metadata: the figure is consistent with a D7 gate failure (`passes_d7_gate = false`) and a shape-normalization scale of `1.021435872266085`.

No fixes required.
