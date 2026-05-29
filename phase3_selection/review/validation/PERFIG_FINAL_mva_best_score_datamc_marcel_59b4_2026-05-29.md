# Per-Figure Validation: `mva_best_score_datamc`

- Session: `marcel_59b4`
- Commit: `63227ca`
- Figure: `phase3_selection/outputs/figures/mva_best_score_datamc.png`
- FIGURES.json entry: `mva_best_score_datamc`

## Verdict

PASS

## Checks

- Data/MC readability: PASS. The main histogram and data markers are legible at review size, and the score axis is readable.
- Pull panel: PASS. The pull panel is present, centered near zero, and the non-zero bin is visually clear without clipping.
- Open-data/open-simulation label: PASS. The figure uses the compliant CMS open-data/open-simulation branding in the main label.
- Title-like text: PASS. There is no plot title; the top-right luminosity/energy text and the experiment label behave as figure annotations, not a title.
- Legend overlap: PASS. The legend sits in an empty region and does not overlap the data points, bars, or pull panel.
- Caption coherence: PASS. The caption in `FIGURES.json` matches the rendered content: best S2 classifier score data/MC comparison in the broad validation window, with rejected-approach context.

## Notes

This figure is a clean data/MC diagnostic with no visible layout or readability red flags under the Level 2 per-figure checks requested.
