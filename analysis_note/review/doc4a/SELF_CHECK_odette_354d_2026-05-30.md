# Doc 4a Self-Check

Session: `odette_354d`  
Date: 2026-05-30

## Compile

- Command: `pixi run tectonic --keep-logs analysis_note/ANALYSIS_NOTE_doc4a_v1.tex`
- PDF: `analysis_note/ANALYSIS_NOTE_doc4a_v1.pdf`
- Page count: 66 pages, from `analysis_note/ANALYSIS_NOTE_doc4a_v1.log`
- BibTeX: PASS. `analysis_note/ANALYSIS_NOTE_doc4a_v1.blg` finds `../references.bib`.
- Undefined citations/cross-references: none found by grep of kept log.
- Overfull boxes: none found by grep of kept log.
- Remaining TeX warnings: underfull hboxes in narrow wrapped tables/paragraphs only.

## Metrics

- Display equations: 10
- Figures included: 49 total, 49 unique, 0 missing files
- Tables: 14
- Systematic subsections: 15 source/status subsections plus one mass-profile subsection; all active and downscoped sources from `systematics_sources.json` are discussed.
- Corrections/model-construction section word count: 541
- Statistical Method section word count: 575
- Systematic section word count: 1288
- Unique cited bibliography keys in the note: 16
- BibTeX entries in `references.bib`: 17
- Comparison statements: the only `consistent` usage is quantitative in the same paragraph, with the expected precision ratio 3.193.
- Future-phase placeholders: 0 `\tbd{}` placeholders in Doc 4a. Observed 10% and full-data results are described as future updates in prose, not as filled values.

## Figure Inventory

All 49 upstream figure PDFs are staged and included:

- 6 Phase 1 reconnaissance figures
- 31 Phase 3 selection/input/MVA/downscope figures
- 12 Phase 4a expected-inference figures

No figure exclusions.

## Required Physics State Checks

- Expected-only result is quoted as `mu = 1.0 -0.51674064615437 +0.6327358408468291`, symmetric uncertainty `0.5747382435005995`.
- Signal-strength fit window is stated as `105 < m4l < 140 GeV`.
- Broad display/training range is stated as `70 < m4l < 170 GeV`.
- Mass scan is documented as `110-140 GeV` and not promoted to an official mass measurement.
- S1 final-state categories are nominal; no VBF category is claimed.
- VBF is formally downscoped because no recoverable jet/VBF information exists.
- MVA/NN attempts are documented and rejected by promotion gates.
- DY+jets MC remains the fake-background proxy; no full fake-rate estimate is claimed.
- Grouped MC-stat treatment is documented as a formal approximation/downscope, not full bin-by-bin HistFactory `staterror`.
- The `m4l_scale_factor_0.8` corruption sensitivity is documented as `documented_low_count_infeasible` after three attempts, not passed.

## Known Limitations

- The note is complete for Doc 4a expected results, but it is not a final observed-data AN. Phase 4b/4c must update observed-data results and rerun low-count stability checks.
- The bibliography was assembled from public source trails and known public references because MCP toggles are false. No MCP citation tools were called.
- The document uses a self-contained LaTeX preamble because the referenced `conventions/an_template.tex` and visible `conventions/` directory are absent in this worktree.

## Mechanical Checks

- `git diff --check`: PASS.
- Figure-reference existence check: PASS, 49 references, 0 missing.
- Kept log grep for `Overfull`, `undefined`, and `Citation`: PASS.
