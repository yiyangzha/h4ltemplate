# Regression Ticket: Phase 3 / Phase 4a Targeted Update

Session: hana_c6cf
Date: 2026-05-30

## Scope

Targeted regression/update covering Phase 3 selection/MVA evidence and Phase 4a expected inference. The update addresses review findings and user instructions to align the fit window and broad mass treatment with the CMS-HIG-16-041 / JHEP 11 (2017) 047 methodology where appropriate, without tuning results to match the reference.

## Required Corrections

- Phase 3 MVA training/evaluation must use broad 70 < m4l < 170 GeV samples, keep m4l out of classifier inputs for mass-shape fits, and only promote MVA if it beats S1 and passes validation gates.
- Phase 4a signal-strength fit window must remain 105 < m4l < 140 GeV.
- Phase 4a m4l distribution plots should show 70 < m4l < 170 GeV where appropriate.
- Phase 4a mass/mH scan must not be a narrow near-125-only check; scan range, grid, exclusions, and limitations must be machine-readable and documented.
- Dmitri A1: add per-systematic shifted-bin payloads with bin edges and nominal/up/down or equivalent shifts for active nuisances by channel/process where applicable; add registered figure(s) for per-bin shape effects and rate-only impacts without inventing fake shapes.
- Dmitri B1: grouped MC-stat must be documented as a formal downscope/approximation, not a completed full bin-by-bin profiling treatment.
- Dmitri B2: run corruption sensitivity in the final-state simultaneous workspace if feasible, or document quantitative infeasibility.

## Constraints

- Do not force or tune agreement with CMS-HIG-16-041.
- Do not use the reference measured result as a fit input or optimization target.
- Use pixi tasks/commands for Python and analysis execution.
- Keep edits scoped to Phase 3, Phase 4a, allowed tracking files, and review/handoff markdown.

## Verification Target

Verification must demonstrate regenerated Phase 3 and Phase 4a artifacts, passing plot lint, registry smoke tests, metadata sanity checks, and no forced-alignment wording.
