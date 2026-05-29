# Per-figure Validation: `input_validation_cos_theta1`

- Session: `dagmar_732f`
- Date: `2026-05-29`
- Commit: `0bf8908`
- Verdict: PASS

Checked against:
- `TOGGLES.md`
- `agents/plot_validator.md`
- `methodology/appendix-plotting.md`
- `phase3_selection/outputs/FIGURES.json` entry for `input_validation_cos_theta1`
- `phase3_selection/outputs/figures/input_validation_cos_theta1.png`

Assessment:
- Visual quality is good at rendered size; text is legible and not clipped.
- Caption-figure coherence is good: the plot shows the `cos(theta_1)` input-validation comparison in the broad `70 <= m4l <= 170 GeV` window, with the pull panel included as described by the metadata.
- Legend is complete for the content shown: `MC prediction` and `Data` are both present and distinct.
- Labels and units are acceptable: x-axis is labeled `cos theta_1`, y-axis is `Events`, and the pull panel is labeled `Pull`.
- CMS/open-data/open-simulation labeling is compliant: the figure shows `CMS` with `Open Data and Open Simulation`, and the top-right luminosity/energy label is present.
- There is no title-like broad or fit-window text inside the plot area.
- No text overlap, clipping, or panel collision is visible.
- Axis ranges are appropriate: the data occupy the plot area well, and the pull panel is centered sensibly around zero.
- Error bars and pull values look reasonable for a binned comparison; nothing suggests an omitted-`yerr` trap.
- The visible shape is consistent with the registered metadata: `chi2 = 8.000746130056507`, `ndf = 5`, `p = 0.15619451168087164`, and `passes_d7_gate = false`.

Conclusion: this figure passes final Level 2 per-figure validation.
