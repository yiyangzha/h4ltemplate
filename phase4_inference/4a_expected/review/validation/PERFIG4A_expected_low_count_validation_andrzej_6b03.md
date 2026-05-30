# PERFIG4A_expected_low_count_validation

Session: `andrzej_6b03`

Result: PASS

Checked figure: `phase4_inference/4a_expected/outputs/figures/expected_low_count_validation.png`

Registry entry: `phase4_inference/4a_expected/outputs/FIGURES.json`

Assessment:
- Visual quality is good: text is legible, the y-axis category labels are readable, and there is no clipping or text collision that would block interpretation.
- Caption/metadata coherence is good: the rendered content matches the registry caption and the stored metadata for the low-count toy and corruption tests.
- Legend completeness is sufficient for this figure: the only explicit legend item is the red dashed `p = 0.05` reference line, and it is present and readable.
- Label quality is acceptable: axis and panel labels are publication-style, not code identifiers.
- Number consistency is good:
  - toy success marker is consistent with `fit_success_fraction = 1.0`
  - toy median-bias marker is consistent with `|median_bias| = 0.06064996537909362`
  - corruption markers are consistent with `p_value = 0.01934008970762087` and `p_value = 3.1049330873040137e-18`
- Physics sanity is good: both corrupted mass-response tests fall below the `p = 0.05` threshold, which matches the caption claim that the closure test is sensitive to a 20 percent corruption.

No fixes required.
