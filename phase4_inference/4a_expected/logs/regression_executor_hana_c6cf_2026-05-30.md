# Regression Executor Log

Session: hana_c6cf
Date: 2026-05-30

## Milestones

- Read `TOGGLES.md`, `agents/executor.md`, Phase 3/4a instructions, strategy/selection artifacts, Dmitri critical review, Celeste plot validation, relevant source, and current JSON outputs.
- Wrote regression ticket and plan before code edits.
- Updated Phase 3 MVA code to record broad-window training/evaluation metadata, preserve `m4l` exclusion, and add a tuned BDT trial.
- Regenerated Phase 3 with `pixi run p3-all`; S1 remains nominal because S2 still fails promotion gates.
- Updated Phase 4a expected inference to add broadened mass scan metadata, final-state corruption sensitivity, per-systematic shifted-bin payloads, and formal MC-stat downscope labeling.
- Added broad expected `m4l` and systematic-shift summary figures.
- Regenerated Phase 4a with pixi tasks and repeated plotting/artifact updates after documenting the final-state corruption limitation.
- Ran `pixi run lint-plots`, registry smoke tests, and JSON sanity checks.

## Open Issue

The final-state simultaneous 20 percent corruption test is not fully sensitive in both directions. The `+20%` mass-response corruption fails as required; the `-20%` direction does not (`p = 0.4595`). This is recorded as a quantitative limitation in `expected_validation.json` and `INFERENCE_EXPECTED.md`.
