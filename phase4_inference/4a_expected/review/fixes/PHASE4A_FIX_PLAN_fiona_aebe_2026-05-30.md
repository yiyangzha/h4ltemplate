# Phase 4a Fix Plan

Session: `fiona_aebe`
Date: 2026-05-30

## Scope

Resolve the blocking Phase 4a review findings without touching unrelated
phases. All analysis execution will use `pixi run ...`; MCP tools are disabled
by `TOGGLES.md`.

## Planned fixes

1. D9 mass-extraction traceability
   - Replace the inclusive shifted-template mass scan with a simultaneous
     final-state category scan using the same `4mu`, `4e`, and `2e2mu`
     categories as the expected `mu` workspace.
   - Profile `mu` in each mass-hypothesis fit and in injected-mass closure
     fits.
   - Write explicit method metadata in `expected_mass_scan.json` showing the
     categories, active nuisances, template-shift method, profiled parameter,
     and closure result.

2. Systematic-source evidence completeness
   - Add `analysis_note/results/systematics_sources.json` with one row per
     Phase 4a source, including source name/commitment label, variation size,
     citation or analysis trail, fallback flag, affected templates/processes,
     evaluation method, and Phase 4a status.
   - Add explicit SP2 prompt-effective-cross-section and SP6 pileup/PV rows.
   - Make fallback priors explicit for signal theory, qqZZ, ggZZ, and DY.
   - Keep `expected_systematics.json`, `INFERENCE_EXPECTED.md`,
     `COMMITMENTS.md`, and `experiment_log.md` consistent with the new source
     table.

3. MC-stat consistency
   - Keep the actual grouped MC-stat approximation unless full per-bin
     `staterror` is implemented.
   - Record grouped MC-stat as a nonzero component consistently in
     `expected_covariance.json` and label it as grouped, not bin-by-bin.
   - Update commitments to avoid overclaiming full bin-by-bin profiling.

4. Plot-validation blockers
   - Replace custom CMS/Open Simulation text in
     `expected_m4l_final_state_templates` with `mh.label.exp_label(...)` on
     every independent panel.
   - Move the `expected_mu_profile_scan` legend away from the rising
     high-`mu` profile tail.
   - Address the final-state template legend placement with `mpl_magic(ax)` or
     an equivalent non-overlap placement.
   - Regenerate the full registered Phase 4a figure set.

## Verification

- Run `pixi run p4a-all`.
- Run `pixi run lint-plots`.
- Run a registry smoke test: `FIGURES.json` exists; all registered PNG/PDF
  files exist and are nonzero; no orphan PNG/PDF files exist in
  `outputs/figures/`; registered figure files are newer than the plotting
  script.
- Inspect the fixed `expected_m4l_final_state_templates.png` and
  `expected_mu_profile_scan.png`.
- Write a fix summary mapping every review finding to evidence, then commit
  only if verification passes.
