# Phase 2 Strategy Arbiter

Session: `albert_0ea5`
Date: 2026-05-29
Artifact: `phase2_strategy/outputs/STRATEGY.md`
Reviews adjudicated:

- `phase2_strategy/review/physics/STRATEGY_PHYSICS_REVIEW_ada_fe45_2026-05-29.md`
- `phase2_strategy/review/critical/STRATEGY_CRITICAL_REVIEW_boris_db73_2026-05-29.md`
- `phase2_strategy/review/constructive/STRATEGY_CONSTRUCTIVE_REVIEW_celeste_3982_2026-05-29.md`

## Verdict

ITERATE.

The strategy is directionally sound, but it cannot pass Phase 2 with the
current mass-extraction plan, convention coverage, and binding audit trail.
The physics and critical reviews independently identify the same blocking
problem: the user requested a simultaneous mass fit and `mu` extraction, while
the strategy currently makes `mu` the only explicit likelihood POI and leaves
mass as a secondary estimator or optional cross-check. The critical review's
commitment and convention-coverage findings are also substantiated by direct
comparison of `STRATEGY.md`, `COMMITMENTS.md`, and `conventions/search.md`.

No reviewer findings are dismissed. No plot-validator red flags exist for this
phase because the strategy phase produced no figures.

## Structured Adjudication Table

| # | Finding | Source | Their Cat | Final Cat | Rationale |
|---|---------|--------|-----------|-----------|-----------|
| 1 | Nominal mass extraction is under-specified and too easy to downgrade below the requested simultaneous category mass fit. | Physics, Critical | A, A | A | Accepted. `STRATEGY.md` defines `mu` as the only explicit fit POI (`lines 135-140`, `166-167`), calls mass a secondary observable with peak-estimator fallback (`lines 142-147`), and makes the parametric mass-shape fit a cross-check if feasible (`lines 174-180`, `333-344`). The prompt explicitly asks for a mass fit with all categories fit simultaneously. This blocks Phase 2. |
| 2 | `COMMITMENTS.md` does not explicitly carry all [D1]-[D9] strategy decisions. | Critical | A | A | Accepted. `STRATEGY.md` defines [D1]-[D9] (`lines 99-131`), but `COMMITMENTS.md` explicitly labels only [D2], [D7], and [D9] plus related A/L entries (`lines 14`, `47`, `53-55`, `84-94`). Missing [D3]-[D6] and [D8] are material fit/category/fake/modeling commitments. Later regression checks cannot enforce decisions that are not carried forward. |
| 3 | Adopted shape-fit/search convention is not enumerated row-by-row. | Critical | A | A | Accepted. The strategy adopts the shape-fit portion of `conventions/search.md` (`STRATEGY.md:151-158`). That convention requires explicit sources for signal modeling, background estimation, detector/reconstruction, and theory inputs (`conventions/search.md:43-94`), including pp replacements for beam-related rows (`lines 45-48`). The current systematic table (`STRATEGY.md:298-316`) covers many items but does not row-map signal acceptance/generator comparison, signal shape/mass-width variations, PDF/QCD scale acceptance for signal and ZZ, or inapplicable fragmentation/heavy-flavour rows. The Phase 2 template requires "Will implement" or "Not applicable because" for every required convention source. |
| 4 | Signal-injection validation omits the `5x` stress point from the adopted search convention. | Critical | B | B | Accepted. `conventions/search.md` specifies injections at `0x`, `1x`, `2x`, and `5x` (`lines 35-36`, `105-108`). The strategy and commitments list only `mu = 0, 1, 2` (`STRATEGY.md:336-337`; `COMMITMENTS.md:56-57`). Either add `5x` or justify a measurement-specific replacement stress test. |
| 5 | TTBar/fake-background treatment lacks a quantitative promotion or omission threshold. | Physics, Critical | B, B | B | Accepted. The strategy intentionally uses DY+jets as nominal fake proxy but leaves TTBar diagnostic unless "non-negligible" (`STRATEGY.md:81-83`, `188-194`, `309-310`). With DY and TTBar selected entries both low and comparable in Phase 1, "non-negligible" must be defined before Phase 3. |
| 6 | Sideband protocol is not specific enough to prevent signal-window tuning. | Physics | B | B | Accepted. The strategy allows background normalization to be constrained or floated in sidebands (`STRATEGY.md:116-118`, `308-310`) but does not define the sideband regions, whether the signal window is excluded from constraints, or how sideband-derived uncertainties enter the simultaneous fit. This is necessary to avoid circular tuning. |
| 7 | Fallback-driven systematic prescriptions are too vague to be reviewable. | Critical | B | B | Accepted. Terms such as "conservative closure-derived envelopes" and "scale reference if applicable" (`STRATEGY.md:300-303`) do not define a source hierarchy, envelope construction, or machine-readable evidence. Phase 2 need not provide final impacts, but it must define how fallback uncertainties are derived. |
| 8 | Luminosity nuisance treatment is ambiguous for the 10 fb^-1 subset. | Constructive | B | B | Accepted as a separate blocker, not folded away. Phase 1 records user-provided `10 fb^-1` and full-year CMS 2017 `42.12 +/- 0.34 fb^-1`; the strategy says to use the CMS uncertainty "as a scale reference if applicable" (`STRATEGY.md:300`). The nuisance prescription must state whether the subset inherits a cited luminosity uncertainty or is treated as user-provided with a conservative normalization envelope. |
| 9 | VBF recovery branch is operationally underspecified under current allowed paths. | Constructive | B | B | Accepted. The strategy says to check a safe join to an allowed upstream source (`STRATEGY.md:251-253`), but `paths.json` allows only the flat ntuple data and MC directories. The strategy should state that actual jet recovery requires expanded allowed inputs; otherwise Phase 3 should perform an immediate formal downscope after documenting branch/provenance and allow-list evidence. |
| 10 | Angular/NN category promotion needs a minimum-statistics viability gate. | Constructive | B | B | Accepted. The strategy has input-modeling, no-`m4l`, mass-sculpting, held-out validation, and 10% improvement gates (`STRATEGY.md:275-291`) but no hard minimum-statistics table/veto for category/bin sparsity. Given the low 10 fb^-1 candidate statistics cited in Phase 1 and the strategy's own low-yield concerns (`STRATEGY.md:362-366`), a relative Asimov improvement alone is not enough. |
| 11 | Final AN comparison needs an explicit comparability matrix. | Constructive | B | B | Accepted. The user asked for comprehensive comparison to CMS-HIG-16-041 as far as available ntuples allow. The strategy currently promises one comparison summary figure/table (`STRATEGY.md:393-394`) while `COMMITMENTS.md` lists reference quantities that are not all measured (`lines 105-143`). A bound matrix must classify each reference result/category as matched, approximated, or unavailable. |
| 12 | Commitment origin traceability is too weak for long-chain audit. | Constructive, Critical | C, A-related | B | Upgraded to B for the unlabeled-origin portion. Critical A1 already covers missing [D] labels as Category A. Beyond that, many generic `COMMITMENTS.md` checkboxes lack origin tags (`COMMITMENTS.md:17-32`, `39-46`, `58-61`, `70-80`, `95-101`). This is fixable now and materially improves Phase 4c/Doc auditability, so it should be addressed before PASS. |
| 13 | Angular/NN plan should add overtraining and category-boundary stability checks. | Physics | C | C | Accepted as a suggestion. Current gates already cover the largest blockers, but adding training-vs-validation score tests and score-threshold stability is cheap and aligns with the stronger B-level minimum-statistics gate. |
| 14 | HEPData source-ID ambiguity should be resolved before numerical extraction. | Critical | C | C | Accepted as a downstream cleanup item. The ambiguity is already documented in `STRATEGY.md:37-38` and `COMMITMENTS.md:115-120`; it need not block Phase 2 once the A/B items are fixed, but Phase 3/Doc phases should resolve it before tables/captions use HEPData values. |

## Regression Check

No Phase 2 regression investigation is triggered by this review cycle.

- Validation test failure without three remediation attempts: NO. Phase 2 has
  no fit validation outputs yet.
- Single systematic greater than 80% of total uncertainty: NO. No fitted
  uncertainty budget exists yet.
- GoF toy inconsistency: NO. No GoF toys exist yet.
- More than 50% bin exclusion: NO. No binning gate has run yet.
- Tautological comparison presented as validation: NO. Strategy-only phase;
  however, the mass-plan fix must avoid circular template calibration.
- Data/MC disagreement on observable or MVA inputs: NO current trigger.
  Phase 3 must evaluate this through the [D7] gate.
- Binding commitments fulfilled: NOT YET APPLICABLE, but the binding
  commitment registry is incomplete and therefore must be fixed before PASS.

## Required Fix List For ITERATE

The fixer can work from this list without re-reading the panel reviews:

1. Define a binding nominal mass-extraction attempt. Specify a simultaneous
   category mass model or scan with `mu` profiled, the signal-shape construction
   or morphing/shift procedure, injected-mass closure tests, and a hard
   downgrade rule. Add matching `COMMITMENTS.md` checkboxes. The mass result
   may be downgraded only after the documented attempt fails the stated closure
   criteria or after three concrete infeasibility attempts.

2. Add explicit `COMMITMENTS.md` entries for every [D1]-[D9] decision. Each
   entry must say what downstream artifact or machine-readable output proves
   fulfillment. Include at minimum [D3] fit-window enforcement, [D4] nominal
   categories, [D5] global `mu`, [D6] no data-integral hand scaling of DY, and
   [D8] angular-NN prerequisite validation.

3. Add a convention-coverage matrix for the adopted shape-fit/search
   convention. Row-map `conventions/search.md` signal modeling, background,
   detector/reconstruction, and theory-input rows to "Will implement", "Will
   approximate by ...", or "Not applicable because ...". Explicitly include
   pp replacements for beam/ISR rows: PDF/QCD scales, pileup, luminosity, and
   relevant acceptance/modeling uncertainties.

4. Update signal-injection validation to include `mu = 5`, or document why a
   measurement-specific stress test replaces it and what large-signal
   nonlinearity that replacement tests.

5. Make the fake-background plan quantitative. Define sideband regions,
   signal-window exclusion for constraints, whether DY is fixed/constrained/
   floated under low statistics, and a numeric TTBar threshold for inclusion
   as a nominal component versus template-derived omission systematic.

6. Make fallback systematics reviewable. For luminosity, effective cross
   sections, lepton efficiencies, and other fallback envelopes, define the
   source hierarchy, the closure/comparison used to set the envelope, the
   minimum machine-readable evidence, and the precise treatment when only a
   user-provided value exists.

7. Clarify VBF recovery under current input permissions. State that real jet
   recovery requires expanded allowed paths beyond the current `paths.json`;
   otherwise Phase 3 performs an immediate formal VBF downscope after branch,
   provenance, and allow-list checks, with no lepton-only category labeled VBF.

8. Add an angular/NN category viability gate. Require a prefit table of
   expected total, signal, and background counts per proposed category and
   `m4l` bin, count bins below the low-stat threshold, and veto any category
   split that makes MC-stat terms or GoF unstable. Add overtraining and
   category-boundary stability checks as a C-level improvement while editing.

9. Add a final AN comparability matrix commitment. It must cover inclusive
   `mu`, mass, fiducial cross section, width, production-sensitive categories,
   VBF categories, and reducible-background treatment, classifying each as
   matched, approximated/not directly comparable, or unavailable/not measured.
   Require pulls only for matched quantitative observables.

10. Add origin tags to generic `COMMITMENTS.md` entries, e.g. strategy
    decision label, validation-test number, systematic-plan row, or flagship
    figure number. This is separate from the required [D1]-[D9] carryover.

11. Keep the HEPData `ins1608162` versus `ins1608166` ambiguity as a tracked
    downstream cleanup item to resolve before numerical comparison extraction.

After fixes, Phase 2 needs verification of these exact items and then fresh
review. Do not advance to Phase 3 with unresolved A or B items.
