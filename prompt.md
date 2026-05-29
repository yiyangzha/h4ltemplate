# Analysis Title: H=>4L Mass measurment with CMS Open Data 

# You are performing a Higgs boson measurement in the 4 lepton (electron or muon) decay channel using CMS Open Data from 2017 at √s = 13 TeV. The final state is 4 electrons or muons that are loosely isolated, and ideally come from a Higgs boson decay. Your goal is to produce distributions of key observables — particularly the 4 lepton mass — showing the Higgs signal contribution on top of Standard Model backgrounds, with this mass distribution we then ask that you perform a fit of the mass and compute the mu value. This loosely follows the official CMS publication (JHEP 11 (2017) 047). To optimize the higgs signal selection, do some categorization, in particular add a VBF category, be sure to fit all categories simulataneously when you extract the mass. To improve the discrimination can you further train a neural network on the 4 lepton angular parameters in the 4 lepton rest frame, so that we can extract signal from teh background. Lastly, for the fake background just use drell-yan+jets Monte Carlo, don't bother with a full fake rate esimtate. 

# Data source: flat ntuples produced with the script h4l_ntuplize.py that is run on NANOAOD from CMS open data
# Below we list the samples and their cross sections

#GluGluToHToZZ.root cross-section:2.887e+01 pb  fullname:GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_minloHJJ_JHUGenV7011_pythia8
#VBF_HToZZ.root   cross-section:3.935e+00 pb      fullname:VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8
#ZHToZZ.root      cross-section:7.935e-01 pb      fullname:ZH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8
#WPHToZZ.root     cross-section:8.648e-01 pb      fullname:WplusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8
#WMHToZZ.root     cross-section:5.409e-01 pb      fullname:WminusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8/NANOAODSIM/106X_mc2017_realistic_v9-v2
#ZZTo4L.root      cross-section:1.325e+00 pb      fullname:ZZTo4L_TuneCP5_13TeV_powheg_pythia8
#DYJetsToLL.root  cross-section:5.396e+03 pb      fullname:DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8
#TTBar.root       cross-section:5.270e+01 pb      fullname:TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8


