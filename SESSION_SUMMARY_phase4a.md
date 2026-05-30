# Session Summary Phase 4a

Date: 2026-05-30T03:37:40Z

Phase 4a expected inference passed the blocking expected-inference gate after one review/fix cycle and a targeted regression update requested by the user.

Key results:
- Expected `mu = 1.0 -0.51674064615437 +0.6327358408468291`.
- Symmetric expected uncertainty: `0.5747382435005995`.
- Signal-strength fit window: `105 < m4l < 140 GeV`.
- Broad `m4l` display range: `70 < m4l < 170 GeV`.
- Mass scan range: `110-140 GeV`, with Z/sideband-adjacent exclusions documented.

Key decisions:
- S1 final-state categories remain nominal. The targeted MVA update used broad `70 < m4l < 170 GeV` training/evaluation and a tuned BDT trial, but did not pass promotion gates.
- CMS-HIG-16-041 / JHEP 11 (2017) 047 is used as methodology/comparison context only; results are not tuned to match it.
- Full bin-by-bin HistFactory `staterror` profiling is formally downscoped in Phase 4a to grouped group/category MC-stat normsys terms.
- The final-state `m4l_scale_factor_0.8` corruption sensitivity criterion is documented as low-count infeasible after three attempts, not passed.

Gate evidence:
- Plot validation `celeste_62e7`: PASS.
- Regression gate `klaus_a64b`: PASS.
- Corruption follow-up commit `f214807`: documented three failed `-20%` sensitivity attempts and fixed VT12 wording.
- `REGRESSION_CHECK_phase4a.md`: PASS with documented low-count limitation.

Next step: begin Doc 4a note writing from the current Phase 4a artifacts.
