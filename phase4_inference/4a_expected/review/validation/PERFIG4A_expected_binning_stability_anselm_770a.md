# Per-figure validation: `expected_binning_stability`

Session: `anselm_770a`

Verdict: **FAIL**

## What I checked

- Read `agents/plot_validator.md`
- Read `methodology/appendix-plotting.md`
- Read `phase4_inference/4a_expected/outputs/FIGURES.json`
- Inspected `phase4_inference/4a_expected/outputs/figures/expected_binning_stability.png`

## Assessment

The figure is broadly coherent with its metadata:

- The four plotted configurations match the four rows in `FIGURES.json`:
  - `final_state_nominal` at `mu_uncertainty = 0.5723579328235826`
  - `inclusive_nominal` at `mu_uncertainty = 0.5754539025760244`
  - `inclusive_coarse` at `mu_uncertainty = 0.5867959543075851`
  - `inclusive_peak_side` at `mu_uncertainty = 0.5895033645790071`
- The plot content is physics-sane for an Asimov stability comparison:
  - uncertainties are tightly clustered
  - the ordering is plausible
  - the figure shows no suspicious overlap or spurious annotations
- The `CMS Open Simulation` label is present and legible.

## Failure

The x-axis label is **clipped at the right edge** of the rendered PNG. The label text is visibly truncated, so the figure fails the readability/layout requirement.

This is a publication-quality issue because the axis label is part of the figure’s scientific meaning. It is not acceptable to leave it partially cut off in the rendered output.

## Concrete fix instructions

1. Reduce the x-axis label length or rephrase it so it fits cleanly within the rendered canvas.
2. If the label must stay long, adjust the figure layout so the full label renders inside the image bounds.
3. Re-render the PNG and confirm that the entire x-axis label is visible with no cropping at the right edge.

## Result

**FAIL** until the clipped axis label is fixed and the figure is regenerated.
