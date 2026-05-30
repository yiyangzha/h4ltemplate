# Phase 4a Regression Gate

Session: `klaus_a64b`  
Date: 2026-05-30  
Scope: compact targeted verification after regression commit `be3a796`; not a broad new panel.

## Verdict

PASS

No targeted blocker remains for the requested gate items.

## Targeted Checks

| Item | Verdict | Evidence |
| --- | --- | --- |
| User-requested windows and method wording | PASS | `phase3_selection/outputs/mva_training_metadata.json` records both training and evaluation windows as `70-170 GeV`, with `m4l_used_as_classifier_input: false`. Phase 4a fit artifacts keep the signal-strength fit window at `105-140 GeV`. `expected_m4l_broad_inclusive` is registered with display range `70-170 GeV` and fit window metadata `105-140 GeV`. `expected_mass_scan.json` scans `110-140 GeV` in `2.5 GeV` steps and documents the excluded `70-105 GeV` Z/sideband-adjacent range. Grep of Phase 3/4 outputs and relevant source found reference comparisons and a "tuned BDT" label only; no wording says the physics result was tuned or forced to match CMS/JHEP values. |
| Dmitri A1 shifted-bin payload and figures | PASS | `analysis_note/results/expected_systematic_shifts.json` exists with 9 active systematics, final-state categories `4mu`, `4e`, `2e2mu`, fit window `105-140 GeV`, and nominal/up/down arrays with 7 bin edges and 6 bin values per checked channel/process payload. `expected_systematic_shift_summary` is registered and sourced to that JSON; it shows the `m4l_scale` shape-source shifts separately from rate-only source impacts. |
| Dmitri B1 grouped MC-stat downscope | PASS | `INFERENCE_EXPECTED.md`, `expected_validation.json`, `expected_systematic_shifts.json`, and `COMMITMENTS.md` all state that MC stat is a grouped group/category normsys approximation, not full per-bin HistFactory `staterror` profiling. `COMMITMENTS.md` leaves `[D2][SP3]` unchecked with status "formally downscoped in Phase 4a, not completed." |
| Dmitri B2 corruption sensitivity | PASS WITH LIMITATION | The final-state simultaneous corruption test was rerun in channels `4mu`, `4e`, `2e2mu`. `m4l_scale_factor_1.2` is rejected (`p = 9.242e-14`), while `m4l_scale_factor_0.8` is not (`p = 0.4595`). The limitation is explicit in `expected_validation.json`, `INFERENCE_EXPECTED.md`, and the low-count validation figure caption. For Phase 4a expected-only inference this is sufficient to proceed because the nominal low-count toy validation passes and observed Phase 4b/4c are required to repeat stability checks and merge/rebin if needed. |
| Newly added figure sanity | PASS | `expected_m4l_broad_inclusive.png`: readable broad `70-170 GeV` validation display with clear labels and legend; large low-mass expected bin drives vertical scale but does not hide the signal-window points. `expected_systematic_shift_summary.png`: readable two-panel display, clear labels, no overlap, and no fake shape dependence for rate-only sources. |
| Non-mutating checks | PASS | `pixi run lint-plots` passed: no plotting violations in 25 files. Phase 4a registry smoke test: 12 entries, no missing files, no zero-byte files, no orphan PNGs. Phase 3 registry smoke test: 31 entries, no missing files, no zero-byte files, no orphan PNGs. |

## Notes

- Reference values appear only in comparison/precision-ratio outputs and plot code, not as fit inputs. The Phase 4a workspace summary points to Phase 3 fit inputs and uses `mu = 1` Asimov pseudo-data from the nominal model.
- Minor non-blocking consistency issue outside this compact gate: `COMMITMENTS.md` says VT12 injected masses are 124, 125, and 126 GeV, while `expected_mass_scan.json` records 115, 125, and 135 GeV. This does not affect the targeted regression gate verdict.

Final verdict: PASS.
