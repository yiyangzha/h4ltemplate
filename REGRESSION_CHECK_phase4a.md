# Phase 4a Regression Check

Date: 2026-05-30T03:37:40Z

Verdict: PASS with documented low-count limitation.

Review evidence:
- Fresh critical review `dmitri_46e5`: ITERATE on missing per-systematic shifts.
- Plot validation `celeste_62e7`: PASS.
- Regression gate `klaus_a64b`: PASS after commit `be3a796`.
- Corruption follow-up `hana_c6cf`: `m4l_scale_factor_0.8` remains non-rejecting after three documented final-state attempts and is marked `documented_low_count_infeasible`.

## Mandatory Checklist

- Validation test failures without 3 documented remediation attempts? NO unresolved. The `m4l_scale_factor_0.8` final-state corruption sensitivity does not reject (`p = 0.45954`) but has three documented attempts: profiled Poisson deviance, profiled per-channel shape-only deviance, and profiled Pearson chi2. It is not claimed as passed.
- GoF toy distribution inconsistent with observed chi2? NO. Phase 4a uses Asimov expected data; `chi2 = 0, p = 1` is labelled self-consistency only. Low-count toys: 80 toys, success fraction `1.0`, median bias `-0.06064996537909362`.
- Flat-prior gate excluding >50% of bins? NO evidence of a flat-prior bin-exclusion gate.
- Tautological comparison presented as independent validation? NO. Asimov GoF is explicitly not promoted to independent validation; validation evidence is toys, injections, corruption checks, binning variants, and documented infeasibility where sensitivity is insufficient.
- Visually identical distributions that should be independent? NO. Plot validation and regression gate found no blocking figure issue.
- Result with >30% relative deviation from a well-measured reference value? NO for expected `mu`: expected `1.0` versus CMS-HIG-16-041 reference context `1.05`; the reference is comparison context, not a fit input.
- Binding commitments [D1]-[D9] fulfilled? YES with documented downscopes. D9 mass closure uses category-simultaneous shifted-template closure over injected masses `115, 125, 135 GeV`; SP3 full bin-by-bin MC stat remains formally downscoped to grouped group/category normsys approximation.
- Fit chi2 identically zero? YES, but only for Asimov self-consistency. It is documented as an audit quantity, not a physics validation.
- Precision comparison >5x reference uncertainty? NO. Ratio is `3.192990241669998`.
- MC normalization method documented and not data-integral normalization? YES. Phase 3/4 commitments retain prompt `sigma_eff * L / nEvents` normalization and no hand-scaling to data integral.
- Dominant systematic >80% of total uncertainty? NO. Largest per-systematic variance is `zz_norm = 0.00939126129924922` versus total variance `0.33032404854215447` and systematic variance `0.023955108369782596`.
- Unresolved findings without Resolution/Evidence? NO blocking unresolved findings. The only remaining limitation is the documented low-count infeasibility of the `-20%` final-state corruption sensitivity test.

## Maximality Check

Feasible review findings were addressed:
- Broad `70 < m4l < 170 GeV` MVA training/evaluation metadata and tuned BDT trial added; S1 remains nominal because the MVA still does not pass promotion gates.
- Broad `70 < m4l < 170 GeV` display figure added.
- Fit window remains `105 < m4l < 140 GeV`.
- Mass scan broadened to `110-140 GeV`, with Z/sideband-adjacent exclusions documented.
- Per-systematic shifted-bin payload and summary figure added.
- MC-stat treatment labelled as formal grouped approximation/downscope.
- Final-state corruption limitation documented with three attempts.

No additional feasible Phase 4a work is being deferred except repeating stability checks on 10% and full observed data in Phase 4b/4c.
