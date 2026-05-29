# Commitments

Tracks all binding commitments from Phase 2 onward.
Update at every phase boundary.

## Status key

- `[x]` Resolved
- `[D]` Formally downscoped (with documented justification)
- `[ ]` Not yet addressed

## Strategy decision carryover

Every Phase 2 decision label must have a downstream artifact or
machine-readable proof item.

- [x] [D1][VT1] Use primary prompt data/MC paths, not local copies. Proof:
  `phase3_selection/outputs/selection_provenance.json` records path, file
  size, tree entries, metadata denominators, and local/primary mixing status.
- [ ] [D2][VT9][VT10] Use a binned simultaneous `pyhf`/HistFactory-style
  template likelihood. Proof: Phase 4 workspaces and fit result JSON include
  categories, samples, Poisson terms, nuisance constraints, MC-stat terms,
  GoF, pulls, and impacts.
- [x] [D3][VT1][VT3] Enforce `105 < m4l < 140 GeV` for signal-strength and
  mass/width inference. Proof: fit-ready histogram metadata and selection
  cutflow JSON record the fit window; broader sideband plots are labeled
  validation-only.
- [x] [D4][VT6][VT13] Nominal categories are final states 4mu, 4e, and 2e2mu,
  with extra classifier categories only after viability gates; no VBF-like
  category unless jet recovery passes [A3]. Proof: category schema JSON,
  prefit count table, and `SELECTION.md` category decision section.
- [ ] [D5][VT9][FIG3] Use one global `mu` scaling all Higgs production
  templates together. Proof: workspace parameter JSON and `mu` likelihood scan
  show a single POI, with production modes retained only as components or
  composition nuisances.
- [x] [D6][VT2][SP10] Use DY+jets MC as the default reducible fake template,
  sideband constrained/floated as specified, and never hand-scale to the data
  integral. Proof: MC normalization table, sideband transfer-factor JSON, and
  fit configuration show DY treatment and absence of data-integral scaling.
- [x] [D7][VT4][FIG4] Apply the input-modeling gate before any MVA/NN input is
  used. Proof: input-validation table with chi2/ndf, p-values, ratio-trend
  verdicts, and discard/calibrate decisions.
- [x] [D8][VT5][SP13] Attempt the angular NN only after four-vector, Z-pairing,
  and angular-formula validation. Proof: angular closure JSON and physical
  range checks precede any classifier training artifact.
- [ ] [D9][VT7][VT12][FIG3] Address method parity through a binding
  simultaneous category mass-extraction attempt with `mu` profiled and
  injected-mass closure, or document three concrete infeasibility attempts
  before downgrade. Proof: mass workspace/scan JSON, injected-mass closure
  table, or infeasibility log with filenames and failure modes.

## Systematic sources

- [ ] [D2][SP1] Integrated luminosity normalization nuisance for all MC
  templates. Proof: `systematics_sources.json` row with central `10 fb^-1`,
  uncertainty source hierarchy, fallback flag if user-provided, and prior scan.
- [x] [A2][SP2] Prompt effective cross-section validation or documented
  user-provided fallback with normalization uncertainty. Proof:
  public/campaign search trail, yield-closure comparison, and per-process
  nuisance in `systematics_sources.json`.
- [ ] [D2][SP3][VT9] MC statistical uncertainty terms for all fit templates.
  Proof: workspace includes bin-by-bin MC-stat modifiers and stability tests.
- [ ] [D7][SP4] Lepton reconstruction, identification, and trigger efficiency
  uncertainty. Proof: public scale-factor source or closure-derived envelope
  with channel ratios, trigger/ID plots, and chi2/p-values.
- [ ] [D9][SP5][VT12] Lepton momentum scale and resolution shape uncertainty
  propagated to `m4l`, `mZ1`, `mZ2`, and angular inputs where used. Proof:
  shifted/smeared template files and mass-closure impact table.
- [x] [A6][SP6] Pileup/PV modeling validation; `pvNdof` excluded unless
  validated. Proof: input-validation verdict and explicit classifier input
  allow/discard list.
- [ ] [D5][SP7] Signal production normalization/composition uncertainty for
  ggH, VBF, WH, ZH signal templates. Proof: workspace nuisance list and
  composition impact on inclusive `mu`.
- [ ] [FIG6][SP8] Higgs branching-fraction uncertainty if converting `mu` to a
  cross section. Proof: comparison/fiducial-cross-section JSON records whether
  the conversion was performed and the cited branching-fraction source.
- [ ] [SP9] qqZZ and ggZZ background normalization and shape uncertainties.
  Proof: background nuisance rows, sideband closure, and alternative-binning
  variations.
- [x] [D6][SP10] DY+jets fake-proxy normalization and shape uncertainty.
  Proof: DY sideband transfer-factor closure and fit nuisance prior/floating
  status.
- [x] [L2][SP11] TTBar omission/inclusion cross-check systematic. Proof:
  TTBar/DY weighted-yield ratios in sidebands and signal window, nominal
  inclusion decision, and omission-systematic template if below threshold.
- [ ] [D7][D8][SP12] Classifier/NN input modeling and category migration
  uncertainty if MVA categories are used. Proof: score-shape closure,
  boundary-stability scan, and migration nuisance table.
- [x] [D8][SP13] Angular reconstruction uncertainty if angular variables are
  used. Proof: four-vector/Z-pairing closure and physical-range counts.
- [D] [A3] Jet/VBF decision gate: complete provenance, branch-inventory, and
  allowed-source join checks before either adding jet energy scale/resolution
  plus VBF migration systematics or formally downscoping VBF. Proof:
  `SELECTION.md` VBF subsection and allow-list/provenance evidence; no
  lepton-only category may be labeled VBF.

## Validation tests

- [x] [D1][VT1] File provenance check: primary paths, file sizes, tree entries,
  metadata denominators, and no local/primary mixing. Proof:
  `selection_provenance.json`.
- [x] [D6][VT2] MC normalization check: `sigma_eff * L / nEvents` weights and
  expected yields per sample. Proof: normalization JSON/table, with luminosity
  not inferred from data.
- [x] [D3][VT3] Selection cutflow monotonicity with counts and weighted yields
  per sample/channel. Proof: cutflow JSON and `SELECTION.md` table.
- [x] [D7][VT4] Candidate-variable data/MC validation for every selection or
  classifier input with chi2/ndf and p-values. Proof: input-validation JSON.
- [x] [D7][VT4] Enforce input gate: chi2/ndf <= 5, no coherent >20% ratio
  trend, and no unphysical tails unless calibrated. Proof: discard/calibrate
  verdict table with before/after plots for calibrated inputs.
- [x] [D8][VT5] Angular reconstruction closure: stored-vs-recomputed `m4l`,
  `mZ1`, `mZ2`, and physical angular ranges. Proof: angular-closure JSON.
- [x] [D4][VT6] S1 cut-based versus S2 classifier/category approach comparison
  using expected precision, GoF, and closure. Proof: approach-comparison JSON.
- [ ] [D9] Method-parity cross-check: compare the nominal binned `pyhf`
  signal-strength fit to a simultaneous category mass-shape fit if feasible;
  otherwise document three concrete failed attempts and the exact blocking
  reason. Proof: mass-fit workspace/scan JSON or infeasibility log.
- [ ] [D9][VT8] Signal injection/recovery at `mu = 0`, `1`, `2`, and `5`; bias
  above 20% triggers investigation. Proof: injection-result JSON with injected
  and fitted `mu`.
- [ ] [D2][VT9] Combined and per-category goodness-of-fit with chi2/ndf and
  p-value. Proof: GoF JSON and toy-validation output if low-stat bins remain.
- [ ] [D2][VT10] Nuisance pulls/constraints and impact ranking after fits.
  Proof: pulls/impacts JSON and systematic impact figure.
- [ ] [VT11] Fixed-seed 10% data validation compared to expected results.
  Proof: seed, event-count, and stability-comparison JSON.
- [ ] [D9][VT12] Mass-template closure if any mass estimator or morphing scan
  is reported. Proof: injected-mass closure table with bias threshold verdict.
- [D] [A3][D4] VBF downscope review gate: if no jet information is recoverable,
  produce a `SELECTION.md` subsection with the evidence and a CMS category
  non-comparability table. Proof: branch/provenance/allow-list evidence and
  no VBF label on lepton-only proxies.
- [x] [D7][D8][VT13] Angular/NN promotion gate: NN must beat the BDT/logistic
  baseline by at least 10% expected `mu` uncertainty and pass all GoF/input
  validation gates. Proof: prefit category/bin count table, low-stat bin
  count, overtraining test, category-boundary stability scan, and GoF veto
  outcomes.

## Flagship figures

- [x] [FIG1][D6] Inclusive `m4l` stacked data/MC distribution over broad and
  signal windows with ratio panel and DY fake-proxy caveat.
- [ ] [FIG2][D4] Prefit/postfit `m4l` distributions in final-state categories
  and any validated classifier categories.
- [ ] [FIG3][D5][D9] Signal-strength likelihood scan for `mu` and validated
  simultaneous mass profile or explicitly downgraded peak-estimator scan.
- [x] [FIG4][D7][D8] Classifier/angular input validation grid with chi2/ndf
  labels and discard/calibrate verdicts.
- [ ] [FIG5][D2][SP*] Systematic impact ranking and uncertainty breakdown on
  `mu`.
- [ ] [FIG6][REF-MATRIX] Comparison summary figure/table against
  CMS-HIG-16-041, CMS-HIG-19-001, and PDG/world-average mass values.

## Cross-checks

- [x] [A1][D1][VT1] Primary-vs-local ROOT copy freeze: use primary prompt paths
  unless formal provenance revision is reviewed.
- [D] [A3][D4] VBF recovery attempt from provenance/upstream ntuples; real jet
  recovery requires expanded allowed paths beyond current `paths.json`; if
  failed, formal downscope with evidence.
- [x] [A4][D8][VT5] Angular variables recomputed from lepton four-vectors and
  validated before NN use.
- [x] [D8][VT5] Stored-vs-recomputed four-vector closure: median absolute
  differences below `0.1 GeV` for `m4l`, `mZ1`, and `mZ2`, or documented
  unit/pairing explanation.
- [x] [L2][D6][SP11] TTBar reducible-background diagnostic compared with
  DY-only nominal fake proxy and numeric inclusion/omission threshold.
- [x] [D6][SP10] Sideband background normalization and shape closure before
  signal-window interpretation, with `105 < m4l < 140 GeV` excluded from
  sideband constraints.
- [x] [D7][D8] Classifier mass-sculpting check: score categories must not
  create a fake `m4l` peak.
- [ ] [D2][VT9] Alternative binning stability for `m4l` templates.
- [ ] [D4][D5] Final-state channel compatibility: 4e, 4mu, and 2e2mu fitted
  separately and compared to combined result.

## Final AN comparability matrix

- [ ] [REF-MATRIX][FIG6] Inclusive `mu`: classify as matched if the fit has
  one global signal-strength POI in the same `105 < m4l < 140 GeV` inference
  window and compatible category inclusiveness; pulls required only if matched.
- [ ] [REF-MATRIX][D9] Mass: classify as matched only if the simultaneous
  category mass extraction with `mu` profiled passes injected-mass closure;
  otherwise classify as approximated detector-level peak comparison.
- [ ] [REF-MATRIX] Fiducial cross section: classify as matched only if a
  documented acceptance/fiducial conversion is implemented with cited
  branching-fraction and acceptance inputs; otherwise approximated or
  unavailable.
- [ ] [REF-MATRIX] Width: classify as unavailable unless a validated width
  likelihood/shape interpretation is implemented; no pull required when
  unavailable.
- [ ] [REF-MATRIX][D4] Production-sensitive categories: classify as matched
  only for categories with comparable observables and acceptance; otherwise
  approximated/not directly comparable.
- [ ] [REF-MATRIX][A3] VBF categories: classify as unavailable/not measured
  unless real jet recovery passes; lepton-only proxies are not VBF matches.
- [ ] [REF-MATRIX][D6] Reducible-background treatment: classify as
  approximated because DY+jets MC replaces official data-driven Z+X unless a
  later reviewed method changes this.

## Comparison targets

- [REF-CMS-HIG-16-041] CMS-HIG-16-041 / JHEP 11 (2017) 047, 35.9 fb^-1 at
  13 TeV. Public page reports `mu = 1.05 +0.19/-0.17` at
  `mH = 125.09 GeV`; fiducial cross section
  `2.92 +0.48/-0.44 (stat) +0.28/-0.24 (syst) fb`; SM fiducial prediction
  `2.76 +/- 0.14 fb`; `mH = 125.26 +/- 0.21 GeV`; and
  `Gamma_H < 1.10 GeV` at 95% CL. Methodology: profile-likelihood H->4l
  analysis with seven production-sensitive categories, official lepton
  calibrations, kinematic discriminants, and data-driven Z+X. MC sample size:
  NOT FOUND in public page/Phase 1 trail. Source:
  https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-16-041/
- [REF-HEPDATA-HIG-16-041] HEPData record linked from CMS-HIG-16-041 for
  public numerical tables and correlations. Use for differential/fiducial
  comparison extraction where available. MC sample size: NOT APPLICABLE.
  Source: https://www.hepdata.net/record/ins1608162. Note: Phase 1 artifacts
  also mention an `ins1608166` URL/DOI trail; Phase 3/Doc phases must use the
  CMS public-page-linked HEPData record or document any HEPData redirect
  before numerical comparison extraction.
- [REF-CMS-HIG-19-001] CMS-HIG-19-001 / EPJC 81 (2021) 488, 137 fb^-1 at
  13 TeV. Public page reports `mu = 0.94 +/- 0.07 (stat) +0.09/-0.08 (syst)`
  at `mH = 125.38 GeV`; inclusive fiducial cross section
  `2.84 +0.23/-0.22 (stat) +0.26/-0.21 (syst) fb`; SM prediction
  `2.84 +/- 0.15 fb`. Methodology: full Run 2 production cross-section
  analysis with STXS-style categories, parametric signal models, kinematic
  discriminants, and systematic impact ranking. MC sample size: NOT FOUND in
  public page/Phase 1 trail. Source:
  https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-19-001/
- [REF-METHOD-PARITY] Public CMS reference methodology targets to compare
  against, not necessarily to reproduce exactly: CMS-HIG-16-041 uses seven
  production-sensitive categories and mass/width likelihood scans in the
  `105 < m4l < 140 GeV` signal range; CMS-HIG-19-001 public figures document
  category yields and kinematic discriminants in `105 < m4l < 140 GeV` and
  list dominant systematic sources. Phase 4a must state which ingredients are
  matched, approximated, or unavailable.
- [REF-PDG-2024] PDG 2024 gauge/Higgs summary values retained by Phase 1:
  `mZ = 91.1880 +/- 0.0020 GeV`, `Gamma_Z = 2.4955 +/- 0.0023 GeV`,
  `mH = 125.20 +/- 0.11 GeV`, Higgs width summary
  `3.7 +1.9/-1.4 MeV`, and `H->ZZ*` fraction `2.80 +/- 0.30%`.
  Methodology: world-average validation inputs, not fit tuning. MC sample
  size: NOT APPLICABLE. Source:
  https://pdg.lbl.gov/2024/tables/rpp2024-sum-gauge-higgs-bosons.pdf
