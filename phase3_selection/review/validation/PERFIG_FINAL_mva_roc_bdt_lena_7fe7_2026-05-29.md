# Per-figure validation: `mva_roc_bdt`

Result: FAIL

Checks performed:
- Readability: pass. Axis labels, ticks, diagonal reference, and ROC curve are legible.
- ROC labeling: pass. The plot clearly shows signal/background efficiency axes and the random baseline.
- Legend: pass visually, but the model label is written as `bdt` rather than a publication-grade presentation label.
- No title-like text: pass. No figure title is present.
- No code identifiers in presentation text: fail. The legend entry `bdt AUC=0.548` exposes a lower-case code-style identifier; this should be presented as `BDT` or another publication-facing name.
- Caption coherence: pass. The figure matches the registry entry for a BDT ROC curve and the reported AUC value is consistent with the plotted legend.

Verdict: FAIL because the legend contains code-style presentation text (`bdt`).
