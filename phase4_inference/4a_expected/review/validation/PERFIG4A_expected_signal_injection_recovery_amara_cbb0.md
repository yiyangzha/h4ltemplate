# Per-figure validation: expected_signal_injection_recovery

Verdict: PASS

Checks:
- Visual quality: the figure is clean and readable at rendered size.
- Legend completeness: both entries are present, distinct, and legible (`Exact recovery`, `Fit result`).
- Label quality: axis labels are publication-quality and the experiment label is correctly shown as `CMS Open Simulation`.
- Metadata coherence: the registry caption and metadata match the image content. The plotted recovery points correspond to the injected values `0, 1, 2, 5`, and the fitted values in `FIGURES.json` round to the displayed points.
- Physics sanity: the recovered fit follows the exact-recovery line with negligible bias across all tested injections, consistent with a successful signal-injection closure test.

No fixes required.
