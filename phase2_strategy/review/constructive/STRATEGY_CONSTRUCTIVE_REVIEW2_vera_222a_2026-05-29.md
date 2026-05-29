# Phase 2 Strategy Constructive Re-Review

Session: `vera_222a`
Date: 2026-05-29
Artifact: `phase2_strategy/outputs/STRATEGY.md`
Scope: fresh constructive review after the ITERATE fix cycle

## Verdict

ITERATE.

The strategy is now materially stronger than the previous reviewed version. The
mass-extraction attempt is binding instead of optional, the fake-background and
sideband protocol is quantitative, the VBF recovery/downscope path is explicit,
the angular/NN promotion gates are operational, and the final AN comparability
plan is broad enough to support an honest note. I do not find any remaining
Category A issue.

One Category B issue remains: the commitment registry now carries machine tags,
but several of those tags still do not point back to explicit anchors in the
strategy artifact itself. For a long downstream audit chain, that is still too
weak to pass.

## Findings

### B1. Commitment-origin traceability is still incomplete for non-decision tags.

Evidence:

- `COMMITMENTS.md:54-202` uses explicit origin tags for systematic rows,
  validation tests, flagship figures, and the final comparability plan:
  `[SP1]`-`[SP13]`, `[VT1]`-`[VT13]`, `[FIG1]`-`[FIG6]`, and
  `[REF-MATRIX]`.
- The strategy artifact contains the corresponding sections at
  `STRATEGY.md:369-449` (systematics), `451-481` (validation tests),
  `519-540` (flagship figures and comparability matrix), but it does not define
  any explicit `[SP*]`, `[VT*]`, `[FIG*]`, or `[REF-MATRIX]` anchors.
- Independent tag scan during this review found zero matches for those four tag
  families in `phase2_strategy/outputs/STRATEGY.md`, while the same tags are
  relied on throughout `COMMITMENTS.md`.

Why this matters:

The fix cycle solved the "untagged checkbox" problem inside `COMMITMENTS.md`,
but not the source-anchor problem in the strategy itself. Right now a future
reviewer can infer that `[VT8]` means validation test 8 because of section
ordering, but cannot grep an explicit `[VT8]` origin in `STRATEGY.md`. That is
fragile under future edits and weakens the audit trail the commitments file is
supposed to provide from Phase 2 through Doc 4c.

Requested fix:

Make the origin mapping explicit in one of these two ways:

1. Add bracketed anchors in `STRATEGY.md` for the systematic rows, validation
   tests, flagship figures, and the comparability-matrix block, or
2. Retag the affected `COMMITMENTS.md` entries so they point only to anchors
   that already exist verbatim in `STRATEGY.md`.

I do not need new physics content here. This is a narrow traceability repair.

## Category C Suggestions

### C1. Add a compact "Phase 3 gates at a glance" table.

Evidence:

- The operational gates are now present, but spread across
  `STRATEGY.md:239-259`, `302-327`, `329-366`, and `550-569`.

Why this would help:

The strategy is now dense with valid gates. A one-screen summary table would
reduce the chance that the Phase 3 executor misses one of the sideband, TTBar,
VBF, or NN viability conditions while implementing the plan.

### C2. Make the eventual comparison figure explicitly include SM fiducial
prediction rows when a fiducial conversion exists.

Evidence:

- `STRATEGY.md:530-540` requires a comparison matrix.
- `COMMITMENTS.md:206-231` already stores SM fiducial prediction context for
  CMS-HIG-16-041 and CMS-HIG-19-001.

Why this would help:

The comparison plan is already broad enough to advance once B1 is fixed, but
the final Figure 6/Table will be clearer if the theory/SM fiducial prediction
row is explicitly expected whenever the analysis performs a fiducial
conversion.

## What Improved Since The Previous Review

- Binding simultaneous mass-extraction attempt:
  `STRATEGY.md:135-163`
- Quantitative DY/TTBar sideband protocol:
  `STRATEGY.md:239-259`
- Explicit VBF recovery/downscope gate under current path permissions:
  `STRATEGY.md:302-327`
- Operational angular/NN viability criteria:
  `STRATEGY.md:329-366`
- Reviewable fallback-systematics hierarchy:
  `STRATEGY.md:419-448`
- Final AN comparability matrix concept is now comprehensive in scope:
  `STRATEGY.md:533-540`

## Bottom Line

No Category A remains. The strategy is close to ready, but I do not recommend
advance with the current source-tag mismatch between `COMMITMENTS.md` and
`STRATEGY.md`. Fix that traceability gap and this constructive lane should pass.
