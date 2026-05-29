# Phase 2 Strategy Critical Review

Session: `boris_db73`  
Date: 2026-05-29  
Artifact reviewed: `phase2_strategy/outputs/STRATEGY.md`  
Role: critical reviewer

## Verdict

ITERATE.

The strategy is directionally sound: it uses the Phase 1 inventory, includes a
cut-based path and an MVA/classifier path, treats VBF honestly given the missing
jet branches, uses the requested `105 < m4l < 140 GeV` fit window, classifies
the available backgrounds, and records public CMS/PDG comparison targets.
However, I do not sign off because the binding audit trail is incomplete and
the systematic/validation plan does not yet cover the adopted shape-fit
convention row-by-row. These are Phase 2 responsibilities, not details to
discover only in Phase 4a.

No figures or compiled PDF exist for Phase 2, so no image review was performed.
MCP toggles are false; I did not call MCP tools. I used public `curl` only to
verify the CMS-HIG-16-041 HEPData link and key public-page numeric citations.

## Findings

### A1. `COMMITMENTS.md` does not carry all binding strategy decisions, so downstream review cannot enforce them

Evidence:

- The strategy defines nine decision labels [D1]-[D9] (`STRATEGY.md:99-131`).
- `COMMITMENTS.md` only explicitly carries `[D2]` (`COMMITMENTS.md:14`), `[D7]`
  (`COMMITMENTS.md:47`), and `[D9]` (`COMMITMENTS.md:53-55`). It has related
  A/L-labeled entries for primary paths and angular reconstruction, but no
  explicit `[D1]`, `[D3]`, `[D4]`, `[D5]`, `[D6]`, or `[D8]` entries
  (`COMMITMENTS.md:37-101`).
- Missing examples are material: `[D3]` fixes the mass window
  (`STRATEGY.md:104-109`), `[D4]` fixes nominal categories
  (`STRATEGY.md:110-112`), `[D5]` fixes one global `mu`
  (`STRATEGY.md:113-115`), and `[D6]` forbids hand-scaling DY to data
  (`STRATEGY.md:116-118`).
- The Phase 2 template requires `COMMITMENTS.md` to contain every binding
  commitment before review, including validations, cross-checks, figures, and
  reference entries (`phase2_strategy/CLAUDE.md:176-187`).

Why this matters:

The root regression checklist later asks whether all binding strategy decisions
were fulfilled. If several [D] labels are absent from `COMMITMENTS.md`, Phase
3/4 executors can silently drift from the reviewed strategy without triggering a
clear checklist failure.

Required fix:

Add explicit checkbox entries for every [D1]-[D9] decision, not just related
A/L entries. Each entry should name the downstream artifact or machine-readable
output that will prove fulfillment. For example, `[D3]` should require all
fit-ready histograms and workspaces to record `105 < m4l < 140 GeV`; `[D6]`
should require a DY normalization treatment record showing fixed, constrained,
or floated sideband handling, and explicitly no data-integral hand scaling.

### A2. The strategy adopts the shape-fit/search convention but does not enumerate its required systematic sources row-by-row

Evidence:

- The strategy says `extraction.md` and `unfolding.md` are not governing and
  that the closest methodological convention is the shape-fit portion of
  `conventions/search.md` (`STRATEGY.md:151-158`).
- `conventions/search.md` requires explicit treatment of signal modeling,
  background estimation, detector/reconstruction, and theory-input sources,
  with pp replacements for beam-related rows (`conventions/search.md:43-95`).
- The Phase 2 template requires every required convention source to be marked
  "Will implement" or "Not applicable because [reason]"
  (`phase2_strategy/CLAUDE.md:87-95`, `phase2_strategy/CLAUDE.md:204-206`).
- The strategy systematic table has useful rows for luminosity, MC stats,
  lepton efficiency/scale, pileup, Higgs normalization, backgrounds, DY, TTBar,
  classifier, angular, category migration, and jets (`STRATEGY.md:298-316`),
  but it does not explicitly cover or declare inapplicable several convention
  rows: signal acceptance/generator comparison, signal shape from mass/width or
  template parameter variations, PDF/QCD scale acceptance effects for signal and
  ZZ, or fragmentation/heavy-flavour rows where inapplicable
  (`conventions/search.md:60-95`).

Why this matters:

This is not just terminology. Signal acceptance and ZZ theory/shape systematics
are exactly where an open-data H->4l result can become non-comparable to
CMS-HIG-16-041/HIG-19-001. A Phase 4a reviewer cannot know whether a missing
PDF/QCD/acceptance row is intentionally inapplicable or accidentally omitted.
The spec says silent omissions in the Phase 2 systematic enumeration are
blocking.

Required fix:

Add a convention-coverage matrix keyed to `conventions/search.md`, plus a CMS
reference-coverage column if possible. Every row should say "Will implement",
"Will approximate by ...", or "Not applicable because ...". For pp-specific
adaptation, explicitly replace ISR/beam-energy rows with PDF, pileup,
luminosity, and relevant acceptance/modeling uncertainties.

### A3. The mass measurement plan remains too easy to downgrade below the user's requested simultaneous mass fit

Evidence:

- The user prompt asks to fit the four-lepton mass and compute `mu`, with all
  categories fit simultaneously (`prompt.md:14-20`).
- The strategy makes `mu` the only explicit likelihood parameter of interest
  (`STRATEGY.md:135-140`, `STRATEGY.md:160-172`).
- The mass result is described as secondary and may become a detector-level
  peak estimator if morphing is not validated (`STRATEGY.md:142-147`,
  `STRATEGY.md:431-434`).
- The method-parity decision requires only a parametric mass-shape
  cross-check if feasible, not a nominal simultaneous mass-profile plan
  (`STRATEGY.md:126-131`, `STRATEGY.md:174-180`).
- `COMMITMENTS.md` has mass-template closure only "if any mass estimator or
  morphing scan is reported" (`COMMITMENTS.md:61`), so the requested mass fit
  can disappear without a formal Phase 2 commitment.

Why this matters:

It is acceptable to conclude later that official-quality `mH` extraction is
infeasible with only M125 signal MC, but that conclusion must come after a
binding attempt and closure criteria. At present the strategy can satisfy the
letter of the artifact by producing a `mu` fit plus a peak-position diagnostic,
which is weaker than the requested physics deliverable and weaker than the CMS
method-parity target.

Required fix:

Define the nominal mass-extraction attempt in Phase 2: a simultaneous-category
profile or staged scan with `mu` profiled, the exact signal-shape construction
or morphing/shift model, closure with injected mass shifts, and a hard downgrade
criterion. Add corresponding `COMMITMENTS.md` checkboxes so Phase 4a review can
verify the attempt or a formally documented infeasibility decision.

### B1. Signal-injection validation omits the convention's high-strength stress point without justification

Evidence:

- `conventions/search.md` standard configuration requires signal injection at
  `0x`, `1x`, `2x`, and `5x` the expected cross section
  (`conventions/search.md:35-36`), and validation check #2 requires reporting
  injected versus fitted signal strength with bias >20% investigated
  (`conventions/search.md:105-108`).
- The strategy requires only `mu = 0`, `1`, and `2`
  (`STRATEGY.md:336-337`).
- `COMMITMENTS.md` repeats only `mu = 0`, `1`, and `2`
  (`COMMITMENTS.md:56-57`).

Why this matters:

For a measurement, the `5x` point may be less central than for a limit-setting
search, but the strategy explicitly imported the shape-fit/search convention.
If the high-strength point is intentionally omitted, the artifact needs to say
why. Otherwise Phase 4a has a silent convention deviation.

Required fix:

Either add the `mu = 5` injection stress point, or add an explicit
"Not applicable" justification explaining why the measurement-specific
validation suite replaces it and what stress test covers large-signal
nonlinearity instead.

### B2. TTBar/fake-background treatment lacks a quantitative promotion or omission threshold

Evidence:

- The strategy follows the user simplification by making DY+jets the nominal
  fake proxy and TTBar diagnostic only (`STRATEGY.md:81-83`,
  `STRATEGY.md:188-194`).
- Phase 1 selected-entry counts are comparable for the two reducible samples:
  DY has 463 entries and TTBar has 639 in the primary files
  (`DATA_RECONNAISSANCE.md:33`, `DATA_RECONNAISSANCE.md:38`).
- The systematic plan says TTBar is included or assigned an omission systematic
  if non-negligible, but does not define non-negligible (`STRATEGY.md:309-310`).

Why this matters:

The prompt permits avoiding a full fake-rate estimate; it does not justify an
undefined reducible-background decision rule. TTBar can have a different mass
shape from DY and could matter in sidebands even if it is not nominal.

Required fix:

Define a numeric criterion before Phase 3 executes, such as a maximum allowed
TTBar fraction of reducible yield in the broad sideband and signal window. If
above threshold, include TTBar as a separate nominal reducible component or
assign a template-derived omission systematic.

### B3. Several systematic treatments are too vague to be enforceable in Phase 4a

Evidence:

- Lepton efficiency uncertainty is described as "public CMS references or
  conservative closure-derived envelopes if scale factors are unavailable"
  (`STRATEGY.md:303`).
- Luminosity uses the user target luminosity and "public CMS 2017 luminosity
  uncertainty as a scale reference if applicable" (`STRATEGY.md:300`).
- Prompt effective cross sections get a validation trail or user-provided
  fallback (`STRATEGY.md:301`), but the fallback uncertainty size or method is
  not specified.

Why this matters:

Flat or ad hoc uncertainties are a recurring review failure mode. Phase 2 does
not need final numerical impacts, but it should define how fallback envelopes
are derived and what independent source or closure calculation bounds them.

Required fix:

For each fallback-driven systematic, specify the derivation method and minimum
evidence required: source hierarchy, closure comparison, envelope construction,
and machine-readable output expected from Phase 3/4. Avoid phrases like
"conservative" unless the strategy defines what quantity is being enveloped.

### C1. HEPData source-ID ambiguity is handled, but downstream should resolve it early

Evidence:

- Phase 1 cited `ins1608166` for the HIG-16-041 HEPData trail
  (`INPUT_INVENTORY.md:11-14`, `LITERATURE_SURVEY.md:45`).
- The strategy and commitments switched to the CMS public-page-linked
  `ins1608162` and noted the mismatch (`STRATEGY.md:37-38`,
  `COMMITMENTS.md:115-120`).
- Public `curl` check during this review found that the CMS-HIG-16-041 public
  page links `https://www.hepdata.net/record/ins1608162`; `ins1608162` reports
  DOI `10.17182/hepdata.80189`, while `ins1608166` reports
  `10.17182/hepdata.80168`.

Suggestion:

Resolve the HEPData identity in Phase 3 before extracting comparison tables.
The current note in `COMMITMENTS.md` is sufficient for Phase 2, but downstream
should not keep both identifiers alive in tables or captions.

## Checks That Passed

- Phase 1 findings are materially used: primary/local copy mismatch,
  missing jet/VBF branches, missing truth branches, missing precomputed
  MELA/angular branches, `miniRelIso`/`pvNdof` caveats, trigger bit decoding,
  and flavor-specific ID handling are reflected in strategy labels and Phase 3
  instructions (`STRATEGY.md:53-73`, `STRATEGY.md:207-241`,
  `STRATEGY.md:402-423`).
- At least two qualitatively different selection approaches are present:
  S1 cut/channel fit and S2 angular/kinematic classifier categories
  (`STRATEGY.md:202-241`).
- The MVA/NN path is grounded in available branches and has useful input
  modeling, no-`m4l`, mass-sculpting, and baseline-promotion gates
  (`STRATEGY.md:225-237`, `STRATEGY.md:275-291`).
- The fit window is adequately cited for Phase 2. Public `curl` against the
  CMS-HIG-16-041 page found the expected public-page snippets for
  `mu = 1.05 +0.19/-0.17`, `2.92 +0.48/-0.44 (stat) +0.28/-0.24 (syst) fb`,
  and `mH = 125.26 +/- 0.21 GeV`; Phase 1 independently recorded the
  `105 < m4l < 140 GeV` reference window (`INPUT_INVENTORY.md:10`).
- Background classes are complete for the provided samples: signal, qqZZ/ggZZ
  irreducible, DY reducible/instrumental fake proxy, and TTBar reducible/top
  diagnostic (`STRATEGY.md:188-194`).

## Required Before PASS

Resolve A1-A3 and B1-B3. C1 can be carried as a downstream cleanup item once
the HEPData record identity is fixed before numerical extraction.
