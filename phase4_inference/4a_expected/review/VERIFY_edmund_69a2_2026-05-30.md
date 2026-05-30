# Phase 4a VERIFY Exchange

Executor session: `edmund_69a2`  
Phase: Phase 4a expected inference  
Date: 2026-05-30

## Executor Initial Completion Signal

The executor reported Phase 4a expected-inference execution complete with:

- `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md`
- `analysis_note/results/expected_parameters.json`
- `analysis_note/results/expected_systematics.json`
- `analysis_note/results/expected_covariance.json`
- `analysis_note/results/expected_validation.json`
- `analysis_note/results/expected_mass_scan.json`
- 10 registered PNG/PDF figure pairs under `phase4_inference/4a_expected/outputs/figures/`
- Updated `COMMITMENTS.md`, `pixi.toml`, `experiment_log.md`, and executor log
- New scripts `build_inference_artifact.py` and `update_commitments_phase4a.py`

Reported validation:

- `pixi run p4a-all`: PASS
- `pixi run lint-plots`: PASS, no plotting violations in 25 plotting scripts
- Figure smoke test: 10 entries, no missing/empty/orphan PNG/PDF files
- Result JSON smoke test: required expected JSON files exist with `phase = 4a_expected`
- Watcher recheck `PLOT_WATCHER_RECHECK_vera_ee63.md`: PASS, unresolved blockers 0

Key reported numbers:

- `mu = 1.0 -0.5167 +0.6327`, symmetric expected uncertainty `0.5747`
- Low-count toys: 80 toys, success fraction `1.0`, median bias `-0.06065`
- Precision ratio vs CMS-HIG-16-041 symmetrized `mu` uncertainty: `3.193`
- Signal injection at `mu = 0, 1, 2, 5`: PASS
- Corruption closure p-values: `0.01934` and `3.1049e-18`

## Follow-Up 1 Prompt

The orchestrator sent:

> Re-read `phase4_inference/4a_expected/plan.md` line by line. For each item, verify it is DONE, not merely started. Run every self-check from `phase4_inference/4a_expected/CLAUDE.md` and the relevant executor checks. Show evidence: output/result listings with mtimes, explicit DONE/INFEASIBLE status for every plan item, exact validation numbers, figure registry smoke-test result, `pixi run p4a-all` and `pixi run lint-plots` summaries, and one-sentence description of every PNG. Only signal completion when every plan item is DONE or formally infeasible with evidence, every required Phase 4a completion criterion is checked, and every check passes.

## Follow-Up 1 Response Summary

The executor re-read `plan.md` and reported every checkbox complete. No item was declared infeasible.

Evidence included:

- Output listing: `FIGURES.json` and `INFERENCE_EXPECTED.md` present; 20 non-zero figure files.
- Result listing: five expected JSON files present with May 30 01:26 mtimes.
- Figure smoke test: 10 registry entries, 20 registered files, missing `0`, empty `0`, orphan `0`.
- `pixi run p4a-all`: exit `0`.
- `pixi run lint-plots`: exit `0`, `No plotting violations found in 25 file(s).`

Exact validation numbers reported:

- Fit: `mu = 1.0`, uncertainties `-0.51674064615437 / +0.6327358408468291`, symmetric `0.5747382435005995`, `twice_nll = 104.17723150400087`, converged `true`.
- Asimov GoF self-consistency: combined `chi2 = 0.0`, `ndf = 17`, `p = 1.0`; combined deviance `0.0`, `ndf = 17`, `p = 1.0`; per-channel `chi2 = 0.0`, deviance `0.0`, `ndf = 5`, `p = 1.0`.
- Low-count toys: `n_toys = 80`, seed `4269`, failures `0`, success fraction `1.0`, median `mu = 0.9393500346209064`, median bias `-0.06064996537909362`, mean `1.02125847598412`, std `0.5972534571136956`.
- Injection: `mu=0` fitted `5.390643701715379e-21`; `mu=1` fitted `1.0`; `mu=2` fitted `1.999995527598417`; `mu=5` fitted `4.999924244479526`; all pass the 20% bias gate.
- Corruption closure: scale `0.8` deviance `13.47136390295552`, `ndf = 5`, `p = 0.01934008970762087`; scale `1.2` deviance `91.59556067192092`, `ndf = 5`, `p = 3.1049330873040137e-18`; both fail as required.
- Channel compatibility: `4mu`, `4e`, `2e2mu` all have `mu = 1.0`, pull `0.0`, `p = 1.0`, with uncertainties `0.8669205858368869`, `1.8113475516379003`, and `0.8771049995474594`.
- Precision ratio: reference uncertainty `0.18`, expected uncertainty `0.5747382435005995`, ratio `3.192990241669998`, not above 5x.
- Mass closure: injected `124, 125, 126 GeV` recover `124, 125, 126 GeV`; closure passes; not promoted to nominal mass measurement because independent mass-hypothesis MC or official calibration/morphing inputs are unavailable.

Figure descriptions were provided for all 10 registered figures.

## Follow-Up 2 Prompt

The orchestrator sent:

> Switch to critic mode. Re-read `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md`, all Phase 4a result JSON, `COMMITMENTS.md`, and every current Phase 4a PNG as a skeptical referee. For each figure: what would you criticize? For each major claim: is the evidence convincing or merely asserted? Pay special attention to Asimov GoF values of exactly zero/p=1.0, grouped MC-stat nuisance approximation, low-count final-state validation, mass-profile/method-parity claim, external numeric systematic/citation basis, and stale watcher feedback with old FAIL text. Fix what you find.

## Follow-Up 2 Response Summary

The executor found substantive issues and fixed them in commit `733fde9` (`fix: clarify phase 4a validation caveats`):

- Clarified that Asimov `chi2 = 0` and `p = 1` are self-consistency checks, not independent validation.
- Marked grouped MC-stat nuisances as a grouped approximation, not equivalent to full per-bin `staterror` profiling.
- Scoped low-count category retention to Phase 4a expected inference only; 4b/4c must repeat checks and merge/rebin if unstable.
- Strengthened mass-profile non-promotion/downgrade wording.
- Added `variation_basis` metadata and explicit `implemented_fallback_prior` statuses for fallback priors.
- Resolved stale watcher confusion by committing watcher audit files and noting that `vera_ee63` PASS supersedes earlier FAIL/BLOCKED watcher files.
- Improved `expected_binning_stability` spacing and legend handling; clarified selected figure captions/prose.

Follow-up validation rerun:

- `pixi run p4a-all`: PASS
- `pixi run lint-plots`: PASS, no plotting violations in 25 files
- Figure registry smoke test: entries `10`, registered files `20`, missing `0`, empty `0`, orphan `0`

Key numerical results remained unchanged after the fixes.

## Orchestrator Smoke Checks After VERIFY

The orchestrator independently ran:

- `git diff --check`: PASS
- `pixi run lint-plots`: PASS, no plotting violations in 25 files
- Figure registry smoke test: `figures=10 registered_files=20 missing=0 empty=0 orphan=0`

## VERIFY Status

Both required VERIFY follow-ups were sent and satisfactory responses were received. The phase may proceed to per-figure validation swarm before blocking review.
