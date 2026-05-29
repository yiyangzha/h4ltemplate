# Phase 2 Strategy Targeted Fix Verification

Session: `sigrid_87cc`
Date: 2026-05-29
Artifact: `phase2_strategy/outputs/STRATEGY.md`
Fix report: `phase2_strategy/review/FIX_REPORT_fiona_8d6e_2026-05-29.md`
Controlling verdict:
`phase2_strategy/review/arbiter/STRATEGY_ARBITER_albert_0ea5_2026-05-29.md`

## Scope

This is targeted fix verification for the 11 Required Fix List items from the
previous arbiter verdict. I did not conduct a broad fresh review.

## Verification Results

| # | Required fix | Status | Evidence |
|---|---|---|---|
| 1 | Binding nominal mass-extraction attempt with simultaneous categories, `mu` profiled, shape construction/morphing, injected-mass closure, and hard downgrade rule. | FIXED | `STRATEGY.md:135-160` defines the binding attempt. It requires the same simultaneous category workspace as the `mu` fit (`140-142`), explicit morphing/shift or parametric shape construction (`143-149`), profiling `mu` during the mass scan (`150-151`), injected-mass closure at at least three hypotheses (`152-157`), and downgrade only after closure failure with an attempted fix or three documented infeasibility attempts (`158-160`). `COMMITMENTS.md:46-50`, `117-122`, and `130-131` carry proof hooks. |
| 2 | `COMMITMENTS.md` carries explicit `[D1]`-`[D9]` entries and proof artifacts for each. Grep all labels. | FIXED | Strategy decision carryover has explicit entries with proof artifacts: `[D1]` `COMMITMENTS.md:17-19`, `[D2]` `20-23`, `[D3]` `24-27`, `[D4]` `28-31`, `[D5]` `32-34`, `[D6]` `36-39`, `[D7]` `40-42`, `[D8]` `43-45`, `[D9]` `46-50`. Grep also finds the same `[D1]`-`[D9]` decision labels in `STRATEGY.md:99-129`. |
| 3 | Convention-coverage matrix row-maps adopted `conventions/search.md` rows and pp replacements. | FIXED | `conventions/search.md` required rows are signal modeling (`64-67`), background estimation (`73-77`), detector/reconstruction (`83-86`), and theory inputs (`92-94`). `STRATEGY.md:394-417` maps each row: signal cross-section, acceptance, shape, ISR, 4-fermion backgrounds, background normalization/shape, qqbar(gamma), MC statistics, detector model, object calibration, beam energy, luminosity, QCD scales, fragmentation, and heavy flavour. pp replacements are explicit for ISR/PDF/QCD/pileup (`405`), qqbar/DY fake modeling (`409`), beam energy/lepton scale (`413`), luminosity (`414`), and QCD scales (`415`). |
| 4 | Signal injection includes `mu = 5`. | FIXED | `STRATEGY.md:470-471` requires injections at `mu = 0`, `1`, `2`, and `5`. `COMMITMENTS.md:121-123` repeats the same injection points with proof via injection-result JSON. |
| 5 | Fake-background/sideband plan is quantitative: sideband regions, signal exclusion, DY treatment, numeric TTBar threshold. | FIXED | `STRATEGY.md:239-258` defines the fake-background and sideband protocol. It excludes `105 < m4l < 140 GeV` from sideband constraints (`241-243`), defines low/high sidebands as `70 <= m4l < 105 GeV` and `140 < m4l <= 170 GeV` (`244-247`), specifies DY log-normal sideband transfer-factor treatment and weak/floating treatment below 10 expected sideband events (`249-253`), and sets TTBar promotion thresholds at 10% of DY in the signal window or 20% in either sideband (`254-258`). Commitment proof hooks are in `COMMITMENTS.md:36-39`, `81-86`, and `169-173`. |
| 6 | Fallback systematics have source hierarchy, closure/comparison, machine-readable evidence, and user-provided-only treatment. | FIXED | `STRATEGY.md:419-448` defines fallback evidence rules. It requires `systematics_sources.json` or equivalent machine-readable fields (`421-424`), a source hierarchy (`426-429`), user-provided luminosity treatment (`431-435`), effective-cross-section search trail and yield-closure treatment (`436-440`), lepton-efficiency closure envelopes (`441-443`), and user-provided-only fallback labeling plus wider prior/limitation reporting (`445-448`). `COMMITMENTS.md:54-60`, `63-68`, and related SP rows carry proof artifacts. |
| 7 | VBF recovery/current permission limits and no lepton-only VBF label are explicit. | FIXED | `paths.json` allows only the flat ntuple data and MC directories. `STRATEGY.md:302-327` defines the VBF recovery/downscope path, including checking safe joins under `paths.json` (`311-312`), requiring expanded inputs beyond the current allow-list for real jet recovery (`313-315`), immediate formal downscope if not approved/joinable (`315-317`), and forbidding any lepton-only category from being called VBF (`325-327`). `COMMITMENTS.md:92-96`, `132-135`, `161-163`, and `198-199` carry proof hooks and no-lepton-only-VBF language. |
| 8 | Angular/NN viability gate has prefit count table requirement, low-stat vetoes, MC-stat/GoF checks, overtraining, boundary stability. | FIXED | `STRATEGY.md:329-366` defines Angular NN feasibility. It requires a prefit viability table with expected total, signal, and background counts per category and `m4l` bin (`357-358`), low-stat bin counting and vetoes for more than 25% below five expected events or zero expected background (`358-361`), MC-stat dominance and GoF/toy p-value vetoes (`361-363`), overtraining checks (`364-365`), and boundary/threshold stability scans (`365-366`). `COMMITMENTS.md:136-140` repeats the proof requirements. |
| 9 | Final AN comparability matrix commitment covers requested result classes and matched/approximated/unavailable classification. | FIXED | `STRATEGY.md:533-539` requires the final AN matrix to cover inclusive `mu`, mass, fiducial cross section, width, production-sensitive categories, VBF categories, and reducible-background treatment; it also requires matched/approximated/unavailable classification and pulls only for matched quantitative observables. `COMMITMENTS.md:180-202` carries row-level commitments for each requested class. |
| 10 | Generic commitment entries have origin tags; run/emulate untagged checkbox scan. | FIXED | Emulated fixer scan command: `awk '/^- \\[[ xD]\\]/ {checked++; if ($0 !~ /^- \\[[ xD]\\] \\[[^]]+\\]/) {bad++; print NR \":\" $0}} END {print \"checked=\" checked; print \"untagged=\" (bad+0)}' COMMITMENTS.md`. Result: `checked=60`, `untagged=0`. |
| 11 | HEPData `ins1608162` vs `ins1608166` ambiguity remains tracked downstream before numerical extraction. | FIXED | `STRATEGY.md:37-38` records `ins1608162`; `STRATEGY.md:538-540` keeps the `ins1608162` versus `ins1608166` ambiguity as a cleanup item before numerical table extraction. `COMMITMENTS.md:216-222` requires Phase 3/Doc phases to use the CMS public-page-linked record or document redirects before numerical comparison extraction. |

## Required Command Checks

- `git diff --check`: PASS after writing this verification report/log.
- Pre-write `git status --short`: clean.
- Post-write `git status --short`: only the two allowed new files:
  - `?? phase2_strategy/logs/arbiter_sigrid_87cc_20260529T201839Z.md`
  - `?? phase2_strategy/review/arbiter/STRATEGY_FIX_VERIFICATION_sigrid_87cc_2026-05-29.md`

## Overall Verdict

ALL FIXED.

No remaining Required Fix List items from the previous arbiter verdict remain
unfixed in the targeted verification scope.
