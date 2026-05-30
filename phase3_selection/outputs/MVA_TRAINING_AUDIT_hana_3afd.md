# MVA Training Audit

Session: `hana_3afd`
Date: 2026-05-30

## Root Cause

- The old classifier was not broken by labels or a failed train/test split.
  It was underpowered: the D7 gate was used as a hard whitelist and left only
  `lead_abs_eta` and `phi1` as active inputs. With those two variables, the
  best AUC was about `0.55`, consistent with near-random separation.
- The previous MVA comparison mixed broad-window MVA diagnostics with an
  older `105 < m4l < 140 GeV` S1 precision proxy. The repaired comparison uses
  `80 < m4l < 170 GeV` for the active S1/S2 training metric.
- Strong JHEP-like variables including `mZ1` and `mZ2` improve raw separation
  but induce visible score-mass correlation in the broad background sample, so
  they are retained as diagnostic-only rather than used in nominal fit
  categories.
- The repaired mass-safe feature set is no longer random, but S2 still fails
  promotion because score-shape data/MC and low-stat category gates fail.

## Repair

`phase3_selection/src/train_mva.py` was restored and changed to train weighted
models in `80 < m4l < 170 GeV`, excluding `m4l` itself. The nominal mass-safe
features are:

`pt4l`, `eta4l`, `lead_lepton_pt`, `sublead_lepton_pt`, `lead_abs_eta`,
`sublead_abs_eta`, `cos_theta_star`, `cos_theta1`, `cos_theta2`, `phi`, `phi1`,
and `channel_code`.

The diagnostic JHEP-like set adds `mZ1` and `mZ2`, but those variants are not
eligible for nominal promotion because their mass-sculpting diagnostics fail.

D7 still records the broad-window data/MC modeling stress: the variables that
passed the original gate were only `lead_abs_eta` and `phi1`. Variables such as
`pt4l`, lepton kinematics, angular terms, `mZ1`, and `mZ2` have useful
discrimination, so they are evaluated in the repaired MVA with explicit
score-shape and mass-sculpting gates rather than silently discarded.

## New Numbers

From `phase3_selection/outputs/mva_metrics.json`:

| Model | AUC | Promotion use |
|---|---:|---|
| `logistic_mass_safe` | `0.7430` | eligible but fails score-shape gate |
| `bdt_mass_safe` | `0.7929` | best nominal candidate, not promoted |
| `logistic_jhep_like_diagnostic` | `0.8428` | diagnostic only |
| `bdt_jhep_like_diagnostic` | `0.9176` | diagnostic only |

Background score-mass correlation in `80 < m4l < 170 GeV`:

- `logistic_mass_safe`: `0.1453`, mass-sculpting gate passes.
- `bdt_mass_safe`: `0.3578`, mass-sculpting gate fails.
- `logistic_jhep_like_diagnostic`: `0.5744`, diagnostic-only.
- `bdt_jhep_like_diagnostic`: `0.4462`, diagnostic-only.

The best nominal candidate is `bdt_mass_safe`. Its broad-window proxy improves
over S1 by about `0.190`, but the score data/MC gate fails
(`chi2 = 85.96`, `ndf = 4`, `p = 9.50e-18`) and the broad category viability
fails, so `promote_s2 = false`.

## Decision

Keep S1 final-state categories for Phase 4c. The MVA training was materially
improved and the random-classifier failure is resolved, but the repaired
classifier is not safe enough to define final fit categories.

## Commands Run

```bash
pixi run p3-train-mva
pixi run p3-compare
pixi run p3-selection-plots
pixi run p3-artifact
pixi run lint-plots
git diff --check
```
