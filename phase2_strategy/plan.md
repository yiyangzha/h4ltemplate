# Phase 2 Strategy Plan

Session: `viktor_dfa6`
Date: 2026-05-29

## Scope

Produce the Phase 2 detector-level strategy for the CMS Open Data 2017
H->ZZ->4l mass and signal-strength measurement. No ROOT exploration or
analysis scripts will be written in this phase unless a later review asks for
a narrow mitigation prototype. The strategy will use Phase 1 artifacts as the
data/MC truth source and public web/INSPIRE/arXiv/CMS/HEPData/PDG fallback
literature routes because `MCP_ALPHAXIV=false` and `MCP_LEP_CORPUS=false`.

## Read-In Checklist

- DONE: `TOGGLES.md`, `CLAUDE.md`, `prompt.md`, `paths.json`,
  `agents/executor.md`
- DONE: `phase2_strategy/CLAUDE.md`
- DONE: `methodology/03-phases.md`, `03a-orchestration.md`,
  `05-artifacts.md`, `06-review.md`, `07-tools.md`, `11-coding.md`
- DONE: `conventions/extraction.md`
- DONE: Phase 1 artifacts and review/state files listed in the executor
  prompt

## Strategy Elements To Write

1. Define the observable: reconstructed four-lepton invariant mass in the
   CMS-HIG-16-041 fit window, detector-level categories, and signal-strength
   parameter `mu`.
2. Choose the statistical technique: binned simultaneous template likelihood
   using `pyhf`; explicitly document why `conventions/extraction.md` does not
   apply.
3. Freeze data-source policy: primary prompt paths are binding unless Phase 3
   documents a formal provenance change.
4. Define at least two qualitatively different Phase 3 selection approaches:
   a cut-based/reference-like approach and a classifier/category approach with
   strict data/MC input validation before training.
5. Define the category plan: inclusive/channel categories as guaranteed;
   VBF-like category only after jet-source recovery or formal downscope.
6. Define angular-NN feasibility path: compute rest-frame angular inputs from
   retained lepton four-vectors if validated; otherwise downscope with a
   diagnostic appendix.
7. Classify all backgrounds and specify the reducible-background simplification
   requested by the user: DY+jets MC only, with validation and an explicit
   comparability limitation.
8. Enumerate systematics and validation tests. Use reference H->4l analyses
   and applicable tool/method conventions, not the closed-form extraction
   convention, as the binding source list.
9. Estimate precision from Phase 1 MC statistics and reference luminosities,
   with a realistic caveat that the 10 fb^-1 open-data result will be
   statistics and method limited.
10. Build the reference-analysis table and `[REF]` entries with central values,
    uncertainties, methods, and MC-size status or `NOT FOUND`.
11. Define six flagship figures and the exact Phase 3 instructions required to
    make the downstream work reviewable.
12. Update root `COMMITMENTS.md` with systematics, validation tests,
    flagship figures, cross-checks, comparison targets, and `[REF]` entries.

## Phase 1 Constraints And Mitigations To Carry

- [A1] Primary and local ROOT copies differ. Mitigation: freeze primary paths
  and require Phase 3 reproducibility checks that record file sizes and entry
  counts before processing.
- [A2] Prompt effective MC cross sections are user-provided. Mitigation:
  require Phase 3 public-source/campaign-name validation where possible and
  closure/yield sanity checks before any yield-normalized fit is accepted.
- [A3] No jet/VBF branches. Mitigation: require provenance recovery attempt
  for jet information; if not recoverable, use no fake VBF category and
  document the impact with a review-gated downscope.
- [A4] No precomputed MELA/angular branches. Mitigation: require computation
  of angular primitives from lepton four-vectors and validate their kinematic
  consistency before using a NN.
- [A5] No truth-level branches. Mitigation: use sample-level labels only for
  MC classifier training and split MC for closure; do not claim truth-matched
  closure.
- [A6] `miniRelIso` tails and small `pvNdof`. Mitigation: exclude from default
  training/selection unless Phase 3 data/MC validation passes and calibration
  is documented.

## Planned Outputs

- `phase2_strategy/outputs/STRATEGY.md`
- root `COMMITMENTS.md`
- `phase2_strategy/logs/executor_viktor_dfa6_<timestamp>.md`
- appended root `experiment_log.md`

## Self-Check Before Completion

Run the Phase 2 pre-review checklist from `phase2_strategy/CLAUDE.md` by
inspection. Because Phase 2 produces no figures or scripts, no plot lint or
pixi task updates are expected unless the plan changes.
