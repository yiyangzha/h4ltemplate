PASS

# Doc 4a Plot Validation

Session: `theo_3fc9`  
Date: `2026-05-30`

Scope: validation of AN-used staged figures in `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex`, using `agents/plot_validator.md` as the base protocol and focusing on blocker-level mechanical or visual issues only.

## Checks run

- Read `agents/plot_validator.md`
- Read `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex`
- Read `analysis_note/review/doc4a/SELF_CHECK_odette_354d_2026-05-30.md`
- Read `phase3_selection/outputs/FIGURES.json`
- Read `phase4_inference/4a_expected/outputs/FIGURES.json`
- Verified every `\includegraphics{...}` target exists
- Ran `pixi run lint-plots`
- Visually validated the staged AN figure set, with explicit spot checks of:
  - broad-window vs fit-window `m4l` figures
  - final-state fit templates
  - `expected_systematic_shift_summary`
  - profile scan, nuisance impacts, uncertainty breakdown
  - rejected-approach diagnostic figure used in the AN

## Result

No blocker-level issues found.

## Evidence

- `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex` contains 49 `\includegraphics` references; all 49 resolve to existing staged files.
- `pixi run lint-plots` completed successfully with:
  - `No plotting violations found in 25 file(s).`
- Caption/figure coherence is acceptable for the AN-used figures reviewed.
- The broad `70 < m_{4\ell} < 170` context figure and the `105 < m_{4\ell} < 140` fit-window figures are visually distinguishable and consistent with their captions.
- The systematic-shift summary matches the captioned split between shape-source bin shifts (upper panel) and rate-only source maxima (lower panel).
- No blocker-level text overlap, legend collisions, missing labels, missing files, or unreadable annotations were found in the validated AN figure set.

## Verdict

PASS
