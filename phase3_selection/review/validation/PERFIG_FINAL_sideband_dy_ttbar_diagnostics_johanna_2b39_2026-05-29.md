# Per-Figure Validation

Session: `johanna_2b39`  
Phase: 3 selection  
Figure: `sideband_dy_ttbar_diagnostics`  
Commit: `63227ca`  
Date: 2026-05-29

## Verdict

PASS

## Checks

- Readability: PASS. Axis labels, tick labels, legend text, and CMS/Open Simulation labels are legible at rendered size.
- Labels: PASS. The plot labels the y-axis as `Expected events` and the x-axis regions as `Low sideband`, `Signal window`, and `High sideband`, which matches the diagnostic content.
- Legend: PASS. `DYJetsToLL` and `TTBar` are clearly distinguished and the legend does not overlap the data.
- Caption/metadata coherence: PASS. The registry entry describes the same sideband diagnostic and reports TTBar/DY ratios of 0.0954, 0.0444, and 0.1635 with `promote_ttbar_to_nominal: false`; the rendered figure shows DYJetsToLL dominating TTBar in all three regions, consistent with that metadata and caption.
- TTBar/DY ratio presentation: PASS. The figure presents the expected-event comparison in a way that supports the ratio statement in the registry entry: TTBar is visibly below DYJetsToLL in the low sideband, signal window, and high sideband, with the signal window especially suppressed.

## Notes

- The figure is visually clean, with no clipping, overlap, or unreadable annotations.
- No file modifications were made other than this validation record.
