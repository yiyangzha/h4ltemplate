# Per-Figure Validation: `mva_roc_logistic`

- Session: `leopold_2b39`
- Phase: 3 selection
- Commit context: `63227ca`
- Figure: `phase3_selection/outputs/figures/mva_roc_logistic.png`
- Registry entry: `phase3_selection/outputs/FIGURES.json`

## Verdict

PASS

## Checks

- Readability: PASS. Axis labels, tick labels, and legend text are legible at rendered size.
- ROC labeling: PASS. The plot clearly shows signal efficiency vs background efficiency, with the diagonal random baseline included.
- Legend: PASS. The legend is present, readable, and does not overlap the ROC curve.
- Title-like text: PASS. There is no plot title. The CMS/Open Simulation and `13 TeV` experiment labels are presentation labels, not a title.
- Code identifiers in presentation text: PASS. No raw code variable names are visible in the figure.
- Caption coherence: PASS. The rendered figure matches the registry caption describing a logistic classifier ROC curve with weak separation, and the displayed AUC value is consistent with that description.

## Notes

- The figure is consistent with the `FIGURES.json` entry:
  - `id`: `mva_roc_logistic`
  - `png`: `figures/mva_roc_logistic.png`
  - `description` / `caption`: logistic classifier ROC curve for the S2 attempt

