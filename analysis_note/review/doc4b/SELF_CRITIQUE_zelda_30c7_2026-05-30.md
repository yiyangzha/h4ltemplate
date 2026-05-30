# Doc 4b Self-Critique

Session: `zelda_30c7`  
Date: 2026-05-30

## Critic Mode Findings

### Finding 1: Stable Phase 3/4a captions could be misread as the Doc 4b fit window

Risk: The abstract, Results, and Statistical Method correctly state that the Phase 4b 10% observed-data result uses `70 < m4l < 170 GeV`, including the Z peak. However, earlier stable Event Selection text and appendix captions still described `105-140` as "the fit window" or said "Phase 4 must validate" without explicitly limiting that statement to the Phase 3/4a expected handoff. A skeptical reader could encounter those pages before the Results section and think Doc 4b still used `105-140`.

Fix: Updated the Event Selection paragraph, cutflow caption, fit-window inclusive caption, broad-window appendix caption, and final-state appendix captions to say `105-140` is the Phase 3/4a expected handoff window and that Doc 4b uses the separate `70-170` partial-data fit.

Evidence: `analysis_note/ANALYSIS_NOTE_doc4b_v1.tex` now states the Doc 4b override in the abstract, Change Log, Event Selection, Statistical Method, Results, Comparison, Conclusions, and Reproduction Contract.

### Finding 2: "Principal comparison target" wording could imply tuning

Risk: The Introduction described CMS-HIG-16-041 as the "principal comparison target." Even though later text says the analysis is not tuned to CMS/JHEP results, the word "target" could be read as optimization language.

Fix: Changed this to "principal contextual reference."

### Finding 3: Comparison table carried a Phase 4a-only phrase into Doc 4b

Risk: The fiducial cross-section row said "unavailable in Phase 4a." In Doc 4b this is still true, but the phrasing was stale and could imply a fiducial cross section might now exist in the partial-data update.

Fix: Changed the row to "unavailable in this detector-level analysis."

## Strongest Remaining Criticisms and Where Addressed

- The 10% result lands at the physical boundary and has no finite lower interval. Addressed in the abstract, Change Log, `tab:partial-mu-result`, `fig:partial-expected-mu-comparison`, and Conclusions.
- The expected-vs-partial comparison might be overstated. Addressed by presenting pull `-0.6795` as an internal compatibility metric only, saying it is a validation-stage outcome, and explicitly stating that public CMS results are contextual references, not tuning targets.
- The 70--170 GeV Phase 4b override differs from the Phase 4a expected methodology. Addressed explicitly in the abstract, Event Selection, Statistical Method, Results, and Reproduction Contract.
- The Z-peak-inclusive window could make the result less CMS-like. Addressed by describing it as the latest user-requested Phase 4b override and not as an official-equivalent CMS measurement.
- The split consistency figure could be misread as a true run-period check. Addressed in the split table caption, split figure caption, Conclusions, Known Limitations, and Change Log as a deterministic proxy only.
- Doc 4a limitations could be lost in the update. Addressed in the Change Log, Systematics, Conclusions, Known Limitations, Limitation Index, and appendix figure inventory.

## Verification After Fixes

- Recompiled with `pixi run tectonic --keep-logs analysis_note/ANALYSIS_NOTE_doc4b_v1.tex`.
- Re-ran figure inclusion, stale-window grep, unresolved citation/reference/Overfull grep, and `git diff --check`.
- All checks passed after the fixes.
