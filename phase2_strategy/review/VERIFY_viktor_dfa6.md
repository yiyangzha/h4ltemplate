# Phase 2 VERIFY Exchange — viktor_dfa6

Date: 2026-05-29

## Follow-up 1 Prompt

Re-read your `phase2_strategy/plan.md` line by line. For each item, verify it is DONE, not merely started. Run every self-check from `phase2_strategy/CLAUDE.md`. Show evidence: `ls -la` style file listing with mtimes for `phase2_strategy/outputs/`, explicit DONE for each plan item, evidence that `COMMITMENTS.md` has all required sections populated, exact source/search evidence for every numeric reference value used, and explicit notes for items that are intentionally not applicable in Phase 2. Only signal completion when every item is done and every check passes.

## Follow-up 1 Response Summary

Executor reported PASS with:

- `phase2_strategy/outputs/STRATEGY.md` present, mtime 2026-05-29 19:43, size 25811 bytes.
- `phase2_strategy/plan.md`, `COMMITMENTS.md`, `experiment_log.md`, and executor log present.
- All 12 `plan.md` strategy items marked DONE.
- `COMMITMENTS.md` populated with systematic sources, validation tests, flagship figures, cross-checks, comparison targets, and `[REF-*]` entries.
- Numeric source trails for user luminosity, CMS-HIG-16-041 fit window and published values, CMS-HIG-19-001 values, PDG values, and MC entry counts.
- Phase 2 self-check passed by inspection.
- Not applicable items documented: no ROOT exploration, no code/scripts/figures, no pixi task updates, no plot lint, no MCP calls.

## Follow-up 2 Prompt

Switch to critic mode. Re-read `phase2_strategy/outputs/STRATEGY.md` and `COMMITMENTS.md` as a skeptical collaboration reviewer. For each major claim: is the evidence convincing or merely asserted? Check especially numeric citations/source IDs, the fit-window citation, the method parity with CMS-HIG-16-041/CMS-HIG-19-001, whether every Phase 1 constraint has a concrete mitigation, whether VBF and angular-NN downscope gates are strong enough, and whether COMMITMENTS.md is sufficiently binding for Phase 3/4 review. Fix what you find. If you find zero issues, that is not satisfactory; look harder and report concrete criticisms, fixes applied, regenerated files, and any remaining limitations.

## Follow-up 2 Response Summary

Executor found and fixed issues:

- Fit-window citation was too indirect for the user-requested CMS-HIG-16-041 parity.
- Method parity was overstated; a binned `pyhf` template fit is not equivalent to the official CMS profile-likelihood machinery with richer discriminants/calibrations.
- VBF downscope gate was too weak.
- Angular-NN promotion criteria needed hard validation and a baseline comparison.
- `COMMITMENTS.md` incorrectly used `[D]` for Jet/VBF before a formal reviewed downscope existed.
- HEPData source ID was ambiguous: Phase 1 mentions an `ins1608166` trail, while the CMS public page links `ins1608162`.

Fixes applied:

- Updated `STRATEGY.md` with `[L5]` method-parity limitation, `[D9]` Phase 4a parametric mass-shape cross-check, stronger `105 < m4l < 140 GeV` CMS-HIG-16-041 citation, stronger VBF recovery checklist, and harder angular-NN gates.
- Updated `COMMITMENTS.md`: changed Jet/VBF from premature `[D]` downscope to open `[ ]` decision gate, added `[D9]`, VBF downscope review gate, angular/NN promotion gate, stored-vs-recomputed four-vector closure, `[REF-METHOD-PARITY]`, and HEPData ID ambiguity note.
- Updated executor log and `experiment_log.md`.

Remaining limitations:

- VBF remains infeasible unless Phase 3 recovers jet information.
- Mass measurement remains limited unless Phase 4a validates template morphing or a parametric mass-shape cross-check.
- HEPData record identity must be verified downstream because Phase 1 and the CMS public page point to different record trails.
