# Per-Figure Validation: `input_validation_cos_theta_star`

- Session: `dolores_58ad`
- Date: `2026-05-29`
- Phase: 3 selection, final Level 2 validation
- Artifact: `phase3_selection/outputs/figures/input_validation_cos_theta_star.png`
- Registry entry: `phase3_selection/outputs/FIGURES.json`

## Verdict

PASS

## Checks

- Visual quality: pass. The plot is legible at the rendered size, with no obvious clipping, overlap, or broken layout.
- Caption-figure coherence: pass. The figure matches the registry description of a broad `70 <= m4l <= 170 GeV` input-validation distribution for `cos_theta_star`.
- Legend completeness: pass. Both `MC prediction` and `Data` are shown.
- Labels and units: pass. The x-axis uses `cos theta*` notation and the y-axis is labeled `Events`; the figure also includes the standard CMS/open-data/open-simulation labeling.
- CMS/open-data/open-simulation compliance: pass. The figure shows `CMS` and `Open Data and Open Simulation`.
- No title-like broad/fit-window top text: pass. The upper-right `13 TeV, 10 fb^-1` annotation is standard experiment labeling, not a title.
- Text overlap / clipping: pass. No visible collisions between labels, legend, or axes text.
- Axis ranges: pass. The main panel and pull panel span the plotted content without obvious truncation.
- Error bars / pulls: pass. The pull panel is centered near zero with reasonable spread for a shape-comparison validation plot.
- Number consistency with metadata: pass. The registry reports `chi2 = 5.035685036829564`, `ndf = 5`, `p = 0.4115406899048306`, and `passes_d7_gate = false`; the figure is consistent with a non-pathological comparison and the displayed pull pattern.

## Notes

The figure is acceptable for publication-quality use in the Phase 3 selection review chain. No fix instructions are required.
