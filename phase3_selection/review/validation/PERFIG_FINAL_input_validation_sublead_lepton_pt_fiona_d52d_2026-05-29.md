# Per-Figure Validation

Session: `fiona_d52d`
Date: `2026-05-29`
Figure: `input_validation_sublead_lepton_pt`

## Inputs Checked
- `TOGGLES.md`
- `agents/plot_validator.md`
- `methodology/appendix-plotting.md`
- `phase3_selection/outputs/FIGURES.json` entry for `input_validation_sublead_lepton_pt`
- Rendered figure: `phase3_selection/outputs/figures/input_validation_sublead_lepton_pt.png`

## Metadata
- PNG exists on disk and is non-zero size.
- FIGURES.json entry matches the rendered file name.
- Metadata values in the entry:
  - `chi2 = 3397.904290296771`
  - `ndf = 4`
  - `p_value = 0.0`
  - `passes_d7_gate = false`
  - `shape_normalization_scale_data_over_mc = 0.9688238676560702`

## Validation Result
PASS

## Checks
- The figure uses the CMS style and a square single-panel + ratio layout consistent with the plotting standard.
- The experiment label is present on the main panel only; the ratio panel does not carry a duplicate label.
- Axis labels are legible and include units where applicable: `Subleading lepton p_T [GeV]` and `Pull`.
- Legend placement does not overlap plotted content.
- The ratio panel is readable and does not show clipping, spurious text, or visible panel separation artifacts.
- The data/MC comparison and pull panel are visually coherent with the metadata in `FIGURES.json`.

## Verdict
PASS
