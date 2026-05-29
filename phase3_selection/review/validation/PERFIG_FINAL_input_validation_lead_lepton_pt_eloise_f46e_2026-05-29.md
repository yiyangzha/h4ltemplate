# Per-Figure Validation: `input_validation_lead_lepton_pt`

**Verdict:** PASS

Checked against `phase3_selection/outputs/FIGURES.json` entry `input_validation_lead_lepton_pt` and the PNG at `phase3_selection/outputs/figures/input_validation_lead_lepton_pt.png`.

The figure is publication-clean for this validation use case. The CMS/Open Data/Open Simulation labeling is present and correctly formatted, the luminosity/energy tag is placed in the upper right, the legend is complete (`MC prediction`, `Data`), and the axes are labeled with the correct observable and units. The lower pull panel is present with a visible zero line and nontrivial residuals, which matches the metadata indicating a failed D7 shape gate (`chi2/ndf = 4.056365380026655`, `p = 0.0027310794648283346`).

I do not see title-like fit-window text on the plot itself, and there is no obvious overlap or clipping. The histogram ranges and error bars are internally consistent with the metadata and the plotted data/MC comparison. The caption in `FIGURES.json` is coherent with the visual content and the stated role of the figure as an input-validation distribution rather than a normalization template.
