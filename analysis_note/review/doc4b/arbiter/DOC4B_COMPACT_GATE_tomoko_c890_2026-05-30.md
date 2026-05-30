# Doc 4b Compact Gate

Session: `tomoko_c890`
Date: 2026-05-30
Scope: user-directed reduced gate covering blockers only across physics, number consistency, rendering/compile, figure inclusion, and BibTeX. No child agents spawned.

## Inputs Checked

- `agents/arbiter.md`
- `analysis_note/ANALYSIS_NOTE_doc4b_v1.tex`
- `analysis_note/ANALYSIS_NOTE_doc4b_v1.pdf`
- `analysis_note/review/doc4b/VERIFY_zelda_30c7_2026-05-30.md`
- `analysis_note/review/doc4b/SELF_CHECK_zelda_30c7_2026-05-30.md`
- `analysis_note/results/partial_parameters.json`
- `analysis_note/results/partial_validation.json`
- `analysis_note/results/partial_covariance.json`
- `phase4_inference/4b_partial/outputs/INFERENCE_PARTIAL.md`
- `references.bib`

## Mechanical Checks

| Check | Result | Evidence |
| --- | --- | --- |
| Fresh compile | PASS | `pixi run tectonic --keep-logs analysis_note/ANALYSIS_NOTE_doc4b_v1.tex` completed and wrote `analysis_note/ANALYSIS_NOTE_doc4b_v1.pdf` plus log/blg. Tectonic reported underfull hboxes only. |
| Unresolved refs/citations/Overfull | PASS | Grep of TeX/log/blg for `??`, `Citation`, `undefined`, and `Overfull` returned no matches. |
| BibTeX entries | PASS | All cite keys used in TeX have entries in `references.bib`; `.blg` has no warnings. |
| PDF artifact | PASS | Fresh compile wrote non-empty `analysis_note/ANALYSIS_NOTE_doc4b_v1.pdf` (1200764 bytes). Direct PDF text/raster inspection was limited by missing `pdftotext`/PDF readers and ImageMagick PDF security policy, so rendering evidence is from the successful Tectonic pass and clean log. |

## Required Content Checks

| Check | Result | Evidence |
| --- | --- | --- |
| 10% fit window is `70 < m4l < 170` including Z peak | PASS | TeX states the Phase 4b 10% rerun uses `70 < m_{4\ell} < 170` including the Z peak in the abstract, change log, method, results, figures, and conclusions. |
| No stale claim that 10% result uses `105-140` | PASS | The only Phase 4b `105-140` mentions state that the earlier instruction was superseded; Phase 4a expected baseline remains explicitly separate. |
| Seed | PASS | JSON and TeX both give seed `9417`. |
| Event count | PASS | JSON and TeX both give `20 / 203` selected events. |
| Effective luminosity | PASS | JSON and TeX both give `1.0 fb^-1`. |
| Signal strength | PASS | JSON and TeX both give `mu = 0.0 +1.3548619813595435` with lower interval at the physical boundary. |
| GoF | PASS | JSON and TeX both give `chi2/ndf = 31.755141641709276 / 38`, `p = 0.752432307059706`. |
| Expected-vs-partial pull | PASS | JSON and TeX both give exact pull `-0.679474677941247` at least once; several narrative mentions round it to `-0.6795`, which is acceptable. |
| Staging clarity | PASS | The note says Phase 4a is expected-only, Doc 4b is fixed-seed 10% observed validation, and the full observed-data result is reserved for Phase 4c. No full-data signal-strength result is implied. |
| Limitations preserved | PASS | The note preserves the `mu=0` boundary, deterministic split proxy, VBF and NN/MVA downscope, DY+jets fake proxy, and grouped MC-stat approximation. |

## Figure Inclusion

All seven Phase 4b figures are included in the TeX and the included PDF files exist under `analysis_note/figures/`. The original Phase 4b PNG and PDF outputs also exist under `phase4_inference/4b_partial/outputs/figures/`.

| Figure | Included | Included PDF | Original PNG |
| --- | --- | --- | --- |
| `partial_m4l_broad_inclusive` | PASS | PASS | PASS |
| `partial_m4l_70_170_categories` | PASS | PASS | PASS |
| `partial_expected_mu_comparison` | PASS | PASS | PASS |
| `partial_nuisance_pulls` | PASS | PASS | PASS |
| `partial_nuisance_impacts` | PASS | PASS | PASS |
| `partial_binning_stability` | PASS | PASS | PASS |
| `partial_split_consistency` | PASS | PASS | PASS |

## Adjudication Table

| # | Finding | Source | Their Cat | Final Cat | Rationale |
| --- | --- | --- | --- | --- | --- |
| 1 | No compact-gate blocker found. | Arbiter check | n/a | n/a | Compile, references/citations, key numbers, fit-window staging, figure inclusion, BibTeX, and required limitations all pass. |

## Verdict

PASS.
