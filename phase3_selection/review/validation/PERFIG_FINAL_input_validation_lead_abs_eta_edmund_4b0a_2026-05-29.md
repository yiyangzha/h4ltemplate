# Per-Figure Validation: `input_validation_lead_abs_eta`

- Session: `edmund_4b0a`
- Phase: 3 selection
- Figure: `phase3_selection/outputs/figures/input_validation_lead_abs_eta.png`
- Metadata source: `phase3_selection/outputs/FIGURES.json`

## Verdict

PASS

## Checks

- Visual quality: pass. The plot is clean, with no obvious overlap, clipping, or rendering artifacts.
- Caption-figure coherence: pass. The figure shows the requested leading lepton `|eta|` input-validation comparison, including the ratio/pull panel consistent with the captioned D7 gate context.
- Legend completeness: pass. Both MC prediction and Data are present and readable.
- Labels and units: pass. Axis labels are present and legible; `eta` is dimensionless, so no unit label is required on the x-axis.
- CMS / open-data / open-simulation compliance: pass. The figure carries the CMS label and the open data / open simulation labeling expected by the plotting standard.
- No title-like broad text: pass. There is no plot title or fit-window header inside the plotting area.
- Text overlap / clipping: pass. The annotations, legend, and axes do not collide, and no text is visibly clipped.
- Axis ranges: pass. The data populate the plotted range sensibly, and the pull panel is centered around zero with a reasonable scale.
- Error bars / pulls: pass. The error bars and pull values look consistent with a low-statistics binned comparison and do not show the sqrt(N) trap signature.
- Number consistency with metadata: pass. The figure content is consistent with the JSON metadata: `chi2 = 1.893784742626727`, `ndf = 4`, `p_value = 0.7552866554534795`, and `passes_d7_gate = true`. The five visible bins match the expected binning.

## Notes

No fix required.
