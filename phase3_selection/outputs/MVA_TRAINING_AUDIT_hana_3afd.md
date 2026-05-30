# MVA Training Audit — `hana_3afd`

Date: 2026-05-30

## Scope

Fast repair of the Phase 3 MVA training path after the previous worker left
`phase3_selection/src/train_mva.py` in a broken state and the current MVA was
effectively random (`lead_abs_eta` + `phi1`, AUC about 0.55).

## Root Cause

The weak MVA was not one single bug. It was a stack of bad constraints:

1. Training had collapsed onto the strict D7-passing whitelist, which left only
   `lead_abs_eta` and `phi1`.
2. The training path was not explicitly locked to the requested
   `80 < m4l < 170 GeV` MC window.
3. The old implementation mixed incompatible model variants and output
   contracts, which made the Phase 3 task graph fragile.
4. The previous setup did not present a clear broad-feature diagnostic using
   JHEP-like observables, so there was no fast audit trail for whether the weak
   AUC came from the feature content or from a code path failure.

## Repair Applied

- Restored `phase3_selection/src/train_mva.py` to a working script and rewired
  it to a fixed `TRAINING_WINDOW = (80.0, 170.0)`.
- Applied the MC training/evaluation mask
  `(~is_data) & (80 < m4l < 170)`.
- Kept `m4l` out of all classifier inputs.
- Trained four cheap weighted models:
  - `logistic_mass_safe`
  - `bdt_mass_safe`
  - `logistic_jhep_like_diagnostic`
  - `bdt_jhep_like_diagnostic`
- Preserved downstream JSON fields needed by Phase 3 consumers.

## Feature Policy

### D7 broad-window pass/fail summary used for the audit

- D7-passing inputs: `lead_abs_eta`, `phi1`
- D7-failing inputs: `cos_theta1`, `cos_theta2`, `cos_theta_star`, `eta4l`,
  `lead_lepton_pt`, `mZ1`, `mZ2`, `phi`, `pt4l`, `sublead_abs_eta`,
  `sublead_lepton_pt`, `y4l`

### Nominal repaired mass-safe feature set

`pt4l`, `eta4l`, `lead_lepton_pt`, `sublead_lepton_pt`, `lead_abs_eta`,
`sublead_abs_eta`, `cos_theta_star`, `cos_theta1`, `cos_theta2`, `phi`,
`phi1`, `channel_code`

### JHEP-like diagnostic feature set

Nominal mass-safe set plus `mZ1`, `mZ2`.

These diagnostic models were kept non-nominal because the fast mass-sculpting
checks failed badly.

## New Numbers

From `phase3_selection/outputs/mva_metrics.json` after the repair:

| Model | Weighted test AUC | AUC gap | Signal mean gap | Score gate | Category viability | Mass sculpting |
|---|---:|---:|---:|---|---|---|
| `logistic_mass_safe` | 0.7430 | 0.0070 | 0.0003 | FAIL | FAIL | PASS |
| `bdt_mass_safe` | 0.7929 | 0.0173 | 0.0006 | FAIL | FAIL | FAIL |
| `logistic_jhep_like_diagnostic` | 0.8428 | 0.0033 | 0.0000 | FAIL | FAIL | FAIL |
| `bdt_jhep_like_diagnostic` | 0.9176 | 0.0163 | 0.0002 | FAIL | FAIL | FAIL |

Mass-sculpting correlation diagnostic on background in `80 < m4l < 170 GeV`:

- `logistic_mass_safe`: `corr(score, m4l) = 0.1453`
- `bdt_mass_safe`: `corr(score, m4l) = 0.3578`
- `logistic_jhep_like_diagnostic`: `corr(score, m4l) = 0.5744`
- `bdt_jhep_like_diagnostic`: `corr(score, m4l) = 0.4462`

Promotion summary:

- Best nominal model: `bdt_mass_safe`
- Best nominal weighted test AUC: `0.7929`
- Relative precision-proxy improvement vs S1 in `80 < m4l < 170 GeV`:
  `+0.1902`
- `promote_s2 = false`

## Decision

S2 stays rejected.

Reason: even after the repair and broader feature content, the classifier still
fails the score data/MC gate and the low-stat category viability gate, and the
best nominal BDT also fails the fast mass-sculpting diagnostic. The broader
`mZ1/mZ2`-inclusive diagnostic models are more powerful in AUC but clearly less
safe for a mass fit.

## Commands Run

```bash
pixi run p3-train-mva
pixi run p3-compare
git diff --check
```

## Remaining Limitation

This was a fast Phase 3 repair, not a full redesign of the category scheme.
The current classifier infrastructure is working again, but there is still no
mass-safe S2 configuration that clears the Phase 3 promotion gates.
