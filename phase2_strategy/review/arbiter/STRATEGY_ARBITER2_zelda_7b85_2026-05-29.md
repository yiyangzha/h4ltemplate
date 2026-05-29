# Phase 2 Strategy Arbiter 2

Session: `zelda_7b85`
Date: 2026-05-29
Artifact: `phase2_strategy/outputs/STRATEGY.md`
Review type: fresh arbiter after first fix cycle

Reviews adjudicated:

- `phase2_strategy/review/physics/STRATEGY_PHYSICS_REVIEW2_tomoko_5f05_2026-05-29.md`
- `phase2_strategy/review/critical/STRATEGY_CRITICAL_REVIEW2_ursula_ee36_2026-05-29.md`
- `phase2_strategy/review/constructive/STRATEGY_CONSTRUCTIVE_REVIEW2_vera_222a_2026-05-29.md`

## Verdict

ITERATE.

The first fix cycle resolved the prior physics and critical blockers, and the
fresh physics and critical reviewers both PASS. The fresh constructive
Category B finding stands: `COMMITMENTS.md` now relies on `[SP*]`, `[VT*]`,
`[FIG*]`, and `[REF-MATRIX]` tags, but `STRATEGY.md` does not explicitly
define those tag namespaces or anchors. Under methodology §6.1, Category B
items must be fixed before PASS. This is not a physics regression, but it is a
cheap traceability repair that strengthens the downstream audit chain.

No plot-validator red flags exist for this strategy phase because no figures
were produced.

## Structured Adjudication Table

| # | Finding | Source | Their Cat | Final Cat | Rationale |
|---|---------|--------|-----------|-----------|-----------|
| 1 | Prior mass-extraction, convention-coverage, fake-background, VBF, angular/NN, comparability, and fallback-systematics blockers remain fixed after the first ITERATE cycle. | Physics, Critical, targeted verification | PASS / fixed | None | Accepted as resolved. The targeted verifier found all 11 prior Required Fix List items fixed. The fresh physics review specifically verifies the binding simultaneous mass extraction with shared categories, explicit morphing/parametric shape path, `mu` profiled, injected-mass closure, and hard downgrade criteria in `STRATEGY.md:135-163`. The fresh critical review verifies the prior A/B fixes, including `[D1]`-`[D9]` carryover in `COMMITMENTS.md:17-50`, convention mapping in `STRATEGY.md:394-417`, signal injection at `mu = 0, 1, 2, 5` in `STRATEGY.md:470-471`, and fake-background thresholds in `STRATEGY.md:241-259`. |
| 2 | Non-decision commitment tags are not explicitly anchored in `STRATEGY.md`: `[SP*]`, `[VT*]`, `[FIG*]`, and `[REF-MATRIX]` appear in `COMMITMENTS.md` but not in the strategy artifact. | Constructive | B | B | Accepted. Direct grep evidence supports the reviewer: `COMMITMENTS.md` uses these tags throughout, including `[SP1]`-`[SP13]` at lines 54-90, `[VT1]`-`[VT13]` at lines 17-46 and 100-136, `[FIG1]`-`[FIG6]` at lines 32-46 and 144-154, and `[REF-MATRIX]` at lines 154 and 182-200. The matching grep for those tag families in `phase2_strategy/outputs/STRATEGY.md` returned no lines. The strategy sections are present (`STRATEGY.md:369-449`, `451-481`, `519-540`), but the tags themselves are not explicit anchors. Future reviewers can infer the mapping from section order, but cannot grep the declared origin. That is a real traceability weakness and the requested fix is under one agent-hour. |
| 3 | Add a compact Phase 3 gates table. | Constructive | C | C | Accepted as optional. The gates exist, but are spread across `STRATEGY.md:239-259`, `302-327`, `329-366`, and `550-569`. This is useful but not blocking. |
| 4 | Make the eventual comparison figure explicitly include SM fiducial prediction rows when a fiducial conversion exists. | Constructive | C | C | Accepted as optional. The comparison machinery already covers the necessary Phase 2 scope through `STRATEGY.md:533-540` and `COMMITMENTS.md:206-231`; this can be folded into a later edit but does not block by itself. |

## Dismissals

No Category A or B reviewer finding is dismissed.

The constructive B finding is not dismissed because it is factually correct,
cheap to fix, and directly affects the auditability of Phase 3 through Doc 4c.
It does not change the physics method or conclusions, but the review protocol
does not allow PASS with an unresolved Category B.

## Regression Check

No Phase 2 regression investigation is triggered.

- Validation test failure without three remediation attempts: NO. No fit or
  closure validation has run in this strategy phase.
- Single systematic greater than 80% of total uncertainty: NO. No fitted
  uncertainty budget exists yet.
- GoF toy inconsistency: NO. No GoF toys exist yet.
- More than 50% bin exclusion: NO. No binning gate has run yet.
- Tautological comparison presented as validation: NO current trigger. The
  strategy includes downstream validation and comparability obligations, but
  no result is being claimed here.
- Data/MC disagreement on observable or MVA inputs: NO current trigger. This
  remains a Phase 3 validation obligation through the input-modeling gate.
- Binding commitments silently replaced: NO. The remaining issue is tag
  origin anchoring, not a changed physics decision.

## Required Fix List For ITERATE

1. Add explicit source anchors for the non-decision tag families. Either:
   - add bracketed anchors in `STRATEGY.md` for the systematic-plan rows
     (`[SP1]`-`[SP13]`), validation tests (`[VT1]`-`[VT13]`), flagship figures
     (`[FIG1]`-`[FIG6]`), and comparability matrix (`[REF-MATRIX]`), or
   - retag `COMMITMENTS.md` so every tag points to an anchor already present
     verbatim in `STRATEGY.md`.

2. Keep the fix narrow. Do not change the physics strategy unless the tagging
   edit exposes a genuine mismatch. The expected verification is a grep showing
   every non-decision tag family used in `COMMITMENTS.md` has an explicit
   origin in `STRATEGY.md`, plus a short statement that no strategy content
   changed beyond traceability labels.

3. Category C suggestions may be applied opportunistically, but they are not
   required for PASS.

After this narrow fix, request targeted verification of the tag-anchor repair
and then a fresh arbiter decision. The full physics strategy does not need to
be re-litigated unless the fix changes substantive content.
