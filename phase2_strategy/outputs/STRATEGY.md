# Phase 2 Strategy: CMS Open Data H->ZZ->4l Mass and Signal Strength

Session: `viktor_dfa6`
Date: 2026-05-29

## Summary

This analysis will measure the reconstructed H->ZZ->4l signal strength `mu`
and a detector-level Higgs mass estimator using CMS Open Data 2017 flat
ntuples corresponding to the user-provided 10 fb^-1 target luminosity. The
primary method is a binned simultaneous template likelihood in the same
signal-fit mass window used by the public CMS H->4l reference figures,
`105 < m4l < 140 GeV`, with categories that are feasible from the retained
branches. The strategy explicitly downscopes official-style VBF categories
unless Phase 3 recovers jet information, because Phase 1 found no jet,
truth, or precomputed MELA/angular branches in the primary ntuples.

MCP literature tools are disabled (`MCP_ALPHAXIV=false`,
`MCP_LEP_CORPUS=false`), so all literature inputs use public CMS, arXiv,
HEPData, PDG, and local Phase 1 artifacts.

## Sources Used

Public fallback searches run in this Phase 2 session:

- `CMS-HIG-16-041 JHEP 11 2017 047 H ZZ 4l mass window 105 140 signal strength 1.05`
- `CMS-HIG-16-041 HEPData signal strength fiducial cross section mass width`
- `CMS-HIG-19-001 signal strength 0.94 0.07 0.09 fiducial cross section 2.84`
- `PDG 2025 Gauge and Higgs Bosons Summary Table Higgs mass 125.20 0.11`
- `CMS-HIG-16-041 systematic uncertainties lepton efficiency luminosity H ZZ 4l`
- `Higgs ZZ 4l angular variables rest frame angles matrix element discriminant CMS HIG-16-041`

Primary retained references:

- CMS-HIG-16-041 / JHEP 11 (2017) 047 public page and arXiv:1706.09936:
  https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-16-041/
- HEPData record linked from CMS-HIG-16-041:
  https://www.hepdata.net/record/ins1608162
- CMS-HIG-19-001 / EPJC 81 (2021) 488 public page and arXiv:2103.04956:
  https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-19-001/
- PDG gauge and Higgs boson summary tables:
  https://pdg.lbl.gov/2024/tables/rpp2024-sum-gauge-higgs-bosons.pdf.
  The Phase 2 search also checked for a 2025 table, but the numeric values
  used here are the Phase 1-retained PDG 2024 values.
- Phase 1 deliverables:
  `phase1_exploration/outputs/DATA_RECONNAISSANCE.md`,
  `INPUT_INVENTORY.md`, and `LITERATURE_SURVEY.md`.

## Constraint, Limitation, And Decision Labels

### Constraints

- [A1] Primary and local ROOT copies differ in file size, metadata rows, and
  event entries. Phase 3 must use the prompt/user-specified primary paths from
  `paths.json` unless it writes a formal provenance-change note and re-runs
  all normalization checks.
- [A2] Effective MC cross sections are user-provided. They are usable as the
  nominal normalization inputs only after Phase 3 records the prompt values,
  metadata denominators, public/campaign search trail, and yield-closure
  checks.
- [A3] The primary flat ntuples contain no jet collections, jet counts,
  dijet mass, or VBF discriminant branches. Official VBF-1jet/VBF-2jet
  categorization is therefore not implementable from the retained event
  content alone.
- [A4] No precomputed MELA/angular discriminant branches are present. Angular
  inputs must be recomputed from the four retained lepton four-vectors and
  Z1/Z2 assignment labels.
- [A5] No generator/truth branches are present. Phase 3 may use MC sample
  membership labels for training and closure, but must not claim truth-matched
  object or particle-level closure.
- [A6] Phase 1 found long `miniRelIso` tails and very small `pvNdof` values.
  These variables are excluded from default selections and classifiers unless
  Phase 3 validates and, if needed, calibrates them.

### Limitations

- [L1] This is a detector-level open-data measurement, not the official CMS
  analysis. It lacks official lepton calibrations, per-event mass
  uncertainties, data-driven Z+X fake estimation, and jet-based production
  categorization.
- [L2] Reducible background is modeled with DY+jets MC only in the nominal
  fit, as requested. TTBar is retained only as a diagnostic/alternative-shape
  cross-check unless review requires inclusion.
- [L3] A mass scan using only M125 signal MC requires approximate template
  shifting or morphing. Phase 4 may quote a mass estimator only if MC closure
  demonstrates that the morphing bias is small relative to the reported
  uncertainty; otherwise the mass result is a calibrated peak-position
  cross-check, not a competitive Higgs mass measurement.
- [L4] VBF sensitivity will be much weaker than CMS-HIG-16-041 unless jet
  information is recovered. If not recovered, the analysis must compare only
  inclusive/channel/category results and explicitly list VBF as non-comparable.
- [L5] The nominal binned `pyhf` template fit is methodologically simpler than
  the official CMS profile-likelihood implementations, which use richer
  category discriminants, official calibrations, and parametric signal
  modeling. This is a method-parity gap, not just a presentation caveat.

### Decisions

- [D1] Use the primary prompt data/MC paths, not local copies, for all nominal
  downstream work.
- [D2] Use a binned simultaneous `pyhf`/HistFactory-style template likelihood,
  with Poisson terms per mass bin and category, Gaussian/log-normal nuisance
  constraints, and MC statistical uncertainty terms.
- [D3] Fit window is fixed to `105 < m4l < 140 GeV`. This matches the signal
  range stated on the CMS-HIG-16-041 public page for the observed
  `mH`/`Gamma_H` likelihood scans and is also used on the CMS-HIG-19-001
  public page for category-yield and kinematic-discriminant figures. The
  broad `70 < m4l < 170 GeV` plots are validation/sideband figures only, not
  the signal-strength or mass/width fit window.
- [D4] Guaranteed nominal categories are final state channels: 4mu, 4e, and
  2e2mu, optionally split by a validated angular/classifier score. VBF-like
  categories are included only after jet recovery passes [A3] mitigation.
- [D5] The nominal signal-strength parameter `mu` scales all Higgs production
  templates together. Production-mode-specific strengths are not a nominal
  deliverable with 10 fb^-1 and no jet categories.
- [D6] The default reducible fake template is DY+jets MC. Its normalization is
  constrained or floated in sidebands if sideband statistics allow; it is not
  hand-scaled to data.
- [D7] Any MVA or NN input must pass a data/MC modeling gate before training:
  chi2/ndf <= 5 in validation distributions, no coherent ratio trend above
  about 20 percent across the populated range, and no unphysical tails. Failing
  inputs are calibrated with before/after plots or discarded.
- [D8] The angular NN is attempted only after Phase 3 validates the lepton
  four-vector reconstruction, Z pairing, and angular-variable formulas on
  MC/data control distributions.
- [D9] Method parity with CMS-HIG-16-041/CMS-HIG-19-001 is addressed by using
  a profile-likelihood signal-strength extraction as the nominal method and
  by requiring Phase 4a to attempt the simultaneous category mass extraction
  defined below, with `mu` profiled. A `zfit` or equivalent parametric
  mass-shape model is an acceptable implementation path. If the mass
  extraction cannot be made, the executor must document closure failure or
  three concrete infeasibility attempts and keep the result as a detector-level
  simplification rather than an official-equivalent method.

### Binding Mass-Extraction Attempt

The nominal Phase 4 mass result must first attempt a simultaneous category
mass extraction, not only a peak estimator. The required attempt is:

1. Build the same simultaneous category workspace used for the `mu` fit, with
   final-state categories and any validated classifier categories sharing a
   common Higgs-mass parameter.
2. Construct signal templates from the M125 samples by an explicit,
   reviewable morphing/shift procedure: apply mass hypotheses by shifting the
   signal `m4l` template relative to the nominal M125 peak, propagate lepton
   momentum scale/resolution variations through the shifted templates, and
   preserve per-category normalization separately from shape changes. A
   `zfit` parametric signal-shape model may replace binned morphing if it
   uses the same categories and records fitted shape parameters.
3. Profile `mu` while scanning/fitting the mass parameter. `mu` is not fixed
   to its nominal or Asimov value in the mass extraction.
4. Run injected-mass closure tests on MC/Asimov pseudo-data using at least
   three mass hypotheses spanning the intended scan range, including the
   nominal M125 point and two shifted injected masses. The reported mass bias
   must be below the larger of `0.2 GeV` or one-third of the expected
   statistical mass uncertainty in every tested category combination; otherwise
   the bias is corrected and revalidated or the mass result is downgraded.
5. Downgrade is allowed only after the closure criteria fail after a
   documented attempted fix, or after three concrete infeasibility attempts
   are recorded with filenames, error/failure mode, and why no supported
   implementation remains. If downgraded, the AN may report only a
   detector-level peak-position cross-check and must not label it a nominal
   simultaneous mass fit.

## Observable Definition

The primary observable is the reconstructed four-lepton invariant mass
`m4l` stored in `h4lTree`, with masses in GeV. The fitted range is
`105 < m4l < 140 GeV` [D3]. The signal-strength fit has one global parameter
of interest, `mu`, defined as the ratio of the fitted H->ZZ->4l signal rate to
the nominal standard-model expectation encoded by the prompt-provided
effective sample cross sections and metadata-generated event counts. The mass
fit adds a shared mass parameter and profiles `mu`.

The secondary observable is a Higgs mass estimator. With only M125 signal
samples, Phase 4 must not claim an official-quality mass scan unless a
validated signal-template morphing procedure is implemented. The fallback is
a detector-level peak estimator in the signal-enhanced category, compared to
CMS-HIG-16-041 `mH = 125.26 +/- 0.21 GeV` and PDG Higgs mass values as
external validation targets.

## Technique Selection

`conventions/extraction.md` does not apply as the governing convention:
this analysis is not a closed-form double-tag, hemisphere-counting, or
tag-and-probe extraction. `conventions/unfolding.md` also does not apply as
the governing convention because no particle-level truth or response matrix
exists in the flat ntuples. The closest methodological convention is the
shape-fit portion of `conventions/search.md`, adapted to a measurement:
profile likelihood, signal injection/recovery, nuisance pulls/constraints,
impact ranking, goodness of fit, and MC statistical uncertainties.

The likelihood model is:

- Categories: final state channels and optional validated classifier-score
  bins; VBF-like categories only if [A3] is resolved.
- Samples: ggH, VBF, WH, ZH signal templates; qqZZ and ggZZ irreducible
  backgrounds; DY+jets reducible fake proxy; TTBar diagnostic only.
- Parameters: `mu` for all signal modes together, nuisance parameters for
  luminosity/normalization, shape, lepton, background, and MC-stat sources.
- Mass extraction: a simultaneous mass scan or fit sharing categories with the
  `mu` workspace is a binding Phase 4a attempt. In that model `mu` is profiled
  and the mass-shape/morphing closure criteria in "Binding Mass-Extraction
  Attempt" control whether the result is nominal or downgraded.
- Binning: variable or fixed `m4l` bins inside `105 < m4l < 140 GeV`, with
  no bin accepted below about five total expected events unless the fit uses
  toy validation and MC-stat terms remain stable.
- Validation: MC-only expected fit in Phase 4a, 10 percent data in Phase 4b,
  full data in Phase 4c.

Method parity requirement [D9]: the binned `pyhf` workspace is acceptable as
the nominal open-data signal-strength method because it keeps the
profile-likelihood structure used by the CMS references. It is not by itself
equivalent to the official analyses. Phase 4a must therefore compare the
nominal binned model to a parametric mass-shape fit or explicitly document why
the available M125-only signal samples and flat ntuple content make that
cross-check infeasible.

## Samples And Background Plan

Phase 1 sample inventory is binding. The primary source paths are:
`/sandbox/work/jfc/analyses/h4ltemplate/data` and
`/sandbox/work/jfc/analyses/h4ltemplate/mc`.

| Process group | Samples | Classification | Nominal use |
| --- | --- | --- | --- |
| Higgs signal | `GluGluToHToZZ.root`, `VBF_HToZZ.root`, `WPHToZZ.root`, `WMHToZZ.root`, `ZHToZZ.root` | Signal | Summed for inclusive `mu`; production labels retained for stacked plots and optional category purity studies. |
| qqZZ | `ZZTo4L.root` | Irreducible background | Main continuum template; normalization from prompt xsec plus systematic. |
| ggZZ | `GGZZ2E2Mu.root`, `GGZZ4Mu.root`, `GGZZ4E.root` | Irreducible background | Separate or merged by final state; shape and normalization systematic. |
| DY+jets | `DYJetsToLL.root` | Reducible/instrumental fake proxy | Nominal fake-background model per user instruction. Low selected entries require conservative MC-stat and shape checks. |
| TTBar | `TTBar.root` | Reducible/top contamination | Diagnostic cross-check only for [L2], not nominal fake estimate unless review requires it. |

Normalization formula: for each MC sample use
`weight = sigma_eff * L / sum(nEvents from Metadata)`, with `L = 10 fb^-1`
from the user prompt converted consistently with pb cross sections. Phase 3
must record the denominator and weight for every sample and must not infer
luminosity from observed data.

Fake-background and sideband protocol:

- The signal window is `105 < m4l < 140 GeV` and is excluded from any
  sideband-only constraint used to set reducible-background normalization or
  shape uncertainties.
- The broad validation range is `70 < m4l < 170 GeV`. Low-mass sideband:
  `70 <= m4l < 105 GeV`; high-mass sideband: `140 < m4l <= 170 GeV`. Phase 3
  may also make wider diagnostic plots, but the sideband constraint must use
  these predeclared windows unless a review-approved downscope explains why
  the ntuples do not populate them.
- DY+jets is nominally constrained by a log-normal normalization nuisance from
  the sideband transfer-factor closure. If the combined weighted DY sideband
  yield is below 10 expected events, the nuisance must be treated as weakly
  constrained or floated with a documented prior-width scan; it must not be
  fixed to the prompt cross section without a closure comparison.
- TTBar is promoted to a nominal separate reducible component if its weighted
  expected yield is at least 10 percent of the DY+jets weighted yield in the
  signal window, or at least 20 percent in either sideband, after the Phase 3
  selection. If below both thresholds, TTBar remains omitted from the nominal
  fake model but its full template difference is assigned as an omission
  systematic on the reducible background.

## Selection Approaches For Phase 3

Phase 3 must implement and compare at least the following two approaches on
the same blinded/expected validation criteria.

### Approach S1: Reference-Like Cut And Channel Fit

Use the candidate already retained by the ntuplizer, then impose documented
event-level requirements using available branches:

- Trigger bitmask requirement using the Phase 1 decoded map, not equality to
  one integer value.
- Channel split by `finalState` after provenance confirmation.
- Flavor-consistent lepton ID checks: electron IDs only where
  `abs(lNpdgId)==11`, muon IDs only where `abs(lNpdgId)==13`.
- Z-candidate sanity checks using `mZ1`, `mZ2`, `lNzId`, and charge/flavor.
- Fit-window requirement `105 < m4l < 140 GeV` for inference; broader
  sideband plots may use `70 < m4l < 170 GeV`.

Advantages: transparent, robust with low statistics, closest to the retained
flat ntuple content. Cost: weaker separation than official CMS matrix-element
and jet categories.

### Approach S2: Angular/Kinematic Classifier Categories

Build category score bins from validated detector-level inputs. Candidate
inputs are `mZ1`, `mZ2`, `pt4l`, `eta4l`, `y4l`, leading/subleading lepton
pt/eta, and recomputed rest-frame angles from the four lepton four-vectors.
The classifier must not include `m4l` itself for a mass-shape fit, except in a
separate diagnostic study, because it would sculpt the fitted observable.

Training labels may use MC sample group membership: Higgs signal samples
versus qqZZ/ggZZ/DY backgrounds. No truth-matching claims are allowed [A5].
The default model should be simple and reviewable: start with a BDT/logistic
baseline, then a small NN only if it improves expected Asimov precision and
passes the input-modeling gate [D7].

Advantages: may recover part of the official kinematic-discriminant
sensitivity from retained lepton information. Costs: higher risk of data/MC
mismodelling and mass sculpting; requires strict validation.

### Approach S3: VBF Recovery/Downscope Path

Phase 3 must complete all recovery checks below before downscoping VBF:

1. Re-read the ntuplizer/provenance material and record whether jets were
   dropped at ntuplization or never available.
2. Check both primary and local branch inventories for any jet-like branch
   names or candidate-level VBF discriminants without opening event data.
3. Check whether a safe event-key join to an allowed upstream NanoAOD/source
   file is possible under `paths.json`; if not allowed or not uniquely keyed,
   state that explicitly.
4. Real jet recovery requires expanding the allowed inputs beyond the current
   `paths.json` allow-list, which currently permits only the flat ntuple data
   and MC directories. If no expanded path is approved and uniquely joinable,
   Phase 3 must immediately perform a formal VBF downscope after recording the
   branch, provenance, and allow-list checks.
5. If recoverable, define a VBF-enriched category using jet multiplicity and
   dijet kinematics, then add jet-energy and category-migration systematics.
6. If not recoverable, write a formal VBF downscope subsection in
   `SELECTION.md`, with evidence from branch/provenance checks and a
   comparison table explaining which CMS-HIG-16-041 categories are
   non-comparable.

No lepton-only category may be called "VBF" in the nominal result. A
lepton-only high-`pt4l` or angular-score category can be used only as a
"production-enriched proxy" with no VBF label.

## Angular NN Feasibility

The retained branches include lepton four-vector primitives
`lNpt`, `lNeta`, `lNphi`, and `lNmass`, plus Z assignment labels
`lNzId`. Phase 3 should compute standard H->ZZ->4l angular variables in the
four-lepton rest frame: `cos(theta*)`, `cos(theta1)`, `cos(theta2)`, `Phi`,
and `Phi1`, together with `mZ1` and `mZ2`. Sources for definitions include
the angular/MELA references linked by CMS-HIG-16-041, including Oreglia's
Appendix D and Anderson et al., PRD 89 (2014) 035007.

Required validation before use:

- Reconstructed four-lepton mass from lepton four-vectors agrees with stored
  `m4l` with median absolute difference below `0.1 GeV` or an explicit unit/
  convention explanation.
- Computed Z masses agree with `mZ1` and `mZ2` with median absolute difference
  below `0.1 GeV` or an explicit pairing/convention explanation.
- Angular variable ranges are physical for every selected event, with counts
  of any out-of-range events written to machine-readable validation output.
- Data/MC comparisons for every candidate angular input pass [D7] before
  training.
- A classifier trained without `m4l` does not sculpt the pre-fit `m4l`
  background shape; Phase 3 must show pre/post score-bin `m4l` closure.
- The NN is not promoted over the BDT/logistic baseline unless it improves the
  expected `mu` uncertainty by at least 10 percent, passes the same GoF gates,
  and uses a held-out validation split with a fixed random seed. Otherwise the
  NN remains a documented attempted approach.
- Before any category split beyond final state is promoted, Phase 3 must write
  a prefit viability table with expected total, signal, and background counts
  for every proposed category and `m4l` bin, plus the number of bins below
  five total expected events. A split is vetoed if more than 25 percent of its
  fit bins are below five expected events, if any category has zero expected
  background after template smoothing, if MC-stat nuisance terms dominate the
  expected `mu` uncertainty, or if per-category GoF/toy validation gives
  p <= 0.05 without a documented remediation.
- Classifier overtraining must be checked with train-versus-validation score
  distributions and a fixed-seed split. Category boundaries must be varied by
  at least one bin or by a small score-threshold scan; nominal conclusions must
  be stable within the expected statistical uncertainty.

## Systematic Plan

Every row marked "Will implement" is binding for Phase 4a unless a later
review accepts a formal downscope.

| Source | Status | Treatment |
| --- | --- | --- |
| Integrated luminosity | Will implement | Normalization nuisance for all MC templates. Use the user target luminosity for central value and public CMS 2017 luminosity uncertainty as a scale reference if applicable. |
| Prompt effective cross sections | Will implement | Normalization nuisance per process group; Phase 3 validates search trail and propagates uncertainty or flags as user-provided if no public match is found. |
| MC statistical uncertainty | Will implement | Bin-by-bin template statistical terms, required because selected DY/TT samples are small and some signal modes have low effective yields. |
| Lepton reconstruction/ID/trigger efficiency | Will implement | Data/MC validation using channel and object-ID distributions; assign rate/shape variations from public CMS references or conservative closure-derived envelopes if scale factors are unavailable. |
| Lepton momentum scale/resolution | Will implement | Shift/smear lepton four-vectors, recompute `m4l`, `mZ1`, `mZ2`, angular variables, and templates; validate against Z peak comparisons. |
| Pileup/PV modeling | Will implement with caution | Use `nPV`/PV variables only for validation or reweighting. Do not use `pvNdof` as a classifier input unless [A6] is resolved. |
| Signal theory normalization | Will implement | Nuisances for ggH, VBF, WH, ZH relative normalizations where used. For inclusive `mu`, keep these as acceptance/composition uncertainties, not as post-hoc tuning. |
| Higgs branching fraction | Will implement if converting to cross section | Needed for comparison to fiducial/inclusive cross-section references; not needed for pure detector-level `mu` if templates already include effective H->4l rates. |
| qqZZ and ggZZ background normalization/shape | Will implement | Independent normalization and shape variations; compare sideband agreement and, if possible, float dominant background normalizations in sidebands. |
| DY+jets fake proxy normalization/shape | Will implement | Large normalization/shape nuisance or sideband-constrained parameter. Explicitly covers the approximation of using DY MC instead of data-driven Z+X. |
| TTBar omission | Will implement as cross-check | Evaluate TTBar template impact on sidebands and signal window; if non-negligible, either include as separate reducible component or assign an omission systematic. |
| Classifier/NN input modeling | Will implement if MVA used | Input validation gate [D7], score-shape closure, calibration/discard rules, and mass-sculpting checks. |
| Angular reconstruction | Will implement if angular inputs used | Four-vector reconstruction, Z-pairing consistency, physical-range checks, and angle-definition source citation. |
| Category migration | Will implement if categories beyond final state are used | Vary classifier score/calibration or jet recovery inputs and propagate migration across categories. |
| Jet/VBF systematics | Not applicable unless [A3] is resolved | No jet branches exist in primary ntuples. If jets are recovered, add jet energy scale/resolution and VBF category migration systematics before review. |
| Unfolding response/model dependence | Not applicable | No particle-level result or response matrix is defined. |
| Closed-form extraction efficiency correlations | Not applicable | `conventions/extraction.md` does not govern this template fit. |

### Shape-Fit Convention Coverage

This analysis adopts the shape-fit/search convention only where it maps onto a
pp H->4l measurement. Rows below are binding Phase 4a coverage requirements
unless explicitly marked not applicable.

| `conventions/search.md` row | Coverage decision |
| --- | --- |
| Signal cross-section theory uncertainty | Will implement: ggH, VBF, WH, and ZH normalization/composition nuisance inputs from public/theory or prompt-effective source hierarchy; retained as acceptance/composition uncertainty for inclusive `mu`. |
| Signal acceptance | Will approximate by MC sample/category acceptance variations and generator/source comparisons where public alternatives exist; if no alternative generator exists, assign a documented fallback envelope from category-stability and lepton-scale/resolution closure. |
| Signal shape | Will implement through the mass-template shift/morphing or parametric signal-shape procedure used by the binding mass-extraction attempt, including mass and width/shape variations where supported. |
| ISR modeling | Not applicable as a LEP beam row; pp replacement is signal and ZZ PDF/QCD-scale acceptance/modeling uncertainty plus pileup validation. |
| 4-fermion backgrounds | Will implement as pp irreducible qqZZ and ggZZ background normalization/shape uncertainties, not LEP WW/We+nu generator comparisons. |
| Background normalization | Will implement for qqZZ, ggZZ, DY+jets, and promoted TTBar using theory/prompt-source priors and sideband constraints defined above. |
| Background shape | Will implement by template variations, sideband closure, alternative binning, and TTBar/DY reducible-shape comparisons. |
| qqbar(gamma) modeling | Not applicable as a LEP two-fermion row; pp replacement is DY+jets fake-proxy modeling and reducible-background shape/normalization envelope. |
| MC statistics | Will implement bin-by-bin template statistical nuisance terms. |
| Detector simulation model | Will approximate by data/MC validation of retained observables and closure-derived envelopes because no official detector recalibration is available. |
| Object calibration | Will implement lepton efficiency and momentum scale/resolution uncertainties; jet calibration only if real jets are recovered under [A3]. |
| Beam energy | Not applicable to pp mass calibration; pp replacement is lepton momentum scale/resolution and external PDG/CMS mass-reference comparison, never a fitted beam-energy nuisance. |
| Luminosity | Will implement a normalization nuisance. The central value is the user-provided `10 fb^-1`; the uncertainty follows the fallback hierarchy below. |
| QCD scale variations | Will implement for signal and ZZ normalization/acceptance where public values or prompt-effective uncertainties are available; otherwise use documented fallback envelopes. |
| Fragmentation model | Not applicable to the nominal no-jet, leptonic H->4l fit; if real VBF jets are recovered, revisit as jet/category modeling before review. |
| Heavy flavour treatment | Not applicable unless a b-tagged or heavy-flavour category is introduced, which is not part of this strategy. |

### Fallback Systematics Evidence Rules

Fallback nuisance values must be reviewable and machine-readable. For each
source, Phase 3/4 writes `systematics_sources.json` or an equivalent table
with: source name, nominal value, uncertainty, citation/search trail, closure
metric used, fallback flag, and affected templates.

- Source hierarchy: use official public CMS/open-data calibration or paper
  value first; then validated prompt-provided effective value; then
  same-year public reference value scaled only with documented rationale; then
  a conservative closure-derived envelope. Values from model memory are not
  allowed.
- Luminosity: central value remains the user-provided `10 fb^-1`. If no
  certified luminosity uncertainty for that subset exists, treat the central
  value as user-provided and assign a conservative normalization envelope at
  least as large as the public CMS 2017 full-year relative luminosity
  uncertainty used as a scale reference, with a prior-width sensitivity scan.
- Effective cross sections: every prompt effective cross section needs a
  public/campaign search trail and yield-closure comparison. If no public
  match exists, mark it user-provided and assign a per-process normalization
  nuisance from closure and comparison to reference yields rather than
  silently treating it as independently verified.
- Lepton efficiencies: prefer public CMS scale-factor uncertainties. If none
  apply to these ntuples, derive a closure envelope from channel ratios,
  Z-candidate control distributions, and trigger/ID validation plots; store
  before/after yields and chi2/p-values.
- Other fallback envelopes: define the envelope from at least one closure
  comparison or alternative modeling choice. If only a user-provided value
  exists and no closure comparison can be constructed, the artifact must label
  the nuisance as user-provided, scan a wider prior, and report the impact as
  a limitation instead of a calibrated systematic.

## Validation Tests

Phase 3 and Phase 4 must make these machine-readable where practical.

1. File provenance check: primary paths, file sizes, tree entries, metadata
   denominators, and no mixing with local copies.
2. MC normalization check: `sigma_eff * L / nEvents` weights, expected yields
   per sample, and sideband yield comparison.
3. Selection cutflow: monotonic counts and weighted yields per sample/channel.
4. Candidate-variable data/MC validation: chi2/ndf and p-values for every
   selection or classifier input; [D7] discard/calibrate rule enforced.
5. Angular reconstruction closure: stored-vs-recomputed `m4l`, `mZ1`, `mZ2`;
   physical angular ranges.
6. Approach comparison: S1 versus S2 expected precision, GoF, stability, and
   background closure on the same datasets.
7. Method-parity and mass-fit cross-check: execute the binding simultaneous
   category mass extraction or document the three-attempt infeasibility rule,
   and compare the nominal binned `pyhf` signal-strength fit to the mass-shape
   result when feasible.
8. Signal injection/recovery: inject `mu = 0`, `1`, `2`, and `5` into MC/Asimov
   pseudo-data; fitted `mu` bias must be below 20 percent or investigated.
9. Goodness of fit: category and combined chi2/ndf with p-value; toys if
   asymptotic approximations are questionable due to low bin counts.
10. Nuisance pulls/constraints and impact ranking after Phase 4 fits.
11. 10 percent data stability: fixed-seed subsample, compare to expected
    results with statistical scaling.
12. Mass-template closure: if a mass estimator or morphing scan is reported,
    demonstrate bias and uncertainty on MC pseudo-data.
13. Category viability: prefit expected total/signal/background counts per
    proposed category and `m4l` bin, low-stat bin counts, MC-stat stability,
    overtraining, category-boundary stability, and GoF veto outcomes.

## Precision Estimates

CMS-HIG-16-041 reports `mu = 1.05 +0.19/-0.17` at `mH = 125.09 GeV`,
fiducial cross section `2.92 +0.48/-0.44 (stat) +0.28/-0.24 (syst) fb`, and
`mH = 125.26 +/- 0.21 GeV` using 35.9 fb^-1. Scaling the statistical part
from 35.9 fb^-1 to 10 fb^-1 by `sqrt(35.9/10)` suggests an optimistic
signal-strength/fiducial-rate statistical degradation of about a factor of
1.9 before accounting for open-data limitations. Therefore the expected
open-data `mu` precision is likely at best about 30-40 percent and may be
worse if DY fake modeling or category loss dominates.

CMS-HIG-19-001 reports `mu = 0.94 +/- 0.07 (stat) +0.09/-0.08 (syst)` and an
inclusive fiducial cross section `2.84 +0.23/-0.22 (stat) +0.26/-0.21 (syst)
fb` with 137 fb^-1. This is not a direct precision target for 10 fb^-1, but
it supplies a modern systematic coverage checklist.

Phase 1 MC selected-entry counts show large irreducible samples but very
small reducible samples: DY has 463 selected entries and TTBar has 639 in
the primary files, while ZZ has 1,864,310 selected entries and ggH has
138,479 selected entries. The reducible-background uncertainty and MC-stat
terms are therefore expected to be important in sidebands and low-yield bins.

For the mass estimator, scaling the CMS-HIG-16-041 `0.21 GeV` uncertainty by
the same luminosity factor gives roughly `0.4 GeV` before the loss of
per-event mass uncertainty and official lepton calibration. A realistic
open-data mass uncertainty should be treated as order `0.5-1.0 GeV` until
Phase 4a closure tests quantify it.

## Reference Analysis Table

| Reference | Dataset | Central values | Methodology/key choices | MC sample size |
| --- | --- | --- | --- | --- |
| CMS-HIG-16-041 / JHEP 11 (2017) 047 | 35.9 fb^-1 at 13 TeV, 2016 CMS H->ZZ->4l | `mu = 1.05 +0.19/-0.17` at `mH = 125.09 GeV`; fiducial cross section `2.92 +0.48/-0.44 (stat) +0.28/-0.24 (syst) fb`; SM fiducial prediction `2.76 +/- 0.14 fb`; `mH = 125.26 +/- 0.21 GeV`; `Gamma_H < 1.10 GeV` at 95 percent CL. | Profile-likelihood H->4l analysis with seven production-sensitive categories, official lepton calibrations, per-event mass treatment, kinematic discriminants, data-driven Z+X, and differential/fiducial measurements. Public page evidence: abstract gives the central values; Figure 10 states the `105 < m4l < 140 GeV` signal range for mass/width likelihood scans; Summary gives statistical/systematic mass split. | NOT FOUND in public page/Phase 1 trail; requires paper auxiliary tables or CMS internal production details. |
| CMS-HIG-19-001 / EPJC 81 (2021) 488 | 137 fb^-1 at 13 TeV, full Run 2 CMS H->ZZ->4l | `mu = 0.94 +/- 0.07 (stat) +0.09/-0.08 (syst)` at `mH = 125.38 GeV`; inclusive fiducial cross section `2.84 +0.23/-0.22 (stat) +0.26/-0.21 (syst) fb`; SM fiducial prediction `2.84 +/- 0.15 fb`. | Full Run 2 production cross-section analysis with STXS-style categories, parametric signal models, kinematic discriminants, data-driven Z+X, and systematic impact ranking. Public page evidence: abstract gives central values; Figure 3 lists dominant systematic sources; Figures 6, 7, and 9 use `105 < m4l < 140 GeV` for category yields, Z-mass distributions, and kinematic discriminants. | NOT FOUND in public page/Phase 1 trail; use public plots/tables for methodology only. |
| PDG gauge/Higgs summary tables | World averages | Phase 1 retained PDG 2024 values: `mZ = 91.1880 +/- 0.0020 GeV`, `Gamma_Z = 2.4955 +/- 0.0023 GeV`, `mH = 125.20 +/- 0.11 GeV`, Higgs width summary `3.7 +1.9/-1.4 MeV`, and `H->ZZ*` fraction `2.80 +/- 0.30 percent`. | External validation/world-average comparison, not fit tuning. Update to the latest PDG table during Doc 4c if values changed. | Not applicable. |

## Flagship Figures

1. Inclusive `m4l` stacked data/MC distribution over broad and signal windows,
   with ratio panel and clear DY fake proxy caveat.
2. Simultaneous-fit `m4l` distribution in final-state categories and any
   validated classifier categories, including prefit and postfit overlays.
3. Signal-strength likelihood scan for `mu` and, if validated, mass estimator
   scan/profile.
4. Input validation grid for candidate classifier/angular variables, with
   chi2/ndf labels and discard/calibrate verdicts.
5. Systematic impact ranking and uncertainty breakdown on `mu`.
6. Comparison summary table/figure against CMS-HIG-16-041, CMS-HIG-19-001,
   and PDG/world-average mass values, with explicit non-comparable rows.

The final AN must include a comparability matrix before extracting numerical
pulls from reference values. Required rows are inclusive `mu`, mass, fiducial
cross section, width, production-sensitive categories, VBF categories, and
reducible-background treatment. Each row is classified as matched,
approximated/not directly comparable, or unavailable/not measured; pulls are
reported only for matched quantitative observables. The matrix must also keep
the HEPData `ins1608162` versus `ins1608166` ambiguity as a cleanup item until
the record identity is resolved before numerical table extraction.

Methodology diagrams planned for the analysis note:

- Data/MC sample and template-building flow.
- Category decision tree, including VBF recovery/downscope branch.
- Staged validation flow: expected MC -> 10 percent data -> full data.

## Phase 3 Binding Instructions

Phase 3 must:

- Implement S1 and S2, then compare them quantitatively before choosing the
  nominal configuration. Do not select a classifier only because it improves
  expected precision; it must also pass data/MC input modeling and GoF gates.
- Use the primary prompt paths from `paths.json` and record file sizes/tree
  entries before processing.
- Validate MC normalization before any yield-normalized data/MC plot or fit.
- Decode trigger bits using the Phase 1 map.
- Apply lepton ID flags only to matching lepton flavors.
- Exclude `miniRelIso` and `pvNdof` from default inputs unless validation
  passes and a calibration is documented.
- Attempt angular-variable reconstruction from lepton four-vectors; document
  formulas, sources, closure, and physical ranges.
- Attempt VBF information recovery once; if unsuccessful, write a formal
  downscope and do not use a VBF label for lepton-only proxies.
- Produce diagnostic figures for any rejected serious approach, especially a
  rejected classifier or VBF recovery attempt.
- Save machine-readable outputs for cutflows, input validation, classifier
  metrics, and fit-ready histograms.

## Open Issues

- Public validation of prompt effective cross sections may be incomplete for
  private/effective filtered samples. If no source is found, Phase 3 must mark
  them user-provided and carry a normalization systematic instead of treating
  them as independently verified.
- VBF categorization is not feasible from current branches; recovery or formal
  downscope is mandatory.
- A mass result requires validated template morphing or must be presented as a
  limited detector-level peak estimator.
- DY-only fake modeling is a deliberate user simplification and will be a
  visible comparability limitation versus CMS-HIG-16-041 and CMS-HIG-19-001.

## Pre-Review Self-Check

- Phase 1 deliverables read: DONE.
- Fallback literature searches executed: DONE; at least six public searches
  and CMS/HEPData/PDG pages retained.
- Observable definition verified against Phase 1 literature: DONE.
- Backgrounds classified: DONE.
- At least two qualitatively different selection approaches: DONE (S1, S2;
  S3 is a recovery/downscope path).
- MVA/NN considered with binding feasibility gates: DONE.
- Systematic plan enumerated and grounded in MC coverage: DONE.
- Precision estimates grounded in Phase 1 MC statistics and reference values:
  DONE.
- Reference table includes central values, methods, and MC-size status:
  DONE.
- Method parity addressed: DONE; profile likelihood retained, official-only
  ingredients identified as [L5], with a Phase 4a parametric-fit cross-check
  or documented infeasibility required by [D9].
- Mitigation strategy for every Phase 1 constraint: DONE.
- [A], [L], and [D] labels defined: DONE.
- Flagship figures and Phase 3 instructions: DONE.
- `COMMITMENTS.md` populated: DONE in this session.
