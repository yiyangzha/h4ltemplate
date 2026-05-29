# Per-Figure Validation Recheck

Figure: `mva_roc_bdt`

Result: PASS

Checks:
- Legend uses publication text `BDT` rather than code-style `bdt`.
- Figure is readable at rendered size; axis labels, tick labels, and legend text are legible.
- No title-like plot text is present.
- Caption coherence is good: the figure content matches the registry entry for the BDT ROC curve and the reported `BDT AUC=0.548` legend entry.

Evidence:
- Registry entry `phase3_selection/outputs/FIGURES.json`:
  - `id`: `mva_roc_bdt`
  - `caption`: `BDT classifier ROC curve for the S2 attempt. The weak separation and failed category-viability gates prevent promotion to nominal Phase 4 categories.`
  - `metadata.model_label`: `BDT`
- Rendered file:
  - `phase3_selection/outputs/figures/mva_roc_bdt.png`
