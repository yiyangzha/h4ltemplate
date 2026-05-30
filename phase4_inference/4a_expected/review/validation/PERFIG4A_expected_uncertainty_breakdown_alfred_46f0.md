# Per-figure validation: expected_uncertainty_breakdown

- Session: `alfred_46f0`
- Figure: `phase4_inference/4a_expected/outputs/figures/expected_uncertainty_breakdown.png`
- Registry entry: `phase4_inference/4a_expected/outputs/FIGURES.json`

## Verdict

PASS

## Checks

- Caption / metadata coherence: PASS. The registry caption states that this is the expected uncertainty breakdown for the Phase 4a Asimov signal-strength fit, derived from the stat-only, MC-stat, and full nuisance fits. The PNG shows the same four components on the y-axis (`Stat`, `MC stat`, `Syst total`, `Total`) with the expected uncertainty on `mu` on the x-axis.
- Legend completeness: PASS. No legend is needed for this single-series figure; the category labels on the y-axis fully identify the points.
- Label quality: PASS. Axis labels and experiment labeling are publication-quality and readable. The CMS / Open Simulation label and `13 TeV` tag are present and do not collide with the data points.
- Number consistency: PASS. The plotted x-values are consistent with the registry metadata once interpreted as variances from `expected_covariance.json`: `sqrt(0.30636894) = 0.5535`, `sqrt(0.00295608) = 0.0544`, `sqrt(0.02395511) = 0.1548`, and `sqrt(0.33032405) = 0.5747`, matching the four marker positions in the PNG.
- Physics sanity: PASS. The hierarchy is sensible: the total uncertainty is largest, the statistical component dominates, MC-stat is tiny, and the systematic contribution sits between them. Nothing looks unphysical or inverted.
- Visual quality: PASS. All text is legible, the markers are visible, axes are not clipped, and there is no overlap or spurious annotation artifact.

## Notes

The x-axis is dimensionless because it reports the uncertainty on the signal-strength parameter `mu`.
