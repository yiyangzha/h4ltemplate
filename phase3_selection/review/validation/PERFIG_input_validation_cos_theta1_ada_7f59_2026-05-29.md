# Per-figure validation: `input_validation_cos_theta1`

PASS

## Checks

- Visual quality: pass. The main panel and pull panel are both readable at rendered size, with no obvious text collisions or clipped tick labels.
- Caption-figure coherence: pass. The figure shows the broad-window `cos(theta_1)` input-validation comparison with a ratio/pull panel, matching the caption and metadata description.
- Legend completeness: pass. The legend identifies both MC prediction and Data.
- Labels and units: pass. The x-axis is labeled `cos theta_1`; the y-axis is `Events`; the pull panel is labeled `Pull`.
- Experiment label: pass. The figure includes the CMS/open-data label in the main panel only, and it is not repeated on the pull panel.
- Text overlap/clipping: pass. No visible overlap between legend, experiment label, title, or plot content. The title sits close to the top edge but is still legible and not visibly clipped.
- Axis ranges: pass. The main panel range covers the populated bins tightly without excessive whitespace; the pull panel spans the observed residuals cleanly around zero.
- Error bars/pulls: pass. Data error bars and pull points are visually consistent with the event counts and the stated chi2/ndf = 1.6001492260113015 / 5.
- Number consistency: pass. The visible comparison and pull pattern are consistent with the metadata values `chi2 = 8.000746130056507`, `ndf = 5`, `p = 0.15619451168087164`, and the caption statement that the D7 shape gate fails.

## Verdict

PASS. No fix required.
