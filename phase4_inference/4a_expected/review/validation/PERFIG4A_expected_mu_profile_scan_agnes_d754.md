# Per-Figure Validation: `expected_mu_profile_scan`

- Session: `agnes_d754`
- Figure: `phase4_inference/4a_expected/outputs/figures/expected_mu_profile_scan.png`
- Metadata source: `phase4_inference/4a_expected/outputs/FIGURES.json`

## Verdict

PASS

## Checks

- Visual quality: pass. The scan curve is smooth, the horizontal `1\sigma` and `2\sigma` reference lines are clear, and there is no visible clipping or text overlap.
- Caption/metadata coherence: pass. The figure matches the JSON description of an expected profile-likelihood scan for the global signal-strength parameter, with the minimum at `\mu = 1`.
- Legend completeness: pass. The legend entries for `-2\Delta\log L`, `1\sigma`, and `2\sigma` are all present and readable.
- Label quality: pass. Axis labels and experiment label are publication-quality; no raw variable names are shown.
- Number consistency: pass. The plotted curve is consistent with the metadata values `\mu = 1.0` and symmetric uncertainty `0.574738...`; the visible intersections with `\Delta(-2\log L)=1` and `4` are consistent with the asymmetric uncertainty values in the JSON.
- Physics sanity: pass. The scan is convex, has its minimum at the Asimov expectation `\mu = 1`, and crosses the standard profile-likelihood thresholds in the expected places.

## Notes

No fixes required.
