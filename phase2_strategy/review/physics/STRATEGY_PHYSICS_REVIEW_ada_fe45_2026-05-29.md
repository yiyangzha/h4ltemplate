# Phase 2 Strategy Physics Review

Session: `ada_fe45`
Date: 2026-05-29
Artifact reviewed: `phase2_strategy/outputs/STRATEGY.md`

## Verdict

ITERATE.

I would approve most of the strategy as a realistic open-data H->ZZ->4l
signal-strength plan: the `105 < m4l < 140 GeV` fit window is appropriate,
the VBF downscope path is honest, the angular/classifier feasibility gates are
mostly strong, and the comparison targets are sensible. However, the mass
measurement is not yet a publishable physics plan. The prompt asks for a fit of
the mass and `mu`, with simultaneous category treatment; the strategy currently
makes `mu` the true nominal fit and lets the mass result degrade to an optional
or fallback estimator. That must be tightened before Phase 3/4 execution.

No figures or compiled PDF were present in this Phase 2 strategy artifact, so
there were no images to inspect.

## Findings

### A1. Nominal mass extraction is under-specified and not clearly simultaneous with the category fit

Evidence:
- The observable section defines `mu` as the fit parameter and calls mass only a
  "secondary observable"; the fallback is a detector-level peak estimator
  (`STRATEGY.md:135-147`).
- The likelihood model lists `mu` as the parameter of interest, but does not
  define `mH` as a parameter in the simultaneous model (`STRATEGY.md:160-172`).
- The method-parity requirement asks only for a parametric mass-shape
  "cross-check" if feasible, with documented infeasibility allowed
  (`STRATEGY.md:174-180`, `STRATEGY.md:333-335`).
- The open issues again state that the mass result may become only a limited
  peak estimator (`STRATEGY.md:431-434`).

Why this matters:
The user asked for a mass fit and signal-strength extraction, with all
categories fitted simultaneously when extracting the mass. A peak-position
cross-check is not the same physics object as a simultaneous profile-likelihood
mass measurement. With only M125 signal MC, it is acceptable to state that an
official-quality mass scan is not possible, but the strategy must still define
the nominal mass-extraction attempt, its validation tests, and the exact
conditions under which the deliverable is downgraded.

Concrete fix:
Revise the strategy to define a binding Phase 4 mass plan:
- Specify whether the nominal model is a 2D or staged profile likelihood in
  `(mu, mH)` across all selected categories, or a conditional `mH` scan with
  `mu` profiled.
- Define the mass-template construction explicitly: e.g. parametric signal
  shape fit with a floating peak, template morphing/shift from M125 with
  closure, or an unbinned category-simultaneous fit.
- Require MC pseudo-data closure at injected mass shifts, not only `mu = 0,1,2`.
  If only M125 is available, use controlled shifted-template toys and quote the
  induced bias.
- Set a hard promotion rule: only call the result a mass fit if the simultaneous
  category model passes closure with bias smaller than a stated fraction of the
  statistical uncertainty. Otherwise label it everywhere as a detector-level
  peak estimator and state that the requested mass fit was infeasible with the
  available samples.

### B1. DY-only fake model is acceptable as a user simplification, but the TTBar/fake decision rule needs to be quantitative

Evidence:
- The strategy follows the prompt by making DY+jets the nominal reducible fake
  template and TTBar diagnostic only (`STRATEGY.md:81-83`,
  `STRATEGY.md:188-194`).
- It says TTBar should be included or assigned an omission systematic if
  non-negligible, but does not define "non-negligible" (`STRATEGY.md:309-310`).
- The cited selected-entry counts are low for both reducible samples: DY 463
  and TTBar 639 (`STRATEGY.md:362-366`).

Why this matters:
The prompt explicitly permits a simplified fake model, so I am not asking for a
full data-driven Z+X estimate. But TTBar is a provided sample and the selected
entry count is comparable to DY. A purely diagnostic treatment risks biasing
the signal window or sideband constraints if TTBar contributes a different
shape.

Concrete fix:
Before Phase 3 starts, add a quantitative TTBar/fake decision criterion to the
strategy or Phase 3 instructions. For example: if TTBar contributes more than a
specified fraction of the total reducible yield in the broad sideband or signal
window, include it as a separate nominal reducible component; otherwise assign
an omission systematic whose size is derived from the TTBar template. Also
define the sideband regions and whether the DY fake normalization is floated,
constrained, or fixed when sideband statistics are too low.

### B2. The mass-window choice is good, but sideband validation must not contaminate or tune the signal fit

Evidence:
- The fit window is fixed to `105 < m4l < 140 GeV` and broader
  `70 < m4l < 170 GeV` plots are designated as validation only
  (`STRATEGY.md:104-109`, `STRATEGY.md:218-219`).
- The reducible and ZZ backgrounds may be floated or constrained in sidebands
  (`STRATEGY.md:116-118`, `STRATEGY.md:308-310`).

Why this matters:
This is the right window for comparison to the reference analyses, but the plan
should prevent accidental circular tuning of the backgrounds using the same
events that define the Higgs signal extraction.

Concrete fix:
Define a sideband protocol before fitting: which mass regions are used for
background normalization checks, whether the Higgs signal window is excluded
from those constraints, and how uncertainties from sideband-derived constraints
enter the final simultaneous fit.

### C1. Angular NN plan is appropriately cautious; add one explicit overtraining and category-stability check

Evidence:
- The strategy excludes `m4l` from classifier inputs and requires data/MC input
  gates, mass-sculpting checks, and a held-out validation split
  (`STRATEGY.md:225-237`, `STRATEGY.md:275-291`).
- It requires the NN to beat a BDT/logistic baseline by at least 10% expected
  `mu` precision before promotion (`STRATEGY.md:288-291`).

Suggestion:
Add an explicit overtraining test and category-boundary stability check:
training-vs-validation score distributions for signal/background and a small
variation of score thresholds to show that the fitted `mu` and mass estimator
are stable. This is not a blocker because the current gates already address the
largest physics risks.

## Physics Approval Summary

Approved components:
- Observable and fit window: `105 < m4l < 140 GeV` is the right nominal signal
  fit window for comparison; broad mass plots are correctly treated as
  validation/sideband material.
- VBF plan: the strategy correctly refuses to call lepton-only categories VBF
  and requires a recovery attempt plus formal downscope if jets cannot be
  recovered.
- Angular/classifier feasibility: recomputing angles from four-vectors is
  reasonable, and the no-`m4l`, input-modeling, mass-sculpting, and baseline
  comparison gates are good.
- Reference comparisons: CMS-HIG-16-041, CMS-HIG-19-001, and PDG/world-average
  targets are included with appropriate caveats.
- Limitations: the document is unusually honest about missing official
  calibrations, data-driven fakes, VBF categories, and parametric mass modeling.

Blocking issue:
- The mass fit is not yet specified as a nominal simultaneous category
  extraction. Resolve A1 before I would sign off on the strategy.
