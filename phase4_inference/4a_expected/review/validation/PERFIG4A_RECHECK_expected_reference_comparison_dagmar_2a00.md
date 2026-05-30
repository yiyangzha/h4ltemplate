# Per-figure revalidation: `expected_reference_comparison`

Session: `dagmar_2a00`

Status: PASS

Scope checked:
- [x] `phase4_inference/4a_expected/review/validation/PERFIG4A_expected_reference_comparison_cosima_6a51.md`
- [x] `phase4_inference/4a_expected/outputs/FIGURES.json`
- [x] `phase4_inference/4a_expected/outputs/figures/expected_reference_comparison.png`
- [x] `agents/plot_validator.md`

Assessment:
- The prior label-quality issue is fixed. The rendered y-axis labels are publication-grade and match the requested forms:
  - `This analysis (expected)`
  - `CMS-HIG-16-041`
  - `CMS-HIG-19-001`
- The figure is legible at rendered size. Axis labels, tick labels, the CMS label block, and the legend are readable and do not overlap.
- The caption/metadata coherence is also fixed. `FIGURES.json` explicitly states that the `3.19` expected uncertainty/reference ratio is computed relative to `CMS-HIG-16-041` only, and that `CMS-HIG-19-001` is an additional public comparison point.

Concrete evidence:
- `FIGURES.json` entry for `expected_reference_comparison`:
  - caption/description: `The expected uncertainty/reference ratio 3.19 is computed relative to CMS-HIG-16-041 only; CMS-HIG-19-001 is shown as an additional public comparison.`
  - metadata: `ratio_this_over_reference = 3.192990241669998`
  - metadata reference: `CMS-HIG-16-041 mu uncertainty symmetrized from +0.19/-0.17`
- Rendered PNG inspection:
  - top label: `This analysis (expected)`
  - middle label: `CMS-HIG-16-041`
  - bottom label: `CMS-HIG-19-001`
  - legend: `SM expectation`
  - no clipping, overlap, or unreadable text at the shown output size
- File freshness:
  - `phase4_inference/4a_expected/outputs/figures/expected_reference_comparison.png` mtime `2026-05-30 02:06:08.775405873 +0000`
  - `phase4_inference/4a_expected/outputs/FIGURES.json` mtime `2026-05-30 02:06:08.777405836 +0000`

Result: **PASS**
