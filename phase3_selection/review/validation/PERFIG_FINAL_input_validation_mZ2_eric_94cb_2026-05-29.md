# Per-Figure Final Validation: `input_validation_mZ2`

Session: `eric_94cb`
Date: 2026-05-29
Commit: `0bf8908`

Verdict: PASS

Checks performed:
- Visual quality: PASS. The histogram and pull panel are cleanly rendered, text is legible, and there is no clipping or visible overlap.
- Caption coherence: PASS. The figure matches the JSON description of the `mZ2` input-validation distribution in the broad `70 <= m4l <= 170 GeV` window.
- Legend completeness: PASS. Both entries are present and identifiable: `MC prediction` and `Data`.
- Labels/units: PASS. The x-axis is labeled `mZ2 [GeV]`; the y-axis is `Events`; the lower panel is labeled `Pull`.
- CMS/open-data/open-simulation compliance: PASS. The figure carries the CMS label and the open-data/open-simulation branding consistent with the project rules.
- Title/top-text compliance: PASS. There is no axis title or broad fit-window title; the top-right luminosity/energy annotation is acceptable.
- Overlap/clipping: PASS. No visible collisions between labels, legend, data markers, or panel annotations.
- Ranges: PASS. The plotted range is appropriate for the distribution and the pull panel; no suspicious clipping of the data or residuals is visible.
- Error bars/pulls: PASS. Error bars look reasonable and the pull panel is centered near zero with no pathological pattern.
- Number consistency: PASS. The figure content is consistent with the FIGURES.json entry (`chi2 = 192.49734124173966`, `ndf = 6`, `p = 7.490602115287423e-39`, `passes_d7_gate = false`).
