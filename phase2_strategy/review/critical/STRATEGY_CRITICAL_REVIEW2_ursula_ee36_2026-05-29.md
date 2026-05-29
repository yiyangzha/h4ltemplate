# Phase 2 Strategy Critical Re-Review

Session: `ursula_ee36`
Date: 2026-05-29
Artifact reviewed: `phase2_strategy/outputs/STRATEGY.md`
Review type: fresh critical review after ITERATE fix

## Verdict

PASS.

I find no remaining Category A or Category B issues in the fixed Phase 2
strategy. The previous blocking findings are resolved with explicit strategy
language and corresponding proof hooks in `COMMITMENTS.md`. I did not edit
strategy outputs or commitments. No figures or compiled PDF exist for Phase 2,
so no visual review was applicable. MCP toggles are false in `TOGGLES.md`; I
did not call MCP tools.

## Scope Read

Read and checked:

- `TOGGLES.md`: `MCP_ALPHAXIV=false`, `MCP_LEP_CORPUS=false`,
  `REVIEW_MODEL_DIVERSITY=true`.
- `CLAUDE.md` and `agents/critical_reviewer.md`: review must be evidence-based,
  strict, and not advance with unresolved A/B findings.
- `methodology/06-review.md`: Category A/B/C definitions at lines 5-9;
  strategy review focus at lines 144-162; re-review requirement at lines
  506-514.
- `phase2_strategy/CLAUDE.md`: Phase 2 must enumerate selection approaches,
  systematic/convention coverage, reference analyses, mitigation strategies,
  and `COMMITMENTS.md` entries.
- Current `phase2_strategy/outputs/STRATEGY.md` and current `COMMITMENTS.md`.
- Phase 1 deliverables: `DATA_RECONNAISSANCE.md`, `INPUT_INVENTORY.md`,
  `LITERATURE_SURVEY.md`.
- Prior review chain: `VERIFY_viktor_dfa6.md`, original arbiter,
  `FIX_REPORT_fiona_8d6e_2026-05-29.md`, and targeted fix verification
  `STRATEGY_FIX_VERIFICATION_sigrid_87cc_2026-05-29.md`.
- `conventions/search.md` and `conventions/extraction.md`.

## Prior A/B Findings

| Prior item | Status | Evidence |
| --- | --- | --- |
| Mass plan under-specified | RESOLVED | `STRATEGY.md:135-163` now defines a binding simultaneous category mass-extraction attempt, common mass parameter, mass-template shift/morphing or `zfit` path, `mu` profiled in the mass scan, injected-mass closure at three hypotheses, and a downgrade rule requiring closure failure plus attempted fix or three infeasibility attempts. `COMMITMENTS.md:46-50`, `117-120`, `130-131`, and `148-149` carry proof hooks. |
| [D1]-[D9] carryover incomplete | RESOLVED | `COMMITMENTS.md:17-50` has explicit downstream proof entries for [D1] through [D9]. My label count check found each D label present in both files: [D1]-[D9] all have at least one `STRATEGY.md` occurrence and at least one `COMMITMENTS.md` occurrence. |
| Search/shape-fit convention not row-mapped | RESOLVED | `conventions/search.md:43-94` lists required systematic rows. `STRATEGY.md:394-417` maps signal cross section, acceptance, shape, ISR replacement, 4-fermion/ZZ replacement, background normalization/shape, qqbar/DY replacement, MC statistics, detector model, object calibration, beam-energy replacement, luminosity, QCD scales, fragmentation, and heavy flavour to implement/approximate/not applicable decisions. |
| `mu=5` injection missing | RESOLVED | `STRATEGY.md:470-471` and `COMMITMENTS.md:121-123` require injections at `mu = 0`, `1`, `2`, and `5`, with bias above 20 percent triggering investigation. |
| Fake/sideband plan too qualitative | RESOLVED | `STRATEGY.md:241-253` excludes `105 < m4l < 140 GeV` from sideband constraints, defines sidebands `70 <= m4l < 105 GeV` and `140 < m4l <= 170 GeV`, and specifies weak/floating DY treatment below 10 expected sideband events. `STRATEGY.md:254-259` gives TTBar promotion thresholds: at least 10 percent of DY in the signal window or at least 20 percent in either sideband. |
| Fallback systematics vague | RESOLVED | `STRATEGY.md:419-449` requires machine-readable `systematics_sources.json` or equivalent with nominal value, uncertainty, citation/search trail, closure metric, fallback flag, and affected templates; it defines hierarchy and specific luminosity, effective cross-section, lepton-efficiency, and other fallback rules. `COMMITMENTS.md:54-96` carries proof hooks for the systematic rows. |
| Luminosity nuisance ambiguous | RESOLVED | Although the summary table still says the public 2017 uncertainty is a scale reference if applicable (`STRATEGY.md:376`), the controlling fallback rule is explicit at `STRATEGY.md:431-435`: if no certified 10 fb^-1 subset uncertainty exists, central luminosity is user-provided and a normalization envelope at least as large as the public 2017 relative uncertainty is assigned, with prior-width sensitivity scan. `COMMITMENTS.md:54-56` requires central value, hierarchy, fallback flag, and prior scan. |
| VBF permissions underspecified | RESOLVED | `STRATEGY.md:302-327` now states that real jet recovery requires expanded inputs beyond current `paths.json`, that no expanded/joinable path means immediate formal VBF downscope, and that no lepton-only category may be called VBF. This matches Phase 1 missing-content evidence in `DATA_RECONNAISSANCE.md:3989-3995` and current `paths.json`, which only allows the flat ntuple data and MC directories. |
| Angular/NN stat gates incomplete | RESOLVED | `STRATEGY.md:356-367` requires prefit total/signal/background counts per category and `m4l` bin, low-stat bin counts, vetoes for more than 25 percent of bins below five expected events, zero expected background after smoothing, MC-stat dominance, GoF/toy p <= 0.05 without remediation, overtraining checks, and category-boundary stability. `COMMITMENTS.md:136-140` carries the proof hook. |
| Final AN comparability matrix missing | RESOLVED | `STRATEGY.md:533-540` requires a comparability matrix before numerical pulls, covering inclusive `mu`, mass, fiducial cross section, width, production-sensitive categories, VBF categories, and reducible-background treatment. `COMMITMENTS.md:180-202` has row-level commitments. |
| Origin tags weak | RESOLVED | I emulated the prior checker: 60 checkbox commitments, 0 untagged lines. `COMMITMENTS.md` entries now carry tags such as [D], [VT], [SP], [FIG], [REF-MATRIX], [A], or [L]. |
| HEPData ambiguity | RESOLVED FOR PHASE 2 | The ambiguity remains tracked, not hidden. `STRATEGY.md:37-38` retains the CMS public-page-linked `ins1608162`, while `STRATEGY.md:538-540` and `COMMITMENTS.md:216-222` require resolving the `ins1608162` versus `ins1608166` trail before numerical comparison extraction. This is appropriate as a downstream cleanup, not a Phase 2 blocker. |

## Fresh Review Checks

No new A/B issue found.

- Phase 1 constraints are used. Primary/local file differences and prompt-path
  choice are captured in `STRATEGY.md:53-56` and `COMMITMENTS.md:17-19`, based
  on `DATA_RECONNAISSANCE.md:12-26`. Missing jets, truth, and MELA/angular
  branches are captured in `STRATEGY.md:61-70`, with VBF and angular mitigation
  in `STRATEGY.md:302-367`.
- Backgrounds are complete for available samples. `STRATEGY.md:225-231`
  classifies Higgs signal, qqZZ, ggZZ, DY+jets, and TTBar. This covers the MC
  inventory in `DATA_RECONNAISSANCE.md:30-43`.
- Selection exploration satisfies Phase 2. S1 cut/channel fit and S2
  angular/kinematic classifier categories are qualitatively different and
  grounded in available retained branches (`STRATEGY.md:261-300`).
- Convention coverage is sufficient for the chosen adapted shape-fit method.
  Extraction is correctly rejected as governing convention because this is not
  closed-form double-tag or hemisphere counting (`STRATEGY.md:184-190`;
  `conventions/extraction.md:184-197`).
- Reference analysis coverage is adequate. `STRATEGY.md:511-517` tabulates
  CMS-HIG-16-041, CMS-HIG-19-001, and PDG values/method context, while
  `COMMITMENTS.md:206-245` records the comparison targets.
- Precision expectations are contextualized. `STRATEGY.md:485-509` scales the
  CMS-HIG-16-041 statistical precision from 35.9 fb^-1 to 10 fb^-1, notes
  open-data limitations, and estimates mass precision as order `0.5-1.0 GeV`
  until Phase 4a closure quantifies it.
- Validation target obligations are set up for later phases. `COMMITMENTS.md`
  includes reference values and a method-parity target; Phase 4 review can
  apply the validation target rule against these references.

## Findings

None.

No Category A findings.
No Category B findings.
No Category C findings requiring action before PASS.

## Residual Risks To Monitor Downstream

These are not Phase 2 blockers because the fixed strategy binds downstream
tests and proof artifacts:

- The mass extraction is ambitious with only M125 signal MC. Phase 4a must
  enforce the closure and downgrade criteria in `STRATEGY.md:135-163`.
- DY-only fake modeling is a deliberate user simplification. Phase 3/4 must
  report the sideband and TTBar checks rather than treating this as official
  CMS-equivalent Z+X estimation.
- HEPData record identity must be resolved before numerical tables or captions
  use HEPData values.

## Final Verdict

PASS. The fixed Phase 2 strategy satisfies the Phase 2 requirements and the
previous A/B findings are resolved with auditable evidence.
