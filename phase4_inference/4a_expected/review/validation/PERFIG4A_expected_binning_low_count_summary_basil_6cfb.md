# Per-figure validation: `expected_binning_low_count_summary`

**Verdict: PASS**

Checked against `phase4_inference/4a_expected/outputs/FIGURES.json` and the rendered PNG
`phase4_inference/4a_expected/outputs/figures/expected_binning_low_count_summary.png`.

- Visual quality: clean rendering, no clipped text, no overlap, and no stray artifacts.
- Caption/metadata coherence: the registry description matches the plot content. The four category labels on the y-axis correspond to the four configurations in the JSON metadata.
- Legend completeness: no legend is needed for this summary plot; the single-series scatter encoding is self-explanatory.
- Label quality: axis and experiment labels are publication-quality; `CMS Open Simulation` is appropriate for an expected/Asimov figure.
- Number consistency: the plotted values match the registry metadata exactly: `final state nominal = 17`, `inclusive nominal = 0`, `inclusive coarse = 0`, `inclusive peak side = 0`.
- Physics sanity: the intended result is clear. The nominal final-state binning is the only configuration retaining low-expected-count bins, while the inclusive alternatives do not.

