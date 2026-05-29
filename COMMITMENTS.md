# Commitments

Tracks all binding commitments from Phase 2 onward.
Update at every phase boundary.

## Status key

- `[x]` Resolved
- `[D]` Formally downscoped (with documented justification)
- `[ ]` Not yet addressed

## Systematic sources

- [ ] [D2] Integrated luminosity normalization nuisance for all MC templates.
- [ ] [A2] Prompt effective cross-section validation or documented
  user-provided fallback with normalization uncertainty.
- [ ] MC statistical uncertainty terms for all fit templates.
- [ ] Lepton reconstruction, identification, and trigger efficiency
  uncertainty.
- [ ] Lepton momentum scale and resolution shape uncertainty propagated to
  `m4l`, `mZ1`, `mZ2`, and angular inputs where used.
- [ ] Pileup/PV modeling validation; `pvNdof` excluded unless validated.
- [ ] Signal production normalization/composition uncertainty for ggH, VBF,
  WH, ZH signal templates.
- [ ] Higgs branching-fraction uncertainty if converting `mu` to a cross
  section.
- [ ] qqZZ and ggZZ background normalization and shape uncertainties.
- [ ] DY+jets fake-proxy normalization and shape uncertainty.
- [ ] TTBar omission/inclusion cross-check systematic.
- [ ] Classifier/NN input modeling and category migration uncertainty if MVA
  categories are used.
- [ ] Angular reconstruction uncertainty if angular variables are used.
- [ ] [A3] Jet/VBF decision gate: complete provenance, branch-inventory, and
  allowed-source join checks before either adding jet energy scale/resolution
  plus VBF migration systematics or formally downscoping VBF.

## Validation tests

- [ ] File provenance check: primary paths, file sizes, tree entries, metadata
  denominators, and no local/primary mixing.
- [ ] MC normalization check: `sigma_eff * L / nEvents` weights and expected
  yields per sample.
- [ ] Selection cutflow monotonicity with counts and weighted yields per
  sample/channel.
- [ ] Candidate-variable data/MC validation for every selection or classifier
  input with chi2/ndf and p-values.
- [ ] Enforce [D7] input gate: chi2/ndf <= 5, no coherent >20% ratio trend,
  and no unphysical tails unless calibrated.
- [ ] Angular reconstruction closure: stored-vs-recomputed `m4l`, `mZ1`,
  `mZ2`, and physical angular ranges.
- [ ] S1 cut-based versus S2 classifier/category approach comparison using
  expected precision, GoF, and closure.
- [ ] [D9] Method-parity cross-check: compare the nominal binned `pyhf`
  signal-strength fit to a parametric mass-shape fit if feasible; otherwise
  document three concrete failed attempts and the exact blocking reason.
- [ ] Signal injection/recovery at `mu = 0`, `1`, and `2`; bias above 20%
  triggers investigation.
- [ ] Combined and per-category goodness-of-fit with chi2/ndf and p-value.
- [ ] Nuisance pulls/constraints and impact ranking after fits.
- [ ] Fixed-seed 10% data validation compared to expected results.
- [ ] Mass-template closure if any mass estimator or morphing scan is reported.
- [ ] VBF downscope review gate: if no jet information is recoverable, produce
  a `SELECTION.md` subsection with the evidence and a CMS category
  non-comparability table.
- [ ] Angular/NN promotion gate: NN must beat the BDT/logistic baseline by at
  least 10% expected `mu` uncertainty and pass all GoF/input validation gates.

## Flagship figures

- [ ] Inclusive `m4l` stacked data/MC distribution over broad and signal
  windows with ratio panel.
- [ ] Prefit/postfit `m4l` distributions in final-state categories and any
  validated classifier categories.
- [ ] Signal-strength likelihood scan for `mu` and validated mass profile or
  peak-estimator scan.
- [ ] Classifier/angular input validation grid with chi2/ndf labels and
  discard/calibrate verdicts.
- [ ] Systematic impact ranking and uncertainty breakdown on `mu`.
- [ ] Comparison summary figure/table against CMS-HIG-16-041, CMS-HIG-19-001,
  and PDG/world-average mass values.

## Cross-checks

- [ ] [A1] Primary-vs-local ROOT copy freeze: use primary prompt paths unless
  formal provenance revision is reviewed.
- [ ] [A3] VBF recovery attempt from provenance/upstream ntuples; if failed,
  formal downscope with evidence.
- [ ] [A4] Angular variables recomputed from lepton four-vectors and validated
  before NN use.
- [ ] Stored-vs-recomputed four-vector closure: median absolute differences
  below `0.1 GeV` for `m4l`, `mZ1`, and `mZ2`, or documented unit/pairing
  explanation.
- [ ] [L2] TTBar reducible-background diagnostic compared with DY-only nominal
  fake proxy.
- [ ] Sideband background normalization and shape closure before signal-window
  interpretation.
- [ ] Classifier mass-sculpting check: score categories must not create a fake
  `m4l` peak.
- [ ] Alternative binning stability for `m4l` templates.
- [ ] Final-state channel compatibility: 4e, 4mu, and 2e2mu fitted separately
  and compared to combined result.

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
  CMS public-page-linked HEPData record or document any HEPData redirect.
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
