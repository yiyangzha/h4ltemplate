# Per-Figure Validation: `input_validation_lead_abs_eta`

Verdict: PASS

Figure reviewed: `phase3_selection/outputs/figures/input_validation_lead_abs_eta.png`

Caption / metadata used:
- Caption: Leading lepton `$|\eta|$` input-validation distribution in the broad `70 <= m4l <= 170 GeV` window. D7 shape gate passes with `chi2/ndf = 0.47344618565668173` and `p = 0.7552866554534795`; used only to decide classifier-input eligibility, not to normalize fit templates.
- Metadata: `chi2 = 1.893784742626727`, `ndf = 4`, `p_value = 0.7552866554534795`, `passes_d7_gate = true`, `shape_normalization_scale_data_over_mc = 0.968738179599649`, `variable = lead_abs_eta`

Checks:
- Visual quality: PASS. The plot is clean, rendered at normal size, and the two-panel layout is readable.
- Caption-figure coherence: PASS. The figure shows the lead-lepton `|\eta|` input-validation distribution in the broad mass window, matching the caption/metadata.
- Legend completeness: PASS. Legend entries for `MC prediction` and `Data` are present and legible.
- Labels / units: PASS. Axis labels are present and appropriate; `|\eta|` is dimensionless, so no unit label is needed on the x-axis.
- Experiment label: PASS. The figure includes the CMS/open-data branding and the `13 TeV, broad window` annotation.
- Text overlap / clipping: PASS. No visible text collisions, clipped tick labels, or panel-label artifacts.
- Axis ranges: PASS. The main panel and pull panel are appropriately scaled to the plotted content; no excessive whitespace or truncation is visible.
- Error bars / pulls: PASS. Data error bars and pull points are visible and of reasonable magnitude; the pull panel is centered near zero with no pathological behavior.
- Number consistency: PASS. The visible binning and the reported `chi2/ndf` and `p` are consistent with the metadata and caption. The visible data/MC shape agreement is compatible with the stated D7 gate pass.

No fixes required.
