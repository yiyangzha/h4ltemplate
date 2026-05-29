# Literature Survey

Session: `albert_0f97`
Created: 2026-05-29T18:42:39.946563+00:00

## Search Trail

- MCP status: `MCP_ALPHAXIV=false`, `MCP_LEP_CORPUS=false`; no MCP tools called.
- Public searches: `CMS-HIG-16-041 JHEP 11 2017 047`, `arXiv 1706.09936 mass window`, `HEPData CMS-HIG-16-041`, `CMS luminosity 2017 13 TeV`, and `PDG 2024 Gauge and Higgs Bosons Summary Table`.
- Primary public sources retained: CMS-HIG-16-041 public publication page, CMS-PAS-HIG-16-041 public preliminary page, HEPData record DOI 10.17182/hepdata.80189, CMS-PAS-LUM-20-001 luminosity page, and PDG 2024 summary table.

## Reference Analysis: CMS-HIG-16-041 / JHEP 11 (2017) 047

CMS-HIG-16-041 measured properties of the Higgs boson in H->ZZ->4l with 35.9 fb^-1 at 13 TeV. The public CMS page gives the signal-strength definition and reports mu = 1.05 +0.19/-0.17 at mH = 125.09 GeV, a fiducial cross section of 2.92 +0.48/-0.44 (stat) +0.28/-0.24 (syst) fb compatible with an SM prediction of 2.76 +/- 0.14 fb, mH = 125.26 +/- 0.21 GeV, and Gamma_H < 1.10 GeV at 95% CL. The same page documents seven production-sensitive categories, including VBF-1jet and VBF-2jet categories, and shows categorization discriminants in 118 < m4l < 130 GeV.

For this open-data analysis, the most directly comparable results are the m4l distribution shape, a simplified simultaneous category signal-strength fit, the inclusive signal strength, and broad production-category behavior. The full CMS mass measurement is only partially comparable because the official result uses calibrated lepton momenta, per-event mass uncertainties, a kinematic discriminant, data-driven Z+X estimation, and the full 35.9 fb^-1 2016 dataset, while this analysis uses 10 fb^-1 of 2017 open-data ntuples and a DY+jets MC approximation for reducible background.

## Mass Window and Methods

The public figure descriptions for CMS-HIG-16-041 state that the observed mass/width likelihood scans use the signal range 105 < m4l < 140 GeV. Phase 2 should therefore adopt that fit window for the mass/signal-strength extraction unless the ntuple content makes it infeasible. The broader 70 < m4l < 170 GeV distribution is useful for exploratory and sideband plots but is not the quoted mass-fit window.

## Modern/Public Comparable Results

The HEPData record for the same paper provides public numerical tables for integrated and differential fiducial cross sections and correlations. A later CMS H->4l production cross-section publication using 137 fb^-1 reports mu = 0.94 +/- 0.07 (stat) +0.09/-0.08 (syst) and an inclusive fiducial cross section of 2.84 +0.23/-0.22 (stat) +0.26/-0.21 (syst) fb at mH = 125.38 GeV. This is useful as context but less directly comparable because it uses the full Run 2 dataset and a later analysis configuration.

## PDG and World-Average Inputs

The PDG 2024 Gauge and Higgs Bosons Summary Table gives mZ = 91.1880 +/- 0.0020 GeV, Gamma_Z = 2.4955 +/- 0.0023 GeV, mH = 125.20 +/- 0.11 GeV, a Higgs width summary value of 3.7 +1.9/-1.4 MeV under the stated on/off-shell coupling assumption, and H->ZZ* fraction 2.80 +/- 0.30%. These are validation/reference inputs, not tunable analysis parameters.

## Implications for Downstream Strategy

- The official CMS reference uses a simultaneous fit with production-sensitive categories; this open-data analysis should keep at least inclusive, VBF-like, and other categories if statistics allow.
- The requested NN angular discriminator is methodologically aligned with matrix-element/angular information used in official H->4l analyses, but Phase 2/3 must verify that the ntuples include the kinematic inputs needed to compute rest-frame angles.
- DY+jets MC for reducible background is a deliberate simplification relative to official data-driven Z+X estimation; the final note must state this as a comparability limitation.
- Published values above should be used as validation targets and table entries, with explicit caveats for luminosity, year, selection, and background-method differences.

## Source Index

| Source | Use |
| --- | --- |
| CMS-HIG-16-041 | CMS-HIG-16-041 / JHEP 11 (2017) 047 public page, arXiv:1706.09936, DOI 10.1007/JHEP11(2017)047: https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-16-041/ |
| HEPData-80189 | HEPData record for CMS-HIG-16-041, DOI 10.17182/hepdata.80189: https://www.hepdata.net/record/ins1608166 |
| CMS-LUM-20-001 | CMS-PAS-LUM-20-001 public page for CMS 2017 luminosity: https://cms-results.web.cern.ch/cms-results/public-results/preliminary-results/LUM-20-001/ |
| PDG-2024 | PDG 2024 Gauge and Higgs Bosons Summary Table, Phys. Rev. D 110, 030001 (2024): https://pdg.lbl.gov/2024/tables/rpp2024-sum-gauge-higgs-bosons.pdf |
