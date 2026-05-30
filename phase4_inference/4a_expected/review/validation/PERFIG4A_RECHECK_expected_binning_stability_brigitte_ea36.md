# Per-figure revalidation: `expected_binning_stability`

Session: `brigitte_ea36`

Verdict: **PASS**

## What I checked

- Read `phase4_inference/4a_expected/review/validation/PERFIG4A_expected_binning_stability_anselm_770a.md`
- Read `phase4_inference/4a_expected/outputs/FIGURES.json`
- Inspected `phase4_inference/4a_expected/outputs/figures/expected_binning_stability.png`
- Consulted `agents/plot_validator.md` for the visual readability requirements

## Assessment

The rendered figure is coherent with its metadata:

- `FIGURES.json` lists the figure as `expected_binning_stability`
- The metadata rows match the rendered four-point comparison:
  - `final_state_nominal` with `mu_uncertainty = 0.5723579328235826`
  - `inclusive_nominal` with `mu_uncertainty = 0.5754539025760244`
  - `inclusive_coarse` with `mu_uncertainty = 0.5867959543075851`
  - `inclusive_peak_side` with `mu_uncertainty = 0.5895033645790071`
- The figure caption/description in `FIGURES.json` matches the plot content: an alternative-binning stability comparison for the expected signal-strength fit

## Recheck result

The previous failure is fixed.

The x-axis label is now fully visible in the rendered PNG. In the current image, the label reads cleanly as `Expected mu uncertainty` with no truncation at the right edge, and the text sits inside the canvas bounds rather than being cut off.

## Basic readability check

- Axis label text is legible
- The plotted markers are not obscured by any overlapping annotation
- The `CMS Open Simulation` label remains readable
- No new clipping or layout regressions are visible in the current render

## Result

**PASS**. The prior right-edge clipping issue is resolved, and the figure remains consistent with its registry metadata.
