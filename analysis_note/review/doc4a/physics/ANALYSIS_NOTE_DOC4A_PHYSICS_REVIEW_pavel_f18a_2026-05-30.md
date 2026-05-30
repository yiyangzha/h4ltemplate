PASS

# Doc 4a Physics Review

Reviewer session: `pavel_f18a`  
Date: 2026-05-30  
Artifact: `analysis_note/ANALYSIS_NOTE_doc4a_v1.{tex,pdf}`

## Findings

No Category A or Category B physics findings.

### C1. Keep the low-count sensitivity limitation prominent in observed-data updates

Category C.

The note correctly does not hide the limitation: 17/18 final-state bins are below five expected events, and the -20% mass-response corruption test is not rejected after three profiled tests. Evidence:
- `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:424` states that none of the three final-state-aligned profiled tests rejects at `p < 0.05`.
- `analysis_note/results/expected_validation.json` records `criterion_status = documented_low_count_infeasible`, `passes = false`, with p-values 0.4595, 0.6049, and 0.1584.
- The conclusion and limitation index carry this forward at `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:573` and `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:843`.

This is acceptable for expected-only Doc 4a because it is explicitly documented rather than presented as a passed validation. In Doc 4b/4c, the same limitation should be revisited with observed-data GoF and nuisance behavior before any stronger physics claim is made.

### C2. Grouped MC-stat treatment is acceptable here, but should remain a named approximation

Category C.

The expected fit uses grouped process/category MC-stat normalization nuisances rather than full per-bin HistFactory `staterror`. The note identifies this as a formal downscope and checks alternative binning. Evidence:
- `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:205` through `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:210` defines the grouped approximation and explicitly contrasts it with full per-bin profiling.
- `analysis_note/results/expected_covariance.json` records `mc_stat_treatment = group_category_normsys_from_sumw2; not full bin-by-bin HistFactory staterror profiling`.
- Alternative-binning uncertainties are stable at about 0.572-0.590 in `analysis_note/results/expected_validation.json`.

This does not block Doc 4a because the approximation is visible, subdominant, and not used to claim official CMS-equivalent precision.

## Positive Checks

- Expected-only scope is correctly enforced. The abstract and result section state that no observed-data signal-strength result is reported, and the fit observation is Asimov pseudo-data (`analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:33`, `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:198`, `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:463`).
- The method follows CMS-HIG-16-041 where feasible without forcing agreement: same `105 < m4l < 140 GeV` fit window, simultaneous final-state template fit, and explicit comparison to CMS references, while VBF and classifier categories are downscoped with reasons (`analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:49`, `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:103`, `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:536`).
- MC normalization is not data-integral normalized for the fit. The note uses prompt effective cross sections and metadata denominators and explicitly separates diagnostic shape rescaling from fit templates (`analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:55`, `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:212`).
- The fake-background limitation is honestly stated. DY+jets is used as the user-requested proxy, with a broad nuisance and direct comparison to CMS data-driven Z+X (`analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:288`, `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:555`, `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:579`).
- The expected signal-strength result is internally consistent with the JSON: `mu = 1.0 +0.6327/-0.5167`, symmetric uncertainty 0.5747, and the Asimov `chi2 = 0, p = 1` is explicitly labeled as a bookkeeping/self-consistency check rather than validation.
- Key result and validation figures inspected from the corresponding upstream PNG renderings show no obvious data/MC normalization pathology requiring a physics block. The observed-data Phase 3 `m4l` displays show finite pulls rather than a bulk factor-of-two mismatch, and the expected-only template plots are correctly labeled as open simulation.

## Verdict Rationale

I would approve Doc 4a as an expected-only analysis note. It does not overclaim observed results, does not tune to CMS-HIG-16-041, and makes the major open-data limitations visible enough for downstream 10% and full-data updates.
