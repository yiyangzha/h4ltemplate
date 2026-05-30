# Phase 4c Compact Gate

Date: 2026-05-30

This compact gate replaces a full review loop for the current turn because the
user explicitly requested reduced review overhead. It checks only whether the
existing Phase 4c observed inference is internally consistent enough to start
Doc 4c.

## Checks Run

```bash
pixi run lint-plots
pixi run py - <<'PY'
# figure registry, JSON, fit-window, event-count, normalization, and viability checks
PY
git diff --check
```

## Evidence

- Phase 4c figure registry: 9 entries, no missing files, no orphan PNGs.
- Observed result: `mu = 2.4776040008517612 -0.7138966295430187 +0.8387787105161486`.
- Fit window: `[70.0, 170.0]` GeV, including the Z peak.
- Full data selected events: `203`.
- MC normalization policy: no data-integral normalization.
- GoF: `chi2/ndf = 47.326/38`, p-value `0.14274016366544112`.
- Boundary/triviality checks: `mu_at_boundary = false`, `zero_chi2_warning = false`.
- Viability: `PASS`, relative total uncertainty `0.3133421118801435`.
- Observed mass scan: best grid point `125.0 GeV`; scan range `110.0-150.0`
  GeV in `2.5` GeV steps; shifted-template result is not promoted to an
  official calibrated mass measurement.

## Verdict

PASS for starting Doc 4c. Remaining limitations must be carried into the final
AN: S1 categories only, no real VBF category, repaired MVA not promoted,
DY+jets fake proxy, grouped MC-stat approximation, and shifted-template mass
scan limitation.
