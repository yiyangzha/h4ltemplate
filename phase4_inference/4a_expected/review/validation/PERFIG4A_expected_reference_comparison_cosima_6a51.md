# Per-figure validation: `expected_reference_comparison`

Session: `cosima_6a51`

Status: FAIL

Scope checked:
- [x] `agents/plot_validator.md`
- [x] `methodology/appendix-plotting.md`
- [x] `phase4_inference/4a_expected/outputs/FIGURES.json`
- [x] `phase4_inference/4a_expected/outputs/figures/expected_reference_comparison.png`

Assessment:
- The figure is visually clean and readable. The dashed SM expectation line, the three horizontal measurements, and the legend are all legible.
- The precision-ratio claim is numerically consistent with the metadata: `0.5747382435005995 / 0.18 = 3.192990241669998`, matching the declared ratio `3.19`.

Findings:
1. **Label quality / publication naming**  
   The y-axis category labels are not publication-grade: `This expected`, `CMS HIG 16 041`, and `CMS HIG 19 001` are rendered without standard hyphenation or a clear label for the current result. This is a readability and presentation issue for an AN figure.  
   **Category:** A  
   **Fix:** Rename the labels to publication-standard forms, e.g. `This analysis (expected)`, `CMS-HIG-16-041`, and `CMS-HIG-19-001`. Keep the comparison labels consistent with the caption and FIGURES.json metadata.

2. **Caption/label coherence for the ratio claim**  
   The caption/metadata state that the expected uncertainty/reference ratio `3.19` is for `CMS-HIG-16-041`, but the figure itself shows two public references. That is not wrong, but the target of the ratio claim should be explicit on the figure or in the accompanying caption so readers do not infer that `3.19` applies to both reference points.  
   **Category:** B  
   **Fix:** Add a short clarifying phrase in the caption or figure annotation identifying that `3.19` is relative to `CMS-HIG-16-041` only, while `CMS-HIG-19-001` is an additional comparison point.

Result: **FAIL** until the label naming is corrected and the ratio target is made explicit.
