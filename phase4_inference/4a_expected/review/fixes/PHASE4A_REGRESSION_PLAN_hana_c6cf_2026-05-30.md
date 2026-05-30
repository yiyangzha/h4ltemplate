# Phase 4a Regression Plan

Session: hana_c6cf
Date: 2026-05-30

## Plan

1. Read required phase instructions, upstream artifacts, reviewer findings, source files, current JSON outputs, and pixi tasks.
2. Audit Phase 3 MVA training window, inputs, validation gates, and approach-comparison promotion logic.
3. Update Phase 3 code and artifacts so MVA training/evaluation uses 70 < m4l < 170 GeV, excludes m4l from classifier inputs, tries at least one meaningful improvement, and promotes MVA only if it beats S1 and passes all gates.
4. Audit Phase 4a expected inference code for fit-window metadata, broad plot windows, mass scan range, nuisance payload structure, MC-stat treatment, and corruption sensitivity.
5. Update Phase 4a code/results to preserve 105 < m4l < 140 GeV for signal strength, use broad 70 < m4l < 170 GeV displays where appropriate, broaden/document the mass scan, add per-systematic shifted-bin payloads and figures, document grouped MC-stat downscope, and run or quantify corruption sensitivity for the simultaneous final-state workspace.
6. Regenerate Phase 3 and Phase 4a outputs through pixi tasks.
7. Run `pixi run lint-plots`, registry smoke tests, and JSON sanity checks for required metadata and payloads.
8. Update Phase 3/4a artifacts, commitments/log/session markdown, write regression summary and executor log, then commit passing truthful outputs.

## Non-Tuning Policy

No fit parameter, classifier setting, scan range, or systematic treatment will be chosen to improve numerical agreement with CMS-HIG-16-041. The reference methodology guides fit-window and template-likelihood structure only.
