/goal Complete the following task:

# Analysis Title: H=>4L Mass measurment with CMS Open Data 

You are performing a Higgs boson measurement in the 4 lepton (electron or muon) decay channel using CMS Open Data from 2017 at √s = 13 TeV. The final state is 4 electrons or muons that are loosely isolated, and ideally come from a Higgs boson decay. Your goal is to produce distributions of key observables — particularly the 4 lepton mass — showing the Higgs signal contribution on top of Standard Model backgrounds, with this mass distribution we then ask that you perform a fit of the mass and compute the mu value. This loosely follows the official CMS publication (JHEP 11 (2017) 047). To optimize the higgs signal selection, do some categorization, in particular add a VBF category, be sure to fit all categories simulataneously when you extract the mass. To improve the discrimination can you further train a neural network on the 4 lepton angular parameters in the 4 lepton rest frame, so that we can extract signal from teh background. Lastly, for the fake background just use drell-yan+jets Monte Carlo, don't bother with a full fake rate esimtate. 

- In the final analysis note, compare the final results with JHEP 11 (2017) 047 / CMS-HIG-16-041 as comprehensively as the available ntuples and this analysis scope allow. Cover every result from that paper that is meaningfully comparable; for non-comparable results, state the reason explicitly.
- In those comparison tables and figures, include previous-study results and PDG/world-average results where the paper or public references provide them.
- Use the same fit mass window as in JHEP 11 (2017) 047 / CMS-HIG-16-041.

Data and MC are flat ntuples produced with the script h4l_ntuplize.py.

Data: /sandbox/work/jfc/analyses/h4ltemplate/data (10 fb^-1)
MC: /sandbox/work/jfc/analyses/h4ltemplate/mc

#GluGluToHToZZ.root cross-section:6.024e-03 pb     fullname:GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_minloHJJ_JHUGenV7011_pythia8
#VBF_HToZZ.root   cross-section:4.8794e-04 pb    fullname:VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8
#ZHToZZ.root      cross-section:9.8394e-05 pb    fullname:ZH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8
#WPHToZZ.root     cross-section:1.072352e-04 pb  fullname:WplusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8
#WMHToZZ.root     cross-section:6.706e-05 pb     fullname:WminusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8/NANOAODSIM/106X_mc2017_realistic_v9-v2
#ZZTo4L.root      cross-section:1.325e+00 pb     fullname:ZZTo4L_TuneCP5_13TeV_powheg_pythia8
#DYJetsToLL.root  cross-section:5.396e+03 pb     fullname:DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8
#TTBar.root       cross-section:5.270e+01 pb     fullname:TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8
#GGZZ2E2Mu.root   cross-section:3.185e-03 pb     fullname:GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8
#GGZZ4Mu.root     cross-section:1.575e-03 pb     fullname:GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8
#GGZZ4E.root      cross-section:1.619e-03 pb     fullname:GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8

Note:
- These cross sections are the effective sample cross sections for the originally generated MC entries, including the decay or final-state definition implied by each sample name, and should be used to compute the MC event weight so that the simulated sample is normalized to the target data luminosity.
- For each MC ROOT file, the Metadata tree records the number of originally generated entries; the total generated event count should be obtained by summing nEvents over all entries in the Metadata tree.
