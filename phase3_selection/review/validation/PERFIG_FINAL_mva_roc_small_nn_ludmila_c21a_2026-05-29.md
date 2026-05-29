# Per-figure Validation: `mva_roc_small_nn`

- Session: `ludmila_c21a`
- Phase: 3 Selection
- Review tier: Level 2 per-figure validation
- Commit under validation: `63227ca`
- Figure: `phase3_selection/outputs/figures/mva_roc_small_nn.png`

## Result: PASS

The rendered ROC curve is readable at review size, the axes are correctly labeled as signal efficiency vs background efficiency, the diagonal random baseline is present, and the legend is legible without overlapping the curve. The figure contains no title text, no spurious code identifiers, and the presentation text is coherent with the FIGURES.json entry.

## Checks

- Readability: PASS
- ROC labeling: PASS
- Legend: PASS
- No title-like text: PASS
- No code identifiers in presentation text: PASS
- Caption coherence with `FIGURES.json`: PASS

## Evidence

- `FIGURES.json` entry `mva_roc_small_nn` describes a small NN classifier ROC curve for the S2 attempt.
- The figure shows a single ROC curve labeled `small nn AUC=0.550` plus the `Random` diagonal baseline.
- Axis labels are `Signal efficiency` and `Background efficiency`.
- The `CMS` and `Open Simulation` label block is present and not colliding with the plotted content.
