# Per-figure validation: expected_nuisance_impacts

- Session: `albert_5619`
- Figure: `phase4_inference/4a_expected/outputs/figures/expected_nuisance_impacts.png`
- Registry entry: `phase4_inference/4a_expected/outputs/FIGURES.json`

## Verdict

PASS

## Checks

- Caption / metadata coherence: PASS. The registry caption says this is the expected nuisance-impact ranking on the global signal-strength parameter from fixing each nuisance at +/-1 sigma and refitting the Asimov model. The PNG shows exactly that: a ranked one-dimensional impact plot with the nuisance names on the y-axis and the maximum absolute shift in `mu` on the x-axis.
- Legend completeness: PASS. No legend is needed for this single-series plot; the content is fully encoded by the nuisance labels and the one plotted marker series.
- Label quality: PASS. Axis labels and nuisance names are publication-quality and readable. No raw code identifiers appear. The CMS / Open Simulation label is present and legible.
- Number consistency: PASS. The plot shows 10 nuisance entries, matching the 10 items listed in the figure metadata (`shown`).
- Physics sanity: PASS. All shifts are non-negative, the ordering is sensible, and the dominant impacts are the expected background-systematic terms (`dy fake norm`, `qqZZ norm`) rather than a pathological or unphysical nuisance.
- Visual quality: PASS. Text is readable, markers are visible, and there is no obvious overlap, clipping, or layout artifact.

## Notes

The x-axis is intentionally dimensionless because it reports a shift in the fitted signal-strength parameter `mu`, not a quantity with physical units.
