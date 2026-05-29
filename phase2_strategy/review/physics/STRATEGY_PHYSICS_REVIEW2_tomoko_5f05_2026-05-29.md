# Phase 2 Strategy Physics Review 2

Session: `tomoko_5f05`
Date: 2026-05-29
Artifact: `phase2_strategy/outputs/STRATEGY.md`
Review type: fresh physics review after ITERATE fix

## Verdict

PASS.

I find no Category A or Category B physics blockers in the revised Phase 2
strategy. The previous blocking issue is resolved: the strategy now binds
Phase 4a to a simultaneous category mass extraction attempt, using the same
category workspace as the `mu` fit, a shared mass parameter, and `mu` profiled
in the mass scan rather than fixed (`STRATEGY.md:135-163`,
`STRATEGY.md:167-173`, `STRATEGY.md:201-204`). This is a credible strategy
for the requested detector-level open-data measurement, with honest downgrade
rules if the available M125-only samples cannot support a defensible mass
model.

No figures were produced in this strategy phase, so figure inspection is not
applicable.

## Physics Assessment

### Simultaneous Mass and `mu` Fit

The user's core request is a mass fit and `mu` extraction with all categories
fit simultaneously (`prompt.md:5`). The revised strategy now requires:

- Same simultaneous category workspace for `mu` and mass, with final-state
  categories and any validated classifier categories sharing a common mass
  parameter (`STRATEGY.md:140-142`).
- Explicit signal-shape construction from the M125 samples by reviewable
  morphing/shift or a `zfit`-style parametric signal model
  (`STRATEGY.md:143-149`).
- Profiling of `mu` during the mass extraction (`STRATEGY.md:150-151`).
- Injected-mass closure over at least three hypotheses, with a quantitative
  bias threshold of the larger of `0.2 GeV` or one-third of expected
  statistical mass uncertainty (`STRATEGY.md:152-157`).
- A downgrade path only after closure failure with attempted fix, or three
  concrete infeasibility attempts (`STRATEGY.md:158-163`).

This is now binding enough for Phase 2. It does not overclaim official CMS
mass precision: the limitations explicitly recognize the absence of
per-event mass uncertainties, official calibrations, and alternate mass-point
signal samples (`STRATEGY.md:77-88`, `STRATEGY.md:175-180`).

### VBF Plan

The user's prompt asks for a VBF category (`prompt.md:5`). The strategy gives
the physically correct answer for the available ntuples: no lepton-only
category may be labeled VBF, real VBF recovery requires jet information, and
if the jet information is unrecoverable Phase 3 must write a formal downscope
with comparison consequences (`STRATEGY.md:61-64`, `STRATEGY.md:302-327`).
That is preferable to inventing a VBF category from `pt4l` or angular score.

### Angular NN Feasibility

The angular/classifier plan is appropriately gated. The strategy uses the
retained lepton four-vectors and Z labels to compute standard H->ZZ->4l
angles, forbids `m4l` as a classifier input for the mass-shape fit, requires
stored-vs-recomputed mass and Z-mass closure, checks physical angular ranges,
and only promotes an NN if it beats a simpler baseline by at least 10 percent
in expected `mu` uncertainty while passing data/MC and GoF gates
(`STRATEGY.md:284-300`, `STRATEGY.md:329-366`). This is a sound physics
strategy for an open-data analysis with limited retained features.

### Fake Background Simplification

The nominal reducible-background plan follows the user instruction to use
DY+jets MC instead of a full fake-rate estimate (`prompt.md:5`,
`STRATEGY.md:81-83`, `STRATEGY.md:225-231`). The revised sideband treatment
is no longer circular: the signal window is excluded from sideband constraints,
the sidebands are predeclared, DY is constrained or floated depending on
statistics, and TTBar has a numeric inclusion/omission threshold
(`STRATEGY.md:239-259`). This is not official-quality Z+X modeling, but it is
honestly treated as a comparability limitation (`STRATEGY.md:581-582`).

### Systematics and Validation

The systematic plan now covers the main physics risks for a detector-level
template fit: luminosity, prompt effective cross sections, MC statistics,
lepton efficiency and momentum scale/resolution, reducible and irreducible
backgrounds, classifier modeling, angular reconstruction, and category
migration (`STRATEGY.md:371-392`). The fallback evidence rules make nuisance
choices reviewable and machine-readable rather than arbitrary
(`STRATEGY.md:419-449`). The validation suite includes provenance,
normalization, input modeling, angular closure, approach comparison, signal
injection at `mu = 0, 1, 2, 5`, GoF, pulls/impacts, 10 percent data stability,
mass-template closure, and category viability (`STRATEGY.md:451-481`).

### Comparison Scope and Honest Limitations

The comparison plan is sufficiently comprehensive for Phase 2. It records
CMS-HIG-16-041, CMS-HIG-19-001, HEPData, and PDG targets
(`STRATEGY.md:511-517`) and requires a final AN comparability matrix covering
inclusive `mu`, mass, fiducial cross section, width, production-sensitive
categories, VBF categories, and reducible-background treatment before
computing pulls (`STRATEGY.md:533-540`). The strategy repeatedly distinguishes
matched results from approximated or unavailable comparisons, which is the
right posture for this open-data scope.

## Findings

### Category A

None.

### Category B

None.

### Category C

1. M125-only mass morphing closure should be described downstream as an
   implementation and modeling-stress validation, not as an independent
   generator-level validation. With only M125 signal samples, pseudo-data made
   from the same shift/morphing family used in the fit can be tautological.
   The strategy already mitigates this by requiring explicit limitations,
   closure thresholds, and either a parametric-shape comparison or documented
   infeasibility (`STRATEGY.md:143-163`, `STRATEGY.md:211-217`). This is a
   documentation caution for Phase 4/AN, not a blocker for Phase 2.

## Final Judgment

I would approve this revised strategy to proceed to Phase 3. The mass and
`mu` extraction is now binding and reviewable, the VBF and angular-NN plans
respect the actual retained information, the DY-only fake approximation is
controlled rather than hidden, and the reference-comparison scope is honest.
