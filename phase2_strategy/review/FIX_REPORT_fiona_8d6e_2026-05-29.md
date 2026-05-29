# Phase 2 Strategy Fix Report

Session: `fiona_8d6e`
Date: 2026-05-29
Controlling verdict:
`phase2_strategy/review/arbiter/STRATEGY_ARBITER_albert_0ea5_2026-05-29.md`

## Summary

All arbiter Required Fix List items are RESOLVED in the Phase 2 strategy
artifact and commitment registry. No Phase 1 or Phase 3+ artifacts were
edited. No analysis code was added or run.

## Required Fix List

1. RESOLVED — Binding nominal mass-extraction attempt.
   Changed `STRATEGY.md`: added "Binding Mass-Extraction Attempt"; updated
   [D9], Observable Definition, Technique Selection, Validation Tests, and
   Flagship Figures. The strategy now requires a simultaneous category mass
   extraction or scan, profiles `mu`, defines signal-template shift/morphing
   or parametric-shape construction, requires injected-mass closure, and allows
   downgrade only after closure failure or three documented infeasibility
   attempts. Changed `COMMITMENTS.md`: added [D9] proof entries, VT7, VT12,
   and FIG3 mass-profile commitments.

2. RESOLVED — Explicit [D1]-[D9] commitment carryover.
   Changed `COMMITMENTS.md`: added "Strategy decision carryover" with [D1]
   through [D9], each tied to a downstream artifact or machine-readable proof.
   Minimum requested entries are present for [D3] fit-window enforcement, [D4]
   categories, [D5] global `mu`, [D6] no data-integral DY hand scaling, and
   [D8] angular-NN prerequisite validation.

3. RESOLVED — Convention-coverage matrix.
   Changed `STRATEGY.md`: added "Shape-Fit Convention Coverage" mapping the
   adopted `conventions/search.md` rows to Will implement, Will approximate,
   or Not applicable decisions. The matrix includes pp replacements for
   beam/ISR rows: PDF/QCD scales, pileup, luminosity, lepton mass calibration,
   and acceptance/modeling uncertainties.

4. RESOLVED — Signal injection includes `mu = 5`.
   Changed `STRATEGY.md` Validation Test 8 and `COMMITMENTS.md` VT8 to require
   injections at `mu = 0`, `1`, `2`, and `5`.

5. RESOLVED — Quantitative fake-background plan.
   Changed `STRATEGY.md`: added sideband regions, signal-window exclusion,
   DY constrained/floated low-stat treatment, and TTBar nominal-promotion
   thresholds: at least 10% of DY in the signal window or at least 20% in
   either sideband. Changed `COMMITMENTS.md`: added [D6][SP10] and
   [L2][SP11] proof hooks.

6. RESOLVED — Reviewable fallback systematics.
   Changed `STRATEGY.md`: added "Fallback Systematics Evidence Rules" covering
   source hierarchy, closure/comparison evidence, machine-readable
   `systematics_sources.json`, and treatment of user-provided-only values for
   luminosity, effective cross sections, lepton efficiencies, and other
   fallback envelopes. Changed `COMMITMENTS.md`: added proof fields for SP1
   through SP13.

7. RESOLVED — VBF recovery under current input permissions.
   Changed `STRATEGY.md`: clarified that real jet recovery requires expanding
   allowed paths beyond the current `paths.json`; otherwise Phase 3 must
   immediately write a formal VBF downscope after branch/provenance/allow-list
   checks. Changed `COMMITMENTS.md`: added [A3][D4] proof hooks and reiterated
   that no lepton-only category may be labeled VBF.

8. RESOLVED — Angular/NN viability gate.
   Changed `STRATEGY.md`: added prefit expected total/signal/background counts
   per proposed category and `m4l` bin, low-stat bin counts, zero-background
   and MC-stat/GoF vetoes, overtraining checks, and category-boundary stability
   scans. Changed `COMMITMENTS.md`: added [D7][D8][VT13] proof hooks.

9. RESOLVED — Final AN comparability matrix commitment.
   Changed `STRATEGY.md`: added final AN comparability requirements for
   inclusive `mu`, mass, fiducial cross section, width, production-sensitive
   categories, VBF categories, and reducible-background treatment; pulls are
   required only for matched quantitative observables. Changed
   `COMMITMENTS.md`: added "Final AN comparability matrix".

10. RESOLVED — Origin tags for generic commitments.
    Changed `COMMITMENTS.md`: added decision, validation-test, systematic-plan,
    reference-matrix, or flagship-figure origin tags to generic systematic,
    validation, figure, and cross-check commitments. Neighborhood check found
    one remaining untagged [D7] input-gate line and fixed it.

11. RESOLVED — HEPData `ins1608162` versus `ins1608166` cleanup remains
    tracked.
    Changed `STRATEGY.md` and `COMMITMENTS.md`: kept the ambiguity as a
    downstream cleanup item that must be resolved before numerical comparison
    extraction.

## Verification

Commands run:

- `git diff --check`
- `for d in D1 D2 D3 D4 D5 D6 D7 D8 D9; do grep -q "\\[$d\\]" phase2_strategy/outputs/STRATEGY.md && grep -q "\\[$d\\]" COMMITMENTS.md && printf '%s OK\n' "$d" || printf '%s MISSING\n' "$d"; done`
- `awk '/^- \\[[ xD]\\]/ && $0 !~ /^- \\[[ xD]\\] \\[[^]]+\\]/ {print NR ":" $0}' COMMITMENTS.md`

Evidence:

- `git diff --check` passed with no whitespace errors.
- [D1]-[D9] coverage check passed in both `STRATEGY.md` and
  `COMMITMENTS.md`.
- Commitment origin-tag scan returned one untagged line initially; it was
  patched to `[D7][VT4]`. The final scan returned no lines.

## Files Changed

- `phase2_strategy/outputs/STRATEGY.md`
- `COMMITMENTS.md`
- `phase2_strategy/logs/fixer_fiona_8d6e_20260529T201014Z.md`
- `experiment_log.md`
- `phase2_strategy/review/FIX_REPORT_fiona_8d6e_2026-05-29.md`

## Remaining Risks

- The strategy now binds Phase 3/4 to attempts and proof artifacts, but actual
  feasibility of the mass morphing, sideband constraints, and angular/NN
  categories remains to be established by downstream executors.
- HEPData record identity remains deliberately unresolved until numerical
  comparison extraction; this is tracked and non-blocking for the strategy
  fix.
