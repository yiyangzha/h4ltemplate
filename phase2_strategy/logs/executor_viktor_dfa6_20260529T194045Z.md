# Phase 2 Executor Log

Session: `viktor_dfa6`
Started: 2026-05-29T19:40:45Z

## Milestones

- Read required runtime, phase, methodology, convention, prompt, path,
  executor, Phase 1 artifact, Phase 1 review, and commitment files.
- Confirmed `MCP_ALPHAXIV=false` and `MCP_LEP_CORPUS=false`; no MCP tools
  called.
- Created `phase2_strategy/plan.md` before strategy prose.
- Ran public fallback literature searches for CMS-HIG-16-041,
  CMS-HIG-19-001, PDG Higgs/gauge summaries, H->4l systematics, and angular
  variables.
- Fetched public CMS pages for CMS-HIG-16-041 and CMS-HIG-19-001 and used
  their abstract/figure descriptions for numerical reference values,
  category/mass-window evidence, and systematic-source coverage.
- Read `conventions/extraction.md`, `conventions/search.md`, and
  `conventions/unfolding.md`. Decision: extraction and unfolding do not
  govern this detector-level template fit; profile-likelihood validation
  expectations from the search convention are applicable by analogy.
- Wrote `phase2_strategy/outputs/STRATEGY.md` with [A]/[L]/[D] labels,
  selection approaches, systematic plan, precision estimates, reference
  table, flagship figures, and Phase 3 instructions.
- Updated root `COMMITMENTS.md` with binding systematics, validation tests,
  flagship figures, cross-checks, and `[REF]` entries.

## Key Decisions

- [D1] Nominal downstream processing must use the prompt/user-specified
  primary paths, not local copies.
- [D2] Nominal inference is a binned simultaneous template likelihood with
  `pyhf`/HistFactory-style workspaces.
- [D3] Fit window fixed to `105 < m4l < 140 GeV`.
- [D4] Guaranteed categories are final state channels and validated
  classifier-score bins; VBF requires jet recovery or formal downscope.
- [D7] Classifier/NN inputs require a chi2/ndf and data/MC modeling gate before
  training.

## Open Issues For Review

- Public validation of prompt effective cross sections may remain incomplete
  for effective filtered samples; Phase 3 is instructed to document search
  trails and carry a normalization uncertainty if public metadata are not
  found.
- VBF categorization is not feasible from the current branch inventory unless
  Phase 3 recovers jet information from provenance/upstream sources.
- A Higgs mass result requires validated template morphing; otherwise the
  analysis should report a detector-level peak estimator with limited scope.

## VERIFY Follow-up 2 Self-Critique

Date: 2026-05-29

Critic findings and fixes:

- Fit-window citation was too indirect. Fixed `STRATEGY.md` to cite the
  CMS-HIG-16-041 public-page mass/width likelihood-scan figure text and the
  CMS-HIG-19-001 category/discriminant figure text explicitly.
- Method parity was overstated. Added [L5] and [D9], requiring a Phase 4a
  parametric mass-shape cross-check or documented infeasibility after three
  concrete attempts.
- VBF downscope gate was too weak. Expanded it from one recovery step to
  provenance, branch-inventory, and allowed-source join checks before formal
  downscope.
- Angular-NN gate was too soft. Added stored-vs-recomputed mass tolerances,
  physical-range counts, held-out validation, and a requirement that a NN beat
  a BDT/logistic baseline by at least 10% expected `mu` uncertainty before
  promotion.
- `COMMITMENTS.md` incorrectly used `[D]` for Jet/VBF systematics before a
  formal downscope had been reviewed. Changed it back to an open `[ ]`
  decision gate.
- HEPData source ID was potentially confusing because Phase 1 mentions an
  `ins1608166` trail while the CMS public page links `ins1608162`. Added a
  commitment note requiring downstream phases to use the CMS-linked record or
  document redirects.
