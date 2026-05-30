# Critical Reviewer Log: rainer_114e

Date: 2026-05-30
Phase: Phase 4a expected inference

## Context Read

- Read `TOGGLES.md`: `REVIEW_MODEL_DIVERSITY=true`, `MCP_ALPHAXIV=false`, `MCP_LEP_CORPUS=false`; no MCP calls made.
- Read `mcp_manifest.json` for disabled fallback context only.
- Read `agents/critical_reviewer.md` and applied the evidence-based, decision-traceability, systematic-audit, and completeness checks.
- Read Phase 4a spec, methodology review focus, plotting appendix, prompt, experiment log context, `COMMITMENTS.md`, Phase 2 strategy, Phase 3 selection handoff, Phase 4a plan/VERIFY/per-figure validation/artifact/FIGURES, result JSON, and Phase 4a source files.
- `conventions/fitting.md` referenced by the Phase 4a template is absent. A `conventions/` symlink exists with `extraction.md`, `search.md`, `unfolding.md`, and plotting/typesetting helpers; I used the Phase 4a spec, Phase 2 strategy, `COMMITMENTS.md`, and methodology as governing completeness sources.

## Checks Run

- Result JSON spot check with `pixi run py`: confirmed `mu = 1.0 -0.51674064615437 +0.6327358408468291`, symmetric expected uncertainty `0.5747382435005995`; low-count toys `n_toys=80`, success fraction `1.0`, median bias `-0.06064996537909362`; corruption p-values `0.01934008970762087` and `3.1049330873040137e-18`; precision ratio `3.192990241669998`.
- Figure registry smoke check with `pixi run py`: `entries 10 missing 0 empty 0 orphans 0`.
- Source audit found the mass scan implemented as an inclusive shifted-template profile rather than the required simultaneous category mass extraction.
- Source and JSON audit found hard-coded fallback normalization priors without the required SP2/effective-cross-section evidence table and no `systematics_sources.json`.
- Covariance audit found `expected_covariance.json` has top-level `mc_stat = 0.0029560843175981955` but `per_systematic.mc_stat = 0.0`; source audit confirms this comes from computing the per-systematic loop with `include_staterror=False`.

## Verdict

ITERATE. Category A/B blockers remain; Doc 4a should not begin until they are resolved and re-reviewed.
