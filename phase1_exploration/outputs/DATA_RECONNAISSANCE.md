# Data Reconnaissance

Session: `albert_0f97`
Created: 2026-05-29T19:11:36.196314+00:00

## Summary

Phase 1 structurally inspected both the user-specified `/sandbox/work/jfc/analyses/h4ltemplate` ROOT files and the local `data/` and `mc/` copies. The primary event reconnaissance uses the user-specified paths because those are the prompt inputs; local copies are inventoried separately because their byte sizes differ and should not be assumed identical.

## Primary vs Local Copy Check

| File | Primary size | Local size | Primary tree entries | Local tree entries | Verdict |
| --- | --- | --- | --- | --- | --- |
| DYJetsToLL.root | 183984 | 824181 | {'Metadata': 1, 'h4lTree': 463} | {'Metadata': 69, 'h4lTree': 416} | different |
| GGZZ2E2Mu.root | 44108633 | 35539302 | {'Metadata': 1, 'h4lTree': 247847} | {'Metadata': 21, 'h4lTree': 197379} | different |
| GGZZ4E.root | 75582447 | 72466624 | {'Metadata': 1, 'h4lTree': 434957} | {'Metadata': 25, 'h4lTree': 415426} | different |
| GGZZ4Mu.root | 91319656 | 85729661 | {'Metadata': 1, 'h4lTree': 604772} | {'Metadata': 30, 'h4lTree': 560781} | different |
| GluGluToHToZZ.root | 24949568 | 75821315 | {'Metadata': 1, 'h4lTree': 138479} | {'Metadata': 23, 'h4lTree': 420275} | different |
| TTBar.root | 219230 | 801820 | {'Metadata': 1, 'h4lTree': 639} | {'Metadata': 56, 'h4lTree': 776} | different |
| VBF_HToZZ.root | 15081579 | 13941084 | {'Metadata': 1, 'h4lTree': 83769} | {'Metadata': 13, 'h4lTree': 76779} | different |
| WMHToZZ.root | 5375132 | 4813888 | {'Metadata': 1, 'h4lTree': 29634} | {'Metadata': 16, 'h4lTree': 25280} | different |
| WPHToZZ.root | 7304507 | 3152467 | {'Metadata': 1, 'h4lTree': 40179} | {'Metadata': 13, 'h4lTree': 16304} | different |
| ZHToZZ.root | 13071357 | 13117349 | {'Metadata': 1, 'h4lTree': 72189} | {'Metadata': 1, 'h4lTree': 72515} | different |
| ZZTo4L.root | 333657506 | 600302406 | {'Metadata': 1, 'h4lTree': 1864310} | {'Metadata': 108, 'h4lTree': 3333903} | different |

The primary source paths from `paths.json` are not byte-identical to the local copies for most MC samples, and some local files contain more `Metadata` rows and `h4lTree` entries. Downstream phases should use the user-specified primary paths unless the orchestrator formally changes the data source, because mixing primary and local copies would change yields and generated-event denominators.

## Sample Inventory and MC Coverage

| File | Kind | Events entries | Metadata generated events | Prompt xsec [pb] | Expected yield at 10 fb^-1 | Nominal weight | Generators | Tune | sqrt(s) [TeV] |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cms_10fb_13TeV.root | data | 854 | 854.0 | None | None | None |  | None | 13 |
| DYJetsToLL.root | mc | 463 | 82448537.0 | 5396.0 | 53960000.0 | 0.6544688597688519 | madgraph, pythia8 | CP5 | 13 |
| GGZZ2E2Mu.root | mc | 247847 | 499000.0 | 0.003185 | 31.849999999999998 | 6.382765531062123e-05 | mcfm, pythia8 | CP5 | 13 |
| GGZZ4E.root | mc | 434957 | 992608.0 | 0.001619 | 16.19 | 1.631056771656082e-05 | mcfm, pythia8 | CP5 | 13 |
| GGZZ4Mu.root | mc | 604772 | 997445.0 | 0.001575 | 15.75 | 1.5790344329762544e-05 | mcfm, pythia8 | CP5 | 13 |
| GluGluToHToZZ.root | mc | 138479 | 983914.0 | 0.006024 | 60.239999999999995 | 6.122486314860852e-05 | JHUGen, powheg, powheg2, pythia8 | CP5 | 13 |
| TTBar.root | mc | 639 | 14776503.0 | 52.7 | 527000.0 | 0.03566473068763293 | madgraph, pythia8 | CP5 | 13 |
| VBF_HToZZ.root | mc | 83769 | 498000.0 | 0.00048794 | 4.8794 | 9.797991967871486e-06 | JHUGen, powheg, powheg2, pythia8 | CP5 | 13 |
| WMHToZZ.root | mc | 29634 | 193088.0 | 6.706e-05 | 0.6706 | 3.473027842227378e-06 | JHUGen, powheg, powheg2, pythia8 | CP5 | 13 |
| WPHToZZ.root | mc | 40179 | 294744.0 | 0.0001072352 | 1.072352 | 3.6382487853866405e-06 | JHUGen, powheg, powheg2, pythia8 | CP5 | 13 |
| ZHToZZ.root | mc | 72189 | 486281.0 | 9.8394e-05 | 0.9839399999999999 | 2.023397994163868e-06 | JHUGen, powheg, powheg2, pythia8 | CP5 | 13 |
| ZZTo4L.root | mc | 1864310 | 52104000.0 | 1.325 | 13250.0 | 0.00025429909411945343 | powheg, pythia8 | CP5 | 13 |

The MC cross sections above are prompt-provided effective sample cross sections. For downstream normalization the documented Phase 1 formula is `weight = sigma * L / sum(nEvents from Metadata)`, using the algebraic generated-event denominator recorded in each MC file's Metadata tree where available.

## Tree and Branch Inventory

### `primary_data/cms_10fb_13TeV.root`

- Path: `/sandbox/work/jfc/analyses/h4ltemplate/data/cms_10fb_13TeV.root`
- Size: 9076342 bytes
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 2 |
| h4lTree | 854 | 108 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| lumi_fb | double | AsDtype('>f8') | 1 |
| nEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 854 |
| finalState | int32_t | AsDtype('>i4') | 854 |
| l1charge | int32_t | AsDtype('>i4') | 854 |
| l1dxy | float | AsDtype('>f4') | 854 |
| l1dxyErr | float | AsDtype('>f4') | 854 |
| l1dz | float | AsDtype('>f4') | 854 |
| l1dzErr | float | AsDtype('>f4') | 854 |
| l1elCutBased | int32_t | AsDtype('>i4') | 854 |
| l1elMvaBdt | float | AsDtype('>f4') | 854 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 854 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 854 |
| l1eta | float | AsDtype('>f4') | 854 |
| l1ip3d | float | AsDtype('>f4') | 854 |
| l1mass | float | AsDtype('>f4') | 854 |
| l1miniRelIso | float | AsDtype('>f4') | 854 |
| l1muGlobal | int32_t | AsDtype('>i4') | 854 |
| l1muMedium | int32_t | AsDtype('>i4') | 854 |
| l1muPF | int32_t | AsDtype('>i4') | 854 |
| l1muTight | int32_t | AsDtype('>i4') | 854 |
| l1pdgId | int32_t | AsDtype('>i4') | 854 |
| l1pfRelIso03 | float | AsDtype('>f4') | 854 |
| l1phi | float | AsDtype('>f4') | 854 |
| l1pt | float | AsDtype('>f4') | 854 |
| l1sip3d | float | AsDtype('>f4') | 854 |
| l1zId | int32_t | AsDtype('>i4') | 854 |
| l2charge | int32_t | AsDtype('>i4') | 854 |
| l2dxy | float | AsDtype('>f4') | 854 |
| l2dxyErr | float | AsDtype('>f4') | 854 |
| l2dz | float | AsDtype('>f4') | 854 |
| l2dzErr | float | AsDtype('>f4') | 854 |
| l2elCutBased | int32_t | AsDtype('>i4') | 854 |
| l2elMvaBdt | float | AsDtype('>f4') | 854 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 854 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 854 |
| l2eta | float | AsDtype('>f4') | 854 |
| l2ip3d | float | AsDtype('>f4') | 854 |
| l2mass | float | AsDtype('>f4') | 854 |
| l2miniRelIso | float | AsDtype('>f4') | 854 |
| l2muGlobal | int32_t | AsDtype('>i4') | 854 |
| l2muMedium | int32_t | AsDtype('>i4') | 854 |
| l2muPF | int32_t | AsDtype('>i4') | 854 |
| l2muTight | int32_t | AsDtype('>i4') | 854 |
| l2pdgId | int32_t | AsDtype('>i4') | 854 |
| l2pfRelIso03 | float | AsDtype('>f4') | 854 |
| l2phi | float | AsDtype('>f4') | 854 |
| l2pt | float | AsDtype('>f4') | 854 |
| l2sip3d | float | AsDtype('>f4') | 854 |
| l2zId | int32_t | AsDtype('>i4') | 854 |
| l3charge | int32_t | AsDtype('>i4') | 854 |
| l3dxy | float | AsDtype('>f4') | 854 |
| l3dxyErr | float | AsDtype('>f4') | 854 |
| l3dz | float | AsDtype('>f4') | 854 |
| l3dzErr | float | AsDtype('>f4') | 854 |
| l3elCutBased | int32_t | AsDtype('>i4') | 854 |
| l3elMvaBdt | float | AsDtype('>f4') | 854 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 854 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 854 |
| l3eta | float | AsDtype('>f4') | 854 |
| l3ip3d | float | AsDtype('>f4') | 854 |
| l3mass | float | AsDtype('>f4') | 854 |
| l3miniRelIso | float | AsDtype('>f4') | 854 |
| l3muGlobal | int32_t | AsDtype('>i4') | 854 |
| l3muMedium | int32_t | AsDtype('>i4') | 854 |
| l3muPF | int32_t | AsDtype('>i4') | 854 |
| l3muTight | int32_t | AsDtype('>i4') | 854 |
| l3pdgId | int32_t | AsDtype('>i4') | 854 |
| l3pfRelIso03 | float | AsDtype('>f4') | 854 |
| l3phi | float | AsDtype('>f4') | 854 |
| l3pt | float | AsDtype('>f4') | 854 |
| l3sip3d | float | AsDtype('>f4') | 854 |
| l3zId | int32_t | AsDtype('>i4') | 854 |
| l4charge | int32_t | AsDtype('>i4') | 854 |
| l4dxy | float | AsDtype('>f4') | 854 |
| l4dxyErr | float | AsDtype('>f4') | 854 |
| l4dz | float | AsDtype('>f4') | 854 |
| l4dzErr | float | AsDtype('>f4') | 854 |
| l4elCutBased | int32_t | AsDtype('>i4') | 854 |
| l4elMvaBdt | float | AsDtype('>f4') | 854 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 854 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 854 |
| l4eta | float | AsDtype('>f4') | 854 |
| l4ip3d | float | AsDtype('>f4') | 854 |
| l4mass | float | AsDtype('>f4') | 854 |
| l4miniRelIso | float | AsDtype('>f4') | 854 |
| l4muGlobal | int32_t | AsDtype('>i4') | 854 |
| l4muMedium | int32_t | AsDtype('>i4') | 854 |
| l4muPF | int32_t | AsDtype('>i4') | 854 |
| l4muTight | int32_t | AsDtype('>i4') | 854 |
| l4pdgId | int32_t | AsDtype('>i4') | 854 |
| l4pfRelIso03 | float | AsDtype('>f4') | 854 |
| l4phi | float | AsDtype('>f4') | 854 |
| l4pt | float | AsDtype('>f4') | 854 |
| l4sip3d | float | AsDtype('>f4') | 854 |
| l4zId | int32_t | AsDtype('>i4') | 854 |
| m4l | float | AsDtype('>f4') | 854 |
| mZ1 | float | AsDtype('>f4') | 854 |
| mZ2 | float | AsDtype('>f4') | 854 |
| nPV | int32_t | AsDtype('>i4') | 854 |
| phi4l | float | AsDtype('>f4') | 854 |
| pt4l | float | AsDtype('>f4') | 854 |
| pvChi2 | float | AsDtype('>f4') | 854 |
| pvNdof | float | AsDtype('>f4') | 854 |
| pvScore | float | AsDtype('>f4') | 854 |
| pvX | float | AsDtype('>f4') | 854 |
| pvY | float | AsDtype('>f4') | 854 |
| pvZ | float | AsDtype('>f4') | 854 |
| trigBits | int32_t | AsDtype('>i4') | 854 |
| y4l | float | AsDtype('>f4') | 854 |

### `primary_mc/DYJetsToLL.root`

- Path: `/sandbox/work/jfc/analyses/h4ltemplate/mc/DYJetsToLL.root`
- Size: 183984 bytes
- Prompt cross section: 5396.0 pb
- Full sample name: `DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 1 |
| h4lTree | 463 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 463 |
| event | int64_t | AsDtype('>i8') | 463 |
| finalState | int32_t | AsDtype('>i4') | 463 |
| l1charge | int32_t | AsDtype('>i4') | 463 |
| l1dxy | float | AsDtype('>f4') | 463 |
| l1dxyErr | float | AsDtype('>f4') | 463 |
| l1dz | float | AsDtype('>f4') | 463 |
| l1dzErr | float | AsDtype('>f4') | 463 |
| l1elCutBased | int32_t | AsDtype('>i4') | 463 |
| l1elMvaBdt | float | AsDtype('>f4') | 463 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 463 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 463 |
| l1eta | float | AsDtype('>f4') | 463 |
| l1ip3d | float | AsDtype('>f4') | 463 |
| l1mass | float | AsDtype('>f4') | 463 |
| l1miniRelIso | float | AsDtype('>f4') | 463 |
| l1muGlobal | int32_t | AsDtype('>i4') | 463 |
| l1muMedium | int32_t | AsDtype('>i4') | 463 |
| l1muPF | int32_t | AsDtype('>i4') | 463 |
| l1muTight | int32_t | AsDtype('>i4') | 463 |
| l1pdgId | int32_t | AsDtype('>i4') | 463 |
| l1pfRelIso03 | float | AsDtype('>f4') | 463 |
| l1phi | float | AsDtype('>f4') | 463 |
| l1pt | float | AsDtype('>f4') | 463 |
| l1sip3d | float | AsDtype('>f4') | 463 |
| l1zId | int32_t | AsDtype('>i4') | 463 |
| l2charge | int32_t | AsDtype('>i4') | 463 |
| l2dxy | float | AsDtype('>f4') | 463 |
| l2dxyErr | float | AsDtype('>f4') | 463 |
| l2dz | float | AsDtype('>f4') | 463 |
| l2dzErr | float | AsDtype('>f4') | 463 |
| l2elCutBased | int32_t | AsDtype('>i4') | 463 |
| l2elMvaBdt | float | AsDtype('>f4') | 463 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 463 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 463 |
| l2eta | float | AsDtype('>f4') | 463 |
| l2ip3d | float | AsDtype('>f4') | 463 |
| l2mass | float | AsDtype('>f4') | 463 |
| l2miniRelIso | float | AsDtype('>f4') | 463 |
| l2muGlobal | int32_t | AsDtype('>i4') | 463 |
| l2muMedium | int32_t | AsDtype('>i4') | 463 |
| l2muPF | int32_t | AsDtype('>i4') | 463 |
| l2muTight | int32_t | AsDtype('>i4') | 463 |
| l2pdgId | int32_t | AsDtype('>i4') | 463 |
| l2pfRelIso03 | float | AsDtype('>f4') | 463 |
| l2phi | float | AsDtype('>f4') | 463 |
| l2pt | float | AsDtype('>f4') | 463 |
| l2sip3d | float | AsDtype('>f4') | 463 |
| l2zId | int32_t | AsDtype('>i4') | 463 |
| l3charge | int32_t | AsDtype('>i4') | 463 |
| l3dxy | float | AsDtype('>f4') | 463 |
| l3dxyErr | float | AsDtype('>f4') | 463 |
| l3dz | float | AsDtype('>f4') | 463 |
| l3dzErr | float | AsDtype('>f4') | 463 |
| l3elCutBased | int32_t | AsDtype('>i4') | 463 |
| l3elMvaBdt | float | AsDtype('>f4') | 463 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 463 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 463 |
| l3eta | float | AsDtype('>f4') | 463 |
| l3ip3d | float | AsDtype('>f4') | 463 |
| l3mass | float | AsDtype('>f4') | 463 |
| l3miniRelIso | float | AsDtype('>f4') | 463 |
| l3muGlobal | int32_t | AsDtype('>i4') | 463 |
| l3muMedium | int32_t | AsDtype('>i4') | 463 |
| l3muPF | int32_t | AsDtype('>i4') | 463 |
| l3muTight | int32_t | AsDtype('>i4') | 463 |
| l3pdgId | int32_t | AsDtype('>i4') | 463 |
| l3pfRelIso03 | float | AsDtype('>f4') | 463 |
| l3phi | float | AsDtype('>f4') | 463 |
| l3pt | float | AsDtype('>f4') | 463 |
| l3sip3d | float | AsDtype('>f4') | 463 |
| l3zId | int32_t | AsDtype('>i4') | 463 |
| l4charge | int32_t | AsDtype('>i4') | 463 |
| l4dxy | float | AsDtype('>f4') | 463 |
| l4dxyErr | float | AsDtype('>f4') | 463 |
| l4dz | float | AsDtype('>f4') | 463 |
| l4dzErr | float | AsDtype('>f4') | 463 |
| l4elCutBased | int32_t | AsDtype('>i4') | 463 |
| l4elMvaBdt | float | AsDtype('>f4') | 463 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 463 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 463 |
| l4eta | float | AsDtype('>f4') | 463 |
| l4ip3d | float | AsDtype('>f4') | 463 |
| l4mass | float | AsDtype('>f4') | 463 |
| l4miniRelIso | float | AsDtype('>f4') | 463 |
| l4muGlobal | int32_t | AsDtype('>i4') | 463 |
| l4muMedium | int32_t | AsDtype('>i4') | 463 |
| l4muPF | int32_t | AsDtype('>i4') | 463 |
| l4muTight | int32_t | AsDtype('>i4') | 463 |
| l4pdgId | int32_t | AsDtype('>i4') | 463 |
| l4pfRelIso03 | float | AsDtype('>f4') | 463 |
| l4phi | float | AsDtype('>f4') | 463 |
| l4pt | float | AsDtype('>f4') | 463 |
| l4sip3d | float | AsDtype('>f4') | 463 |
| l4zId | int32_t | AsDtype('>i4') | 463 |
| lumi | int32_t | AsDtype('>i4') | 463 |
| m4l | float | AsDtype('>f4') | 463 |
| mZ1 | float | AsDtype('>f4') | 463 |
| mZ2 | float | AsDtype('>f4') | 463 |
| nPV | int32_t | AsDtype('>i4') | 463 |
| phi4l | float | AsDtype('>f4') | 463 |
| pt4l | float | AsDtype('>f4') | 463 |
| pvChi2 | float | AsDtype('>f4') | 463 |
| pvNdof | float | AsDtype('>f4') | 463 |
| pvScore | float | AsDtype('>f4') | 463 |
| pvX | float | AsDtype('>f4') | 463 |
| pvY | float | AsDtype('>f4') | 463 |
| pvZ | float | AsDtype('>f4') | 463 |
| run | int32_t | AsDtype('>i4') | 463 |
| trigBits | int32_t | AsDtype('>i4') | 463 |
| y4l | float | AsDtype('>f4') | 463 |

### `primary_mc/GGZZ2E2Mu.root`

- Path: `/sandbox/work/jfc/analyses/h4ltemplate/mc/GGZZ2E2Mu.root`
- Size: 44108633 bytes
- Prompt cross section: 0.003185 pb
- Full sample name: `GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 1 |
| h4lTree | 247847 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 247847 |
| event | int64_t | AsDtype('>i8') | 247847 |
| finalState | int32_t | AsDtype('>i4') | 247847 |
| l1charge | int32_t | AsDtype('>i4') | 247847 |
| l1dxy | float | AsDtype('>f4') | 247847 |
| l1dxyErr | float | AsDtype('>f4') | 247847 |
| l1dz | float | AsDtype('>f4') | 247847 |
| l1dzErr | float | AsDtype('>f4') | 247847 |
| l1elCutBased | int32_t | AsDtype('>i4') | 247847 |
| l1elMvaBdt | float | AsDtype('>f4') | 247847 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 247847 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 247847 |
| l1eta | float | AsDtype('>f4') | 247847 |
| l1ip3d | float | AsDtype('>f4') | 247847 |
| l1mass | float | AsDtype('>f4') | 247847 |
| l1miniRelIso | float | AsDtype('>f4') | 247847 |
| l1muGlobal | int32_t | AsDtype('>i4') | 247847 |
| l1muMedium | int32_t | AsDtype('>i4') | 247847 |
| l1muPF | int32_t | AsDtype('>i4') | 247847 |
| l1muTight | int32_t | AsDtype('>i4') | 247847 |
| l1pdgId | int32_t | AsDtype('>i4') | 247847 |
| l1pfRelIso03 | float | AsDtype('>f4') | 247847 |
| l1phi | float | AsDtype('>f4') | 247847 |
| l1pt | float | AsDtype('>f4') | 247847 |
| l1sip3d | float | AsDtype('>f4') | 247847 |
| l1zId | int32_t | AsDtype('>i4') | 247847 |
| l2charge | int32_t | AsDtype('>i4') | 247847 |
| l2dxy | float | AsDtype('>f4') | 247847 |
| l2dxyErr | float | AsDtype('>f4') | 247847 |
| l2dz | float | AsDtype('>f4') | 247847 |
| l2dzErr | float | AsDtype('>f4') | 247847 |
| l2elCutBased | int32_t | AsDtype('>i4') | 247847 |
| l2elMvaBdt | float | AsDtype('>f4') | 247847 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 247847 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 247847 |
| l2eta | float | AsDtype('>f4') | 247847 |
| l2ip3d | float | AsDtype('>f4') | 247847 |
| l2mass | float | AsDtype('>f4') | 247847 |
| l2miniRelIso | float | AsDtype('>f4') | 247847 |
| l2muGlobal | int32_t | AsDtype('>i4') | 247847 |
| l2muMedium | int32_t | AsDtype('>i4') | 247847 |
| l2muPF | int32_t | AsDtype('>i4') | 247847 |
| l2muTight | int32_t | AsDtype('>i4') | 247847 |
| l2pdgId | int32_t | AsDtype('>i4') | 247847 |
| l2pfRelIso03 | float | AsDtype('>f4') | 247847 |
| l2phi | float | AsDtype('>f4') | 247847 |
| l2pt | float | AsDtype('>f4') | 247847 |
| l2sip3d | float | AsDtype('>f4') | 247847 |
| l2zId | int32_t | AsDtype('>i4') | 247847 |
| l3charge | int32_t | AsDtype('>i4') | 247847 |
| l3dxy | float | AsDtype('>f4') | 247847 |
| l3dxyErr | float | AsDtype('>f4') | 247847 |
| l3dz | float | AsDtype('>f4') | 247847 |
| l3dzErr | float | AsDtype('>f4') | 247847 |
| l3elCutBased | int32_t | AsDtype('>i4') | 247847 |
| l3elMvaBdt | float | AsDtype('>f4') | 247847 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 247847 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 247847 |
| l3eta | float | AsDtype('>f4') | 247847 |
| l3ip3d | float | AsDtype('>f4') | 247847 |
| l3mass | float | AsDtype('>f4') | 247847 |
| l3miniRelIso | float | AsDtype('>f4') | 247847 |
| l3muGlobal | int32_t | AsDtype('>i4') | 247847 |
| l3muMedium | int32_t | AsDtype('>i4') | 247847 |
| l3muPF | int32_t | AsDtype('>i4') | 247847 |
| l3muTight | int32_t | AsDtype('>i4') | 247847 |
| l3pdgId | int32_t | AsDtype('>i4') | 247847 |
| l3pfRelIso03 | float | AsDtype('>f4') | 247847 |
| l3phi | float | AsDtype('>f4') | 247847 |
| l3pt | float | AsDtype('>f4') | 247847 |
| l3sip3d | float | AsDtype('>f4') | 247847 |
| l3zId | int32_t | AsDtype('>i4') | 247847 |
| l4charge | int32_t | AsDtype('>i4') | 247847 |
| l4dxy | float | AsDtype('>f4') | 247847 |
| l4dxyErr | float | AsDtype('>f4') | 247847 |
| l4dz | float | AsDtype('>f4') | 247847 |
| l4dzErr | float | AsDtype('>f4') | 247847 |
| l4elCutBased | int32_t | AsDtype('>i4') | 247847 |
| l4elMvaBdt | float | AsDtype('>f4') | 247847 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 247847 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 247847 |
| l4eta | float | AsDtype('>f4') | 247847 |
| l4ip3d | float | AsDtype('>f4') | 247847 |
| l4mass | float | AsDtype('>f4') | 247847 |
| l4miniRelIso | float | AsDtype('>f4') | 247847 |
| l4muGlobal | int32_t | AsDtype('>i4') | 247847 |
| l4muMedium | int32_t | AsDtype('>i4') | 247847 |
| l4muPF | int32_t | AsDtype('>i4') | 247847 |
| l4muTight | int32_t | AsDtype('>i4') | 247847 |
| l4pdgId | int32_t | AsDtype('>i4') | 247847 |
| l4pfRelIso03 | float | AsDtype('>f4') | 247847 |
| l4phi | float | AsDtype('>f4') | 247847 |
| l4pt | float | AsDtype('>f4') | 247847 |
| l4sip3d | float | AsDtype('>f4') | 247847 |
| l4zId | int32_t | AsDtype('>i4') | 247847 |
| lumi | int32_t | AsDtype('>i4') | 247847 |
| m4l | float | AsDtype('>f4') | 247847 |
| mZ1 | float | AsDtype('>f4') | 247847 |
| mZ2 | float | AsDtype('>f4') | 247847 |
| nPV | int32_t | AsDtype('>i4') | 247847 |
| phi4l | float | AsDtype('>f4') | 247847 |
| pt4l | float | AsDtype('>f4') | 247847 |
| pvChi2 | float | AsDtype('>f4') | 247847 |
| pvNdof | float | AsDtype('>f4') | 247847 |
| pvScore | float | AsDtype('>f4') | 247847 |
| pvX | float | AsDtype('>f4') | 247847 |
| pvY | float | AsDtype('>f4') | 247847 |
| pvZ | float | AsDtype('>f4') | 247847 |
| run | int32_t | AsDtype('>i4') | 247847 |
| trigBits | int32_t | AsDtype('>i4') | 247847 |
| y4l | float | AsDtype('>f4') | 247847 |

### `primary_mc/GGZZ4E.root`

- Path: `/sandbox/work/jfc/analyses/h4ltemplate/mc/GGZZ4E.root`
- Size: 75582447 bytes
- Prompt cross section: 0.001619 pb
- Full sample name: `GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 1 |
| h4lTree | 434957 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 434957 |
| event | int64_t | AsDtype('>i8') | 434957 |
| finalState | int32_t | AsDtype('>i4') | 434957 |
| l1charge | int32_t | AsDtype('>i4') | 434957 |
| l1dxy | float | AsDtype('>f4') | 434957 |
| l1dxyErr | float | AsDtype('>f4') | 434957 |
| l1dz | float | AsDtype('>f4') | 434957 |
| l1dzErr | float | AsDtype('>f4') | 434957 |
| l1elCutBased | int32_t | AsDtype('>i4') | 434957 |
| l1elMvaBdt | float | AsDtype('>f4') | 434957 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 434957 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 434957 |
| l1eta | float | AsDtype('>f4') | 434957 |
| l1ip3d | float | AsDtype('>f4') | 434957 |
| l1mass | float | AsDtype('>f4') | 434957 |
| l1miniRelIso | float | AsDtype('>f4') | 434957 |
| l1muGlobal | int32_t | AsDtype('>i4') | 434957 |
| l1muMedium | int32_t | AsDtype('>i4') | 434957 |
| l1muPF | int32_t | AsDtype('>i4') | 434957 |
| l1muTight | int32_t | AsDtype('>i4') | 434957 |
| l1pdgId | int32_t | AsDtype('>i4') | 434957 |
| l1pfRelIso03 | float | AsDtype('>f4') | 434957 |
| l1phi | float | AsDtype('>f4') | 434957 |
| l1pt | float | AsDtype('>f4') | 434957 |
| l1sip3d | float | AsDtype('>f4') | 434957 |
| l1zId | int32_t | AsDtype('>i4') | 434957 |
| l2charge | int32_t | AsDtype('>i4') | 434957 |
| l2dxy | float | AsDtype('>f4') | 434957 |
| l2dxyErr | float | AsDtype('>f4') | 434957 |
| l2dz | float | AsDtype('>f4') | 434957 |
| l2dzErr | float | AsDtype('>f4') | 434957 |
| l2elCutBased | int32_t | AsDtype('>i4') | 434957 |
| l2elMvaBdt | float | AsDtype('>f4') | 434957 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 434957 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 434957 |
| l2eta | float | AsDtype('>f4') | 434957 |
| l2ip3d | float | AsDtype('>f4') | 434957 |
| l2mass | float | AsDtype('>f4') | 434957 |
| l2miniRelIso | float | AsDtype('>f4') | 434957 |
| l2muGlobal | int32_t | AsDtype('>i4') | 434957 |
| l2muMedium | int32_t | AsDtype('>i4') | 434957 |
| l2muPF | int32_t | AsDtype('>i4') | 434957 |
| l2muTight | int32_t | AsDtype('>i4') | 434957 |
| l2pdgId | int32_t | AsDtype('>i4') | 434957 |
| l2pfRelIso03 | float | AsDtype('>f4') | 434957 |
| l2phi | float | AsDtype('>f4') | 434957 |
| l2pt | float | AsDtype('>f4') | 434957 |
| l2sip3d | float | AsDtype('>f4') | 434957 |
| l2zId | int32_t | AsDtype('>i4') | 434957 |
| l3charge | int32_t | AsDtype('>i4') | 434957 |
| l3dxy | float | AsDtype('>f4') | 434957 |
| l3dxyErr | float | AsDtype('>f4') | 434957 |
| l3dz | float | AsDtype('>f4') | 434957 |
| l3dzErr | float | AsDtype('>f4') | 434957 |
| l3elCutBased | int32_t | AsDtype('>i4') | 434957 |
| l3elMvaBdt | float | AsDtype('>f4') | 434957 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 434957 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 434957 |
| l3eta | float | AsDtype('>f4') | 434957 |
| l3ip3d | float | AsDtype('>f4') | 434957 |
| l3mass | float | AsDtype('>f4') | 434957 |
| l3miniRelIso | float | AsDtype('>f4') | 434957 |
| l3muGlobal | int32_t | AsDtype('>i4') | 434957 |
| l3muMedium | int32_t | AsDtype('>i4') | 434957 |
| l3muPF | int32_t | AsDtype('>i4') | 434957 |
| l3muTight | int32_t | AsDtype('>i4') | 434957 |
| l3pdgId | int32_t | AsDtype('>i4') | 434957 |
| l3pfRelIso03 | float | AsDtype('>f4') | 434957 |
| l3phi | float | AsDtype('>f4') | 434957 |
| l3pt | float | AsDtype('>f4') | 434957 |
| l3sip3d | float | AsDtype('>f4') | 434957 |
| l3zId | int32_t | AsDtype('>i4') | 434957 |
| l4charge | int32_t | AsDtype('>i4') | 434957 |
| l4dxy | float | AsDtype('>f4') | 434957 |
| l4dxyErr | float | AsDtype('>f4') | 434957 |
| l4dz | float | AsDtype('>f4') | 434957 |
| l4dzErr | float | AsDtype('>f4') | 434957 |
| l4elCutBased | int32_t | AsDtype('>i4') | 434957 |
| l4elMvaBdt | float | AsDtype('>f4') | 434957 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 434957 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 434957 |
| l4eta | float | AsDtype('>f4') | 434957 |
| l4ip3d | float | AsDtype('>f4') | 434957 |
| l4mass | float | AsDtype('>f4') | 434957 |
| l4miniRelIso | float | AsDtype('>f4') | 434957 |
| l4muGlobal | int32_t | AsDtype('>i4') | 434957 |
| l4muMedium | int32_t | AsDtype('>i4') | 434957 |
| l4muPF | int32_t | AsDtype('>i4') | 434957 |
| l4muTight | int32_t | AsDtype('>i4') | 434957 |
| l4pdgId | int32_t | AsDtype('>i4') | 434957 |
| l4pfRelIso03 | float | AsDtype('>f4') | 434957 |
| l4phi | float | AsDtype('>f4') | 434957 |
| l4pt | float | AsDtype('>f4') | 434957 |
| l4sip3d | float | AsDtype('>f4') | 434957 |
| l4zId | int32_t | AsDtype('>i4') | 434957 |
| lumi | int32_t | AsDtype('>i4') | 434957 |
| m4l | float | AsDtype('>f4') | 434957 |
| mZ1 | float | AsDtype('>f4') | 434957 |
| mZ2 | float | AsDtype('>f4') | 434957 |
| nPV | int32_t | AsDtype('>i4') | 434957 |
| phi4l | float | AsDtype('>f4') | 434957 |
| pt4l | float | AsDtype('>f4') | 434957 |
| pvChi2 | float | AsDtype('>f4') | 434957 |
| pvNdof | float | AsDtype('>f4') | 434957 |
| pvScore | float | AsDtype('>f4') | 434957 |
| pvX | float | AsDtype('>f4') | 434957 |
| pvY | float | AsDtype('>f4') | 434957 |
| pvZ | float | AsDtype('>f4') | 434957 |
| run | int32_t | AsDtype('>i4') | 434957 |
| trigBits | int32_t | AsDtype('>i4') | 434957 |
| y4l | float | AsDtype('>f4') | 434957 |

### `primary_mc/GGZZ4Mu.root`

- Path: `/sandbox/work/jfc/analyses/h4ltemplate/mc/GGZZ4Mu.root`
- Size: 91319656 bytes
- Prompt cross section: 0.001575 pb
- Full sample name: `GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 1 |
| h4lTree | 604772 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 604772 |
| event | int64_t | AsDtype('>i8') | 604772 |
| finalState | int32_t | AsDtype('>i4') | 604772 |
| l1charge | int32_t | AsDtype('>i4') | 604772 |
| l1dxy | float | AsDtype('>f4') | 604772 |
| l1dxyErr | float | AsDtype('>f4') | 604772 |
| l1dz | float | AsDtype('>f4') | 604772 |
| l1dzErr | float | AsDtype('>f4') | 604772 |
| l1elCutBased | int32_t | AsDtype('>i4') | 604772 |
| l1elMvaBdt | float | AsDtype('>f4') | 604772 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 604772 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 604772 |
| l1eta | float | AsDtype('>f4') | 604772 |
| l1ip3d | float | AsDtype('>f4') | 604772 |
| l1mass | float | AsDtype('>f4') | 604772 |
| l1miniRelIso | float | AsDtype('>f4') | 604772 |
| l1muGlobal | int32_t | AsDtype('>i4') | 604772 |
| l1muMedium | int32_t | AsDtype('>i4') | 604772 |
| l1muPF | int32_t | AsDtype('>i4') | 604772 |
| l1muTight | int32_t | AsDtype('>i4') | 604772 |
| l1pdgId | int32_t | AsDtype('>i4') | 604772 |
| l1pfRelIso03 | float | AsDtype('>f4') | 604772 |
| l1phi | float | AsDtype('>f4') | 604772 |
| l1pt | float | AsDtype('>f4') | 604772 |
| l1sip3d | float | AsDtype('>f4') | 604772 |
| l1zId | int32_t | AsDtype('>i4') | 604772 |
| l2charge | int32_t | AsDtype('>i4') | 604772 |
| l2dxy | float | AsDtype('>f4') | 604772 |
| l2dxyErr | float | AsDtype('>f4') | 604772 |
| l2dz | float | AsDtype('>f4') | 604772 |
| l2dzErr | float | AsDtype('>f4') | 604772 |
| l2elCutBased | int32_t | AsDtype('>i4') | 604772 |
| l2elMvaBdt | float | AsDtype('>f4') | 604772 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 604772 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 604772 |
| l2eta | float | AsDtype('>f4') | 604772 |
| l2ip3d | float | AsDtype('>f4') | 604772 |
| l2mass | float | AsDtype('>f4') | 604772 |
| l2miniRelIso | float | AsDtype('>f4') | 604772 |
| l2muGlobal | int32_t | AsDtype('>i4') | 604772 |
| l2muMedium | int32_t | AsDtype('>i4') | 604772 |
| l2muPF | int32_t | AsDtype('>i4') | 604772 |
| l2muTight | int32_t | AsDtype('>i4') | 604772 |
| l2pdgId | int32_t | AsDtype('>i4') | 604772 |
| l2pfRelIso03 | float | AsDtype('>f4') | 604772 |
| l2phi | float | AsDtype('>f4') | 604772 |
| l2pt | float | AsDtype('>f4') | 604772 |
| l2sip3d | float | AsDtype('>f4') | 604772 |
| l2zId | int32_t | AsDtype('>i4') | 604772 |
| l3charge | int32_t | AsDtype('>i4') | 604772 |
| l3dxy | float | AsDtype('>f4') | 604772 |
| l3dxyErr | float | AsDtype('>f4') | 604772 |
| l3dz | float | AsDtype('>f4') | 604772 |
| l3dzErr | float | AsDtype('>f4') | 604772 |
| l3elCutBased | int32_t | AsDtype('>i4') | 604772 |
| l3elMvaBdt | float | AsDtype('>f4') | 604772 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 604772 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 604772 |
| l3eta | float | AsDtype('>f4') | 604772 |
| l3ip3d | float | AsDtype('>f4') | 604772 |
| l3mass | float | AsDtype('>f4') | 604772 |
| l3miniRelIso | float | AsDtype('>f4') | 604772 |
| l3muGlobal | int32_t | AsDtype('>i4') | 604772 |
| l3muMedium | int32_t | AsDtype('>i4') | 604772 |
| l3muPF | int32_t | AsDtype('>i4') | 604772 |
| l3muTight | int32_t | AsDtype('>i4') | 604772 |
| l3pdgId | int32_t | AsDtype('>i4') | 604772 |
| l3pfRelIso03 | float | AsDtype('>f4') | 604772 |
| l3phi | float | AsDtype('>f4') | 604772 |
| l3pt | float | AsDtype('>f4') | 604772 |
| l3sip3d | float | AsDtype('>f4') | 604772 |
| l3zId | int32_t | AsDtype('>i4') | 604772 |
| l4charge | int32_t | AsDtype('>i4') | 604772 |
| l4dxy | float | AsDtype('>f4') | 604772 |
| l4dxyErr | float | AsDtype('>f4') | 604772 |
| l4dz | float | AsDtype('>f4') | 604772 |
| l4dzErr | float | AsDtype('>f4') | 604772 |
| l4elCutBased | int32_t | AsDtype('>i4') | 604772 |
| l4elMvaBdt | float | AsDtype('>f4') | 604772 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 604772 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 604772 |
| l4eta | float | AsDtype('>f4') | 604772 |
| l4ip3d | float | AsDtype('>f4') | 604772 |
| l4mass | float | AsDtype('>f4') | 604772 |
| l4miniRelIso | float | AsDtype('>f4') | 604772 |
| l4muGlobal | int32_t | AsDtype('>i4') | 604772 |
| l4muMedium | int32_t | AsDtype('>i4') | 604772 |
| l4muPF | int32_t | AsDtype('>i4') | 604772 |
| l4muTight | int32_t | AsDtype('>i4') | 604772 |
| l4pdgId | int32_t | AsDtype('>i4') | 604772 |
| l4pfRelIso03 | float | AsDtype('>f4') | 604772 |
| l4phi | float | AsDtype('>f4') | 604772 |
| l4pt | float | AsDtype('>f4') | 604772 |
| l4sip3d | float | AsDtype('>f4') | 604772 |
| l4zId | int32_t | AsDtype('>i4') | 604772 |
| lumi | int32_t | AsDtype('>i4') | 604772 |
| m4l | float | AsDtype('>f4') | 604772 |
| mZ1 | float | AsDtype('>f4') | 604772 |
| mZ2 | float | AsDtype('>f4') | 604772 |
| nPV | int32_t | AsDtype('>i4') | 604772 |
| phi4l | float | AsDtype('>f4') | 604772 |
| pt4l | float | AsDtype('>f4') | 604772 |
| pvChi2 | float | AsDtype('>f4') | 604772 |
| pvNdof | float | AsDtype('>f4') | 604772 |
| pvScore | float | AsDtype('>f4') | 604772 |
| pvX | float | AsDtype('>f4') | 604772 |
| pvY | float | AsDtype('>f4') | 604772 |
| pvZ | float | AsDtype('>f4') | 604772 |
| run | int32_t | AsDtype('>i4') | 604772 |
| trigBits | int32_t | AsDtype('>i4') | 604772 |
| y4l | float | AsDtype('>f4') | 604772 |

### `primary_mc/GluGluToHToZZ.root`

- Path: `/sandbox/work/jfc/analyses/h4ltemplate/mc/GluGluToHToZZ.root`
- Size: 24949568 bytes
- Prompt cross section: 0.006024 pb
- Full sample name: `GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_minloHJJ_JHUGenV7011_pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 1 |
| h4lTree | 138479 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 138479 |
| event | int64_t | AsDtype('>i8') | 138479 |
| finalState | int32_t | AsDtype('>i4') | 138479 |
| l1charge | int32_t | AsDtype('>i4') | 138479 |
| l1dxy | float | AsDtype('>f4') | 138479 |
| l1dxyErr | float | AsDtype('>f4') | 138479 |
| l1dz | float | AsDtype('>f4') | 138479 |
| l1dzErr | float | AsDtype('>f4') | 138479 |
| l1elCutBased | int32_t | AsDtype('>i4') | 138479 |
| l1elMvaBdt | float | AsDtype('>f4') | 138479 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 138479 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 138479 |
| l1eta | float | AsDtype('>f4') | 138479 |
| l1ip3d | float | AsDtype('>f4') | 138479 |
| l1mass | float | AsDtype('>f4') | 138479 |
| l1miniRelIso | float | AsDtype('>f4') | 138479 |
| l1muGlobal | int32_t | AsDtype('>i4') | 138479 |
| l1muMedium | int32_t | AsDtype('>i4') | 138479 |
| l1muPF | int32_t | AsDtype('>i4') | 138479 |
| l1muTight | int32_t | AsDtype('>i4') | 138479 |
| l1pdgId | int32_t | AsDtype('>i4') | 138479 |
| l1pfRelIso03 | float | AsDtype('>f4') | 138479 |
| l1phi | float | AsDtype('>f4') | 138479 |
| l1pt | float | AsDtype('>f4') | 138479 |
| l1sip3d | float | AsDtype('>f4') | 138479 |
| l1zId | int32_t | AsDtype('>i4') | 138479 |
| l2charge | int32_t | AsDtype('>i4') | 138479 |
| l2dxy | float | AsDtype('>f4') | 138479 |
| l2dxyErr | float | AsDtype('>f4') | 138479 |
| l2dz | float | AsDtype('>f4') | 138479 |
| l2dzErr | float | AsDtype('>f4') | 138479 |
| l2elCutBased | int32_t | AsDtype('>i4') | 138479 |
| l2elMvaBdt | float | AsDtype('>f4') | 138479 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 138479 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 138479 |
| l2eta | float | AsDtype('>f4') | 138479 |
| l2ip3d | float | AsDtype('>f4') | 138479 |
| l2mass | float | AsDtype('>f4') | 138479 |
| l2miniRelIso | float | AsDtype('>f4') | 138479 |
| l2muGlobal | int32_t | AsDtype('>i4') | 138479 |
| l2muMedium | int32_t | AsDtype('>i4') | 138479 |
| l2muPF | int32_t | AsDtype('>i4') | 138479 |
| l2muTight | int32_t | AsDtype('>i4') | 138479 |
| l2pdgId | int32_t | AsDtype('>i4') | 138479 |
| l2pfRelIso03 | float | AsDtype('>f4') | 138479 |
| l2phi | float | AsDtype('>f4') | 138479 |
| l2pt | float | AsDtype('>f4') | 138479 |
| l2sip3d | float | AsDtype('>f4') | 138479 |
| l2zId | int32_t | AsDtype('>i4') | 138479 |
| l3charge | int32_t | AsDtype('>i4') | 138479 |
| l3dxy | float | AsDtype('>f4') | 138479 |
| l3dxyErr | float | AsDtype('>f4') | 138479 |
| l3dz | float | AsDtype('>f4') | 138479 |
| l3dzErr | float | AsDtype('>f4') | 138479 |
| l3elCutBased | int32_t | AsDtype('>i4') | 138479 |
| l3elMvaBdt | float | AsDtype('>f4') | 138479 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 138479 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 138479 |
| l3eta | float | AsDtype('>f4') | 138479 |
| l3ip3d | float | AsDtype('>f4') | 138479 |
| l3mass | float | AsDtype('>f4') | 138479 |
| l3miniRelIso | float | AsDtype('>f4') | 138479 |
| l3muGlobal | int32_t | AsDtype('>i4') | 138479 |
| l3muMedium | int32_t | AsDtype('>i4') | 138479 |
| l3muPF | int32_t | AsDtype('>i4') | 138479 |
| l3muTight | int32_t | AsDtype('>i4') | 138479 |
| l3pdgId | int32_t | AsDtype('>i4') | 138479 |
| l3pfRelIso03 | float | AsDtype('>f4') | 138479 |
| l3phi | float | AsDtype('>f4') | 138479 |
| l3pt | float | AsDtype('>f4') | 138479 |
| l3sip3d | float | AsDtype('>f4') | 138479 |
| l3zId | int32_t | AsDtype('>i4') | 138479 |
| l4charge | int32_t | AsDtype('>i4') | 138479 |
| l4dxy | float | AsDtype('>f4') | 138479 |
| l4dxyErr | float | AsDtype('>f4') | 138479 |
| l4dz | float | AsDtype('>f4') | 138479 |
| l4dzErr | float | AsDtype('>f4') | 138479 |
| l4elCutBased | int32_t | AsDtype('>i4') | 138479 |
| l4elMvaBdt | float | AsDtype('>f4') | 138479 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 138479 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 138479 |
| l4eta | float | AsDtype('>f4') | 138479 |
| l4ip3d | float | AsDtype('>f4') | 138479 |
| l4mass | float | AsDtype('>f4') | 138479 |
| l4miniRelIso | float | AsDtype('>f4') | 138479 |
| l4muGlobal | int32_t | AsDtype('>i4') | 138479 |
| l4muMedium | int32_t | AsDtype('>i4') | 138479 |
| l4muPF | int32_t | AsDtype('>i4') | 138479 |
| l4muTight | int32_t | AsDtype('>i4') | 138479 |
| l4pdgId | int32_t | AsDtype('>i4') | 138479 |
| l4pfRelIso03 | float | AsDtype('>f4') | 138479 |
| l4phi | float | AsDtype('>f4') | 138479 |
| l4pt | float | AsDtype('>f4') | 138479 |
| l4sip3d | float | AsDtype('>f4') | 138479 |
| l4zId | int32_t | AsDtype('>i4') | 138479 |
| lumi | int32_t | AsDtype('>i4') | 138479 |
| m4l | float | AsDtype('>f4') | 138479 |
| mZ1 | float | AsDtype('>f4') | 138479 |
| mZ2 | float | AsDtype('>f4') | 138479 |
| nPV | int32_t | AsDtype('>i4') | 138479 |
| phi4l | float | AsDtype('>f4') | 138479 |
| pt4l | float | AsDtype('>f4') | 138479 |
| pvChi2 | float | AsDtype('>f4') | 138479 |
| pvNdof | float | AsDtype('>f4') | 138479 |
| pvScore | float | AsDtype('>f4') | 138479 |
| pvX | float | AsDtype('>f4') | 138479 |
| pvY | float | AsDtype('>f4') | 138479 |
| pvZ | float | AsDtype('>f4') | 138479 |
| run | int32_t | AsDtype('>i4') | 138479 |
| trigBits | int32_t | AsDtype('>i4') | 138479 |
| y4l | float | AsDtype('>f4') | 138479 |

### `primary_mc/TTBar.root`

- Path: `/sandbox/work/jfc/analyses/h4ltemplate/mc/TTBar.root`
- Size: 219230 bytes
- Prompt cross section: 52.7 pb
- Full sample name: `TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 1 |
| h4lTree | 639 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 639 |
| event | int64_t | AsDtype('>i8') | 639 |
| finalState | int32_t | AsDtype('>i4') | 639 |
| l1charge | int32_t | AsDtype('>i4') | 639 |
| l1dxy | float | AsDtype('>f4') | 639 |
| l1dxyErr | float | AsDtype('>f4') | 639 |
| l1dz | float | AsDtype('>f4') | 639 |
| l1dzErr | float | AsDtype('>f4') | 639 |
| l1elCutBased | int32_t | AsDtype('>i4') | 639 |
| l1elMvaBdt | float | AsDtype('>f4') | 639 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 639 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 639 |
| l1eta | float | AsDtype('>f4') | 639 |
| l1ip3d | float | AsDtype('>f4') | 639 |
| l1mass | float | AsDtype('>f4') | 639 |
| l1miniRelIso | float | AsDtype('>f4') | 639 |
| l1muGlobal | int32_t | AsDtype('>i4') | 639 |
| l1muMedium | int32_t | AsDtype('>i4') | 639 |
| l1muPF | int32_t | AsDtype('>i4') | 639 |
| l1muTight | int32_t | AsDtype('>i4') | 639 |
| l1pdgId | int32_t | AsDtype('>i4') | 639 |
| l1pfRelIso03 | float | AsDtype('>f4') | 639 |
| l1phi | float | AsDtype('>f4') | 639 |
| l1pt | float | AsDtype('>f4') | 639 |
| l1sip3d | float | AsDtype('>f4') | 639 |
| l1zId | int32_t | AsDtype('>i4') | 639 |
| l2charge | int32_t | AsDtype('>i4') | 639 |
| l2dxy | float | AsDtype('>f4') | 639 |
| l2dxyErr | float | AsDtype('>f4') | 639 |
| l2dz | float | AsDtype('>f4') | 639 |
| l2dzErr | float | AsDtype('>f4') | 639 |
| l2elCutBased | int32_t | AsDtype('>i4') | 639 |
| l2elMvaBdt | float | AsDtype('>f4') | 639 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 639 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 639 |
| l2eta | float | AsDtype('>f4') | 639 |
| l2ip3d | float | AsDtype('>f4') | 639 |
| l2mass | float | AsDtype('>f4') | 639 |
| l2miniRelIso | float | AsDtype('>f4') | 639 |
| l2muGlobal | int32_t | AsDtype('>i4') | 639 |
| l2muMedium | int32_t | AsDtype('>i4') | 639 |
| l2muPF | int32_t | AsDtype('>i4') | 639 |
| l2muTight | int32_t | AsDtype('>i4') | 639 |
| l2pdgId | int32_t | AsDtype('>i4') | 639 |
| l2pfRelIso03 | float | AsDtype('>f4') | 639 |
| l2phi | float | AsDtype('>f4') | 639 |
| l2pt | float | AsDtype('>f4') | 639 |
| l2sip3d | float | AsDtype('>f4') | 639 |
| l2zId | int32_t | AsDtype('>i4') | 639 |
| l3charge | int32_t | AsDtype('>i4') | 639 |
| l3dxy | float | AsDtype('>f4') | 639 |
| l3dxyErr | float | AsDtype('>f4') | 639 |
| l3dz | float | AsDtype('>f4') | 639 |
| l3dzErr | float | AsDtype('>f4') | 639 |
| l3elCutBased | int32_t | AsDtype('>i4') | 639 |
| l3elMvaBdt | float | AsDtype('>f4') | 639 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 639 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 639 |
| l3eta | float | AsDtype('>f4') | 639 |
| l3ip3d | float | AsDtype('>f4') | 639 |
| l3mass | float | AsDtype('>f4') | 639 |
| l3miniRelIso | float | AsDtype('>f4') | 639 |
| l3muGlobal | int32_t | AsDtype('>i4') | 639 |
| l3muMedium | int32_t | AsDtype('>i4') | 639 |
| l3muPF | int32_t | AsDtype('>i4') | 639 |
| l3muTight | int32_t | AsDtype('>i4') | 639 |
| l3pdgId | int32_t | AsDtype('>i4') | 639 |
| l3pfRelIso03 | float | AsDtype('>f4') | 639 |
| l3phi | float | AsDtype('>f4') | 639 |
| l3pt | float | AsDtype('>f4') | 639 |
| l3sip3d | float | AsDtype('>f4') | 639 |
| l3zId | int32_t | AsDtype('>i4') | 639 |
| l4charge | int32_t | AsDtype('>i4') | 639 |
| l4dxy | float | AsDtype('>f4') | 639 |
| l4dxyErr | float | AsDtype('>f4') | 639 |
| l4dz | float | AsDtype('>f4') | 639 |
| l4dzErr | float | AsDtype('>f4') | 639 |
| l4elCutBased | int32_t | AsDtype('>i4') | 639 |
| l4elMvaBdt | float | AsDtype('>f4') | 639 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 639 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 639 |
| l4eta | float | AsDtype('>f4') | 639 |
| l4ip3d | float | AsDtype('>f4') | 639 |
| l4mass | float | AsDtype('>f4') | 639 |
| l4miniRelIso | float | AsDtype('>f4') | 639 |
| l4muGlobal | int32_t | AsDtype('>i4') | 639 |
| l4muMedium | int32_t | AsDtype('>i4') | 639 |
| l4muPF | int32_t | AsDtype('>i4') | 639 |
| l4muTight | int32_t | AsDtype('>i4') | 639 |
| l4pdgId | int32_t | AsDtype('>i4') | 639 |
| l4pfRelIso03 | float | AsDtype('>f4') | 639 |
| l4phi | float | AsDtype('>f4') | 639 |
| l4pt | float | AsDtype('>f4') | 639 |
| l4sip3d | float | AsDtype('>f4') | 639 |
| l4zId | int32_t | AsDtype('>i4') | 639 |
| lumi | int32_t | AsDtype('>i4') | 639 |
| m4l | float | AsDtype('>f4') | 639 |
| mZ1 | float | AsDtype('>f4') | 639 |
| mZ2 | float | AsDtype('>f4') | 639 |
| nPV | int32_t | AsDtype('>i4') | 639 |
| phi4l | float | AsDtype('>f4') | 639 |
| pt4l | float | AsDtype('>f4') | 639 |
| pvChi2 | float | AsDtype('>f4') | 639 |
| pvNdof | float | AsDtype('>f4') | 639 |
| pvScore | float | AsDtype('>f4') | 639 |
| pvX | float | AsDtype('>f4') | 639 |
| pvY | float | AsDtype('>f4') | 639 |
| pvZ | float | AsDtype('>f4') | 639 |
| run | int32_t | AsDtype('>i4') | 639 |
| trigBits | int32_t | AsDtype('>i4') | 639 |
| y4l | float | AsDtype('>f4') | 639 |

### `primary_mc/VBF_HToZZ.root`

- Path: `/sandbox/work/jfc/analyses/h4ltemplate/mc/VBF_HToZZ.root`
- Size: 15081579 bytes
- Prompt cross section: 0.00048794 pb
- Full sample name: `VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 1 |
| h4lTree | 83769 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 83769 |
| event | int64_t | AsDtype('>i8') | 83769 |
| finalState | int32_t | AsDtype('>i4') | 83769 |
| l1charge | int32_t | AsDtype('>i4') | 83769 |
| l1dxy | float | AsDtype('>f4') | 83769 |
| l1dxyErr | float | AsDtype('>f4') | 83769 |
| l1dz | float | AsDtype('>f4') | 83769 |
| l1dzErr | float | AsDtype('>f4') | 83769 |
| l1elCutBased | int32_t | AsDtype('>i4') | 83769 |
| l1elMvaBdt | float | AsDtype('>f4') | 83769 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 83769 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 83769 |
| l1eta | float | AsDtype('>f4') | 83769 |
| l1ip3d | float | AsDtype('>f4') | 83769 |
| l1mass | float | AsDtype('>f4') | 83769 |
| l1miniRelIso | float | AsDtype('>f4') | 83769 |
| l1muGlobal | int32_t | AsDtype('>i4') | 83769 |
| l1muMedium | int32_t | AsDtype('>i4') | 83769 |
| l1muPF | int32_t | AsDtype('>i4') | 83769 |
| l1muTight | int32_t | AsDtype('>i4') | 83769 |
| l1pdgId | int32_t | AsDtype('>i4') | 83769 |
| l1pfRelIso03 | float | AsDtype('>f4') | 83769 |
| l1phi | float | AsDtype('>f4') | 83769 |
| l1pt | float | AsDtype('>f4') | 83769 |
| l1sip3d | float | AsDtype('>f4') | 83769 |
| l1zId | int32_t | AsDtype('>i4') | 83769 |
| l2charge | int32_t | AsDtype('>i4') | 83769 |
| l2dxy | float | AsDtype('>f4') | 83769 |
| l2dxyErr | float | AsDtype('>f4') | 83769 |
| l2dz | float | AsDtype('>f4') | 83769 |
| l2dzErr | float | AsDtype('>f4') | 83769 |
| l2elCutBased | int32_t | AsDtype('>i4') | 83769 |
| l2elMvaBdt | float | AsDtype('>f4') | 83769 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 83769 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 83769 |
| l2eta | float | AsDtype('>f4') | 83769 |
| l2ip3d | float | AsDtype('>f4') | 83769 |
| l2mass | float | AsDtype('>f4') | 83769 |
| l2miniRelIso | float | AsDtype('>f4') | 83769 |
| l2muGlobal | int32_t | AsDtype('>i4') | 83769 |
| l2muMedium | int32_t | AsDtype('>i4') | 83769 |
| l2muPF | int32_t | AsDtype('>i4') | 83769 |
| l2muTight | int32_t | AsDtype('>i4') | 83769 |
| l2pdgId | int32_t | AsDtype('>i4') | 83769 |
| l2pfRelIso03 | float | AsDtype('>f4') | 83769 |
| l2phi | float | AsDtype('>f4') | 83769 |
| l2pt | float | AsDtype('>f4') | 83769 |
| l2sip3d | float | AsDtype('>f4') | 83769 |
| l2zId | int32_t | AsDtype('>i4') | 83769 |
| l3charge | int32_t | AsDtype('>i4') | 83769 |
| l3dxy | float | AsDtype('>f4') | 83769 |
| l3dxyErr | float | AsDtype('>f4') | 83769 |
| l3dz | float | AsDtype('>f4') | 83769 |
| l3dzErr | float | AsDtype('>f4') | 83769 |
| l3elCutBased | int32_t | AsDtype('>i4') | 83769 |
| l3elMvaBdt | float | AsDtype('>f4') | 83769 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 83769 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 83769 |
| l3eta | float | AsDtype('>f4') | 83769 |
| l3ip3d | float | AsDtype('>f4') | 83769 |
| l3mass | float | AsDtype('>f4') | 83769 |
| l3miniRelIso | float | AsDtype('>f4') | 83769 |
| l3muGlobal | int32_t | AsDtype('>i4') | 83769 |
| l3muMedium | int32_t | AsDtype('>i4') | 83769 |
| l3muPF | int32_t | AsDtype('>i4') | 83769 |
| l3muTight | int32_t | AsDtype('>i4') | 83769 |
| l3pdgId | int32_t | AsDtype('>i4') | 83769 |
| l3pfRelIso03 | float | AsDtype('>f4') | 83769 |
| l3phi | float | AsDtype('>f4') | 83769 |
| l3pt | float | AsDtype('>f4') | 83769 |
| l3sip3d | float | AsDtype('>f4') | 83769 |
| l3zId | int32_t | AsDtype('>i4') | 83769 |
| l4charge | int32_t | AsDtype('>i4') | 83769 |
| l4dxy | float | AsDtype('>f4') | 83769 |
| l4dxyErr | float | AsDtype('>f4') | 83769 |
| l4dz | float | AsDtype('>f4') | 83769 |
| l4dzErr | float | AsDtype('>f4') | 83769 |
| l4elCutBased | int32_t | AsDtype('>i4') | 83769 |
| l4elMvaBdt | float | AsDtype('>f4') | 83769 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 83769 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 83769 |
| l4eta | float | AsDtype('>f4') | 83769 |
| l4ip3d | float | AsDtype('>f4') | 83769 |
| l4mass | float | AsDtype('>f4') | 83769 |
| l4miniRelIso | float | AsDtype('>f4') | 83769 |
| l4muGlobal | int32_t | AsDtype('>i4') | 83769 |
| l4muMedium | int32_t | AsDtype('>i4') | 83769 |
| l4muPF | int32_t | AsDtype('>i4') | 83769 |
| l4muTight | int32_t | AsDtype('>i4') | 83769 |
| l4pdgId | int32_t | AsDtype('>i4') | 83769 |
| l4pfRelIso03 | float | AsDtype('>f4') | 83769 |
| l4phi | float | AsDtype('>f4') | 83769 |
| l4pt | float | AsDtype('>f4') | 83769 |
| l4sip3d | float | AsDtype('>f4') | 83769 |
| l4zId | int32_t | AsDtype('>i4') | 83769 |
| lumi | int32_t | AsDtype('>i4') | 83769 |
| m4l | float | AsDtype('>f4') | 83769 |
| mZ1 | float | AsDtype('>f4') | 83769 |
| mZ2 | float | AsDtype('>f4') | 83769 |
| nPV | int32_t | AsDtype('>i4') | 83769 |
| phi4l | float | AsDtype('>f4') | 83769 |
| pt4l | float | AsDtype('>f4') | 83769 |
| pvChi2 | float | AsDtype('>f4') | 83769 |
| pvNdof | float | AsDtype('>f4') | 83769 |
| pvScore | float | AsDtype('>f4') | 83769 |
| pvX | float | AsDtype('>f4') | 83769 |
| pvY | float | AsDtype('>f4') | 83769 |
| pvZ | float | AsDtype('>f4') | 83769 |
| run | int32_t | AsDtype('>i4') | 83769 |
| trigBits | int32_t | AsDtype('>i4') | 83769 |
| y4l | float | AsDtype('>f4') | 83769 |

### `primary_mc/WMHToZZ.root`

- Path: `/sandbox/work/jfc/analyses/h4ltemplate/mc/WMHToZZ.root`
- Size: 5375132 bytes
- Prompt cross section: 6.706e-05 pb
- Full sample name: `WminusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 1 |
| h4lTree | 29634 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 29634 |
| event | int64_t | AsDtype('>i8') | 29634 |
| finalState | int32_t | AsDtype('>i4') | 29634 |
| l1charge | int32_t | AsDtype('>i4') | 29634 |
| l1dxy | float | AsDtype('>f4') | 29634 |
| l1dxyErr | float | AsDtype('>f4') | 29634 |
| l1dz | float | AsDtype('>f4') | 29634 |
| l1dzErr | float | AsDtype('>f4') | 29634 |
| l1elCutBased | int32_t | AsDtype('>i4') | 29634 |
| l1elMvaBdt | float | AsDtype('>f4') | 29634 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 29634 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 29634 |
| l1eta | float | AsDtype('>f4') | 29634 |
| l1ip3d | float | AsDtype('>f4') | 29634 |
| l1mass | float | AsDtype('>f4') | 29634 |
| l1miniRelIso | float | AsDtype('>f4') | 29634 |
| l1muGlobal | int32_t | AsDtype('>i4') | 29634 |
| l1muMedium | int32_t | AsDtype('>i4') | 29634 |
| l1muPF | int32_t | AsDtype('>i4') | 29634 |
| l1muTight | int32_t | AsDtype('>i4') | 29634 |
| l1pdgId | int32_t | AsDtype('>i4') | 29634 |
| l1pfRelIso03 | float | AsDtype('>f4') | 29634 |
| l1phi | float | AsDtype('>f4') | 29634 |
| l1pt | float | AsDtype('>f4') | 29634 |
| l1sip3d | float | AsDtype('>f4') | 29634 |
| l1zId | int32_t | AsDtype('>i4') | 29634 |
| l2charge | int32_t | AsDtype('>i4') | 29634 |
| l2dxy | float | AsDtype('>f4') | 29634 |
| l2dxyErr | float | AsDtype('>f4') | 29634 |
| l2dz | float | AsDtype('>f4') | 29634 |
| l2dzErr | float | AsDtype('>f4') | 29634 |
| l2elCutBased | int32_t | AsDtype('>i4') | 29634 |
| l2elMvaBdt | float | AsDtype('>f4') | 29634 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 29634 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 29634 |
| l2eta | float | AsDtype('>f4') | 29634 |
| l2ip3d | float | AsDtype('>f4') | 29634 |
| l2mass | float | AsDtype('>f4') | 29634 |
| l2miniRelIso | float | AsDtype('>f4') | 29634 |
| l2muGlobal | int32_t | AsDtype('>i4') | 29634 |
| l2muMedium | int32_t | AsDtype('>i4') | 29634 |
| l2muPF | int32_t | AsDtype('>i4') | 29634 |
| l2muTight | int32_t | AsDtype('>i4') | 29634 |
| l2pdgId | int32_t | AsDtype('>i4') | 29634 |
| l2pfRelIso03 | float | AsDtype('>f4') | 29634 |
| l2phi | float | AsDtype('>f4') | 29634 |
| l2pt | float | AsDtype('>f4') | 29634 |
| l2sip3d | float | AsDtype('>f4') | 29634 |
| l2zId | int32_t | AsDtype('>i4') | 29634 |
| l3charge | int32_t | AsDtype('>i4') | 29634 |
| l3dxy | float | AsDtype('>f4') | 29634 |
| l3dxyErr | float | AsDtype('>f4') | 29634 |
| l3dz | float | AsDtype('>f4') | 29634 |
| l3dzErr | float | AsDtype('>f4') | 29634 |
| l3elCutBased | int32_t | AsDtype('>i4') | 29634 |
| l3elMvaBdt | float | AsDtype('>f4') | 29634 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 29634 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 29634 |
| l3eta | float | AsDtype('>f4') | 29634 |
| l3ip3d | float | AsDtype('>f4') | 29634 |
| l3mass | float | AsDtype('>f4') | 29634 |
| l3miniRelIso | float | AsDtype('>f4') | 29634 |
| l3muGlobal | int32_t | AsDtype('>i4') | 29634 |
| l3muMedium | int32_t | AsDtype('>i4') | 29634 |
| l3muPF | int32_t | AsDtype('>i4') | 29634 |
| l3muTight | int32_t | AsDtype('>i4') | 29634 |
| l3pdgId | int32_t | AsDtype('>i4') | 29634 |
| l3pfRelIso03 | float | AsDtype('>f4') | 29634 |
| l3phi | float | AsDtype('>f4') | 29634 |
| l3pt | float | AsDtype('>f4') | 29634 |
| l3sip3d | float | AsDtype('>f4') | 29634 |
| l3zId | int32_t | AsDtype('>i4') | 29634 |
| l4charge | int32_t | AsDtype('>i4') | 29634 |
| l4dxy | float | AsDtype('>f4') | 29634 |
| l4dxyErr | float | AsDtype('>f4') | 29634 |
| l4dz | float | AsDtype('>f4') | 29634 |
| l4dzErr | float | AsDtype('>f4') | 29634 |
| l4elCutBased | int32_t | AsDtype('>i4') | 29634 |
| l4elMvaBdt | float | AsDtype('>f4') | 29634 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 29634 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 29634 |
| l4eta | float | AsDtype('>f4') | 29634 |
| l4ip3d | float | AsDtype('>f4') | 29634 |
| l4mass | float | AsDtype('>f4') | 29634 |
| l4miniRelIso | float | AsDtype('>f4') | 29634 |
| l4muGlobal | int32_t | AsDtype('>i4') | 29634 |
| l4muMedium | int32_t | AsDtype('>i4') | 29634 |
| l4muPF | int32_t | AsDtype('>i4') | 29634 |
| l4muTight | int32_t | AsDtype('>i4') | 29634 |
| l4pdgId | int32_t | AsDtype('>i4') | 29634 |
| l4pfRelIso03 | float | AsDtype('>f4') | 29634 |
| l4phi | float | AsDtype('>f4') | 29634 |
| l4pt | float | AsDtype('>f4') | 29634 |
| l4sip3d | float | AsDtype('>f4') | 29634 |
| l4zId | int32_t | AsDtype('>i4') | 29634 |
| lumi | int32_t | AsDtype('>i4') | 29634 |
| m4l | float | AsDtype('>f4') | 29634 |
| mZ1 | float | AsDtype('>f4') | 29634 |
| mZ2 | float | AsDtype('>f4') | 29634 |
| nPV | int32_t | AsDtype('>i4') | 29634 |
| phi4l | float | AsDtype('>f4') | 29634 |
| pt4l | float | AsDtype('>f4') | 29634 |
| pvChi2 | float | AsDtype('>f4') | 29634 |
| pvNdof | float | AsDtype('>f4') | 29634 |
| pvScore | float | AsDtype('>f4') | 29634 |
| pvX | float | AsDtype('>f4') | 29634 |
| pvY | float | AsDtype('>f4') | 29634 |
| pvZ | float | AsDtype('>f4') | 29634 |
| run | int32_t | AsDtype('>i4') | 29634 |
| trigBits | int32_t | AsDtype('>i4') | 29634 |
| y4l | float | AsDtype('>f4') | 29634 |

### `primary_mc/WPHToZZ.root`

- Path: `/sandbox/work/jfc/analyses/h4ltemplate/mc/WPHToZZ.root`
- Size: 7304507 bytes
- Prompt cross section: 0.0001072352 pb
- Full sample name: `WplusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 1 |
| h4lTree | 40179 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 40179 |
| event | int64_t | AsDtype('>i8') | 40179 |
| finalState | int32_t | AsDtype('>i4') | 40179 |
| l1charge | int32_t | AsDtype('>i4') | 40179 |
| l1dxy | float | AsDtype('>f4') | 40179 |
| l1dxyErr | float | AsDtype('>f4') | 40179 |
| l1dz | float | AsDtype('>f4') | 40179 |
| l1dzErr | float | AsDtype('>f4') | 40179 |
| l1elCutBased | int32_t | AsDtype('>i4') | 40179 |
| l1elMvaBdt | float | AsDtype('>f4') | 40179 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 40179 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 40179 |
| l1eta | float | AsDtype('>f4') | 40179 |
| l1ip3d | float | AsDtype('>f4') | 40179 |
| l1mass | float | AsDtype('>f4') | 40179 |
| l1miniRelIso | float | AsDtype('>f4') | 40179 |
| l1muGlobal | int32_t | AsDtype('>i4') | 40179 |
| l1muMedium | int32_t | AsDtype('>i4') | 40179 |
| l1muPF | int32_t | AsDtype('>i4') | 40179 |
| l1muTight | int32_t | AsDtype('>i4') | 40179 |
| l1pdgId | int32_t | AsDtype('>i4') | 40179 |
| l1pfRelIso03 | float | AsDtype('>f4') | 40179 |
| l1phi | float | AsDtype('>f4') | 40179 |
| l1pt | float | AsDtype('>f4') | 40179 |
| l1sip3d | float | AsDtype('>f4') | 40179 |
| l1zId | int32_t | AsDtype('>i4') | 40179 |
| l2charge | int32_t | AsDtype('>i4') | 40179 |
| l2dxy | float | AsDtype('>f4') | 40179 |
| l2dxyErr | float | AsDtype('>f4') | 40179 |
| l2dz | float | AsDtype('>f4') | 40179 |
| l2dzErr | float | AsDtype('>f4') | 40179 |
| l2elCutBased | int32_t | AsDtype('>i4') | 40179 |
| l2elMvaBdt | float | AsDtype('>f4') | 40179 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 40179 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 40179 |
| l2eta | float | AsDtype('>f4') | 40179 |
| l2ip3d | float | AsDtype('>f4') | 40179 |
| l2mass | float | AsDtype('>f4') | 40179 |
| l2miniRelIso | float | AsDtype('>f4') | 40179 |
| l2muGlobal | int32_t | AsDtype('>i4') | 40179 |
| l2muMedium | int32_t | AsDtype('>i4') | 40179 |
| l2muPF | int32_t | AsDtype('>i4') | 40179 |
| l2muTight | int32_t | AsDtype('>i4') | 40179 |
| l2pdgId | int32_t | AsDtype('>i4') | 40179 |
| l2pfRelIso03 | float | AsDtype('>f4') | 40179 |
| l2phi | float | AsDtype('>f4') | 40179 |
| l2pt | float | AsDtype('>f4') | 40179 |
| l2sip3d | float | AsDtype('>f4') | 40179 |
| l2zId | int32_t | AsDtype('>i4') | 40179 |
| l3charge | int32_t | AsDtype('>i4') | 40179 |
| l3dxy | float | AsDtype('>f4') | 40179 |
| l3dxyErr | float | AsDtype('>f4') | 40179 |
| l3dz | float | AsDtype('>f4') | 40179 |
| l3dzErr | float | AsDtype('>f4') | 40179 |
| l3elCutBased | int32_t | AsDtype('>i4') | 40179 |
| l3elMvaBdt | float | AsDtype('>f4') | 40179 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 40179 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 40179 |
| l3eta | float | AsDtype('>f4') | 40179 |
| l3ip3d | float | AsDtype('>f4') | 40179 |
| l3mass | float | AsDtype('>f4') | 40179 |
| l3miniRelIso | float | AsDtype('>f4') | 40179 |
| l3muGlobal | int32_t | AsDtype('>i4') | 40179 |
| l3muMedium | int32_t | AsDtype('>i4') | 40179 |
| l3muPF | int32_t | AsDtype('>i4') | 40179 |
| l3muTight | int32_t | AsDtype('>i4') | 40179 |
| l3pdgId | int32_t | AsDtype('>i4') | 40179 |
| l3pfRelIso03 | float | AsDtype('>f4') | 40179 |
| l3phi | float | AsDtype('>f4') | 40179 |
| l3pt | float | AsDtype('>f4') | 40179 |
| l3sip3d | float | AsDtype('>f4') | 40179 |
| l3zId | int32_t | AsDtype('>i4') | 40179 |
| l4charge | int32_t | AsDtype('>i4') | 40179 |
| l4dxy | float | AsDtype('>f4') | 40179 |
| l4dxyErr | float | AsDtype('>f4') | 40179 |
| l4dz | float | AsDtype('>f4') | 40179 |
| l4dzErr | float | AsDtype('>f4') | 40179 |
| l4elCutBased | int32_t | AsDtype('>i4') | 40179 |
| l4elMvaBdt | float | AsDtype('>f4') | 40179 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 40179 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 40179 |
| l4eta | float | AsDtype('>f4') | 40179 |
| l4ip3d | float | AsDtype('>f4') | 40179 |
| l4mass | float | AsDtype('>f4') | 40179 |
| l4miniRelIso | float | AsDtype('>f4') | 40179 |
| l4muGlobal | int32_t | AsDtype('>i4') | 40179 |
| l4muMedium | int32_t | AsDtype('>i4') | 40179 |
| l4muPF | int32_t | AsDtype('>i4') | 40179 |
| l4muTight | int32_t | AsDtype('>i4') | 40179 |
| l4pdgId | int32_t | AsDtype('>i4') | 40179 |
| l4pfRelIso03 | float | AsDtype('>f4') | 40179 |
| l4phi | float | AsDtype('>f4') | 40179 |
| l4pt | float | AsDtype('>f4') | 40179 |
| l4sip3d | float | AsDtype('>f4') | 40179 |
| l4zId | int32_t | AsDtype('>i4') | 40179 |
| lumi | int32_t | AsDtype('>i4') | 40179 |
| m4l | float | AsDtype('>f4') | 40179 |
| mZ1 | float | AsDtype('>f4') | 40179 |
| mZ2 | float | AsDtype('>f4') | 40179 |
| nPV | int32_t | AsDtype('>i4') | 40179 |
| phi4l | float | AsDtype('>f4') | 40179 |
| pt4l | float | AsDtype('>f4') | 40179 |
| pvChi2 | float | AsDtype('>f4') | 40179 |
| pvNdof | float | AsDtype('>f4') | 40179 |
| pvScore | float | AsDtype('>f4') | 40179 |
| pvX | float | AsDtype('>f4') | 40179 |
| pvY | float | AsDtype('>f4') | 40179 |
| pvZ | float | AsDtype('>f4') | 40179 |
| run | int32_t | AsDtype('>i4') | 40179 |
| trigBits | int32_t | AsDtype('>i4') | 40179 |
| y4l | float | AsDtype('>f4') | 40179 |

### `primary_mc/ZHToZZ.root`

- Path: `/sandbox/work/jfc/analyses/h4ltemplate/mc/ZHToZZ.root`
- Size: 13071357 bytes
- Prompt cross section: 9.8394e-05 pb
- Full sample name: `ZH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 1 |
| h4lTree | 72189 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 72189 |
| event | int64_t | AsDtype('>i8') | 72189 |
| finalState | int32_t | AsDtype('>i4') | 72189 |
| l1charge | int32_t | AsDtype('>i4') | 72189 |
| l1dxy | float | AsDtype('>f4') | 72189 |
| l1dxyErr | float | AsDtype('>f4') | 72189 |
| l1dz | float | AsDtype('>f4') | 72189 |
| l1dzErr | float | AsDtype('>f4') | 72189 |
| l1elCutBased | int32_t | AsDtype('>i4') | 72189 |
| l1elMvaBdt | float | AsDtype('>f4') | 72189 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 72189 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 72189 |
| l1eta | float | AsDtype('>f4') | 72189 |
| l1ip3d | float | AsDtype('>f4') | 72189 |
| l1mass | float | AsDtype('>f4') | 72189 |
| l1miniRelIso | float | AsDtype('>f4') | 72189 |
| l1muGlobal | int32_t | AsDtype('>i4') | 72189 |
| l1muMedium | int32_t | AsDtype('>i4') | 72189 |
| l1muPF | int32_t | AsDtype('>i4') | 72189 |
| l1muTight | int32_t | AsDtype('>i4') | 72189 |
| l1pdgId | int32_t | AsDtype('>i4') | 72189 |
| l1pfRelIso03 | float | AsDtype('>f4') | 72189 |
| l1phi | float | AsDtype('>f4') | 72189 |
| l1pt | float | AsDtype('>f4') | 72189 |
| l1sip3d | float | AsDtype('>f4') | 72189 |
| l1zId | int32_t | AsDtype('>i4') | 72189 |
| l2charge | int32_t | AsDtype('>i4') | 72189 |
| l2dxy | float | AsDtype('>f4') | 72189 |
| l2dxyErr | float | AsDtype('>f4') | 72189 |
| l2dz | float | AsDtype('>f4') | 72189 |
| l2dzErr | float | AsDtype('>f4') | 72189 |
| l2elCutBased | int32_t | AsDtype('>i4') | 72189 |
| l2elMvaBdt | float | AsDtype('>f4') | 72189 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 72189 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 72189 |
| l2eta | float | AsDtype('>f4') | 72189 |
| l2ip3d | float | AsDtype('>f4') | 72189 |
| l2mass | float | AsDtype('>f4') | 72189 |
| l2miniRelIso | float | AsDtype('>f4') | 72189 |
| l2muGlobal | int32_t | AsDtype('>i4') | 72189 |
| l2muMedium | int32_t | AsDtype('>i4') | 72189 |
| l2muPF | int32_t | AsDtype('>i4') | 72189 |
| l2muTight | int32_t | AsDtype('>i4') | 72189 |
| l2pdgId | int32_t | AsDtype('>i4') | 72189 |
| l2pfRelIso03 | float | AsDtype('>f4') | 72189 |
| l2phi | float | AsDtype('>f4') | 72189 |
| l2pt | float | AsDtype('>f4') | 72189 |
| l2sip3d | float | AsDtype('>f4') | 72189 |
| l2zId | int32_t | AsDtype('>i4') | 72189 |
| l3charge | int32_t | AsDtype('>i4') | 72189 |
| l3dxy | float | AsDtype('>f4') | 72189 |
| l3dxyErr | float | AsDtype('>f4') | 72189 |
| l3dz | float | AsDtype('>f4') | 72189 |
| l3dzErr | float | AsDtype('>f4') | 72189 |
| l3elCutBased | int32_t | AsDtype('>i4') | 72189 |
| l3elMvaBdt | float | AsDtype('>f4') | 72189 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 72189 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 72189 |
| l3eta | float | AsDtype('>f4') | 72189 |
| l3ip3d | float | AsDtype('>f4') | 72189 |
| l3mass | float | AsDtype('>f4') | 72189 |
| l3miniRelIso | float | AsDtype('>f4') | 72189 |
| l3muGlobal | int32_t | AsDtype('>i4') | 72189 |
| l3muMedium | int32_t | AsDtype('>i4') | 72189 |
| l3muPF | int32_t | AsDtype('>i4') | 72189 |
| l3muTight | int32_t | AsDtype('>i4') | 72189 |
| l3pdgId | int32_t | AsDtype('>i4') | 72189 |
| l3pfRelIso03 | float | AsDtype('>f4') | 72189 |
| l3phi | float | AsDtype('>f4') | 72189 |
| l3pt | float | AsDtype('>f4') | 72189 |
| l3sip3d | float | AsDtype('>f4') | 72189 |
| l3zId | int32_t | AsDtype('>i4') | 72189 |
| l4charge | int32_t | AsDtype('>i4') | 72189 |
| l4dxy | float | AsDtype('>f4') | 72189 |
| l4dxyErr | float | AsDtype('>f4') | 72189 |
| l4dz | float | AsDtype('>f4') | 72189 |
| l4dzErr | float | AsDtype('>f4') | 72189 |
| l4elCutBased | int32_t | AsDtype('>i4') | 72189 |
| l4elMvaBdt | float | AsDtype('>f4') | 72189 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 72189 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 72189 |
| l4eta | float | AsDtype('>f4') | 72189 |
| l4ip3d | float | AsDtype('>f4') | 72189 |
| l4mass | float | AsDtype('>f4') | 72189 |
| l4miniRelIso | float | AsDtype('>f4') | 72189 |
| l4muGlobal | int32_t | AsDtype('>i4') | 72189 |
| l4muMedium | int32_t | AsDtype('>i4') | 72189 |
| l4muPF | int32_t | AsDtype('>i4') | 72189 |
| l4muTight | int32_t | AsDtype('>i4') | 72189 |
| l4pdgId | int32_t | AsDtype('>i4') | 72189 |
| l4pfRelIso03 | float | AsDtype('>f4') | 72189 |
| l4phi | float | AsDtype('>f4') | 72189 |
| l4pt | float | AsDtype('>f4') | 72189 |
| l4sip3d | float | AsDtype('>f4') | 72189 |
| l4zId | int32_t | AsDtype('>i4') | 72189 |
| lumi | int32_t | AsDtype('>i4') | 72189 |
| m4l | float | AsDtype('>f4') | 72189 |
| mZ1 | float | AsDtype('>f4') | 72189 |
| mZ2 | float | AsDtype('>f4') | 72189 |
| nPV | int32_t | AsDtype('>i4') | 72189 |
| phi4l | float | AsDtype('>f4') | 72189 |
| pt4l | float | AsDtype('>f4') | 72189 |
| pvChi2 | float | AsDtype('>f4') | 72189 |
| pvNdof | float | AsDtype('>f4') | 72189 |
| pvScore | float | AsDtype('>f4') | 72189 |
| pvX | float | AsDtype('>f4') | 72189 |
| pvY | float | AsDtype('>f4') | 72189 |
| pvZ | float | AsDtype('>f4') | 72189 |
| run | int32_t | AsDtype('>i4') | 72189 |
| trigBits | int32_t | AsDtype('>i4') | 72189 |
| y4l | float | AsDtype('>f4') | 72189 |

### `primary_mc/ZZTo4L.root`

- Path: `/sandbox/work/jfc/analyses/h4ltemplate/mc/ZZTo4L.root`
- Size: 333657506 bytes
- Prompt cross section: 1.325 pb
- Full sample name: `ZZTo4L_TuneCP5_13TeV_powheg_pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 1 |
| h4lTree | 1864310 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 1864310 |
| event | int64_t | AsDtype('>i8') | 1864310 |
| finalState | int32_t | AsDtype('>i4') | 1864310 |
| l1charge | int32_t | AsDtype('>i4') | 1864310 |
| l1dxy | float | AsDtype('>f4') | 1864310 |
| l1dxyErr | float | AsDtype('>f4') | 1864310 |
| l1dz | float | AsDtype('>f4') | 1864310 |
| l1dzErr | float | AsDtype('>f4') | 1864310 |
| l1elCutBased | int32_t | AsDtype('>i4') | 1864310 |
| l1elMvaBdt | float | AsDtype('>f4') | 1864310 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 1864310 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 1864310 |
| l1eta | float | AsDtype('>f4') | 1864310 |
| l1ip3d | float | AsDtype('>f4') | 1864310 |
| l1mass | float | AsDtype('>f4') | 1864310 |
| l1miniRelIso | float | AsDtype('>f4') | 1864310 |
| l1muGlobal | int32_t | AsDtype('>i4') | 1864310 |
| l1muMedium | int32_t | AsDtype('>i4') | 1864310 |
| l1muPF | int32_t | AsDtype('>i4') | 1864310 |
| l1muTight | int32_t | AsDtype('>i4') | 1864310 |
| l1pdgId | int32_t | AsDtype('>i4') | 1864310 |
| l1pfRelIso03 | float | AsDtype('>f4') | 1864310 |
| l1phi | float | AsDtype('>f4') | 1864310 |
| l1pt | float | AsDtype('>f4') | 1864310 |
| l1sip3d | float | AsDtype('>f4') | 1864310 |
| l1zId | int32_t | AsDtype('>i4') | 1864310 |
| l2charge | int32_t | AsDtype('>i4') | 1864310 |
| l2dxy | float | AsDtype('>f4') | 1864310 |
| l2dxyErr | float | AsDtype('>f4') | 1864310 |
| l2dz | float | AsDtype('>f4') | 1864310 |
| l2dzErr | float | AsDtype('>f4') | 1864310 |
| l2elCutBased | int32_t | AsDtype('>i4') | 1864310 |
| l2elMvaBdt | float | AsDtype('>f4') | 1864310 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 1864310 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 1864310 |
| l2eta | float | AsDtype('>f4') | 1864310 |
| l2ip3d | float | AsDtype('>f4') | 1864310 |
| l2mass | float | AsDtype('>f4') | 1864310 |
| l2miniRelIso | float | AsDtype('>f4') | 1864310 |
| l2muGlobal | int32_t | AsDtype('>i4') | 1864310 |
| l2muMedium | int32_t | AsDtype('>i4') | 1864310 |
| l2muPF | int32_t | AsDtype('>i4') | 1864310 |
| l2muTight | int32_t | AsDtype('>i4') | 1864310 |
| l2pdgId | int32_t | AsDtype('>i4') | 1864310 |
| l2pfRelIso03 | float | AsDtype('>f4') | 1864310 |
| l2phi | float | AsDtype('>f4') | 1864310 |
| l2pt | float | AsDtype('>f4') | 1864310 |
| l2sip3d | float | AsDtype('>f4') | 1864310 |
| l2zId | int32_t | AsDtype('>i4') | 1864310 |
| l3charge | int32_t | AsDtype('>i4') | 1864310 |
| l3dxy | float | AsDtype('>f4') | 1864310 |
| l3dxyErr | float | AsDtype('>f4') | 1864310 |
| l3dz | float | AsDtype('>f4') | 1864310 |
| l3dzErr | float | AsDtype('>f4') | 1864310 |
| l3elCutBased | int32_t | AsDtype('>i4') | 1864310 |
| l3elMvaBdt | float | AsDtype('>f4') | 1864310 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 1864310 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 1864310 |
| l3eta | float | AsDtype('>f4') | 1864310 |
| l3ip3d | float | AsDtype('>f4') | 1864310 |
| l3mass | float | AsDtype('>f4') | 1864310 |
| l3miniRelIso | float | AsDtype('>f4') | 1864310 |
| l3muGlobal | int32_t | AsDtype('>i4') | 1864310 |
| l3muMedium | int32_t | AsDtype('>i4') | 1864310 |
| l3muPF | int32_t | AsDtype('>i4') | 1864310 |
| l3muTight | int32_t | AsDtype('>i4') | 1864310 |
| l3pdgId | int32_t | AsDtype('>i4') | 1864310 |
| l3pfRelIso03 | float | AsDtype('>f4') | 1864310 |
| l3phi | float | AsDtype('>f4') | 1864310 |
| l3pt | float | AsDtype('>f4') | 1864310 |
| l3sip3d | float | AsDtype('>f4') | 1864310 |
| l3zId | int32_t | AsDtype('>i4') | 1864310 |
| l4charge | int32_t | AsDtype('>i4') | 1864310 |
| l4dxy | float | AsDtype('>f4') | 1864310 |
| l4dxyErr | float | AsDtype('>f4') | 1864310 |
| l4dz | float | AsDtype('>f4') | 1864310 |
| l4dzErr | float | AsDtype('>f4') | 1864310 |
| l4elCutBased | int32_t | AsDtype('>i4') | 1864310 |
| l4elMvaBdt | float | AsDtype('>f4') | 1864310 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 1864310 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 1864310 |
| l4eta | float | AsDtype('>f4') | 1864310 |
| l4ip3d | float | AsDtype('>f4') | 1864310 |
| l4mass | float | AsDtype('>f4') | 1864310 |
| l4miniRelIso | float | AsDtype('>f4') | 1864310 |
| l4muGlobal | int32_t | AsDtype('>i4') | 1864310 |
| l4muMedium | int32_t | AsDtype('>i4') | 1864310 |
| l4muPF | int32_t | AsDtype('>i4') | 1864310 |
| l4muTight | int32_t | AsDtype('>i4') | 1864310 |
| l4pdgId | int32_t | AsDtype('>i4') | 1864310 |
| l4pfRelIso03 | float | AsDtype('>f4') | 1864310 |
| l4phi | float | AsDtype('>f4') | 1864310 |
| l4pt | float | AsDtype('>f4') | 1864310 |
| l4sip3d | float | AsDtype('>f4') | 1864310 |
| l4zId | int32_t | AsDtype('>i4') | 1864310 |
| lumi | int32_t | AsDtype('>i4') | 1864310 |
| m4l | float | AsDtype('>f4') | 1864310 |
| mZ1 | float | AsDtype('>f4') | 1864310 |
| mZ2 | float | AsDtype('>f4') | 1864310 |
| nPV | int32_t | AsDtype('>i4') | 1864310 |
| phi4l | float | AsDtype('>f4') | 1864310 |
| pt4l | float | AsDtype('>f4') | 1864310 |
| pvChi2 | float | AsDtype('>f4') | 1864310 |
| pvNdof | float | AsDtype('>f4') | 1864310 |
| pvScore | float | AsDtype('>f4') | 1864310 |
| pvX | float | AsDtype('>f4') | 1864310 |
| pvY | float | AsDtype('>f4') | 1864310 |
| pvZ | float | AsDtype('>f4') | 1864310 |
| run | int32_t | AsDtype('>i4') | 1864310 |
| trigBits | int32_t | AsDtype('>i4') | 1864310 |
| y4l | float | AsDtype('>f4') | 1864310 |

### `local_data/data_10fb.root`

- Path: `/sandbox/work/jfc/analyses/higgs_4lep_mass/data/data_10fb.root`
- Size: 299192 bytes
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 3 |
| h4lTree | 719 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| lumi_fb | double | AsDtype('>f8') | 1 |
| nInputEvents | int64_t | AsDtype('>i8') | 1 |
| nOutputEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 719 |
| event | int64_t | AsDtype('>i8') | 719 |
| finalState | int32_t | AsDtype('>i4') | 719 |
| l1charge | int32_t | AsDtype('>i4') | 719 |
| l1dxy | float | AsDtype('>f4') | 719 |
| l1dxyErr | float | AsDtype('>f4') | 719 |
| l1dz | float | AsDtype('>f4') | 719 |
| l1dzErr | float | AsDtype('>f4') | 719 |
| l1elCutBased | int32_t | AsDtype('>i4') | 719 |
| l1elMvaBdt | float | AsDtype('>f4') | 719 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 719 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 719 |
| l1eta | float | AsDtype('>f4') | 719 |
| l1ip3d | float | AsDtype('>f4') | 719 |
| l1mass | float | AsDtype('>f4') | 719 |
| l1miniRelIso | float | AsDtype('>f4') | 719 |
| l1muGlobal | int32_t | AsDtype('>i4') | 719 |
| l1muMedium | int32_t | AsDtype('>i4') | 719 |
| l1muPF | int32_t | AsDtype('>i4') | 719 |
| l1muTight | int32_t | AsDtype('>i4') | 719 |
| l1pdgId | int32_t | AsDtype('>i4') | 719 |
| l1pfRelIso03 | float | AsDtype('>f4') | 719 |
| l1phi | float | AsDtype('>f4') | 719 |
| l1pt | float | AsDtype('>f4') | 719 |
| l1sip3d | float | AsDtype('>f4') | 719 |
| l1zId | int32_t | AsDtype('>i4') | 719 |
| l2charge | int32_t | AsDtype('>i4') | 719 |
| l2dxy | float | AsDtype('>f4') | 719 |
| l2dxyErr | float | AsDtype('>f4') | 719 |
| l2dz | float | AsDtype('>f4') | 719 |
| l2dzErr | float | AsDtype('>f4') | 719 |
| l2elCutBased | int32_t | AsDtype('>i4') | 719 |
| l2elMvaBdt | float | AsDtype('>f4') | 719 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 719 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 719 |
| l2eta | float | AsDtype('>f4') | 719 |
| l2ip3d | float | AsDtype('>f4') | 719 |
| l2mass | float | AsDtype('>f4') | 719 |
| l2miniRelIso | float | AsDtype('>f4') | 719 |
| l2muGlobal | int32_t | AsDtype('>i4') | 719 |
| l2muMedium | int32_t | AsDtype('>i4') | 719 |
| l2muPF | int32_t | AsDtype('>i4') | 719 |
| l2muTight | int32_t | AsDtype('>i4') | 719 |
| l2pdgId | int32_t | AsDtype('>i4') | 719 |
| l2pfRelIso03 | float | AsDtype('>f4') | 719 |
| l2phi | float | AsDtype('>f4') | 719 |
| l2pt | float | AsDtype('>f4') | 719 |
| l2sip3d | float | AsDtype('>f4') | 719 |
| l2zId | int32_t | AsDtype('>i4') | 719 |
| l3charge | int32_t | AsDtype('>i4') | 719 |
| l3dxy | float | AsDtype('>f4') | 719 |
| l3dxyErr | float | AsDtype('>f4') | 719 |
| l3dz | float | AsDtype('>f4') | 719 |
| l3dzErr | float | AsDtype('>f4') | 719 |
| l3elCutBased | int32_t | AsDtype('>i4') | 719 |
| l3elMvaBdt | float | AsDtype('>f4') | 719 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 719 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 719 |
| l3eta | float | AsDtype('>f4') | 719 |
| l3ip3d | float | AsDtype('>f4') | 719 |
| l3mass | float | AsDtype('>f4') | 719 |
| l3miniRelIso | float | AsDtype('>f4') | 719 |
| l3muGlobal | int32_t | AsDtype('>i4') | 719 |
| l3muMedium | int32_t | AsDtype('>i4') | 719 |
| l3muPF | int32_t | AsDtype('>i4') | 719 |
| l3muTight | int32_t | AsDtype('>i4') | 719 |
| l3pdgId | int32_t | AsDtype('>i4') | 719 |
| l3pfRelIso03 | float | AsDtype('>f4') | 719 |
| l3phi | float | AsDtype('>f4') | 719 |
| l3pt | float | AsDtype('>f4') | 719 |
| l3sip3d | float | AsDtype('>f4') | 719 |
| l3zId | int32_t | AsDtype('>i4') | 719 |
| l4charge | int32_t | AsDtype('>i4') | 719 |
| l4dxy | float | AsDtype('>f4') | 719 |
| l4dxyErr | float | AsDtype('>f4') | 719 |
| l4dz | float | AsDtype('>f4') | 719 |
| l4dzErr | float | AsDtype('>f4') | 719 |
| l4elCutBased | int32_t | AsDtype('>i4') | 719 |
| l4elMvaBdt | float | AsDtype('>f4') | 719 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 719 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 719 |
| l4eta | float | AsDtype('>f4') | 719 |
| l4ip3d | float | AsDtype('>f4') | 719 |
| l4mass | float | AsDtype('>f4') | 719 |
| l4miniRelIso | float | AsDtype('>f4') | 719 |
| l4muGlobal | int32_t | AsDtype('>i4') | 719 |
| l4muMedium | int32_t | AsDtype('>i4') | 719 |
| l4muPF | int32_t | AsDtype('>i4') | 719 |
| l4muTight | int32_t | AsDtype('>i4') | 719 |
| l4pdgId | int32_t | AsDtype('>i4') | 719 |
| l4pfRelIso03 | float | AsDtype('>f4') | 719 |
| l4phi | float | AsDtype('>f4') | 719 |
| l4pt | float | AsDtype('>f4') | 719 |
| l4sip3d | float | AsDtype('>f4') | 719 |
| l4zId | int32_t | AsDtype('>i4') | 719 |
| lumi | int32_t | AsDtype('>i4') | 719 |
| m4l | float | AsDtype('>f4') | 719 |
| mZ1 | float | AsDtype('>f4') | 719 |
| mZ2 | float | AsDtype('>f4') | 719 |
| nPV | int32_t | AsDtype('>i4') | 719 |
| phi4l | float | AsDtype('>f4') | 719 |
| pt4l | float | AsDtype('>f4') | 719 |
| pvChi2 | float | AsDtype('>f4') | 719 |
| pvNdof | float | AsDtype('>f4') | 719 |
| pvScore | float | AsDtype('>f4') | 719 |
| pvX | float | AsDtype('>f4') | 719 |
| pvY | float | AsDtype('>f4') | 719 |
| pvZ | float | AsDtype('>f4') | 719 |
| run | int32_t | AsDtype('>i4') | 719 |
| trigBits | int32_t | AsDtype('>i4') | 719 |
| y4l | float | AsDtype('>f4') | 719 |

### `local_mc/DYJetsToLL.root`

- Path: `/sandbox/work/jfc/analyses/higgs_4lep_mass/mc/DYJetsToLL.root`
- Size: 824181 bytes
- Prompt cross section: 5396.0 pb
- Full sample name: `DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 69 | 1 |
| h4lTree | 416 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 69 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 416 |
| event | int64_t | AsDtype('>i8') | 416 |
| finalState | int32_t | AsDtype('>i4') | 416 |
| l1charge | int32_t | AsDtype('>i4') | 416 |
| l1dxy | float | AsDtype('>f4') | 416 |
| l1dxyErr | float | AsDtype('>f4') | 416 |
| l1dz | float | AsDtype('>f4') | 416 |
| l1dzErr | float | AsDtype('>f4') | 416 |
| l1elCutBased | int32_t | AsDtype('>i4') | 416 |
| l1elMvaBdt | float | AsDtype('>f4') | 416 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 416 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 416 |
| l1eta | float | AsDtype('>f4') | 416 |
| l1ip3d | float | AsDtype('>f4') | 416 |
| l1mass | float | AsDtype('>f4') | 416 |
| l1miniRelIso | float | AsDtype('>f4') | 416 |
| l1muGlobal | int32_t | AsDtype('>i4') | 416 |
| l1muMedium | int32_t | AsDtype('>i4') | 416 |
| l1muPF | int32_t | AsDtype('>i4') | 416 |
| l1muTight | int32_t | AsDtype('>i4') | 416 |
| l1pdgId | int32_t | AsDtype('>i4') | 416 |
| l1pfRelIso03 | float | AsDtype('>f4') | 416 |
| l1phi | float | AsDtype('>f4') | 416 |
| l1pt | float | AsDtype('>f4') | 416 |
| l1sip3d | float | AsDtype('>f4') | 416 |
| l1zId | int32_t | AsDtype('>i4') | 416 |
| l2charge | int32_t | AsDtype('>i4') | 416 |
| l2dxy | float | AsDtype('>f4') | 416 |
| l2dxyErr | float | AsDtype('>f4') | 416 |
| l2dz | float | AsDtype('>f4') | 416 |
| l2dzErr | float | AsDtype('>f4') | 416 |
| l2elCutBased | int32_t | AsDtype('>i4') | 416 |
| l2elMvaBdt | float | AsDtype('>f4') | 416 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 416 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 416 |
| l2eta | float | AsDtype('>f4') | 416 |
| l2ip3d | float | AsDtype('>f4') | 416 |
| l2mass | float | AsDtype('>f4') | 416 |
| l2miniRelIso | float | AsDtype('>f4') | 416 |
| l2muGlobal | int32_t | AsDtype('>i4') | 416 |
| l2muMedium | int32_t | AsDtype('>i4') | 416 |
| l2muPF | int32_t | AsDtype('>i4') | 416 |
| l2muTight | int32_t | AsDtype('>i4') | 416 |
| l2pdgId | int32_t | AsDtype('>i4') | 416 |
| l2pfRelIso03 | float | AsDtype('>f4') | 416 |
| l2phi | float | AsDtype('>f4') | 416 |
| l2pt | float | AsDtype('>f4') | 416 |
| l2sip3d | float | AsDtype('>f4') | 416 |
| l2zId | int32_t | AsDtype('>i4') | 416 |
| l3charge | int32_t | AsDtype('>i4') | 416 |
| l3dxy | float | AsDtype('>f4') | 416 |
| l3dxyErr | float | AsDtype('>f4') | 416 |
| l3dz | float | AsDtype('>f4') | 416 |
| l3dzErr | float | AsDtype('>f4') | 416 |
| l3elCutBased | int32_t | AsDtype('>i4') | 416 |
| l3elMvaBdt | float | AsDtype('>f4') | 416 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 416 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 416 |
| l3eta | float | AsDtype('>f4') | 416 |
| l3ip3d | float | AsDtype('>f4') | 416 |
| l3mass | float | AsDtype('>f4') | 416 |
| l3miniRelIso | float | AsDtype('>f4') | 416 |
| l3muGlobal | int32_t | AsDtype('>i4') | 416 |
| l3muMedium | int32_t | AsDtype('>i4') | 416 |
| l3muPF | int32_t | AsDtype('>i4') | 416 |
| l3muTight | int32_t | AsDtype('>i4') | 416 |
| l3pdgId | int32_t | AsDtype('>i4') | 416 |
| l3pfRelIso03 | float | AsDtype('>f4') | 416 |
| l3phi | float | AsDtype('>f4') | 416 |
| l3pt | float | AsDtype('>f4') | 416 |
| l3sip3d | float | AsDtype('>f4') | 416 |
| l3zId | int32_t | AsDtype('>i4') | 416 |
| l4charge | int32_t | AsDtype('>i4') | 416 |
| l4dxy | float | AsDtype('>f4') | 416 |
| l4dxyErr | float | AsDtype('>f4') | 416 |
| l4dz | float | AsDtype('>f4') | 416 |
| l4dzErr | float | AsDtype('>f4') | 416 |
| l4elCutBased | int32_t | AsDtype('>i4') | 416 |
| l4elMvaBdt | float | AsDtype('>f4') | 416 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 416 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 416 |
| l4eta | float | AsDtype('>f4') | 416 |
| l4ip3d | float | AsDtype('>f4') | 416 |
| l4mass | float | AsDtype('>f4') | 416 |
| l4miniRelIso | float | AsDtype('>f4') | 416 |
| l4muGlobal | int32_t | AsDtype('>i4') | 416 |
| l4muMedium | int32_t | AsDtype('>i4') | 416 |
| l4muPF | int32_t | AsDtype('>i4') | 416 |
| l4muTight | int32_t | AsDtype('>i4') | 416 |
| l4pdgId | int32_t | AsDtype('>i4') | 416 |
| l4pfRelIso03 | float | AsDtype('>f4') | 416 |
| l4phi | float | AsDtype('>f4') | 416 |
| l4pt | float | AsDtype('>f4') | 416 |
| l4sip3d | float | AsDtype('>f4') | 416 |
| l4zId | int32_t | AsDtype('>i4') | 416 |
| lumi | int32_t | AsDtype('>i4') | 416 |
| m4l | float | AsDtype('>f4') | 416 |
| mZ1 | float | AsDtype('>f4') | 416 |
| mZ2 | float | AsDtype('>f4') | 416 |
| nPV | int32_t | AsDtype('>i4') | 416 |
| phi4l | float | AsDtype('>f4') | 416 |
| pt4l | float | AsDtype('>f4') | 416 |
| pvChi2 | float | AsDtype('>f4') | 416 |
| pvNdof | float | AsDtype('>f4') | 416 |
| pvScore | float | AsDtype('>f4') | 416 |
| pvX | float | AsDtype('>f4') | 416 |
| pvY | float | AsDtype('>f4') | 416 |
| pvZ | float | AsDtype('>f4') | 416 |
| run | int32_t | AsDtype('>i4') | 416 |
| trigBits | int32_t | AsDtype('>i4') | 416 |
| y4l | float | AsDtype('>f4') | 416 |

### `local_mc/GGZZ2E2Mu.root`

- Path: `/sandbox/work/jfc/analyses/higgs_4lep_mass/mc/GGZZ2E2Mu.root`
- Size: 35539302 bytes
- Prompt cross section: 0.003185 pb
- Full sample name: `GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 21 | 1 |
| h4lTree | 197379 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 21 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 197379 |
| event | int64_t | AsDtype('>i8') | 197379 |
| finalState | int32_t | AsDtype('>i4') | 197379 |
| l1charge | int32_t | AsDtype('>i4') | 197379 |
| l1dxy | float | AsDtype('>f4') | 197379 |
| l1dxyErr | float | AsDtype('>f4') | 197379 |
| l1dz | float | AsDtype('>f4') | 197379 |
| l1dzErr | float | AsDtype('>f4') | 197379 |
| l1elCutBased | int32_t | AsDtype('>i4') | 197379 |
| l1elMvaBdt | float | AsDtype('>f4') | 197379 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 197379 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 197379 |
| l1eta | float | AsDtype('>f4') | 197379 |
| l1ip3d | float | AsDtype('>f4') | 197379 |
| l1mass | float | AsDtype('>f4') | 197379 |
| l1miniRelIso | float | AsDtype('>f4') | 197379 |
| l1muGlobal | int32_t | AsDtype('>i4') | 197379 |
| l1muMedium | int32_t | AsDtype('>i4') | 197379 |
| l1muPF | int32_t | AsDtype('>i4') | 197379 |
| l1muTight | int32_t | AsDtype('>i4') | 197379 |
| l1pdgId | int32_t | AsDtype('>i4') | 197379 |
| l1pfRelIso03 | float | AsDtype('>f4') | 197379 |
| l1phi | float | AsDtype('>f4') | 197379 |
| l1pt | float | AsDtype('>f4') | 197379 |
| l1sip3d | float | AsDtype('>f4') | 197379 |
| l1zId | int32_t | AsDtype('>i4') | 197379 |
| l2charge | int32_t | AsDtype('>i4') | 197379 |
| l2dxy | float | AsDtype('>f4') | 197379 |
| l2dxyErr | float | AsDtype('>f4') | 197379 |
| l2dz | float | AsDtype('>f4') | 197379 |
| l2dzErr | float | AsDtype('>f4') | 197379 |
| l2elCutBased | int32_t | AsDtype('>i4') | 197379 |
| l2elMvaBdt | float | AsDtype('>f4') | 197379 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 197379 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 197379 |
| l2eta | float | AsDtype('>f4') | 197379 |
| l2ip3d | float | AsDtype('>f4') | 197379 |
| l2mass | float | AsDtype('>f4') | 197379 |
| l2miniRelIso | float | AsDtype('>f4') | 197379 |
| l2muGlobal | int32_t | AsDtype('>i4') | 197379 |
| l2muMedium | int32_t | AsDtype('>i4') | 197379 |
| l2muPF | int32_t | AsDtype('>i4') | 197379 |
| l2muTight | int32_t | AsDtype('>i4') | 197379 |
| l2pdgId | int32_t | AsDtype('>i4') | 197379 |
| l2pfRelIso03 | float | AsDtype('>f4') | 197379 |
| l2phi | float | AsDtype('>f4') | 197379 |
| l2pt | float | AsDtype('>f4') | 197379 |
| l2sip3d | float | AsDtype('>f4') | 197379 |
| l2zId | int32_t | AsDtype('>i4') | 197379 |
| l3charge | int32_t | AsDtype('>i4') | 197379 |
| l3dxy | float | AsDtype('>f4') | 197379 |
| l3dxyErr | float | AsDtype('>f4') | 197379 |
| l3dz | float | AsDtype('>f4') | 197379 |
| l3dzErr | float | AsDtype('>f4') | 197379 |
| l3elCutBased | int32_t | AsDtype('>i4') | 197379 |
| l3elMvaBdt | float | AsDtype('>f4') | 197379 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 197379 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 197379 |
| l3eta | float | AsDtype('>f4') | 197379 |
| l3ip3d | float | AsDtype('>f4') | 197379 |
| l3mass | float | AsDtype('>f4') | 197379 |
| l3miniRelIso | float | AsDtype('>f4') | 197379 |
| l3muGlobal | int32_t | AsDtype('>i4') | 197379 |
| l3muMedium | int32_t | AsDtype('>i4') | 197379 |
| l3muPF | int32_t | AsDtype('>i4') | 197379 |
| l3muTight | int32_t | AsDtype('>i4') | 197379 |
| l3pdgId | int32_t | AsDtype('>i4') | 197379 |
| l3pfRelIso03 | float | AsDtype('>f4') | 197379 |
| l3phi | float | AsDtype('>f4') | 197379 |
| l3pt | float | AsDtype('>f4') | 197379 |
| l3sip3d | float | AsDtype('>f4') | 197379 |
| l3zId | int32_t | AsDtype('>i4') | 197379 |
| l4charge | int32_t | AsDtype('>i4') | 197379 |
| l4dxy | float | AsDtype('>f4') | 197379 |
| l4dxyErr | float | AsDtype('>f4') | 197379 |
| l4dz | float | AsDtype('>f4') | 197379 |
| l4dzErr | float | AsDtype('>f4') | 197379 |
| l4elCutBased | int32_t | AsDtype('>i4') | 197379 |
| l4elMvaBdt | float | AsDtype('>f4') | 197379 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 197379 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 197379 |
| l4eta | float | AsDtype('>f4') | 197379 |
| l4ip3d | float | AsDtype('>f4') | 197379 |
| l4mass | float | AsDtype('>f4') | 197379 |
| l4miniRelIso | float | AsDtype('>f4') | 197379 |
| l4muGlobal | int32_t | AsDtype('>i4') | 197379 |
| l4muMedium | int32_t | AsDtype('>i4') | 197379 |
| l4muPF | int32_t | AsDtype('>i4') | 197379 |
| l4muTight | int32_t | AsDtype('>i4') | 197379 |
| l4pdgId | int32_t | AsDtype('>i4') | 197379 |
| l4pfRelIso03 | float | AsDtype('>f4') | 197379 |
| l4phi | float | AsDtype('>f4') | 197379 |
| l4pt | float | AsDtype('>f4') | 197379 |
| l4sip3d | float | AsDtype('>f4') | 197379 |
| l4zId | int32_t | AsDtype('>i4') | 197379 |
| lumi | int32_t | AsDtype('>i4') | 197379 |
| m4l | float | AsDtype('>f4') | 197379 |
| mZ1 | float | AsDtype('>f4') | 197379 |
| mZ2 | float | AsDtype('>f4') | 197379 |
| nPV | int32_t | AsDtype('>i4') | 197379 |
| phi4l | float | AsDtype('>f4') | 197379 |
| pt4l | float | AsDtype('>f4') | 197379 |
| pvChi2 | float | AsDtype('>f4') | 197379 |
| pvNdof | float | AsDtype('>f4') | 197379 |
| pvScore | float | AsDtype('>f4') | 197379 |
| pvX | float | AsDtype('>f4') | 197379 |
| pvY | float | AsDtype('>f4') | 197379 |
| pvZ | float | AsDtype('>f4') | 197379 |
| run | int32_t | AsDtype('>i4') | 197379 |
| trigBits | int32_t | AsDtype('>i4') | 197379 |
| y4l | float | AsDtype('>f4') | 197379 |

### `local_mc/GGZZ4E.root`

- Path: `/sandbox/work/jfc/analyses/higgs_4lep_mass/mc/GGZZ4E.root`
- Size: 72466624 bytes
- Prompt cross section: 0.001619 pb
- Full sample name: `GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 25 | 1 |
| h4lTree | 415426 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 25 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 415426 |
| event | int64_t | AsDtype('>i8') | 415426 |
| finalState | int32_t | AsDtype('>i4') | 415426 |
| l1charge | int32_t | AsDtype('>i4') | 415426 |
| l1dxy | float | AsDtype('>f4') | 415426 |
| l1dxyErr | float | AsDtype('>f4') | 415426 |
| l1dz | float | AsDtype('>f4') | 415426 |
| l1dzErr | float | AsDtype('>f4') | 415426 |
| l1elCutBased | int32_t | AsDtype('>i4') | 415426 |
| l1elMvaBdt | float | AsDtype('>f4') | 415426 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 415426 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 415426 |
| l1eta | float | AsDtype('>f4') | 415426 |
| l1ip3d | float | AsDtype('>f4') | 415426 |
| l1mass | float | AsDtype('>f4') | 415426 |
| l1miniRelIso | float | AsDtype('>f4') | 415426 |
| l1muGlobal | int32_t | AsDtype('>i4') | 415426 |
| l1muMedium | int32_t | AsDtype('>i4') | 415426 |
| l1muPF | int32_t | AsDtype('>i4') | 415426 |
| l1muTight | int32_t | AsDtype('>i4') | 415426 |
| l1pdgId | int32_t | AsDtype('>i4') | 415426 |
| l1pfRelIso03 | float | AsDtype('>f4') | 415426 |
| l1phi | float | AsDtype('>f4') | 415426 |
| l1pt | float | AsDtype('>f4') | 415426 |
| l1sip3d | float | AsDtype('>f4') | 415426 |
| l1zId | int32_t | AsDtype('>i4') | 415426 |
| l2charge | int32_t | AsDtype('>i4') | 415426 |
| l2dxy | float | AsDtype('>f4') | 415426 |
| l2dxyErr | float | AsDtype('>f4') | 415426 |
| l2dz | float | AsDtype('>f4') | 415426 |
| l2dzErr | float | AsDtype('>f4') | 415426 |
| l2elCutBased | int32_t | AsDtype('>i4') | 415426 |
| l2elMvaBdt | float | AsDtype('>f4') | 415426 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 415426 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 415426 |
| l2eta | float | AsDtype('>f4') | 415426 |
| l2ip3d | float | AsDtype('>f4') | 415426 |
| l2mass | float | AsDtype('>f4') | 415426 |
| l2miniRelIso | float | AsDtype('>f4') | 415426 |
| l2muGlobal | int32_t | AsDtype('>i4') | 415426 |
| l2muMedium | int32_t | AsDtype('>i4') | 415426 |
| l2muPF | int32_t | AsDtype('>i4') | 415426 |
| l2muTight | int32_t | AsDtype('>i4') | 415426 |
| l2pdgId | int32_t | AsDtype('>i4') | 415426 |
| l2pfRelIso03 | float | AsDtype('>f4') | 415426 |
| l2phi | float | AsDtype('>f4') | 415426 |
| l2pt | float | AsDtype('>f4') | 415426 |
| l2sip3d | float | AsDtype('>f4') | 415426 |
| l2zId | int32_t | AsDtype('>i4') | 415426 |
| l3charge | int32_t | AsDtype('>i4') | 415426 |
| l3dxy | float | AsDtype('>f4') | 415426 |
| l3dxyErr | float | AsDtype('>f4') | 415426 |
| l3dz | float | AsDtype('>f4') | 415426 |
| l3dzErr | float | AsDtype('>f4') | 415426 |
| l3elCutBased | int32_t | AsDtype('>i4') | 415426 |
| l3elMvaBdt | float | AsDtype('>f4') | 415426 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 415426 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 415426 |
| l3eta | float | AsDtype('>f4') | 415426 |
| l3ip3d | float | AsDtype('>f4') | 415426 |
| l3mass | float | AsDtype('>f4') | 415426 |
| l3miniRelIso | float | AsDtype('>f4') | 415426 |
| l3muGlobal | int32_t | AsDtype('>i4') | 415426 |
| l3muMedium | int32_t | AsDtype('>i4') | 415426 |
| l3muPF | int32_t | AsDtype('>i4') | 415426 |
| l3muTight | int32_t | AsDtype('>i4') | 415426 |
| l3pdgId | int32_t | AsDtype('>i4') | 415426 |
| l3pfRelIso03 | float | AsDtype('>f4') | 415426 |
| l3phi | float | AsDtype('>f4') | 415426 |
| l3pt | float | AsDtype('>f4') | 415426 |
| l3sip3d | float | AsDtype('>f4') | 415426 |
| l3zId | int32_t | AsDtype('>i4') | 415426 |
| l4charge | int32_t | AsDtype('>i4') | 415426 |
| l4dxy | float | AsDtype('>f4') | 415426 |
| l4dxyErr | float | AsDtype('>f4') | 415426 |
| l4dz | float | AsDtype('>f4') | 415426 |
| l4dzErr | float | AsDtype('>f4') | 415426 |
| l4elCutBased | int32_t | AsDtype('>i4') | 415426 |
| l4elMvaBdt | float | AsDtype('>f4') | 415426 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 415426 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 415426 |
| l4eta | float | AsDtype('>f4') | 415426 |
| l4ip3d | float | AsDtype('>f4') | 415426 |
| l4mass | float | AsDtype('>f4') | 415426 |
| l4miniRelIso | float | AsDtype('>f4') | 415426 |
| l4muGlobal | int32_t | AsDtype('>i4') | 415426 |
| l4muMedium | int32_t | AsDtype('>i4') | 415426 |
| l4muPF | int32_t | AsDtype('>i4') | 415426 |
| l4muTight | int32_t | AsDtype('>i4') | 415426 |
| l4pdgId | int32_t | AsDtype('>i4') | 415426 |
| l4pfRelIso03 | float | AsDtype('>f4') | 415426 |
| l4phi | float | AsDtype('>f4') | 415426 |
| l4pt | float | AsDtype('>f4') | 415426 |
| l4sip3d | float | AsDtype('>f4') | 415426 |
| l4zId | int32_t | AsDtype('>i4') | 415426 |
| lumi | int32_t | AsDtype('>i4') | 415426 |
| m4l | float | AsDtype('>f4') | 415426 |
| mZ1 | float | AsDtype('>f4') | 415426 |
| mZ2 | float | AsDtype('>f4') | 415426 |
| nPV | int32_t | AsDtype('>i4') | 415426 |
| phi4l | float | AsDtype('>f4') | 415426 |
| pt4l | float | AsDtype('>f4') | 415426 |
| pvChi2 | float | AsDtype('>f4') | 415426 |
| pvNdof | float | AsDtype('>f4') | 415426 |
| pvScore | float | AsDtype('>f4') | 415426 |
| pvX | float | AsDtype('>f4') | 415426 |
| pvY | float | AsDtype('>f4') | 415426 |
| pvZ | float | AsDtype('>f4') | 415426 |
| run | int32_t | AsDtype('>i4') | 415426 |
| trigBits | int32_t | AsDtype('>i4') | 415426 |
| y4l | float | AsDtype('>f4') | 415426 |

### `local_mc/GGZZ4Mu.root`

- Path: `/sandbox/work/jfc/analyses/higgs_4lep_mass/mc/GGZZ4Mu.root`
- Size: 85729661 bytes
- Prompt cross section: 0.001575 pb
- Full sample name: `GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 30 | 1 |
| h4lTree | 560781 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 30 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 560781 |
| event | int64_t | AsDtype('>i8') | 560781 |
| finalState | int32_t | AsDtype('>i4') | 560781 |
| l1charge | int32_t | AsDtype('>i4') | 560781 |
| l1dxy | float | AsDtype('>f4') | 560781 |
| l1dxyErr | float | AsDtype('>f4') | 560781 |
| l1dz | float | AsDtype('>f4') | 560781 |
| l1dzErr | float | AsDtype('>f4') | 560781 |
| l1elCutBased | int32_t | AsDtype('>i4') | 560781 |
| l1elMvaBdt | float | AsDtype('>f4') | 560781 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 560781 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 560781 |
| l1eta | float | AsDtype('>f4') | 560781 |
| l1ip3d | float | AsDtype('>f4') | 560781 |
| l1mass | float | AsDtype('>f4') | 560781 |
| l1miniRelIso | float | AsDtype('>f4') | 560781 |
| l1muGlobal | int32_t | AsDtype('>i4') | 560781 |
| l1muMedium | int32_t | AsDtype('>i4') | 560781 |
| l1muPF | int32_t | AsDtype('>i4') | 560781 |
| l1muTight | int32_t | AsDtype('>i4') | 560781 |
| l1pdgId | int32_t | AsDtype('>i4') | 560781 |
| l1pfRelIso03 | float | AsDtype('>f4') | 560781 |
| l1phi | float | AsDtype('>f4') | 560781 |
| l1pt | float | AsDtype('>f4') | 560781 |
| l1sip3d | float | AsDtype('>f4') | 560781 |
| l1zId | int32_t | AsDtype('>i4') | 560781 |
| l2charge | int32_t | AsDtype('>i4') | 560781 |
| l2dxy | float | AsDtype('>f4') | 560781 |
| l2dxyErr | float | AsDtype('>f4') | 560781 |
| l2dz | float | AsDtype('>f4') | 560781 |
| l2dzErr | float | AsDtype('>f4') | 560781 |
| l2elCutBased | int32_t | AsDtype('>i4') | 560781 |
| l2elMvaBdt | float | AsDtype('>f4') | 560781 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 560781 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 560781 |
| l2eta | float | AsDtype('>f4') | 560781 |
| l2ip3d | float | AsDtype('>f4') | 560781 |
| l2mass | float | AsDtype('>f4') | 560781 |
| l2miniRelIso | float | AsDtype('>f4') | 560781 |
| l2muGlobal | int32_t | AsDtype('>i4') | 560781 |
| l2muMedium | int32_t | AsDtype('>i4') | 560781 |
| l2muPF | int32_t | AsDtype('>i4') | 560781 |
| l2muTight | int32_t | AsDtype('>i4') | 560781 |
| l2pdgId | int32_t | AsDtype('>i4') | 560781 |
| l2pfRelIso03 | float | AsDtype('>f4') | 560781 |
| l2phi | float | AsDtype('>f4') | 560781 |
| l2pt | float | AsDtype('>f4') | 560781 |
| l2sip3d | float | AsDtype('>f4') | 560781 |
| l2zId | int32_t | AsDtype('>i4') | 560781 |
| l3charge | int32_t | AsDtype('>i4') | 560781 |
| l3dxy | float | AsDtype('>f4') | 560781 |
| l3dxyErr | float | AsDtype('>f4') | 560781 |
| l3dz | float | AsDtype('>f4') | 560781 |
| l3dzErr | float | AsDtype('>f4') | 560781 |
| l3elCutBased | int32_t | AsDtype('>i4') | 560781 |
| l3elMvaBdt | float | AsDtype('>f4') | 560781 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 560781 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 560781 |
| l3eta | float | AsDtype('>f4') | 560781 |
| l3ip3d | float | AsDtype('>f4') | 560781 |
| l3mass | float | AsDtype('>f4') | 560781 |
| l3miniRelIso | float | AsDtype('>f4') | 560781 |
| l3muGlobal | int32_t | AsDtype('>i4') | 560781 |
| l3muMedium | int32_t | AsDtype('>i4') | 560781 |
| l3muPF | int32_t | AsDtype('>i4') | 560781 |
| l3muTight | int32_t | AsDtype('>i4') | 560781 |
| l3pdgId | int32_t | AsDtype('>i4') | 560781 |
| l3pfRelIso03 | float | AsDtype('>f4') | 560781 |
| l3phi | float | AsDtype('>f4') | 560781 |
| l3pt | float | AsDtype('>f4') | 560781 |
| l3sip3d | float | AsDtype('>f4') | 560781 |
| l3zId | int32_t | AsDtype('>i4') | 560781 |
| l4charge | int32_t | AsDtype('>i4') | 560781 |
| l4dxy | float | AsDtype('>f4') | 560781 |
| l4dxyErr | float | AsDtype('>f4') | 560781 |
| l4dz | float | AsDtype('>f4') | 560781 |
| l4dzErr | float | AsDtype('>f4') | 560781 |
| l4elCutBased | int32_t | AsDtype('>i4') | 560781 |
| l4elMvaBdt | float | AsDtype('>f4') | 560781 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 560781 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 560781 |
| l4eta | float | AsDtype('>f4') | 560781 |
| l4ip3d | float | AsDtype('>f4') | 560781 |
| l4mass | float | AsDtype('>f4') | 560781 |
| l4miniRelIso | float | AsDtype('>f4') | 560781 |
| l4muGlobal | int32_t | AsDtype('>i4') | 560781 |
| l4muMedium | int32_t | AsDtype('>i4') | 560781 |
| l4muPF | int32_t | AsDtype('>i4') | 560781 |
| l4muTight | int32_t | AsDtype('>i4') | 560781 |
| l4pdgId | int32_t | AsDtype('>i4') | 560781 |
| l4pfRelIso03 | float | AsDtype('>f4') | 560781 |
| l4phi | float | AsDtype('>f4') | 560781 |
| l4pt | float | AsDtype('>f4') | 560781 |
| l4sip3d | float | AsDtype('>f4') | 560781 |
| l4zId | int32_t | AsDtype('>i4') | 560781 |
| lumi | int32_t | AsDtype('>i4') | 560781 |
| m4l | float | AsDtype('>f4') | 560781 |
| mZ1 | float | AsDtype('>f4') | 560781 |
| mZ2 | float | AsDtype('>f4') | 560781 |
| nPV | int32_t | AsDtype('>i4') | 560781 |
| phi4l | float | AsDtype('>f4') | 560781 |
| pt4l | float | AsDtype('>f4') | 560781 |
| pvChi2 | float | AsDtype('>f4') | 560781 |
| pvNdof | float | AsDtype('>f4') | 560781 |
| pvScore | float | AsDtype('>f4') | 560781 |
| pvX | float | AsDtype('>f4') | 560781 |
| pvY | float | AsDtype('>f4') | 560781 |
| pvZ | float | AsDtype('>f4') | 560781 |
| run | int32_t | AsDtype('>i4') | 560781 |
| trigBits | int32_t | AsDtype('>i4') | 560781 |
| y4l | float | AsDtype('>f4') | 560781 |

### `local_mc/GluGluToHToZZ.root`

- Path: `/sandbox/work/jfc/analyses/higgs_4lep_mass/mc/GluGluToHToZZ.root`
- Size: 75821315 bytes
- Prompt cross section: 0.006024 pb
- Full sample name: `GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_minloHJJ_JHUGenV7011_pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 23 | 1 |
| h4lTree | 420275 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 23 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 420275 |
| event | int64_t | AsDtype('>i8') | 420275 |
| finalState | int32_t | AsDtype('>i4') | 420275 |
| l1charge | int32_t | AsDtype('>i4') | 420275 |
| l1dxy | float | AsDtype('>f4') | 420275 |
| l1dxyErr | float | AsDtype('>f4') | 420275 |
| l1dz | float | AsDtype('>f4') | 420275 |
| l1dzErr | float | AsDtype('>f4') | 420275 |
| l1elCutBased | int32_t | AsDtype('>i4') | 420275 |
| l1elMvaBdt | float | AsDtype('>f4') | 420275 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 420275 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 420275 |
| l1eta | float | AsDtype('>f4') | 420275 |
| l1ip3d | float | AsDtype('>f4') | 420275 |
| l1mass | float | AsDtype('>f4') | 420275 |
| l1miniRelIso | float | AsDtype('>f4') | 420275 |
| l1muGlobal | int32_t | AsDtype('>i4') | 420275 |
| l1muMedium | int32_t | AsDtype('>i4') | 420275 |
| l1muPF | int32_t | AsDtype('>i4') | 420275 |
| l1muTight | int32_t | AsDtype('>i4') | 420275 |
| l1pdgId | int32_t | AsDtype('>i4') | 420275 |
| l1pfRelIso03 | float | AsDtype('>f4') | 420275 |
| l1phi | float | AsDtype('>f4') | 420275 |
| l1pt | float | AsDtype('>f4') | 420275 |
| l1sip3d | float | AsDtype('>f4') | 420275 |
| l1zId | int32_t | AsDtype('>i4') | 420275 |
| l2charge | int32_t | AsDtype('>i4') | 420275 |
| l2dxy | float | AsDtype('>f4') | 420275 |
| l2dxyErr | float | AsDtype('>f4') | 420275 |
| l2dz | float | AsDtype('>f4') | 420275 |
| l2dzErr | float | AsDtype('>f4') | 420275 |
| l2elCutBased | int32_t | AsDtype('>i4') | 420275 |
| l2elMvaBdt | float | AsDtype('>f4') | 420275 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 420275 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 420275 |
| l2eta | float | AsDtype('>f4') | 420275 |
| l2ip3d | float | AsDtype('>f4') | 420275 |
| l2mass | float | AsDtype('>f4') | 420275 |
| l2miniRelIso | float | AsDtype('>f4') | 420275 |
| l2muGlobal | int32_t | AsDtype('>i4') | 420275 |
| l2muMedium | int32_t | AsDtype('>i4') | 420275 |
| l2muPF | int32_t | AsDtype('>i4') | 420275 |
| l2muTight | int32_t | AsDtype('>i4') | 420275 |
| l2pdgId | int32_t | AsDtype('>i4') | 420275 |
| l2pfRelIso03 | float | AsDtype('>f4') | 420275 |
| l2phi | float | AsDtype('>f4') | 420275 |
| l2pt | float | AsDtype('>f4') | 420275 |
| l2sip3d | float | AsDtype('>f4') | 420275 |
| l2zId | int32_t | AsDtype('>i4') | 420275 |
| l3charge | int32_t | AsDtype('>i4') | 420275 |
| l3dxy | float | AsDtype('>f4') | 420275 |
| l3dxyErr | float | AsDtype('>f4') | 420275 |
| l3dz | float | AsDtype('>f4') | 420275 |
| l3dzErr | float | AsDtype('>f4') | 420275 |
| l3elCutBased | int32_t | AsDtype('>i4') | 420275 |
| l3elMvaBdt | float | AsDtype('>f4') | 420275 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 420275 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 420275 |
| l3eta | float | AsDtype('>f4') | 420275 |
| l3ip3d | float | AsDtype('>f4') | 420275 |
| l3mass | float | AsDtype('>f4') | 420275 |
| l3miniRelIso | float | AsDtype('>f4') | 420275 |
| l3muGlobal | int32_t | AsDtype('>i4') | 420275 |
| l3muMedium | int32_t | AsDtype('>i4') | 420275 |
| l3muPF | int32_t | AsDtype('>i4') | 420275 |
| l3muTight | int32_t | AsDtype('>i4') | 420275 |
| l3pdgId | int32_t | AsDtype('>i4') | 420275 |
| l3pfRelIso03 | float | AsDtype('>f4') | 420275 |
| l3phi | float | AsDtype('>f4') | 420275 |
| l3pt | float | AsDtype('>f4') | 420275 |
| l3sip3d | float | AsDtype('>f4') | 420275 |
| l3zId | int32_t | AsDtype('>i4') | 420275 |
| l4charge | int32_t | AsDtype('>i4') | 420275 |
| l4dxy | float | AsDtype('>f4') | 420275 |
| l4dxyErr | float | AsDtype('>f4') | 420275 |
| l4dz | float | AsDtype('>f4') | 420275 |
| l4dzErr | float | AsDtype('>f4') | 420275 |
| l4elCutBased | int32_t | AsDtype('>i4') | 420275 |
| l4elMvaBdt | float | AsDtype('>f4') | 420275 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 420275 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 420275 |
| l4eta | float | AsDtype('>f4') | 420275 |
| l4ip3d | float | AsDtype('>f4') | 420275 |
| l4mass | float | AsDtype('>f4') | 420275 |
| l4miniRelIso | float | AsDtype('>f4') | 420275 |
| l4muGlobal | int32_t | AsDtype('>i4') | 420275 |
| l4muMedium | int32_t | AsDtype('>i4') | 420275 |
| l4muPF | int32_t | AsDtype('>i4') | 420275 |
| l4muTight | int32_t | AsDtype('>i4') | 420275 |
| l4pdgId | int32_t | AsDtype('>i4') | 420275 |
| l4pfRelIso03 | float | AsDtype('>f4') | 420275 |
| l4phi | float | AsDtype('>f4') | 420275 |
| l4pt | float | AsDtype('>f4') | 420275 |
| l4sip3d | float | AsDtype('>f4') | 420275 |
| l4zId | int32_t | AsDtype('>i4') | 420275 |
| lumi | int32_t | AsDtype('>i4') | 420275 |
| m4l | float | AsDtype('>f4') | 420275 |
| mZ1 | float | AsDtype('>f4') | 420275 |
| mZ2 | float | AsDtype('>f4') | 420275 |
| nPV | int32_t | AsDtype('>i4') | 420275 |
| phi4l | float | AsDtype('>f4') | 420275 |
| pt4l | float | AsDtype('>f4') | 420275 |
| pvChi2 | float | AsDtype('>f4') | 420275 |
| pvNdof | float | AsDtype('>f4') | 420275 |
| pvScore | float | AsDtype('>f4') | 420275 |
| pvX | float | AsDtype('>f4') | 420275 |
| pvY | float | AsDtype('>f4') | 420275 |
| pvZ | float | AsDtype('>f4') | 420275 |
| run | int32_t | AsDtype('>i4') | 420275 |
| trigBits | int32_t | AsDtype('>i4') | 420275 |
| y4l | float | AsDtype('>f4') | 420275 |

### `local_mc/TTBar.root`

- Path: `/sandbox/work/jfc/analyses/higgs_4lep_mass/mc/TTBar.root`
- Size: 801820 bytes
- Prompt cross section: 52.7 pb
- Full sample name: `TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 56 | 1 |
| h4lTree | 776 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 56 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 776 |
| event | int64_t | AsDtype('>i8') | 776 |
| finalState | int32_t | AsDtype('>i4') | 776 |
| l1charge | int32_t | AsDtype('>i4') | 776 |
| l1dxy | float | AsDtype('>f4') | 776 |
| l1dxyErr | float | AsDtype('>f4') | 776 |
| l1dz | float | AsDtype('>f4') | 776 |
| l1dzErr | float | AsDtype('>f4') | 776 |
| l1elCutBased | int32_t | AsDtype('>i4') | 776 |
| l1elMvaBdt | float | AsDtype('>f4') | 776 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 776 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 776 |
| l1eta | float | AsDtype('>f4') | 776 |
| l1ip3d | float | AsDtype('>f4') | 776 |
| l1mass | float | AsDtype('>f4') | 776 |
| l1miniRelIso | float | AsDtype('>f4') | 776 |
| l1muGlobal | int32_t | AsDtype('>i4') | 776 |
| l1muMedium | int32_t | AsDtype('>i4') | 776 |
| l1muPF | int32_t | AsDtype('>i4') | 776 |
| l1muTight | int32_t | AsDtype('>i4') | 776 |
| l1pdgId | int32_t | AsDtype('>i4') | 776 |
| l1pfRelIso03 | float | AsDtype('>f4') | 776 |
| l1phi | float | AsDtype('>f4') | 776 |
| l1pt | float | AsDtype('>f4') | 776 |
| l1sip3d | float | AsDtype('>f4') | 776 |
| l1zId | int32_t | AsDtype('>i4') | 776 |
| l2charge | int32_t | AsDtype('>i4') | 776 |
| l2dxy | float | AsDtype('>f4') | 776 |
| l2dxyErr | float | AsDtype('>f4') | 776 |
| l2dz | float | AsDtype('>f4') | 776 |
| l2dzErr | float | AsDtype('>f4') | 776 |
| l2elCutBased | int32_t | AsDtype('>i4') | 776 |
| l2elMvaBdt | float | AsDtype('>f4') | 776 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 776 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 776 |
| l2eta | float | AsDtype('>f4') | 776 |
| l2ip3d | float | AsDtype('>f4') | 776 |
| l2mass | float | AsDtype('>f4') | 776 |
| l2miniRelIso | float | AsDtype('>f4') | 776 |
| l2muGlobal | int32_t | AsDtype('>i4') | 776 |
| l2muMedium | int32_t | AsDtype('>i4') | 776 |
| l2muPF | int32_t | AsDtype('>i4') | 776 |
| l2muTight | int32_t | AsDtype('>i4') | 776 |
| l2pdgId | int32_t | AsDtype('>i4') | 776 |
| l2pfRelIso03 | float | AsDtype('>f4') | 776 |
| l2phi | float | AsDtype('>f4') | 776 |
| l2pt | float | AsDtype('>f4') | 776 |
| l2sip3d | float | AsDtype('>f4') | 776 |
| l2zId | int32_t | AsDtype('>i4') | 776 |
| l3charge | int32_t | AsDtype('>i4') | 776 |
| l3dxy | float | AsDtype('>f4') | 776 |
| l3dxyErr | float | AsDtype('>f4') | 776 |
| l3dz | float | AsDtype('>f4') | 776 |
| l3dzErr | float | AsDtype('>f4') | 776 |
| l3elCutBased | int32_t | AsDtype('>i4') | 776 |
| l3elMvaBdt | float | AsDtype('>f4') | 776 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 776 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 776 |
| l3eta | float | AsDtype('>f4') | 776 |
| l3ip3d | float | AsDtype('>f4') | 776 |
| l3mass | float | AsDtype('>f4') | 776 |
| l3miniRelIso | float | AsDtype('>f4') | 776 |
| l3muGlobal | int32_t | AsDtype('>i4') | 776 |
| l3muMedium | int32_t | AsDtype('>i4') | 776 |
| l3muPF | int32_t | AsDtype('>i4') | 776 |
| l3muTight | int32_t | AsDtype('>i4') | 776 |
| l3pdgId | int32_t | AsDtype('>i4') | 776 |
| l3pfRelIso03 | float | AsDtype('>f4') | 776 |
| l3phi | float | AsDtype('>f4') | 776 |
| l3pt | float | AsDtype('>f4') | 776 |
| l3sip3d | float | AsDtype('>f4') | 776 |
| l3zId | int32_t | AsDtype('>i4') | 776 |
| l4charge | int32_t | AsDtype('>i4') | 776 |
| l4dxy | float | AsDtype('>f4') | 776 |
| l4dxyErr | float | AsDtype('>f4') | 776 |
| l4dz | float | AsDtype('>f4') | 776 |
| l4dzErr | float | AsDtype('>f4') | 776 |
| l4elCutBased | int32_t | AsDtype('>i4') | 776 |
| l4elMvaBdt | float | AsDtype('>f4') | 776 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 776 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 776 |
| l4eta | float | AsDtype('>f4') | 776 |
| l4ip3d | float | AsDtype('>f4') | 776 |
| l4mass | float | AsDtype('>f4') | 776 |
| l4miniRelIso | float | AsDtype('>f4') | 776 |
| l4muGlobal | int32_t | AsDtype('>i4') | 776 |
| l4muMedium | int32_t | AsDtype('>i4') | 776 |
| l4muPF | int32_t | AsDtype('>i4') | 776 |
| l4muTight | int32_t | AsDtype('>i4') | 776 |
| l4pdgId | int32_t | AsDtype('>i4') | 776 |
| l4pfRelIso03 | float | AsDtype('>f4') | 776 |
| l4phi | float | AsDtype('>f4') | 776 |
| l4pt | float | AsDtype('>f4') | 776 |
| l4sip3d | float | AsDtype('>f4') | 776 |
| l4zId | int32_t | AsDtype('>i4') | 776 |
| lumi | int32_t | AsDtype('>i4') | 776 |
| m4l | float | AsDtype('>f4') | 776 |
| mZ1 | float | AsDtype('>f4') | 776 |
| mZ2 | float | AsDtype('>f4') | 776 |
| nPV | int32_t | AsDtype('>i4') | 776 |
| phi4l | float | AsDtype('>f4') | 776 |
| pt4l | float | AsDtype('>f4') | 776 |
| pvChi2 | float | AsDtype('>f4') | 776 |
| pvNdof | float | AsDtype('>f4') | 776 |
| pvScore | float | AsDtype('>f4') | 776 |
| pvX | float | AsDtype('>f4') | 776 |
| pvY | float | AsDtype('>f4') | 776 |
| pvZ | float | AsDtype('>f4') | 776 |
| run | int32_t | AsDtype('>i4') | 776 |
| trigBits | int32_t | AsDtype('>i4') | 776 |
| y4l | float | AsDtype('>f4') | 776 |

### `local_mc/VBF_HToZZ.root`

- Path: `/sandbox/work/jfc/analyses/higgs_4lep_mass/mc/VBF_HToZZ.root`
- Size: 13941084 bytes
- Prompt cross section: 0.00048794 pb
- Full sample name: `VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 13 | 1 |
| h4lTree | 76779 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 13 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 76779 |
| event | int64_t | AsDtype('>i8') | 76779 |
| finalState | int32_t | AsDtype('>i4') | 76779 |
| l1charge | int32_t | AsDtype('>i4') | 76779 |
| l1dxy | float | AsDtype('>f4') | 76779 |
| l1dxyErr | float | AsDtype('>f4') | 76779 |
| l1dz | float | AsDtype('>f4') | 76779 |
| l1dzErr | float | AsDtype('>f4') | 76779 |
| l1elCutBased | int32_t | AsDtype('>i4') | 76779 |
| l1elMvaBdt | float | AsDtype('>f4') | 76779 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 76779 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 76779 |
| l1eta | float | AsDtype('>f4') | 76779 |
| l1ip3d | float | AsDtype('>f4') | 76779 |
| l1mass | float | AsDtype('>f4') | 76779 |
| l1miniRelIso | float | AsDtype('>f4') | 76779 |
| l1muGlobal | int32_t | AsDtype('>i4') | 76779 |
| l1muMedium | int32_t | AsDtype('>i4') | 76779 |
| l1muPF | int32_t | AsDtype('>i4') | 76779 |
| l1muTight | int32_t | AsDtype('>i4') | 76779 |
| l1pdgId | int32_t | AsDtype('>i4') | 76779 |
| l1pfRelIso03 | float | AsDtype('>f4') | 76779 |
| l1phi | float | AsDtype('>f4') | 76779 |
| l1pt | float | AsDtype('>f4') | 76779 |
| l1sip3d | float | AsDtype('>f4') | 76779 |
| l1zId | int32_t | AsDtype('>i4') | 76779 |
| l2charge | int32_t | AsDtype('>i4') | 76779 |
| l2dxy | float | AsDtype('>f4') | 76779 |
| l2dxyErr | float | AsDtype('>f4') | 76779 |
| l2dz | float | AsDtype('>f4') | 76779 |
| l2dzErr | float | AsDtype('>f4') | 76779 |
| l2elCutBased | int32_t | AsDtype('>i4') | 76779 |
| l2elMvaBdt | float | AsDtype('>f4') | 76779 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 76779 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 76779 |
| l2eta | float | AsDtype('>f4') | 76779 |
| l2ip3d | float | AsDtype('>f4') | 76779 |
| l2mass | float | AsDtype('>f4') | 76779 |
| l2miniRelIso | float | AsDtype('>f4') | 76779 |
| l2muGlobal | int32_t | AsDtype('>i4') | 76779 |
| l2muMedium | int32_t | AsDtype('>i4') | 76779 |
| l2muPF | int32_t | AsDtype('>i4') | 76779 |
| l2muTight | int32_t | AsDtype('>i4') | 76779 |
| l2pdgId | int32_t | AsDtype('>i4') | 76779 |
| l2pfRelIso03 | float | AsDtype('>f4') | 76779 |
| l2phi | float | AsDtype('>f4') | 76779 |
| l2pt | float | AsDtype('>f4') | 76779 |
| l2sip3d | float | AsDtype('>f4') | 76779 |
| l2zId | int32_t | AsDtype('>i4') | 76779 |
| l3charge | int32_t | AsDtype('>i4') | 76779 |
| l3dxy | float | AsDtype('>f4') | 76779 |
| l3dxyErr | float | AsDtype('>f4') | 76779 |
| l3dz | float | AsDtype('>f4') | 76779 |
| l3dzErr | float | AsDtype('>f4') | 76779 |
| l3elCutBased | int32_t | AsDtype('>i4') | 76779 |
| l3elMvaBdt | float | AsDtype('>f4') | 76779 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 76779 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 76779 |
| l3eta | float | AsDtype('>f4') | 76779 |
| l3ip3d | float | AsDtype('>f4') | 76779 |
| l3mass | float | AsDtype('>f4') | 76779 |
| l3miniRelIso | float | AsDtype('>f4') | 76779 |
| l3muGlobal | int32_t | AsDtype('>i4') | 76779 |
| l3muMedium | int32_t | AsDtype('>i4') | 76779 |
| l3muPF | int32_t | AsDtype('>i4') | 76779 |
| l3muTight | int32_t | AsDtype('>i4') | 76779 |
| l3pdgId | int32_t | AsDtype('>i4') | 76779 |
| l3pfRelIso03 | float | AsDtype('>f4') | 76779 |
| l3phi | float | AsDtype('>f4') | 76779 |
| l3pt | float | AsDtype('>f4') | 76779 |
| l3sip3d | float | AsDtype('>f4') | 76779 |
| l3zId | int32_t | AsDtype('>i4') | 76779 |
| l4charge | int32_t | AsDtype('>i4') | 76779 |
| l4dxy | float | AsDtype('>f4') | 76779 |
| l4dxyErr | float | AsDtype('>f4') | 76779 |
| l4dz | float | AsDtype('>f4') | 76779 |
| l4dzErr | float | AsDtype('>f4') | 76779 |
| l4elCutBased | int32_t | AsDtype('>i4') | 76779 |
| l4elMvaBdt | float | AsDtype('>f4') | 76779 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 76779 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 76779 |
| l4eta | float | AsDtype('>f4') | 76779 |
| l4ip3d | float | AsDtype('>f4') | 76779 |
| l4mass | float | AsDtype('>f4') | 76779 |
| l4miniRelIso | float | AsDtype('>f4') | 76779 |
| l4muGlobal | int32_t | AsDtype('>i4') | 76779 |
| l4muMedium | int32_t | AsDtype('>i4') | 76779 |
| l4muPF | int32_t | AsDtype('>i4') | 76779 |
| l4muTight | int32_t | AsDtype('>i4') | 76779 |
| l4pdgId | int32_t | AsDtype('>i4') | 76779 |
| l4pfRelIso03 | float | AsDtype('>f4') | 76779 |
| l4phi | float | AsDtype('>f4') | 76779 |
| l4pt | float | AsDtype('>f4') | 76779 |
| l4sip3d | float | AsDtype('>f4') | 76779 |
| l4zId | int32_t | AsDtype('>i4') | 76779 |
| lumi | int32_t | AsDtype('>i4') | 76779 |
| m4l | float | AsDtype('>f4') | 76779 |
| mZ1 | float | AsDtype('>f4') | 76779 |
| mZ2 | float | AsDtype('>f4') | 76779 |
| nPV | int32_t | AsDtype('>i4') | 76779 |
| phi4l | float | AsDtype('>f4') | 76779 |
| pt4l | float | AsDtype('>f4') | 76779 |
| pvChi2 | float | AsDtype('>f4') | 76779 |
| pvNdof | float | AsDtype('>f4') | 76779 |
| pvScore | float | AsDtype('>f4') | 76779 |
| pvX | float | AsDtype('>f4') | 76779 |
| pvY | float | AsDtype('>f4') | 76779 |
| pvZ | float | AsDtype('>f4') | 76779 |
| run | int32_t | AsDtype('>i4') | 76779 |
| trigBits | int32_t | AsDtype('>i4') | 76779 |
| y4l | float | AsDtype('>f4') | 76779 |

### `local_mc/WMHToZZ.root`

- Path: `/sandbox/work/jfc/analyses/higgs_4lep_mass/mc/WMHToZZ.root`
- Size: 4813888 bytes
- Prompt cross section: 6.706e-05 pb
- Full sample name: `WminusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 16 | 1 |
| h4lTree | 25280 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 16 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 25280 |
| event | int64_t | AsDtype('>i8') | 25280 |
| finalState | int32_t | AsDtype('>i4') | 25280 |
| l1charge | int32_t | AsDtype('>i4') | 25280 |
| l1dxy | float | AsDtype('>f4') | 25280 |
| l1dxyErr | float | AsDtype('>f4') | 25280 |
| l1dz | float | AsDtype('>f4') | 25280 |
| l1dzErr | float | AsDtype('>f4') | 25280 |
| l1elCutBased | int32_t | AsDtype('>i4') | 25280 |
| l1elMvaBdt | float | AsDtype('>f4') | 25280 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 25280 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 25280 |
| l1eta | float | AsDtype('>f4') | 25280 |
| l1ip3d | float | AsDtype('>f4') | 25280 |
| l1mass | float | AsDtype('>f4') | 25280 |
| l1miniRelIso | float | AsDtype('>f4') | 25280 |
| l1muGlobal | int32_t | AsDtype('>i4') | 25280 |
| l1muMedium | int32_t | AsDtype('>i4') | 25280 |
| l1muPF | int32_t | AsDtype('>i4') | 25280 |
| l1muTight | int32_t | AsDtype('>i4') | 25280 |
| l1pdgId | int32_t | AsDtype('>i4') | 25280 |
| l1pfRelIso03 | float | AsDtype('>f4') | 25280 |
| l1phi | float | AsDtype('>f4') | 25280 |
| l1pt | float | AsDtype('>f4') | 25280 |
| l1sip3d | float | AsDtype('>f4') | 25280 |
| l1zId | int32_t | AsDtype('>i4') | 25280 |
| l2charge | int32_t | AsDtype('>i4') | 25280 |
| l2dxy | float | AsDtype('>f4') | 25280 |
| l2dxyErr | float | AsDtype('>f4') | 25280 |
| l2dz | float | AsDtype('>f4') | 25280 |
| l2dzErr | float | AsDtype('>f4') | 25280 |
| l2elCutBased | int32_t | AsDtype('>i4') | 25280 |
| l2elMvaBdt | float | AsDtype('>f4') | 25280 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 25280 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 25280 |
| l2eta | float | AsDtype('>f4') | 25280 |
| l2ip3d | float | AsDtype('>f4') | 25280 |
| l2mass | float | AsDtype('>f4') | 25280 |
| l2miniRelIso | float | AsDtype('>f4') | 25280 |
| l2muGlobal | int32_t | AsDtype('>i4') | 25280 |
| l2muMedium | int32_t | AsDtype('>i4') | 25280 |
| l2muPF | int32_t | AsDtype('>i4') | 25280 |
| l2muTight | int32_t | AsDtype('>i4') | 25280 |
| l2pdgId | int32_t | AsDtype('>i4') | 25280 |
| l2pfRelIso03 | float | AsDtype('>f4') | 25280 |
| l2phi | float | AsDtype('>f4') | 25280 |
| l2pt | float | AsDtype('>f4') | 25280 |
| l2sip3d | float | AsDtype('>f4') | 25280 |
| l2zId | int32_t | AsDtype('>i4') | 25280 |
| l3charge | int32_t | AsDtype('>i4') | 25280 |
| l3dxy | float | AsDtype('>f4') | 25280 |
| l3dxyErr | float | AsDtype('>f4') | 25280 |
| l3dz | float | AsDtype('>f4') | 25280 |
| l3dzErr | float | AsDtype('>f4') | 25280 |
| l3elCutBased | int32_t | AsDtype('>i4') | 25280 |
| l3elMvaBdt | float | AsDtype('>f4') | 25280 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 25280 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 25280 |
| l3eta | float | AsDtype('>f4') | 25280 |
| l3ip3d | float | AsDtype('>f4') | 25280 |
| l3mass | float | AsDtype('>f4') | 25280 |
| l3miniRelIso | float | AsDtype('>f4') | 25280 |
| l3muGlobal | int32_t | AsDtype('>i4') | 25280 |
| l3muMedium | int32_t | AsDtype('>i4') | 25280 |
| l3muPF | int32_t | AsDtype('>i4') | 25280 |
| l3muTight | int32_t | AsDtype('>i4') | 25280 |
| l3pdgId | int32_t | AsDtype('>i4') | 25280 |
| l3pfRelIso03 | float | AsDtype('>f4') | 25280 |
| l3phi | float | AsDtype('>f4') | 25280 |
| l3pt | float | AsDtype('>f4') | 25280 |
| l3sip3d | float | AsDtype('>f4') | 25280 |
| l3zId | int32_t | AsDtype('>i4') | 25280 |
| l4charge | int32_t | AsDtype('>i4') | 25280 |
| l4dxy | float | AsDtype('>f4') | 25280 |
| l4dxyErr | float | AsDtype('>f4') | 25280 |
| l4dz | float | AsDtype('>f4') | 25280 |
| l4dzErr | float | AsDtype('>f4') | 25280 |
| l4elCutBased | int32_t | AsDtype('>i4') | 25280 |
| l4elMvaBdt | float | AsDtype('>f4') | 25280 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 25280 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 25280 |
| l4eta | float | AsDtype('>f4') | 25280 |
| l4ip3d | float | AsDtype('>f4') | 25280 |
| l4mass | float | AsDtype('>f4') | 25280 |
| l4miniRelIso | float | AsDtype('>f4') | 25280 |
| l4muGlobal | int32_t | AsDtype('>i4') | 25280 |
| l4muMedium | int32_t | AsDtype('>i4') | 25280 |
| l4muPF | int32_t | AsDtype('>i4') | 25280 |
| l4muTight | int32_t | AsDtype('>i4') | 25280 |
| l4pdgId | int32_t | AsDtype('>i4') | 25280 |
| l4pfRelIso03 | float | AsDtype('>f4') | 25280 |
| l4phi | float | AsDtype('>f4') | 25280 |
| l4pt | float | AsDtype('>f4') | 25280 |
| l4sip3d | float | AsDtype('>f4') | 25280 |
| l4zId | int32_t | AsDtype('>i4') | 25280 |
| lumi | int32_t | AsDtype('>i4') | 25280 |
| m4l | float | AsDtype('>f4') | 25280 |
| mZ1 | float | AsDtype('>f4') | 25280 |
| mZ2 | float | AsDtype('>f4') | 25280 |
| nPV | int32_t | AsDtype('>i4') | 25280 |
| phi4l | float | AsDtype('>f4') | 25280 |
| pt4l | float | AsDtype('>f4') | 25280 |
| pvChi2 | float | AsDtype('>f4') | 25280 |
| pvNdof | float | AsDtype('>f4') | 25280 |
| pvScore | float | AsDtype('>f4') | 25280 |
| pvX | float | AsDtype('>f4') | 25280 |
| pvY | float | AsDtype('>f4') | 25280 |
| pvZ | float | AsDtype('>f4') | 25280 |
| run | int32_t | AsDtype('>i4') | 25280 |
| trigBits | int32_t | AsDtype('>i4') | 25280 |
| y4l | float | AsDtype('>f4') | 25280 |

### `local_mc/WPHToZZ.root`

- Path: `/sandbox/work/jfc/analyses/higgs_4lep_mass/mc/WPHToZZ.root`
- Size: 3152467 bytes
- Prompt cross section: 0.0001072352 pb
- Full sample name: `WplusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 13 | 1 |
| h4lTree | 16304 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 13 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 16304 |
| event | int64_t | AsDtype('>i8') | 16304 |
| finalState | int32_t | AsDtype('>i4') | 16304 |
| l1charge | int32_t | AsDtype('>i4') | 16304 |
| l1dxy | float | AsDtype('>f4') | 16304 |
| l1dxyErr | float | AsDtype('>f4') | 16304 |
| l1dz | float | AsDtype('>f4') | 16304 |
| l1dzErr | float | AsDtype('>f4') | 16304 |
| l1elCutBased | int32_t | AsDtype('>i4') | 16304 |
| l1elMvaBdt | float | AsDtype('>f4') | 16304 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 16304 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 16304 |
| l1eta | float | AsDtype('>f4') | 16304 |
| l1ip3d | float | AsDtype('>f4') | 16304 |
| l1mass | float | AsDtype('>f4') | 16304 |
| l1miniRelIso | float | AsDtype('>f4') | 16304 |
| l1muGlobal | int32_t | AsDtype('>i4') | 16304 |
| l1muMedium | int32_t | AsDtype('>i4') | 16304 |
| l1muPF | int32_t | AsDtype('>i4') | 16304 |
| l1muTight | int32_t | AsDtype('>i4') | 16304 |
| l1pdgId | int32_t | AsDtype('>i4') | 16304 |
| l1pfRelIso03 | float | AsDtype('>f4') | 16304 |
| l1phi | float | AsDtype('>f4') | 16304 |
| l1pt | float | AsDtype('>f4') | 16304 |
| l1sip3d | float | AsDtype('>f4') | 16304 |
| l1zId | int32_t | AsDtype('>i4') | 16304 |
| l2charge | int32_t | AsDtype('>i4') | 16304 |
| l2dxy | float | AsDtype('>f4') | 16304 |
| l2dxyErr | float | AsDtype('>f4') | 16304 |
| l2dz | float | AsDtype('>f4') | 16304 |
| l2dzErr | float | AsDtype('>f4') | 16304 |
| l2elCutBased | int32_t | AsDtype('>i4') | 16304 |
| l2elMvaBdt | float | AsDtype('>f4') | 16304 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 16304 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 16304 |
| l2eta | float | AsDtype('>f4') | 16304 |
| l2ip3d | float | AsDtype('>f4') | 16304 |
| l2mass | float | AsDtype('>f4') | 16304 |
| l2miniRelIso | float | AsDtype('>f4') | 16304 |
| l2muGlobal | int32_t | AsDtype('>i4') | 16304 |
| l2muMedium | int32_t | AsDtype('>i4') | 16304 |
| l2muPF | int32_t | AsDtype('>i4') | 16304 |
| l2muTight | int32_t | AsDtype('>i4') | 16304 |
| l2pdgId | int32_t | AsDtype('>i4') | 16304 |
| l2pfRelIso03 | float | AsDtype('>f4') | 16304 |
| l2phi | float | AsDtype('>f4') | 16304 |
| l2pt | float | AsDtype('>f4') | 16304 |
| l2sip3d | float | AsDtype('>f4') | 16304 |
| l2zId | int32_t | AsDtype('>i4') | 16304 |
| l3charge | int32_t | AsDtype('>i4') | 16304 |
| l3dxy | float | AsDtype('>f4') | 16304 |
| l3dxyErr | float | AsDtype('>f4') | 16304 |
| l3dz | float | AsDtype('>f4') | 16304 |
| l3dzErr | float | AsDtype('>f4') | 16304 |
| l3elCutBased | int32_t | AsDtype('>i4') | 16304 |
| l3elMvaBdt | float | AsDtype('>f4') | 16304 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 16304 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 16304 |
| l3eta | float | AsDtype('>f4') | 16304 |
| l3ip3d | float | AsDtype('>f4') | 16304 |
| l3mass | float | AsDtype('>f4') | 16304 |
| l3miniRelIso | float | AsDtype('>f4') | 16304 |
| l3muGlobal | int32_t | AsDtype('>i4') | 16304 |
| l3muMedium | int32_t | AsDtype('>i4') | 16304 |
| l3muPF | int32_t | AsDtype('>i4') | 16304 |
| l3muTight | int32_t | AsDtype('>i4') | 16304 |
| l3pdgId | int32_t | AsDtype('>i4') | 16304 |
| l3pfRelIso03 | float | AsDtype('>f4') | 16304 |
| l3phi | float | AsDtype('>f4') | 16304 |
| l3pt | float | AsDtype('>f4') | 16304 |
| l3sip3d | float | AsDtype('>f4') | 16304 |
| l3zId | int32_t | AsDtype('>i4') | 16304 |
| l4charge | int32_t | AsDtype('>i4') | 16304 |
| l4dxy | float | AsDtype('>f4') | 16304 |
| l4dxyErr | float | AsDtype('>f4') | 16304 |
| l4dz | float | AsDtype('>f4') | 16304 |
| l4dzErr | float | AsDtype('>f4') | 16304 |
| l4elCutBased | int32_t | AsDtype('>i4') | 16304 |
| l4elMvaBdt | float | AsDtype('>f4') | 16304 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 16304 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 16304 |
| l4eta | float | AsDtype('>f4') | 16304 |
| l4ip3d | float | AsDtype('>f4') | 16304 |
| l4mass | float | AsDtype('>f4') | 16304 |
| l4miniRelIso | float | AsDtype('>f4') | 16304 |
| l4muGlobal | int32_t | AsDtype('>i4') | 16304 |
| l4muMedium | int32_t | AsDtype('>i4') | 16304 |
| l4muPF | int32_t | AsDtype('>i4') | 16304 |
| l4muTight | int32_t | AsDtype('>i4') | 16304 |
| l4pdgId | int32_t | AsDtype('>i4') | 16304 |
| l4pfRelIso03 | float | AsDtype('>f4') | 16304 |
| l4phi | float | AsDtype('>f4') | 16304 |
| l4pt | float | AsDtype('>f4') | 16304 |
| l4sip3d | float | AsDtype('>f4') | 16304 |
| l4zId | int32_t | AsDtype('>i4') | 16304 |
| lumi | int32_t | AsDtype('>i4') | 16304 |
| m4l | float | AsDtype('>f4') | 16304 |
| mZ1 | float | AsDtype('>f4') | 16304 |
| mZ2 | float | AsDtype('>f4') | 16304 |
| nPV | int32_t | AsDtype('>i4') | 16304 |
| phi4l | float | AsDtype('>f4') | 16304 |
| pt4l | float | AsDtype('>f4') | 16304 |
| pvChi2 | float | AsDtype('>f4') | 16304 |
| pvNdof | float | AsDtype('>f4') | 16304 |
| pvScore | float | AsDtype('>f4') | 16304 |
| pvX | float | AsDtype('>f4') | 16304 |
| pvY | float | AsDtype('>f4') | 16304 |
| pvZ | float | AsDtype('>f4') | 16304 |
| run | int32_t | AsDtype('>i4') | 16304 |
| trigBits | int32_t | AsDtype('>i4') | 16304 |
| y4l | float | AsDtype('>f4') | 16304 |

### `local_mc/ZHToZZ.root`

- Path: `/sandbox/work/jfc/analyses/higgs_4lep_mass/mc/ZHToZZ.root`
- Size: 13117349 bytes
- Prompt cross section: 9.8394e-05 pb
- Full sample name: `ZH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 1 | 1 |
| h4lTree | 72515 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 1 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 72515 |
| event | int64_t | AsDtype('>i8') | 72515 |
| finalState | int32_t | AsDtype('>i4') | 72515 |
| l1charge | int32_t | AsDtype('>i4') | 72515 |
| l1dxy | float | AsDtype('>f4') | 72515 |
| l1dxyErr | float | AsDtype('>f4') | 72515 |
| l1dz | float | AsDtype('>f4') | 72515 |
| l1dzErr | float | AsDtype('>f4') | 72515 |
| l1elCutBased | int32_t | AsDtype('>i4') | 72515 |
| l1elMvaBdt | float | AsDtype('>f4') | 72515 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 72515 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 72515 |
| l1eta | float | AsDtype('>f4') | 72515 |
| l1ip3d | float | AsDtype('>f4') | 72515 |
| l1mass | float | AsDtype('>f4') | 72515 |
| l1miniRelIso | float | AsDtype('>f4') | 72515 |
| l1muGlobal | int32_t | AsDtype('>i4') | 72515 |
| l1muMedium | int32_t | AsDtype('>i4') | 72515 |
| l1muPF | int32_t | AsDtype('>i4') | 72515 |
| l1muTight | int32_t | AsDtype('>i4') | 72515 |
| l1pdgId | int32_t | AsDtype('>i4') | 72515 |
| l1pfRelIso03 | float | AsDtype('>f4') | 72515 |
| l1phi | float | AsDtype('>f4') | 72515 |
| l1pt | float | AsDtype('>f4') | 72515 |
| l1sip3d | float | AsDtype('>f4') | 72515 |
| l1zId | int32_t | AsDtype('>i4') | 72515 |
| l2charge | int32_t | AsDtype('>i4') | 72515 |
| l2dxy | float | AsDtype('>f4') | 72515 |
| l2dxyErr | float | AsDtype('>f4') | 72515 |
| l2dz | float | AsDtype('>f4') | 72515 |
| l2dzErr | float | AsDtype('>f4') | 72515 |
| l2elCutBased | int32_t | AsDtype('>i4') | 72515 |
| l2elMvaBdt | float | AsDtype('>f4') | 72515 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 72515 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 72515 |
| l2eta | float | AsDtype('>f4') | 72515 |
| l2ip3d | float | AsDtype('>f4') | 72515 |
| l2mass | float | AsDtype('>f4') | 72515 |
| l2miniRelIso | float | AsDtype('>f4') | 72515 |
| l2muGlobal | int32_t | AsDtype('>i4') | 72515 |
| l2muMedium | int32_t | AsDtype('>i4') | 72515 |
| l2muPF | int32_t | AsDtype('>i4') | 72515 |
| l2muTight | int32_t | AsDtype('>i4') | 72515 |
| l2pdgId | int32_t | AsDtype('>i4') | 72515 |
| l2pfRelIso03 | float | AsDtype('>f4') | 72515 |
| l2phi | float | AsDtype('>f4') | 72515 |
| l2pt | float | AsDtype('>f4') | 72515 |
| l2sip3d | float | AsDtype('>f4') | 72515 |
| l2zId | int32_t | AsDtype('>i4') | 72515 |
| l3charge | int32_t | AsDtype('>i4') | 72515 |
| l3dxy | float | AsDtype('>f4') | 72515 |
| l3dxyErr | float | AsDtype('>f4') | 72515 |
| l3dz | float | AsDtype('>f4') | 72515 |
| l3dzErr | float | AsDtype('>f4') | 72515 |
| l3elCutBased | int32_t | AsDtype('>i4') | 72515 |
| l3elMvaBdt | float | AsDtype('>f4') | 72515 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 72515 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 72515 |
| l3eta | float | AsDtype('>f4') | 72515 |
| l3ip3d | float | AsDtype('>f4') | 72515 |
| l3mass | float | AsDtype('>f4') | 72515 |
| l3miniRelIso | float | AsDtype('>f4') | 72515 |
| l3muGlobal | int32_t | AsDtype('>i4') | 72515 |
| l3muMedium | int32_t | AsDtype('>i4') | 72515 |
| l3muPF | int32_t | AsDtype('>i4') | 72515 |
| l3muTight | int32_t | AsDtype('>i4') | 72515 |
| l3pdgId | int32_t | AsDtype('>i4') | 72515 |
| l3pfRelIso03 | float | AsDtype('>f4') | 72515 |
| l3phi | float | AsDtype('>f4') | 72515 |
| l3pt | float | AsDtype('>f4') | 72515 |
| l3sip3d | float | AsDtype('>f4') | 72515 |
| l3zId | int32_t | AsDtype('>i4') | 72515 |
| l4charge | int32_t | AsDtype('>i4') | 72515 |
| l4dxy | float | AsDtype('>f4') | 72515 |
| l4dxyErr | float | AsDtype('>f4') | 72515 |
| l4dz | float | AsDtype('>f4') | 72515 |
| l4dzErr | float | AsDtype('>f4') | 72515 |
| l4elCutBased | int32_t | AsDtype('>i4') | 72515 |
| l4elMvaBdt | float | AsDtype('>f4') | 72515 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 72515 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 72515 |
| l4eta | float | AsDtype('>f4') | 72515 |
| l4ip3d | float | AsDtype('>f4') | 72515 |
| l4mass | float | AsDtype('>f4') | 72515 |
| l4miniRelIso | float | AsDtype('>f4') | 72515 |
| l4muGlobal | int32_t | AsDtype('>i4') | 72515 |
| l4muMedium | int32_t | AsDtype('>i4') | 72515 |
| l4muPF | int32_t | AsDtype('>i4') | 72515 |
| l4muTight | int32_t | AsDtype('>i4') | 72515 |
| l4pdgId | int32_t | AsDtype('>i4') | 72515 |
| l4pfRelIso03 | float | AsDtype('>f4') | 72515 |
| l4phi | float | AsDtype('>f4') | 72515 |
| l4pt | float | AsDtype('>f4') | 72515 |
| l4sip3d | float | AsDtype('>f4') | 72515 |
| l4zId | int32_t | AsDtype('>i4') | 72515 |
| lumi | int32_t | AsDtype('>i4') | 72515 |
| m4l | float | AsDtype('>f4') | 72515 |
| mZ1 | float | AsDtype('>f4') | 72515 |
| mZ2 | float | AsDtype('>f4') | 72515 |
| nPV | int32_t | AsDtype('>i4') | 72515 |
| phi4l | float | AsDtype('>f4') | 72515 |
| pt4l | float | AsDtype('>f4') | 72515 |
| pvChi2 | float | AsDtype('>f4') | 72515 |
| pvNdof | float | AsDtype('>f4') | 72515 |
| pvScore | float | AsDtype('>f4') | 72515 |
| pvX | float | AsDtype('>f4') | 72515 |
| pvY | float | AsDtype('>f4') | 72515 |
| pvZ | float | AsDtype('>f4') | 72515 |
| run | int32_t | AsDtype('>i4') | 72515 |
| trigBits | int32_t | AsDtype('>i4') | 72515 |
| y4l | float | AsDtype('>f4') | 72515 |

### `local_mc/ZZTo4L.root`

- Path: `/sandbox/work/jfc/analyses/higgs_4lep_mass/mc/ZZTo4L.root`
- Size: 600302406 bytes
- Prompt cross section: 1.325 pb
- Full sample name: `ZZTo4L_TuneCP5_13TeV_powheg_pythia8`
| Tree | Entries | Branches |
| --- | --- | --- |
| Metadata | 108 | 1 |
| h4lTree | 3333903 | 111 |

#### Branches in `Metadata`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| nEvents | int64_t | AsDtype('>i8') | 108 |

#### Branches in `h4lTree`
| Branch | Type | Interpretation | Entries |
| --- | --- | --- | --- |
| eta4l | float | AsDtype('>f4') | 3333903 |
| event | int64_t | AsDtype('>i8') | 3333903 |
| finalState | int32_t | AsDtype('>i4') | 3333903 |
| l1charge | int32_t | AsDtype('>i4') | 3333903 |
| l1dxy | float | AsDtype('>f4') | 3333903 |
| l1dxyErr | float | AsDtype('>f4') | 3333903 |
| l1dz | float | AsDtype('>f4') | 3333903 |
| l1dzErr | float | AsDtype('>f4') | 3333903 |
| l1elCutBased | int32_t | AsDtype('>i4') | 3333903 |
| l1elMvaBdt | float | AsDtype('>f4') | 3333903 |
| l1elMvaWP80 | int32_t | AsDtype('>i4') | 3333903 |
| l1elMvaWP90 | int32_t | AsDtype('>i4') | 3333903 |
| l1eta | float | AsDtype('>f4') | 3333903 |
| l1ip3d | float | AsDtype('>f4') | 3333903 |
| l1mass | float | AsDtype('>f4') | 3333903 |
| l1miniRelIso | float | AsDtype('>f4') | 3333903 |
| l1muGlobal | int32_t | AsDtype('>i4') | 3333903 |
| l1muMedium | int32_t | AsDtype('>i4') | 3333903 |
| l1muPF | int32_t | AsDtype('>i4') | 3333903 |
| l1muTight | int32_t | AsDtype('>i4') | 3333903 |
| l1pdgId | int32_t | AsDtype('>i4') | 3333903 |
| l1pfRelIso03 | float | AsDtype('>f4') | 3333903 |
| l1phi | float | AsDtype('>f4') | 3333903 |
| l1pt | float | AsDtype('>f4') | 3333903 |
| l1sip3d | float | AsDtype('>f4') | 3333903 |
| l1zId | int32_t | AsDtype('>i4') | 3333903 |
| l2charge | int32_t | AsDtype('>i4') | 3333903 |
| l2dxy | float | AsDtype('>f4') | 3333903 |
| l2dxyErr | float | AsDtype('>f4') | 3333903 |
| l2dz | float | AsDtype('>f4') | 3333903 |
| l2dzErr | float | AsDtype('>f4') | 3333903 |
| l2elCutBased | int32_t | AsDtype('>i4') | 3333903 |
| l2elMvaBdt | float | AsDtype('>f4') | 3333903 |
| l2elMvaWP80 | int32_t | AsDtype('>i4') | 3333903 |
| l2elMvaWP90 | int32_t | AsDtype('>i4') | 3333903 |
| l2eta | float | AsDtype('>f4') | 3333903 |
| l2ip3d | float | AsDtype('>f4') | 3333903 |
| l2mass | float | AsDtype('>f4') | 3333903 |
| l2miniRelIso | float | AsDtype('>f4') | 3333903 |
| l2muGlobal | int32_t | AsDtype('>i4') | 3333903 |
| l2muMedium | int32_t | AsDtype('>i4') | 3333903 |
| l2muPF | int32_t | AsDtype('>i4') | 3333903 |
| l2muTight | int32_t | AsDtype('>i4') | 3333903 |
| l2pdgId | int32_t | AsDtype('>i4') | 3333903 |
| l2pfRelIso03 | float | AsDtype('>f4') | 3333903 |
| l2phi | float | AsDtype('>f4') | 3333903 |
| l2pt | float | AsDtype('>f4') | 3333903 |
| l2sip3d | float | AsDtype('>f4') | 3333903 |
| l2zId | int32_t | AsDtype('>i4') | 3333903 |
| l3charge | int32_t | AsDtype('>i4') | 3333903 |
| l3dxy | float | AsDtype('>f4') | 3333903 |
| l3dxyErr | float | AsDtype('>f4') | 3333903 |
| l3dz | float | AsDtype('>f4') | 3333903 |
| l3dzErr | float | AsDtype('>f4') | 3333903 |
| l3elCutBased | int32_t | AsDtype('>i4') | 3333903 |
| l3elMvaBdt | float | AsDtype('>f4') | 3333903 |
| l3elMvaWP80 | int32_t | AsDtype('>i4') | 3333903 |
| l3elMvaWP90 | int32_t | AsDtype('>i4') | 3333903 |
| l3eta | float | AsDtype('>f4') | 3333903 |
| l3ip3d | float | AsDtype('>f4') | 3333903 |
| l3mass | float | AsDtype('>f4') | 3333903 |
| l3miniRelIso | float | AsDtype('>f4') | 3333903 |
| l3muGlobal | int32_t | AsDtype('>i4') | 3333903 |
| l3muMedium | int32_t | AsDtype('>i4') | 3333903 |
| l3muPF | int32_t | AsDtype('>i4') | 3333903 |
| l3muTight | int32_t | AsDtype('>i4') | 3333903 |
| l3pdgId | int32_t | AsDtype('>i4') | 3333903 |
| l3pfRelIso03 | float | AsDtype('>f4') | 3333903 |
| l3phi | float | AsDtype('>f4') | 3333903 |
| l3pt | float | AsDtype('>f4') | 3333903 |
| l3sip3d | float | AsDtype('>f4') | 3333903 |
| l3zId | int32_t | AsDtype('>i4') | 3333903 |
| l4charge | int32_t | AsDtype('>i4') | 3333903 |
| l4dxy | float | AsDtype('>f4') | 3333903 |
| l4dxyErr | float | AsDtype('>f4') | 3333903 |
| l4dz | float | AsDtype('>f4') | 3333903 |
| l4dzErr | float | AsDtype('>f4') | 3333903 |
| l4elCutBased | int32_t | AsDtype('>i4') | 3333903 |
| l4elMvaBdt | float | AsDtype('>f4') | 3333903 |
| l4elMvaWP80 | int32_t | AsDtype('>i4') | 3333903 |
| l4elMvaWP90 | int32_t | AsDtype('>i4') | 3333903 |
| l4eta | float | AsDtype('>f4') | 3333903 |
| l4ip3d | float | AsDtype('>f4') | 3333903 |
| l4mass | float | AsDtype('>f4') | 3333903 |
| l4miniRelIso | float | AsDtype('>f4') | 3333903 |
| l4muGlobal | int32_t | AsDtype('>i4') | 3333903 |
| l4muMedium | int32_t | AsDtype('>i4') | 3333903 |
| l4muPF | int32_t | AsDtype('>i4') | 3333903 |
| l4muTight | int32_t | AsDtype('>i4') | 3333903 |
| l4pdgId | int32_t | AsDtype('>i4') | 3333903 |
| l4pfRelIso03 | float | AsDtype('>f4') | 3333903 |
| l4phi | float | AsDtype('>f4') | 3333903 |
| l4pt | float | AsDtype('>f4') | 3333903 |
| l4sip3d | float | AsDtype('>f4') | 3333903 |
| l4zId | int32_t | AsDtype('>i4') | 3333903 |
| lumi | int32_t | AsDtype('>i4') | 3333903 |
| m4l | float | AsDtype('>f4') | 3333903 |
| mZ1 | float | AsDtype('>f4') | 3333903 |
| mZ2 | float | AsDtype('>f4') | 3333903 |
| nPV | int32_t | AsDtype('>i4') | 3333903 |
| phi4l | float | AsDtype('>f4') | 3333903 |
| pt4l | float | AsDtype('>f4') | 3333903 |
| pvChi2 | float | AsDtype('>f4') | 3333903 |
| pvNdof | float | AsDtype('>f4') | 3333903 |
| pvScore | float | AsDtype('>f4') | 3333903 |
| pvX | float | AsDtype('>f4') | 3333903 |
| pvY | float | AsDtype('>f4') | 3333903 |
| pvZ | float | AsDtype('>f4') | 3333903 |
| run | int32_t | AsDtype('>i4') | 3333903 |
| trigBits | int32_t | AsDtype('>i4') | 3333903 |
| y4l | float | AsDtype('>f4') | 3333903 |


## Physics Capability From Branch Names

| Capability | Status | Matching branches |
| --- | --- | --- |
| Four-lepton mass | FOUND | m4l |
| Z candidate masses | FOUND | mZ1, mZ2 |
| Four-lepton kinematics | FOUND | eta4l, phi4l, pt4l |
| Per-lepton four-vector inputs | FOUND | l1eta, l1mass, l1phi, l1pt, l4eta, l4mass, l4phi, l4pt |
| Jet/VBF observables | NOT FOUND | none in primary h4lTree/Metadata branches |
| Angular primitives | FOUND | l1phi, l2phi, l3phi, l4phi, phi4l |
| Precomputed MELA/angular discriminants | NOT FOUND | none in primary h4lTree/Metadata branches |
| Generator/truth branches | NOT FOUND | none in primary h4lTree/Metadata branches |

Phase 1 finds the core four-lepton variables (`m4l`, `mZ1`, `mZ2`, `pt4l`, `eta4l`, `phi4l`) and per-lepton kinematics/ID/isolation variables. It finds azimuthal-angle primitives but does not find jet/VBF branches, generator-level truth branches, or precomputed MELA/angular discriminants in the primary branch inventory. Phase 2/3 must therefore either compute VBF and angular inputs from available lower-level information if possible, or formally document the limitation before committing to those analysis features.

## Integer and Flag Unique-Value Survey

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cms_10fb_13TeV.root | Metadata | nEvents | 1 | 854.0 | 854.0 | 854.0 | 854(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cms_10fb_13TeV.root | h4lTree | finalState | 3 | 0.0 | 2.0 | 1.3114754098360655 | 0(162), 1(264), 2(428) |
| cms_10fb_13TeV.root | h4lTree | l1charge | 2 | -1.0 | 1.0 | 0.04449648711943794 | -1(408), 1(446) |
| cms_10fb_13TeV.root | h4lTree | l1elCutBased | 5 | 0.0 | 4.0 | 1.5784543325526932 | 0(480), 1(18), 2(27), 3(40), 4(289) |
| cms_10fb_13TeV.root | h4lTree | l1elMvaWP80 | 2 | 0.0 | 1.0 | 0.35362997658079626 | 0(552), 1(302) |
| cms_10fb_13TeV.root | h4lTree | l1elMvaWP90 | 2 | 0.0 | 1.0 | 0.4098360655737705 | 0(504), 1(350) |
| cms_10fb_13TeV.root | h4lTree | l1miniRelIso | 286 | 0.0 | 2.7662646770477295 | 0.037709299474954605 | 0.0(569), 3.019454379682429e-05(1), 0.0001441500207874924(1), 0.0001820303441490978(1), 0.00025966373505070806(1), 0.00036592641845345497(1), 0.0006193785811774433(1), 0.0007055146270431578(1), 0.0009871992515400052(1), 0.0010177784133702517(1), 0.0014457624638453126(1), 0.0017305269138887525(1), ... |
| cms_10fb_13TeV.root | h4lTree | l1muGlobal | 2 | 0.0 | 1.0 | 0.5046838407494145 | 0(423), 1(431) |
| cms_10fb_13TeV.root | h4lTree | l1muMedium | 2 | 0.0 | 1.0 | 0.5035128805620609 | 0(424), 1(430) |
| cms_10fb_13TeV.root | h4lTree | l1muPF | 2 | 0.0 | 1.0 | 0.5070257611241218 | 0(421), 1(433) |
| cms_10fb_13TeV.root | h4lTree | l1muTight | 2 | 0.0 | 1.0 | 0.5011709601873536 | 0(426), 1(428) |
| cms_10fb_13TeV.root | h4lTree | l1pdgId | 4 | -13.0 | 13.0 | -0.5245901639344263 | -13(224), -11(222), 11(199), 13(209) |
| cms_10fb_13TeV.root | h4lTree | l1zId | 1 | 1.0 | 1.0 | 1.0 | 1(854) |
| cms_10fb_13TeV.root | h4lTree | l2charge | 2 | -1.0 | 1.0 | -0.04449648711943794 | -1(446), 1(408) |
| cms_10fb_13TeV.root | h4lTree | l2elCutBased | 5 | 0.0 | 4.0 | 1.4098360655737705 | 0(495), 1(26), 2(48), 3(58), 4(227) |
| cms_10fb_13TeV.root | h4lTree | l2elMvaWP80 | 2 | 0.0 | 1.0 | 0.319672131147541 | 0(581), 1(273) |
| cms_10fb_13TeV.root | h4lTree | l2elMvaWP90 | 2 | 0.0 | 1.0 | 0.3840749414519906 | 0(526), 1(328) |
| cms_10fb_13TeV.root | h4lTree | l2miniRelIso | 370 | 0.0 | 1.8134676218032837 | 0.05782383680343628 | 0.0(485), 3.1877512810751796e-05(1), 0.0003637155459728092(1), 0.0005583939491771162(1), 0.0007696639513596892(1), 0.0007775037083774805(1), 0.0007950871367938817(1), 0.001501002348959446(1), 0.0018119103042408824(1), 0.0020047049038112164(1), 0.002281763358041644(1), 0.0023264100309461355(1), ... |
| cms_10fb_13TeV.root | h4lTree | l2muGlobal | 2 | 0.0 | 1.0 | 0.5 | 0(427), 1(427) |
| cms_10fb_13TeV.root | h4lTree | l2muMedium | 2 | 0.0 | 1.0 | 0.5046838407494145 | 0(423), 1(431) |
| cms_10fb_13TeV.root | h4lTree | l2muPF | 2 | 0.0 | 1.0 | 0.5070257611241218 | 0(421), 1(433) |
| cms_10fb_13TeV.root | h4lTree | l2muTight | 2 | 0.0 | 1.0 | 0.49882903981264637 | 0(428), 1(426) |
| cms_10fb_13TeV.root | h4lTree | l2pdgId | 4 | -13.0 | 13.0 | 0.5245901639344263 | -13(209), -11(199), 11(222), 13(224) |
| cms_10fb_13TeV.root | h4lTree | l2zId | 1 | 1.0 | 1.0 | 1.0 | 1(854) |
| cms_10fb_13TeV.root | h4lTree | l3charge | 2 | -1.0 | 1.0 | 0.05620608899297424 | -1(403), 1(451) |
| cms_10fb_13TeV.root | h4lTree | l3elCutBased | 5 | 0.0 | 4.0 | 1.148711943793911 | 0(536), 1(59), 2(35), 3(44), 4(180) |
| cms_10fb_13TeV.root | h4lTree | l3elMvaWP80 | 2 | 0.0 | 1.0 | 0.2576112412177986 | 0(634), 1(220) |
| cms_10fb_13TeV.root | h4lTree | l3elMvaWP90 | 2 | 0.0 | 1.0 | 0.31030444964871196 | 0(589), 1(265) |
| cms_10fb_13TeV.root | h4lTree | l3miniRelIso | 416 | 0.0 | 4.271037578582764 | 0.19912084937095642 | 0.0(439), 0.0008135265088640153(1), 0.0008985612075775862(1), 0.001548677682876587(1), 0.0018017597030848265(1), 0.0019248327007517219(1), 0.0019795142579823732(1), 0.002514755818992853(1), 0.0026119393296539783(1), 0.0029856127221137285(1), 0.0030230097472667694(1), 0.0031774325761944056(1), ... |
| cms_10fb_13TeV.root | h4lTree | l3muGlobal | 2 | 0.0 | 1.0 | 0.3618266978922717 | 0(545), 1(309) |
| cms_10fb_13TeV.root | h4lTree | l3muMedium | 2 | 0.0 | 1.0 | 0.3618266978922717 | 0(545), 1(309) |
| cms_10fb_13TeV.root | h4lTree | l3muPF | 2 | 0.0 | 1.0 | 0.3711943793911007 | 0(537), 1(317) |
| cms_10fb_13TeV.root | h4lTree | l3muTight | 2 | 0.0 | 1.0 | 0.3548009367681499 | 0(551), 1(303) |
| cms_10fb_13TeV.root | h4lTree | l3pdgId | 4 | -13.0 | 13.0 | -0.6721311475409836 | -13(171), -11(280), 11(255), 13(148) |
| cms_10fb_13TeV.root | h4lTree | l3zId | 1 | 2.0 | 2.0 | 2.0 | 2(854) |
| cms_10fb_13TeV.root | h4lTree | l4charge | 2 | -1.0 | 1.0 | -0.05620608899297424 | -1(451), 1(403) |
| cms_10fb_13TeV.root | h4lTree | l4elCutBased | 5 | 0.0 | 4.0 | 1.0644028103044496 | 0(538), 1(65), 2(56), 3(48), 4(147) |
| cms_10fb_13TeV.root | h4lTree | l4elMvaWP80 | 2 | 0.0 | 1.0 | 0.2540983606557377 | 0(637), 1(217) |
| cms_10fb_13TeV.root | h4lTree | l4elMvaWP90 | 2 | 0.0 | 1.0 | 0.3185011709601874 | 0(582), 1(272) |
| cms_10fb_13TeV.root | h4lTree | l4miniRelIso | 427 | 0.0 | 4.777987003326416 | 0.21162281930446625 | 0.0(428), 0.002301748376339674(1), 0.003619271330535412(1), 0.0036670395638793707(1), 0.0037324181757867336(1), 0.004136817995458841(1), 0.0045366790145635605(1), 0.0046554263681173325(1), 0.005148862022906542(1), 0.005458403844386339(1), 0.0057211145758628845(1), 0.00575930206105113(1), ... |
| cms_10fb_13TeV.root | h4lTree | l4muGlobal | 2 | 0.0 | 1.0 | 0.3665105386416862 | 0(541), 1(313) |
| cms_10fb_13TeV.root | h4lTree | l4muMedium | 2 | 0.0 | 1.0 | 0.3665105386416862 | 0(541), 1(313) |
| cms_10fb_13TeV.root | h4lTree | l4muPF | 2 | 0.0 | 1.0 | 0.373536299765808 | 0(535), 1(319) |
| cms_10fb_13TeV.root | h4lTree | l4muTight | 2 | 0.0 | 1.0 | 0.3583138173302108 | 0(548), 1(306) |
| cms_10fb_13TeV.root | h4lTree | l4pdgId | 4 | -13.0 | 13.0 | 0.6721311475409836 | -13(148), -11(255), 11(280), 13(171) |
| cms_10fb_13TeV.root | h4lTree | l4zId | 1 | 2.0 | 2.0 | 2.0 | 2(854) |
| cms_10fb_13TeV.root | h4lTree | nPV | 36 | 4.0 | 47.0 | 18.10889929742389 | 4(3), 5(3), 6(6), 7(6), 8(12), 9(22), 10(25), 11(27), 12(49), 13(43), 14(52), 15(58) |
| cms_10fb_13TeV.root | h4lTree | pvNdof | 510 | 0.77734375 | 282.0 | 82.69284057617188 | 0.77734375(1), 0.783203125(1), 5.421875(1), 7.34375(1), 7.984375(1), 8.46875(1), 8.96875(1), 9.3125(1), 9.5(1), 9.5625(1), 9.65625(1), 10.25(1), ... |
| cms_10fb_13TeV.root | h4lTree | trigBits | 33 | 0.0 | 1791.0 | 461.89227166276345 | 0(56), 1(4), 3(113), 12(1), 16(18), 32(48), 48(180), 143(2), 256(10), 257(3), 259(143), 271(5) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DYJetsToLL.root | Metadata | nEvents | 1 | 82448537.0 | 82448537.0 | 82448537.0 | 82448537(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DYJetsToLL.root | h4lTree | event | 463 | 358385.0 | 249932041.0 | 124086413.36285098 | 358385(1), 541115(1), 812566(1), 1051865(1), 1362591(1), 1392698(1), 2790171(1), 3031879(1), 3444487(1), 3554661(1), 3759221(1), 4022789(1), ... |
| DYJetsToLL.root | h4lTree | finalState | 3 | 0.0 | 2.0 | 1.4838012958963283 | 0(11), 1(217), 2(235) |
| DYJetsToLL.root | h4lTree | l1charge | 2 | -1.0 | 1.0 | -0.028077753779697623 | -1(238), 1(225) |
| DYJetsToLL.root | h4lTree | l1elCutBased | 5 | 0.0 | 4.0 | 1.5874730021598271 | 0(259), 1(9), 2(15), 3(24), 4(156) |
| DYJetsToLL.root | h4lTree | l1elMvaWP80 | 2 | 0.0 | 1.0 | 0.3563714902807775 | 0(298), 1(165) |
| DYJetsToLL.root | h4lTree | l1elMvaWP90 | 2 | 0.0 | 1.0 | 0.39956803455723544 | 0(278), 1(185) |
| DYJetsToLL.root | h4lTree | l1miniRelIso | 167 | 0.0 | 2.7662646770477295 | 0.06662872433662415 | 0.0(297), 3.019454379682429e-05(1), 0.0006193785811774433(1), 0.0007055146270431578(1), 0.0007756886770948768(1), 0.0010177784133702517(1), 0.0014831225853413343(1), 0.0018501821905374527(1), 0.001918937312439084(1), 0.0022898465394973755(1), 0.0025449017994105816(1), 0.003008380765095353(1), ... |
| DYJetsToLL.root | h4lTree | l1muGlobal | 2 | 0.0 | 1.0 | 0.4557235421166307 | 0(252), 1(211) |
| DYJetsToLL.root | h4lTree | l1muMedium | 2 | 0.0 | 1.0 | 0.45788336933045354 | 0(251), 1(212) |
| DYJetsToLL.root | h4lTree | l1muPF | 2 | 0.0 | 1.0 | 0.46436285097192226 | 0(248), 1(215) |
| DYJetsToLL.root | h4lTree | l1muTight | 2 | 0.0 | 1.0 | 0.4535637149028078 | 0(253), 1(210) |
| DYJetsToLL.root | h4lTree | l1pdgId | 4 | -13.0 | 13.0 | 0.3563714902807775 | -13(102), -11(123), 11(125), 13(113) |
| DYJetsToLL.root | h4lTree | l1zId | 1 | 1.0 | 1.0 | 1.0 | 1(463) |
| DYJetsToLL.root | h4lTree | l2charge | 2 | -1.0 | 1.0 | 0.028077753779697623 | -1(225), 1(238) |
| DYJetsToLL.root | h4lTree | l2elCutBased | 5 | 0.0 | 4.0 | 1.3347732181425487 | 0(271), 1(18), 2(32), 3(32), 4(110) |
| DYJetsToLL.root | h4lTree | l2elMvaWP80 | 2 | 0.0 | 1.0 | 0.28509719222462204 | 0(331), 1(132) |
| DYJetsToLL.root | h4lTree | l2elMvaWP90 | 2 | 0.0 | 1.0 | 0.34773218142548595 | 0(302), 1(161) |
| DYJetsToLL.root | h4lTree | l2miniRelIso | 210 | 0.0 | 1.9007847309112549 | 0.08618508279323578 | 0.0(254), 3.1877512810751796e-05(1), 0.0002531506179366261(1), 0.0007696639513596892(1), 0.001501002348959446(1), 0.0020047049038112164(1), 0.0023264100309461355(1), 0.002678211545571685(1), 0.004289028234779835(1), 0.004431428853422403(1), 0.00457176985219121(1), 0.006148205138742924(1), ... |
| DYJetsToLL.root | h4lTree | l2muGlobal | 2 | 0.0 | 1.0 | 0.46220302375809935 | 0(249), 1(214) |
| DYJetsToLL.root | h4lTree | l2muMedium | 2 | 0.0 | 1.0 | 0.46004319654427644 | 0(250), 1(213) |
| DYJetsToLL.root | h4lTree | l2muPF | 2 | 0.0 | 1.0 | 0.46436285097192226 | 0(248), 1(215) |
| DYJetsToLL.root | h4lTree | l2muTight | 2 | 0.0 | 1.0 | 0.4557235421166307 | 0(252), 1(211) |
| DYJetsToLL.root | h4lTree | l2pdgId | 4 | -13.0 | 13.0 | -0.3563714902807775 | -13(113), -11(125), 11(123), 13(102) |
| DYJetsToLL.root | h4lTree | l2zId | 1 | 1.0 | 1.0 | 1.0 | 1(463) |
| DYJetsToLL.root | h4lTree | l3charge | 2 | -1.0 | 1.0 | 0.0755939524838013 | -1(214), 1(249) |
| DYJetsToLL.root | h4lTree | l3elCutBased | 5 | 0.0 | 4.0 | 0.693304535637149 | 0(329), 1(52), 2(22), 3(15), 4(45) |
| DYJetsToLL.root | h4lTree | l3elMvaWP80 | 2 | 0.0 | 1.0 | 0.11447084233261338 | 0(410), 1(53) |
| DYJetsToLL.root | h4lTree | l3elMvaWP90 | 2 | 0.0 | 1.0 | 0.1468682505399568 | 0(395), 1(68) |
| DYJetsToLL.root | h4lTree | l3miniRelIso | 359 | 0.0 | 4.271037578582764 | 0.49907588958740234 | 0.0(105), 1.611664265510626e-05(1), 0.0008985612075775862(1), 0.0016978139756247401(1), 0.0029856127221137285(1), 0.0030230097472667694(1), 0.0031774325761944056(1), 0.004798394162207842(1), 0.008460895158350468(1), 0.008561327122151852(1), 0.009199143387377262(1), 0.010586817748844624(1), ... |
| DYJetsToLL.root | h4lTree | l3muGlobal | 2 | 0.0 | 1.0 | 0.0755939524838013 | 0(428), 1(35) |
| DYJetsToLL.root | h4lTree | l3muMedium | 2 | 0.0 | 1.0 | 0.0734341252699784 | 0(429), 1(34) |
| DYJetsToLL.root | h4lTree | l3muPF | 2 | 0.0 | 1.0 | 0.08855291576673865 | 0(422), 1(41) |
| DYJetsToLL.root | h4lTree | l3muTight | 2 | 0.0 | 1.0 | 0.0734341252699784 | 0(429), 1(34) |
| DYJetsToLL.root | h4lTree | l3pdgId | 4 | -13.0 | 13.0 | -0.8488120950323974 | -13(23), -11(226), 11(195), 13(19) |
| DYJetsToLL.root | h4lTree | l3zId | 1 | 2.0 | 2.0 | 2.0 | 2(463) |
| DYJetsToLL.root | h4lTree | l4charge | 2 | -1.0 | 1.0 | -0.0755939524838013 | -1(249), 1(214) |
| DYJetsToLL.root | h4lTree | l4elCutBased | 5 | 0.0 | 4.0 | 0.6997840172786177 | 0(310), 1(67), 2(32), 3(23), 4(31) |
| DYJetsToLL.root | h4lTree | l4elMvaWP80 | 2 | 0.0 | 1.0 | 0.10151187904967603 | 0(416), 1(47) |
| DYJetsToLL.root | h4lTree | l4elMvaWP90 | 2 | 0.0 | 1.0 | 0.17062634989200864 | 0(384), 1(79) |
| DYJetsToLL.root | h4lTree | l4miniRelIso | 326 | 0.0 | 4.777987003326416 | 0.47845694422721863 | 0.0(138), 0.0036670395638793707(1), 0.0045366790145635605(1), 0.005148862022906542(1), 0.008184370584785938(1), 0.008730952627956867(1), 0.010784476064145565(1), 0.010859299451112747(1), 0.0116179920732975(1), 0.012260176241397858(1), 0.012581649236381054(1), 0.0159135852009058(1), ... |
| DYJetsToLL.root | h4lTree | l4muGlobal | 2 | 0.0 | 1.0 | 0.08855291576673865 | 0(422), 1(41) |
| DYJetsToLL.root | h4lTree | l4muMedium | 2 | 0.0 | 1.0 | 0.08423326133909287 | 0(424), 1(39) |
| DYJetsToLL.root | h4lTree | l4muPF | 2 | 0.0 | 1.0 | 0.09071274298056156 | 0(421), 1(42) |
| DYJetsToLL.root | h4lTree | l4muTight | 2 | 0.0 | 1.0 | 0.08423326133909287 | 0(424), 1(39) |
| DYJetsToLL.root | h4lTree | l4pdgId | 4 | -13.0 | 13.0 | 0.8488120950323974 | -13(19), -11(195), 11(226), 13(23) |
| DYJetsToLL.root | h4lTree | l4zId | 1 | 2.0 | 2.0 | 2.0 | 2(463) |
| DYJetsToLL.root | h4lTree | lumi | 462 | 144.0 | 99973.0 | 49635.06479481641 | 144(1), 217(1), 326(1), 421(1), 546(1), 558(1), 1117(1), 1213(1), 1378(1), 1422(1), 1504(1), 1610(1), ... |
| DYJetsToLL.root | h4lTree | nPV | 29 | 5.0 | 34.0 | 17.930885529157667 | 5(1), 6(2), 7(3), 8(10), 9(11), 10(17), 11(16), 12(14), 13(20), 14(34), 15(25), 16(37) |
| DYJetsToLL.root | h4lTree | pvNdof | 342 | 0.783203125 | 282.0 | 89.70538330078125 | 0.783203125(1), 5.25(1), 7.90625(1), 8.96875(1), 9.5625(1), 12.25(1), 13.125(1), 14.21875(1), 14.96875(1), 15.0(1), 15.28125(1), 15.375(1), ... |
| DYJetsToLL.root | h4lTree | run | 1 | 1.0 | 1.0 | 1.0 | 1(463) |
| DYJetsToLL.root | h4lTree | trigBits | 19 | 0.0 | 1585.0 | 177.93088552915768 | 0(53), 1(5), 3(145), 16(19), 32(41), 48(133), 259(10), 512(2), 544(1), 560(5), 1024(1), 1027(15) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GGZZ2E2Mu.root | Metadata | nEvents | 1 | 499000.0 | 499000.0 | 499000.0 | 499000(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GGZZ2E2Mu.root | h4lTree | event | 1000 | 257002.0 | 376999.0 | 352142.889 | 257002(1), 257006(1), 257007(1), 257009(1), 257010(1), 257011(1), 257012(1), 257014(1), 257018(1), 257019(1), 257026(1), 257027(1), ... |
| GGZZ2E2Mu.root | h4lTree | finalState | 2 | 1.0 | 2.0 | 1.999 | 1(1), 2(999) |
| GGZZ2E2Mu.root | h4lTree | l1charge | 2 | -1.0 | 1.0 | 0.076 | -1(462), 1(538) |
| GGZZ2E2Mu.root | h4lTree | l1elCutBased | 5 | 0.0 | 4.0 | 1.61 | 0(568), 1(7), 2(29), 3(39), 4(357) |
| GGZZ2E2Mu.root | h4lTree | l1elMvaWP80 | 2 | 0.0 | 1.0 | 0.36 | 0(640), 1(360) |
| GGZZ2E2Mu.root | h4lTree | l1elMvaWP90 | 2 | 0.0 | 1.0 | 0.413 | 0(587), 1(413) |
| GGZZ2E2Mu.root | h4lTree | l1miniRelIso | 317 | 0.0 | 1.1993787288665771 | 0.01034116093069315 | 0.0(684), 0.00030327291460707784(1), 0.00043069268576800823(1), 0.0005980747519060969(1), 0.0006836410611867905(1), 0.001066184719093144(1), 0.0011503981659188867(1), 0.0012887726770713925(1), 0.0019559445790946484(1), 0.0024547120556235313(1), 0.002456194721162319(1), 0.002495045308023691(1), ... |
| GGZZ2E2Mu.root | h4lTree | l1muGlobal | 2 | 0.0 | 1.0 | 0.547 | 0(453), 1(547) |
| GGZZ2E2Mu.root | h4lTree | l1muMedium | 2 | 0.0 | 1.0 | 0.547 | 0(453), 1(547) |
| GGZZ2E2Mu.root | h4lTree | l1muPF | 2 | 0.0 | 1.0 | 0.552 | 0(448), 1(552) |
| GGZZ2E2Mu.root | h4lTree | l1muTight | 2 | 0.0 | 1.0 | 0.539 | 0(461), 1(539) |
| GGZZ2E2Mu.root | h4lTree | l1pdgId | 4 | -13.0 | 13.0 | -0.912 | -13(295), -11(243), 11(205), 13(257) |
| GGZZ2E2Mu.root | h4lTree | l1zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ2E2Mu.root | h4lTree | l2charge | 2 | -1.0 | 1.0 | -0.076 | -1(538), 1(462) |
| GGZZ2E2Mu.root | h4lTree | l2elCutBased | 5 | 0.0 | 4.0 | 1.471 | 0(576), 1(28), 2(46), 3(49), 4(301) |
| GGZZ2E2Mu.root | h4lTree | l2elMvaWP80 | 2 | 0.0 | 1.0 | 0.344 | 0(656), 1(344) |
| GGZZ2E2Mu.root | h4lTree | l2elMvaWP90 | 2 | 0.0 | 1.0 | 0.401 | 0(599), 1(401) |
| GGZZ2E2Mu.root | h4lTree | l2miniRelIso | 378 | 0.0 | 1.569351077079773 | 0.024053677916526794 | 0.0(623), 0.0004314871912356466(1), 0.0008622162858955562(1), 0.001154250232502818(1), 0.0019835466518998146(1), 0.0020179220009595156(1), 0.002171098720282316(1), 0.002222234383225441(1), 0.002503430936485529(1), 0.0029626430477946997(1), 0.002972907852381468(1), 0.0037733595818281174(1), ... |
| GGZZ2E2Mu.root | h4lTree | l2muGlobal | 2 | 0.0 | 1.0 | 0.546 | 0(454), 1(546) |
| GGZZ2E2Mu.root | h4lTree | l2muMedium | 2 | 0.0 | 1.0 | 0.548 | 0(452), 1(548) |
| GGZZ2E2Mu.root | h4lTree | l2muPF | 2 | 0.0 | 1.0 | 0.552 | 0(448), 1(552) |
| GGZZ2E2Mu.root | h4lTree | l2muTight | 2 | 0.0 | 1.0 | 0.538 | 0(462), 1(538) |
| GGZZ2E2Mu.root | h4lTree | l2pdgId | 4 | -13.0 | 13.0 | 0.912 | -13(257), -11(205), 11(243), 13(295) |
| GGZZ2E2Mu.root | h4lTree | l2zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ2E2Mu.root | h4lTree | l3charge | 2 | -1.0 | 1.0 | -0.002 | -1(501), 1(499) |
| GGZZ2E2Mu.root | h4lTree | l3elCutBased | 5 | 0.0 | 4.0 | 1.906 | 0(473), 1(20), 2(45), 3(52), 4(410) |
| GGZZ2E2Mu.root | h4lTree | l3elMvaWP80 | 2 | 0.0 | 1.0 | 0.442 | 0(558), 1(442) |
| GGZZ2E2Mu.root | h4lTree | l3elMvaWP90 | 2 | 0.0 | 1.0 | 0.501 | 0(499), 1(501) |
| GGZZ2E2Mu.root | h4lTree | l3miniRelIso | 313 | 0.0 | 1.8319333791732788 | 0.015186404809355736 | 0.0(688), 0.0001340514572802931(1), 0.0005267488886602223(1), 0.0009982009651139379(1), 0.0011564070591703057(1), 0.0014073256170377135(1), 0.001429109019227326(1), 0.001434996142052114(1), 0.0014738434692844748(1), 0.0018218191107735038(1), 0.0018727662973105907(1), 0.002143809339031577(1), ... |
| GGZZ2E2Mu.root | h4lTree | l3muGlobal | 2 | 0.0 | 1.0 | 0.442 | 0(558), 1(442) |
| GGZZ2E2Mu.root | h4lTree | l3muMedium | 2 | 0.0 | 1.0 | 0.444 | 0(556), 1(444) |
| GGZZ2E2Mu.root | h4lTree | l3muPF | 2 | 0.0 | 1.0 | 0.447 | 0(553), 1(447) |
| GGZZ2E2Mu.root | h4lTree | l3muTight | 2 | 0.0 | 1.0 | 0.433 | 0(567), 1(433) |
| GGZZ2E2Mu.root | h4lTree | l3pdgId | 4 | -13.0 | 13.0 | -0.016 | -13(233), -11(266), 11(287), 13(214) |
| GGZZ2E2Mu.root | h4lTree | l3zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| GGZZ2E2Mu.root | h4lTree | l4charge | 2 | -1.0 | 1.0 | 0.002 | -1(499), 1(501) |
| GGZZ2E2Mu.root | h4lTree | l4elCutBased | 5 | 0.0 | 4.0 | 1.692 | 0(500), 1(39), 2(57), 3(77), 4(327) |
| GGZZ2E2Mu.root | h4lTree | l4elMvaWP80 | 2 | 0.0 | 1.0 | 0.389 | 0(611), 1(389) |
| GGZZ2E2Mu.root | h4lTree | l4elMvaWP90 | 2 | 0.0 | 1.0 | 0.477 | 0(523), 1(477) |
| GGZZ2E2Mu.root | h4lTree | l4miniRelIso | 423 | 0.0 | 1.0098072290420532 | 0.02987116202712059 | 0.0(578), 7.664875738555565e-05(1), 0.0007177283405326307(1), 0.0009410095517523587(1), 0.0011616802075877786(1), 0.0013699749251827598(1), 0.0016821571625769138(1), 0.0018865334568545222(1), 0.002218150068074465(1), 0.0023365234956145287(1), 0.002437188755720854(1), 0.0027046874165534973(1), ... |
| GGZZ2E2Mu.root | h4lTree | l4muGlobal | 2 | 0.0 | 1.0 | 0.44 | 0(560), 1(440) |
| GGZZ2E2Mu.root | h4lTree | l4muMedium | 2 | 0.0 | 1.0 | 0.443 | 0(557), 1(443) |
| GGZZ2E2Mu.root | h4lTree | l4muPF | 2 | 0.0 | 1.0 | 0.447 | 0(553), 1(447) |
| GGZZ2E2Mu.root | h4lTree | l4muTight | 2 | 0.0 | 1.0 | 0.437 | 0(563), 1(437) |
| GGZZ2E2Mu.root | h4lTree | l4pdgId | 4 | -13.0 | 13.0 | 0.016 | -13(214), -11(287), 11(266), 13(233) |
| GGZZ2E2Mu.root | h4lTree | l4zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| GGZZ2E2Mu.root | h4lTree | lumi | 3 | 258.0 | 377.0 | 352.661 | 258(45), 335(452), 377(503) |
| GGZZ2E2Mu.root | h4lTree | nPV | 35 | 4.0 | 38.0 | 17.606 | 4(2), 5(6), 6(11), 7(15), 8(21), 9(21), 10(33), 11(37), 12(56), 13(61), 14(71), 15(65) |
| GGZZ2E2Mu.root | h4lTree | pvNdof | 552 | 6.21875 | 255.5 | 82.14131164550781 | 6.21875(1), 7.40625(1), 9.4375(1), 11.0625(1), 11.3125(1), 11.625(1), 11.84375(1), 12.28125(1), 13.09375(1), 13.28125(1), 13.375(1), 13.71875(1), ... |
| GGZZ2E2Mu.root | h4lTree | run | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ2E2Mu.root | h4lTree | trigBits | 27 | 0.0 | 1843.0 | 1457.613 | 0(10), 3(18), 16(2), 17(1), 32(1), 48(5), 512(7), 528(3), 544(6), 547(1), 560(32), 1025(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GGZZ4E.root | Metadata | nEvents | 1 | 992608.0 | 992608.0 | 992608.0 | 992608(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GGZZ4E.root | h4lTree | event | 1000 | 1850.0 | 6029.0 | 4100.908 | 1850(1), 1851(1), 1856(1), 1857(1), 1858(1), 1861(1), 1864(1), 1872(1), 1873(1), 1874(1), 1877(1), 1879(1), ... |
| GGZZ4E.root | h4lTree | finalState | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ4E.root | h4lTree | l1charge | 2 | -1.0 | 1.0 | -0.018 | -1(509), 1(491) |
| GGZZ4E.root | h4lTree | l1elCutBased | 5 | 0.0 | 4.0 | 3.603 | 0(33), 1(20), 2(55), 3(95), 4(797) |
| GGZZ4E.root | h4lTree | l1elMvaWP80 | 2 | 0.0 | 1.0 | 0.792 | 0(208), 1(792) |
| GGZZ4E.root | h4lTree | l1elMvaWP90 | 2 | 0.0 | 1.0 | 0.91 | 0(90), 1(910) |
| GGZZ4E.root | h4lTree | l1miniRelIso | 339 | 0.0 | 1.58071768283844 | 0.013719305396080017 | 0.0(662), 0.00018133677076548338(1), 0.00019571934535633773(1), 0.0005227462970651686(1), 0.0005473658093251288(1), 0.0006411991198547184(1), 0.0006943971966393292(1), 0.0007747902418486774(1), 0.0008775403257459402(1), 0.0009898657444864511(1), 0.0010917637264356017(1), 0.001109114266000688(1), ... |
| GGZZ4E.root | h4lTree | l1muGlobal | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l1muMedium | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l1muPF | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l1muTight | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l1pdgId | 2 | -11.0 | 11.0 | 0.198 | -11(491), 11(509) |
| GGZZ4E.root | h4lTree | l1zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ4E.root | h4lTree | l2charge | 2 | -1.0 | 1.0 | 0.018 | -1(491), 1(509) |
| GGZZ4E.root | h4lTree | l2elCutBased | 5 | 0.0 | 4.0 | 3.264 | 0(62), 1(49), 2(119), 3(103), 4(667) |
| GGZZ4E.root | h4lTree | l2elMvaWP80 | 2 | 0.0 | 1.0 | 0.758 | 0(242), 1(758) |
| GGZZ4E.root | h4lTree | l2elMvaWP90 | 2 | 0.0 | 1.0 | 0.885 | 0(115), 1(885) |
| GGZZ4E.root | h4lTree | l2miniRelIso | 391 | 0.0 | 1.4816964864730835 | 0.026944132521748543 | 0.0(610), 2.997030969709158e-05(1), 9.004755702335387e-05(1), 9.044836042448878e-05(1), 0.0005379098001867533(1), 0.0006412737420760095(1), 0.0013045400846749544(1), 0.001585913123562932(1), 0.00171239348128438(1), 0.0020205313339829445(1), 0.0021370560862123966(1), 0.0021585854701697826(1), ... |
| GGZZ4E.root | h4lTree | l2muGlobal | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l2muMedium | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l2muPF | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l2muTight | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l2pdgId | 2 | -11.0 | 11.0 | -0.198 | -11(509), 11(491) |
| GGZZ4E.root | h4lTree | l2zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ4E.root | h4lTree | l3charge | 2 | -1.0 | 1.0 | -0.05 | -1(525), 1(475) |
| GGZZ4E.root | h4lTree | l3elCutBased | 5 | 0.0 | 4.0 | 3.417 | 0(63), 1(30), 2(76), 3(89), 4(742) |
| GGZZ4E.root | h4lTree | l3elMvaWP80 | 2 | 0.0 | 1.0 | 0.762 | 0(238), 1(762) |
| GGZZ4E.root | h4lTree | l3elMvaWP90 | 2 | 0.0 | 1.0 | 0.895 | 0(105), 1(895) |
| GGZZ4E.root | h4lTree | l3miniRelIso | 346 | 0.0 | 1.0915106534957886 | 0.021242965012788773 | 0.0(655), 0.00016410902026109397(1), 0.00023141254496295005(1), 0.00024031041539274156(1), 0.00024251002469100058(1), 0.00025952301803044975(1), 0.0006141785997897387(1), 0.0012072761310264468(1), 0.001246259082108736(1), 0.0012576398439705372(1), 0.0012970173265784979(1), 0.0014781779609620571(1), ... |
| GGZZ4E.root | h4lTree | l3muGlobal | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l3muMedium | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l3muPF | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l3muTight | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l3pdgId | 2 | -11.0 | 11.0 | 0.55 | -11(475), 11(525) |
| GGZZ4E.root | h4lTree | l3zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| GGZZ4E.root | h4lTree | l4charge | 2 | -1.0 | 1.0 | 0.05 | -1(475), 1(525) |
| GGZZ4E.root | h4lTree | l4elCutBased | 5 | 0.0 | 4.0 | 3.121 | 0(82), 1(61), 2(111), 3(146), 4(600) |
| GGZZ4E.root | h4lTree | l4elMvaWP80 | 2 | 0.0 | 1.0 | 0.731 | 0(269), 1(731) |
| GGZZ4E.root | h4lTree | l4elMvaWP90 | 2 | 0.0 | 1.0 | 0.867 | 0(133), 1(867) |
| GGZZ4E.root | h4lTree | l4miniRelIso | 398 | 0.0 | 1.3904505968093872 | 0.03327486291527748 | 0.0(603), 1.1030755558749661e-05(1), 0.0001065719552570954(1), 0.0006611080025322735(1), 0.0008085421868599951(1), 0.0008105856250040233(1), 0.0009119045571424067(1), 0.0010252442443743348(1), 0.0013557826168835163(1), 0.0015312314499169588(1), 0.0018634613370522857(1), 0.0020328969694674015(1), ... |
| GGZZ4E.root | h4lTree | l4muGlobal | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l4muMedium | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l4muPF | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l4muTight | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4E.root | h4lTree | l4pdgId | 2 | -11.0 | 11.0 | -0.55 | -11(525), 11(475) |
| GGZZ4E.root | h4lTree | l4zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| GGZZ4E.root | h4lTree | lumi | 3 | 3.0 | 7.0 | 4.982 | 3(409), 6(382), 7(209) |
| GGZZ4E.root | h4lTree | nPV | 40 | 3.0 | 45.0 | 17.651 | 3(1), 4(4), 5(6), 6(6), 7(10), 8(22), 9(24), 10(39), 11(39), 12(51), 13(42), 14(67) |
| GGZZ4E.root | h4lTree | pvNdof | 554 | 0.232421875 | 222.0 | 79.79076385498047 | 0.232421875(1), 3.78125(1), 6.328125(1), 6.71875(1), 7.546875(1), 8.96875(1), 9.5(2), 10.03125(1), 10.21875(1), 10.3125(1), 10.6875(1), 11.875(1), ... |
| GGZZ4E.root | h4lTree | run | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ4E.root | h4lTree | trigBits | 5 | 0.0 | 560.0 | 46.832 | 0(13), 16(6), 32(54), 48(926), 560(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GGZZ4Mu.root | Metadata | nEvents | 1 | 997445.0 | 997445.0 | 997445.0 | 997445(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GGZZ4Mu.root | h4lTree | event | 1000 | 1.0 | 19890.0 | 2428.667 | 1(1), 2(1), 6(1), 7(1), 8(1), 9(1), 11(1), 13(1), 14(1), 16(1), 17(1), 20(1), ... |
| GGZZ4Mu.root | h4lTree | finalState | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4Mu.root | h4lTree | l1charge | 2 | -1.0 | 1.0 | 0.042 | -1(479), 1(521) |
| GGZZ4Mu.root | h4lTree | l1elCutBased | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4Mu.root | h4lTree | l1elMvaWP80 | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4Mu.root | h4lTree | l1elMvaWP90 | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4Mu.root | h4lTree | l1miniRelIso | 301 | 0.0 | 0.25672611594200134 | 0.008525430224835873 | 0.0(700), 0.0021835085935890675(1), 0.0025019359309226274(1), 0.002574673853814602(1), 0.0030227319803088903(1), 0.003245364874601364(1), 0.003473734948784113(1), 0.003491543233394623(1), 0.00366017478518188(1), 0.0037702862173318863(1), 0.0037753779906779528(1), 0.003824717365205288(1), ... |
| GGZZ4Mu.root | h4lTree | l1muGlobal | 2 | 0.0 | 1.0 | 0.993 | 0(7), 1(993) |
| GGZZ4Mu.root | h4lTree | l1muMedium | 2 | 0.0 | 1.0 | 0.992 | 0(8), 1(992) |
| GGZZ4Mu.root | h4lTree | l1muPF | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ4Mu.root | h4lTree | l1muTight | 2 | 0.0 | 1.0 | 0.981 | 0(19), 1(981) |
| GGZZ4Mu.root | h4lTree | l1pdgId | 2 | -13.0 | 13.0 | -0.546 | -13(521), 13(479) |
| GGZZ4Mu.root | h4lTree | l1zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ4Mu.root | h4lTree | l2charge | 2 | -1.0 | 1.0 | -0.042 | -1(521), 1(479) |
| GGZZ4Mu.root | h4lTree | l2elCutBased | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4Mu.root | h4lTree | l2elMvaWP80 | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4Mu.root | h4lTree | l2elMvaWP90 | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4Mu.root | h4lTree | l2miniRelIso | 425 | 0.0 | 0.43683570623397827 | 0.01836390234529972 | 0.0(576), 0.0003572184359654784(1), 0.0008984066080302(1), 0.0011017181677743793(1), 0.0012698310893028975(1), 0.0015038354322314262(1), 0.0017019022488966584(1), 0.0019526410615071654(1), 0.002875184640288353(1), 0.002907551359385252(1), 0.0030546209309250116(1), 0.0033485840540379286(1), ... |
| GGZZ4Mu.root | h4lTree | l2muGlobal | 2 | 0.0 | 1.0 | 0.99 | 0(10), 1(990) |
| GGZZ4Mu.root | h4lTree | l2muMedium | 2 | 0.0 | 1.0 | 0.996 | 0(4), 1(996) |
| GGZZ4Mu.root | h4lTree | l2muPF | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ4Mu.root | h4lTree | l2muTight | 2 | 0.0 | 1.0 | 0.978 | 0(22), 1(978) |
| GGZZ4Mu.root | h4lTree | l2pdgId | 2 | -13.0 | 13.0 | 0.546 | -13(479), 13(521) |
| GGZZ4Mu.root | h4lTree | l2zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ4Mu.root | h4lTree | l3charge | 2 | -1.0 | 1.0 | 0.002 | -1(499), 1(501) |
| GGZZ4Mu.root | h4lTree | l3elCutBased | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4Mu.root | h4lTree | l3elMvaWP80 | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4Mu.root | h4lTree | l3elMvaWP90 | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4Mu.root | h4lTree | l3miniRelIso | 301 | 0.0 | 0.3427743911743164 | 0.010111935436725616 | 0.0(700), 0.0014435185585170984(1), 0.0017126207239925861(1), 0.0020968515891581774(1), 0.0032649708446115255(1), 0.003436938626691699(1), 0.0034499657340347767(1), 0.00346194370649755(1), 0.0035853395238518715(1), 0.003910785540938377(1), 0.003932384308427572(1), 0.004099256359040737(1), ... |
| GGZZ4Mu.root | h4lTree | l3muGlobal | 2 | 0.0 | 1.0 | 0.99 | 0(10), 1(990) |
| GGZZ4Mu.root | h4lTree | l3muMedium | 2 | 0.0 | 1.0 | 0.992 | 0(8), 1(992) |
| GGZZ4Mu.root | h4lTree | l3muPF | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ4Mu.root | h4lTree | l3muTight | 2 | 0.0 | 1.0 | 0.972 | 0(28), 1(972) |
| GGZZ4Mu.root | h4lTree | l3pdgId | 2 | -13.0 | 13.0 | -0.026 | -13(501), 13(499) |
| GGZZ4Mu.root | h4lTree | l3zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| GGZZ4Mu.root | h4lTree | l4charge | 2 | -1.0 | 1.0 | -0.002 | -1(501), 1(499) |
| GGZZ4Mu.root | h4lTree | l4elCutBased | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4Mu.root | h4lTree | l4elMvaWP80 | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4Mu.root | h4lTree | l4elMvaWP90 | 1 | 0.0 | 0.0 | 0.0 | 0(1000) |
| GGZZ4Mu.root | h4lTree | l4miniRelIso | 393 | 0.0 | 0.7985641360282898 | 0.02242426760494709 | 0.0(608), 0.00017839064821600914(1), 0.000665661005768925(1), 0.0008032854530028999(1), 0.0008684914209879935(1), 0.0009455629042349756(1), 0.0014294293941929936(1), 0.0015370051842182875(1), 0.002606909489259124(1), 0.0029812767170369625(1), 0.003131644334644079(1), 0.0032669890206307173(1), ... |
| GGZZ4Mu.root | h4lTree | l4muGlobal | 2 | 0.0 | 1.0 | 0.99 | 0(10), 1(990) |
| GGZZ4Mu.root | h4lTree | l4muMedium | 2 | 0.0 | 1.0 | 0.994 | 0(6), 1(994) |
| GGZZ4Mu.root | h4lTree | l4muPF | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ4Mu.root | h4lTree | l4muTight | 2 | 0.0 | 1.0 | 0.976 | 0(24), 1(976) |
| GGZZ4Mu.root | h4lTree | l4pdgId | 2 | -13.0 | 13.0 | 0.026 | -13(499), 13(501) |
| GGZZ4Mu.root | h4lTree | l4zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| GGZZ4Mu.root | h4lTree | lumi | 4 | 1.0 | 38.0 | 5.045 | 1(315), 3(330), 8(325), 38(30) |
| GGZZ4Mu.root | h4lTree | nPV | 35 | 4.0 | 43.0 | 17.441 | 4(5), 5(7), 6(13), 7(16), 8(15), 9(24), 10(30), 11(42), 12(51), 13(66), 14(62), 15(60) |
| GGZZ4Mu.root | h4lTree | pvNdof | 533 | 3.5 | 218.0 | 85.09590911865234 | 3.5(1), 6.5(1), 10.65625(1), 11.78125(1), 13.59375(1), 13.75(1), 14.0625(1), 14.9375(1), 15.375(1), 16.5625(1), 17.0(1), 17.125(2), ... |
| GGZZ4Mu.root | h4lTree | run | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GGZZ4Mu.root | h4lTree | trigBits | 7 | 3.0 | 1811.0 | 265.857 | 3(5), 256(21), 257(12), 259(956), 1283(2), 1795(2), 1811(2) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GluGluToHToZZ.root | Metadata | nEvents | 1 | 983914.0 | 983914.0 | 983914.0 | 983914(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GluGluToHToZZ.root | h4lTree | event | 1000 | 69486.0 | 2999599.0 | 2131777.116 | 69486(1), 69487(1), 69489(1), 69521(1), 69526(1), 69530(1), 69563(1), 69577(1), 69583(1), 69593(1), 69596(1), 69606(1), ... |
| GluGluToHToZZ.root | h4lTree | finalState | 3 | 0.0 | 2.0 | 1.125 | 0(344), 1(187), 2(469) |
| GluGluToHToZZ.root | h4lTree | l1charge | 2 | -1.0 | 1.0 | -0.004 | -1(502), 1(498) |
| GluGluToHToZZ.root | h4lTree | l1elCutBased | 5 | 0.0 | 4.0 | 1.6 | 0(562), 1(13), 2(29), 3(55), 4(341) |
| GluGluToHToZZ.root | h4lTree | l1elMvaWP80 | 2 | 0.0 | 1.0 | 0.365 | 0(635), 1(365) |
| GluGluToHToZZ.root | h4lTree | l1elMvaWP90 | 2 | 0.0 | 1.0 | 0.42 | 0(580), 1(420) |
| GluGluToHToZZ.root | h4lTree | l1miniRelIso | 407 | 0.0 | 1.0425225496292114 | 0.015881875529885292 | 0.0(594), 0.00017429077706765383(1), 0.00021857563115190715(1), 0.0005152184166945517(1), 0.000537639600224793(1), 0.0007052237051539123(1), 0.0007374825072474778(1), 0.000800493115093559(1), 0.0008082081330940127(1), 0.0012617642059922218(1), 0.0017012613825500011(1), 0.001843778882175684(1), ... |
| GluGluToHToZZ.root | h4lTree | l1muGlobal | 2 | 0.0 | 1.0 | 0.54 | 0(460), 1(540) |
| GluGluToHToZZ.root | h4lTree | l1muMedium | 2 | 0.0 | 1.0 | 0.544 | 0(456), 1(544) |
| GluGluToHToZZ.root | h4lTree | l1muPF | 2 | 0.0 | 1.0 | 0.545 | 0(455), 1(545) |
| GluGluToHToZZ.root | h4lTree | l1muTight | 2 | 0.0 | 1.0 | 0.533 | 0(467), 1(533) |
| GluGluToHToZZ.root | h4lTree | l1pdgId | 4 | -13.0 | 13.0 | 0.096 | -13(260), -11(238), 11(216), 13(286) |
| GluGluToHToZZ.root | h4lTree | l1zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GluGluToHToZZ.root | h4lTree | l2charge | 2 | -1.0 | 1.0 | 0.004 | -1(498), 1(502) |
| GluGluToHToZZ.root | h4lTree | l2elCutBased | 5 | 0.0 | 4.0 | 1.442 | 0(575), 1(35), 2(46), 3(61), 4(283) |
| GluGluToHToZZ.root | h4lTree | l2elMvaWP80 | 2 | 0.0 | 1.0 | 0.345 | 0(655), 1(345) |
| GluGluToHToZZ.root | h4lTree | l2elMvaWP90 | 2 | 0.0 | 1.0 | 0.398 | 0(602), 1(398) |
| GluGluToHToZZ.root | h4lTree | l2miniRelIso | 412 | 0.0 | 1.2752366065979004 | 0.02267560362815857 | 0.0(589), 0.00034000500454567373(1), 0.0004276407416909933(1), 0.0012164647923782468(1), 0.0013134408509358764(1), 0.0016608679434284568(1), 0.0017290567047894(1), 0.0017710609827190638(1), 0.0019834008999168873(1), 0.0025265542790293694(1), 0.0028335019014775753(1), 0.0029599713161587715(1), ... |
| GluGluToHToZZ.root | h4lTree | l2muGlobal | 2 | 0.0 | 1.0 | 0.543 | 0(457), 1(543) |
| GluGluToHToZZ.root | h4lTree | l2muMedium | 2 | 0.0 | 1.0 | 0.539 | 0(461), 1(539) |
| GluGluToHToZZ.root | h4lTree | l2muPF | 2 | 0.0 | 1.0 | 0.546 | 0(454), 1(546) |
| GluGluToHToZZ.root | h4lTree | l2muTight | 2 | 0.0 | 1.0 | 0.534 | 0(466), 1(534) |
| GluGluToHToZZ.root | h4lTree | l2pdgId | 4 | -13.0 | 13.0 | -0.096 | -13(286), -11(216), 11(238), 13(260) |
| GluGluToHToZZ.root | h4lTree | l2zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GluGluToHToZZ.root | h4lTree | l3charge | 2 | -1.0 | 1.0 | 0.008 | -1(496), 1(504) |
| GluGluToHToZZ.root | h4lTree | l3elCutBased | 5 | 0.0 | 4.0 | 1.196 | 0(640), 1(37), 2(51), 3(31), 4(241) |
| GluGluToHToZZ.root | h4lTree | l3elMvaWP80 | 2 | 0.0 | 1.0 | 0.288 | 0(712), 1(288) |
| GluGluToHToZZ.root | h4lTree | l3elMvaWP90 | 2 | 0.0 | 1.0 | 0.341 | 0(659), 1(341) |
| GluGluToHToZZ.root | h4lTree | l3miniRelIso | 435 | 0.0 | 1.3401470184326172 | 0.030994657427072525 | 0.0(566), 0.00021519868460018188(1), 0.00025526955141685903(1), 0.0005397700588218868(1), 0.0007181533728726208(1), 0.0007844035280868411(1), 0.0008999740239232779(1), 0.000957658514380455(1), 0.0009719188674353063(1), 0.0009789122268557549(1), 0.0013840519823133945(1), 0.002051980933174491(1), ... |
| GluGluToHToZZ.root | h4lTree | l3muGlobal | 2 | 0.0 | 1.0 | 0.604 | 0(396), 1(604) |
| GluGluToHToZZ.root | h4lTree | l3muMedium | 2 | 0.0 | 1.0 | 0.608 | 0(392), 1(608) |
| GluGluToHToZZ.root | h4lTree | l3muPF | 2 | 0.0 | 1.0 | 0.611 | 0(389), 1(611) |
| GluGluToHToZZ.root | h4lTree | l3muTight | 2 | 0.0 | 1.0 | 0.596 | 0(404), 1(596) |
| GluGluToHToZZ.root | h4lTree | l3pdgId | 4 | -13.0 | 13.0 | -0.094 | -13(307), -11(197), 11(192), 13(304) |
| GluGluToHToZZ.root | h4lTree | l3zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| GluGluToHToZZ.root | h4lTree | l4charge | 2 | -1.0 | 1.0 | -0.008 | -1(504), 1(496) |
| GluGluToHToZZ.root | h4lTree | l4elCutBased | 5 | 0.0 | 4.0 | 0.91 | 0(673), 1(66), 2(69), 3(62), 4(130) |
| GluGluToHToZZ.root | h4lTree | l4elMvaWP80 | 2 | 0.0 | 1.0 | 0.255 | 0(745), 1(255) |
| GluGluToHToZZ.root | h4lTree | l4elMvaWP90 | 2 | 0.0 | 1.0 | 0.334 | 0(666), 1(334) |
| GluGluToHToZZ.root | h4lTree | l4miniRelIso | 441 | 0.0 | 1.2912787199020386 | 0.04579656943678856 | 0.0(560), 0.0006785807781852782(1), 0.0011064658174291253(1), 0.001401155604980886(1), 0.0016757519915699959(1), 0.002206476405262947(1), 0.0035131836775690317(1), 0.0050933705642819405(1), 0.005242927465587854(1), 0.005379273556172848(1), 0.006025765091180801(1), 0.006243257783353329(1), ... |
| GluGluToHToZZ.root | h4lTree | l4muGlobal | 2 | 0.0 | 1.0 | 0.605 | 0(395), 1(605) |
| GluGluToHToZZ.root | h4lTree | l4muMedium | 2 | 0.0 | 1.0 | 0.6 | 0(400), 1(600) |
| GluGluToHToZZ.root | h4lTree | l4muPF | 2 | 0.0 | 1.0 | 0.61 | 0(390), 1(610) |
| GluGluToHToZZ.root | h4lTree | l4muTight | 2 | 0.0 | 1.0 | 0.593 | 0(407), 1(593) |
| GluGluToHToZZ.root | h4lTree | l4pdgId | 4 | -13.0 | 13.0 | 0.094 | -13(304), -11(192), 11(197), 13(307) |
| GluGluToHToZZ.root | h4lTree | l4zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| GluGluToHToZZ.root | h4lTree | lumi | 19 | 181.0 | 7771.0 | 5523.247 | 181(53), 281(59), 368(49), 406(39), 6157(59), 6197(50), 6215(63), 6233(58), 6369(51), 6445(47), 6789(59), 6950(53) |
| GluGluToHToZZ.root | h4lTree | nPV | 53 | 3.0 | 65.0 | 26.495 | 3(1), 6(1), 8(2), 10(5), 11(12), 12(15), 13(18), 14(9), 15(21), 16(32), 17(35), 18(35), ... |
| GluGluToHToZZ.root | h4lTree | pvNdof | 516 | 10.71875 | 254.5 | 96.24362182617188 | 10.71875(1), 11.4375(1), 13.15625(1), 13.21875(1), 15.21875(1), 16.75(2), 17.75(1), 18.1875(1), 19.1875(1), 20.25(1), 21.375(2), 21.4375(1), ... |
| GluGluToHToZZ.root | h4lTree | run | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| GluGluToHToZZ.root | h4lTree | trigBits | 78 | 0.0 | 1935.0 | 593.445 | 0(15), 3(3), 12(2), 15(21), 16(3), 32(36), 48(148), 51(1), 76(1), 128(1), 140(3), 143(13), ... |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TTBar.root | Metadata | nEvents | 1 | 14776503.0 | 14776503.0 | 14776503.0 | 14776503(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TTBar.root | h4lTree | event | 639 | 91568.0 | 55078327.0 | 29261363.738654148 | 91568(1), 199217(1), 228059(1), 478770(1), 517758(1), 561997(1), 579646(1), 747076(1), 874402(1), 939799(1), 976803(1), 977281(1), ... |
| TTBar.root | h4lTree | finalState | 3 | 0.0 | 2.0 | 1.4960876369327074 | 0(26), 1(270), 2(343) |
| TTBar.root | h4lTree | l1charge | 2 | -1.0 | 1.0 | 0.051643192488262914 | -1(303), 1(336) |
| TTBar.root | h4lTree | l1elCutBased | 5 | 0.0 | 4.0 | 1.3317683881064162 | 0(386), 1(28), 2(27), 3(23), 4(175) |
| TTBar.root | h4lTree | l1elMvaWP80 | 2 | 0.0 | 1.0 | 0.28482003129890454 | 0(457), 1(182) |
| TTBar.root | h4lTree | l1elMvaWP90 | 2 | 0.0 | 1.0 | 0.3458528951486698 | 0(418), 1(221) |
| TTBar.root | h4lTree | l1miniRelIso | 354 | 0.0 | 3.6127068996429443 | 0.19498896598815918 | 0.0(286), 0.0007278723060153425(1), 0.0011847249697893858(1), 0.0012989850947633386(1), 0.0017539270920678973(1), 0.0017705535283312201(1), 0.002397107193246484(1), 0.003021713811904192(1), 0.003780943341553211(1), 0.0042635053396224976(1), 0.004392605274915695(1), 0.004436100833117962(1), ... |
| TTBar.root | h4lTree | l1muGlobal | 2 | 0.0 | 1.0 | 0.3302034428794992 | 0(428), 1(211) |
| TTBar.root | h4lTree | l1muMedium | 2 | 0.0 | 1.0 | 0.3302034428794992 | 0(428), 1(211) |
| TTBar.root | h4lTree | l1muPF | 2 | 0.0 | 1.0 | 0.3317683881064163 | 0(427), 1(212) |
| TTBar.root | h4lTree | l1muTight | 2 | 0.0 | 1.0 | 0.325508607198748 | 0(431), 1(208) |
| TTBar.root | h4lTree | l1pdgId | 4 | -13.0 | 13.0 | -0.5805946791862285 | -13(109), -11(227), 11(198), 13(105) |
| TTBar.root | h4lTree | l1zId | 1 | 1.0 | 1.0 | 1.0 | 1(639) |
| TTBar.root | h4lTree | l2charge | 2 | -1.0 | 1.0 | -0.051643192488262914 | -1(336), 1(303) |
| TTBar.root | h4lTree | l2elCutBased | 5 | 0.0 | 4.0 | 1.0938967136150235 | 0(401), 1(43), 2(45), 3(34), 4(116) |
| TTBar.root | h4lTree | l2elMvaWP80 | 2 | 0.0 | 1.0 | 0.24100156494522693 | 0(485), 1(154) |
| TTBar.root | h4lTree | l2elMvaWP90 | 2 | 0.0 | 1.0 | 0.297339593114241 | 0(449), 1(190) |
| TTBar.root | h4lTree | l2miniRelIso | 392 | 0.0 | 6.042660236358643 | 0.22620923817157745 | 0.0(248), 0.001126431510783732(1), 0.0014644801849499345(1), 0.001624410506337881(1), 0.0017494743224233389(1), 0.0024642152711749077(1), 0.0025970640126615763(1), 0.004088735673576593(1), 0.004128354601562023(1), 0.0049990443512797356(1), 0.005079634487628937(1), 0.005092996172606945(1), ... |
| TTBar.root | h4lTree | l2muGlobal | 2 | 0.0 | 1.0 | 0.3333333333333333 | 0(426), 1(213) |
| TTBar.root | h4lTree | l2muMedium | 2 | 0.0 | 1.0 | 0.3302034428794992 | 0(428), 1(211) |
| TTBar.root | h4lTree | l2muPF | 2 | 0.0 | 1.0 | 0.3333333333333333 | 0(426), 1(213) |
| TTBar.root | h4lTree | l2muTight | 2 | 0.0 | 1.0 | 0.3286384976525822 | 0(429), 1(210) |
| TTBar.root | h4lTree | l2pdgId | 4 | -13.0 | 13.0 | 0.5805946791862285 | -13(105), -11(198), 11(227), 13(109) |
| TTBar.root | h4lTree | l2zId | 1 | 1.0 | 1.0 | 1.0 | 1(639) |
| TTBar.root | h4lTree | l3charge | 2 | -1.0 | 1.0 | 0.02034428794992175 | -1(313), 1(326) |
| TTBar.root | h4lTree | l3elCutBased | 5 | 0.0 | 4.0 | 1.0109546165884193 | 0(423), 1(38), 2(43), 3(18), 4(117) |
| TTBar.root | h4lTree | l3elMvaWP80 | 2 | 0.0 | 1.0 | 0.20970266040688576 | 0(505), 1(134) |
| TTBar.root | h4lTree | l3elMvaWP90 | 2 | 0.0 | 1.0 | 0.27230046948356806 | 0(465), 1(174) |
| TTBar.root | h4lTree | l3miniRelIso | 383 | 0.0 | 3.9855244159698486 | 0.24418877065181732 | 0.0(257), 0.0010403604246675968(1), 0.0015876776305958629(1), 0.002950010122731328(1), 0.003820904763415456(1), 0.004101442638784647(1), 0.004399629309773445(1), 0.0044213226065039635(1), 0.004426846746355295(1), 0.005164770875126123(1), 0.005613362416625023(1), 0.0057199751026928425(1), ... |
| TTBar.root | h4lTree | l3muGlobal | 2 | 0.0 | 1.0 | 0.28012519561815336 | 0(460), 1(179) |
| TTBar.root | h4lTree | l3muMedium | 2 | 0.0 | 1.0 | 0.27856025039123633 | 0(461), 1(178) |
| TTBar.root | h4lTree | l3muPF | 2 | 0.0 | 1.0 | 0.28169014084507044 | 0(459), 1(180) |
| TTBar.root | h4lTree | l3muTight | 2 | 0.0 | 1.0 | 0.27543035993740217 | 0(463), 1(176) |
| TTBar.root | h4lTree | l3pdgId | 4 | -13.0 | 13.0 | -0.2269170579029734 | -13(91), -11(235), 11(223), 13(90) |
| TTBar.root | h4lTree | l3zId | 1 | 2.0 | 2.0 | 2.0 | 2(639) |
| TTBar.root | h4lTree | l4charge | 2 | -1.0 | 1.0 | -0.02034428794992175 | -1(326), 1(313) |
| TTBar.root | h4lTree | l4elCutBased | 5 | 0.0 | 4.0 | 0.7449139280125195 | 0(431), 1(80), 2(43), 3(30), 4(55) |
| TTBar.root | h4lTree | l4elMvaWP80 | 2 | 0.0 | 1.0 | 0.16588419405320814 | 0(533), 1(106) |
| TTBar.root | h4lTree | l4elMvaWP90 | 2 | 0.0 | 1.0 | 0.23943661971830985 | 0(486), 1(153) |
| TTBar.root | h4lTree | l4miniRelIso | 417 | 0.0 | 5.330708026885986 | 0.3102635145187378 | 0.0(223), 0.0009077267604880035(1), 0.0009565864456817508(1), 0.0014102585846558213(1), 0.002545445691794157(1), 0.0038690383080393076(1), 0.00394904799759388(1), 0.004960822407156229(1), 0.006008895579725504(1), 0.006189503241330385(1), 0.006539104972034693(1), 0.006622321903705597(1), ... |
| TTBar.root | h4lTree | l4muGlobal | 2 | 0.0 | 1.0 | 0.27856025039123633 | 0(461), 1(178) |
| TTBar.root | h4lTree | l4muMedium | 2 | 0.0 | 1.0 | 0.27543035993740217 | 0(463), 1(176) |
| TTBar.root | h4lTree | l4muPF | 2 | 0.0 | 1.0 | 0.28169014084507044 | 0(459), 1(180) |
| TTBar.root | h4lTree | l4muTight | 2 | 0.0 | 1.0 | 0.27230046948356806 | 0(465), 1(174) |
| TTBar.root | h4lTree | l4pdgId | 4 | -13.0 | 13.0 | 0.2269170579029734 | -13(90), -11(223), 11(235), 13(91) |
| TTBar.root | h4lTree | l4zId | 1 | 2.0 | 2.0 | 2.0 | 2(639) |
| TTBar.root | h4lTree | lumi | 620 | 29.0 | 17005.0 | 9034.560250391236 | 29(1), 62(1), 71(1), 148(1), 160(1), 174(1), 179(1), 231(1), 270(1), 291(1), 302(2), 342(1), ... |
| TTBar.root | h4lTree | nPV | 35 | 2.0 | 38.0 | 18.156494522691705 | 2(1), 3(1), 5(2), 6(4), 7(4), 8(9), 9(18), 10(14), 11(31), 12(25), 13(47), 14(30) |
| TTBar.root | h4lTree | pvNdof | 405 | 0.2958984375 | 260.0 | 96.08527374267578 | 0.2958984375(1), 0.59765625(1), 0.767578125(1), 0.79296875(1), 1.75(1), 2.90625(1), 3.5(1), 3.8359375(1), 4.265625(1), 4.359375(1), 5.0(1), 5.890625(1), ... |
| TTBar.root | h4lTree | run | 1 | 1.0 | 1.0 | 1.0 | 1(639) |
| TTBar.root | h4lTree | trigBits | 32 | 0.0 | 1843.0 | 428.1001564945227 | 0(56), 1(4), 3(100), 16(32), 32(55), 35(1), 48(148), 256(8), 257(1), 259(46), 512(6), 528(4) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VBF_HToZZ.root | Metadata | nEvents | 1 | 498000.0 | 498000.0 | 498000.0 | 498000(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VBF_HToZZ.root | h4lTree | event | 1000 | 90001.0 | 187985.0 | 147431.898 | 90001(1), 90009(1), 90013(1), 90015(1), 90024(1), 90032(1), 90036(1), 90038(1), 90042(1), 90043(1), 90045(1), 90049(1), ... |
| VBF_HToZZ.root | h4lTree | finalState | 3 | 0.0 | 2.0 | 1.129 | 0(328), 1(215), 2(457) |
| VBF_HToZZ.root | h4lTree | l1charge | 2 | -1.0 | 1.0 | -0.008 | -1(504), 1(496) |
| VBF_HToZZ.root | h4lTree | l1elCutBased | 5 | 0.0 | 4.0 | 1.657 | 0(552), 1(13), 2(26), 3(44), 4(365) |
| VBF_HToZZ.root | h4lTree | l1elMvaWP80 | 2 | 0.0 | 1.0 | 0.368 | 0(632), 1(368) |
| VBF_HToZZ.root | h4lTree | l1elMvaWP90 | 2 | 0.0 | 1.0 | 0.422 | 0(578), 1(422) |
| VBF_HToZZ.root | h4lTree | l1miniRelIso | 321 | 0.0 | 0.9967155456542969 | 0.010537072084844112 | 0.0(680), 2.471783045621123e-05(1), 3.57103199348785e-05(1), 0.00011691906547639519(1), 0.00021622928034048527(1), 0.00029804036603309214(1), 0.00032964744605123997(1), 0.00042058833059854805(1), 0.0006081322790123522(1), 0.001131600234657526(1), 0.0012426639441400766(1), 0.0016543845413252711(1), ... |
| VBF_HToZZ.root | h4lTree | l1muGlobal | 2 | 0.0 | 1.0 | 0.529 | 0(471), 1(529) |
| VBF_HToZZ.root | h4lTree | l1muMedium | 2 | 0.0 | 1.0 | 0.53 | 0(470), 1(530) |
| VBF_HToZZ.root | h4lTree | l1muPF | 2 | 0.0 | 1.0 | 0.535 | 0(465), 1(535) |
| VBF_HToZZ.root | h4lTree | l1muTight | 2 | 0.0 | 1.0 | 0.521 | 0(479), 1(521) |
| VBF_HToZZ.root | h4lTree | l1pdgId | 4 | -13.0 | 13.0 | 0.066 | -13(273), -11(223), 11(242), 13(262) |
| VBF_HToZZ.root | h4lTree | l1zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| VBF_HToZZ.root | h4lTree | l2charge | 2 | -1.0 | 1.0 | 0.008 | -1(496), 1(504) |
| VBF_HToZZ.root | h4lTree | l2elCutBased | 5 | 0.0 | 4.0 | 1.551 | 0(558), 1(21), 2(54), 3(46), 4(321) |
| VBF_HToZZ.root | h4lTree | l2elMvaWP80 | 2 | 0.0 | 1.0 | 0.346 | 0(654), 1(346) |
| VBF_HToZZ.root | h4lTree | l2elMvaWP90 | 2 | 0.0 | 1.0 | 0.404 | 0(596), 1(404) |
| VBF_HToZZ.root | h4lTree | l2miniRelIso | 390 | 0.0 | 1.527430772781372 | 0.022093767300248146 | 0.0(611), 0.00011569239723030478(1), 0.000622621038928628(1), 0.0006951203104108572(1), 0.001482914900407195(1), 0.0017450513551011682(1), 0.0019210345344617963(1), 0.0020151962526142597(1), 0.002022662665694952(1), 0.002215008018538356(1), 0.0024034336674958467(1), 0.0024766470305621624(1), ... |
| VBF_HToZZ.root | h4lTree | l2muGlobal | 2 | 0.0 | 1.0 | 0.527 | 0(473), 1(527) |
| VBF_HToZZ.root | h4lTree | l2muMedium | 2 | 0.0 | 1.0 | 0.531 | 0(469), 1(531) |
| VBF_HToZZ.root | h4lTree | l2muPF | 2 | 0.0 | 1.0 | 0.535 | 0(465), 1(535) |
| VBF_HToZZ.root | h4lTree | l2muTight | 2 | 0.0 | 1.0 | 0.518 | 0(482), 1(518) |
| VBF_HToZZ.root | h4lTree | l2pdgId | 4 | -13.0 | 13.0 | -0.066 | -13(262), -11(242), 11(223), 13(273) |
| VBF_HToZZ.root | h4lTree | l2zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| VBF_HToZZ.root | h4lTree | l3charge | 2 | -1.0 | 1.0 | 0.02 | -1(490), 1(510) |
| VBF_HToZZ.root | h4lTree | l3elCutBased | 5 | 0.0 | 4.0 | 1.319 | 0(616), 1(20), 2(52), 3(53), 4(259) |
| VBF_HToZZ.root | h4lTree | l3elMvaWP80 | 2 | 0.0 | 1.0 | 0.304 | 0(696), 1(304) |
| VBF_HToZZ.root | h4lTree | l3elMvaWP90 | 2 | 0.0 | 1.0 | 0.36 | 0(640), 1(360) |
| VBF_HToZZ.root | h4lTree | l3miniRelIso | 369 | 0.0 | 1.5275698900222778 | 0.02613794431090355 | 0.0(632), 0.00022884266218170524(1), 0.0004161527322139591(1), 0.0008176186820492148(1), 0.0009685183758847415(1), 0.0012258548522368073(1), 0.0016133477911353111(1), 0.0017925864085555077(1), 0.0018226462416350842(1), 0.0018617119640111923(1), 0.001942531205713749(1), 0.001969488337635994(1), ... |
| VBF_HToZZ.root | h4lTree | l3muGlobal | 2 | 0.0 | 1.0 | 0.566 | 0(434), 1(566) |
| VBF_HToZZ.root | h4lTree | l3muMedium | 2 | 0.0 | 1.0 | 0.573 | 0(427), 1(573) |
| VBF_HToZZ.root | h4lTree | l3muPF | 2 | 0.0 | 1.0 | 0.578 | 0(422), 1(578) |
| VBF_HToZZ.root | h4lTree | l3muTight | 2 | 0.0 | 1.0 | 0.559 | 0(441), 1(559) |
| VBF_HToZZ.root | h4lTree | l3pdgId | 4 | -13.0 | 13.0 | -0.24 | -13(294), -11(216), 11(206), 13(284) |
| VBF_HToZZ.root | h4lTree | l3zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| VBF_HToZZ.root | h4lTree | l4charge | 2 | -1.0 | 1.0 | -0.02 | -1(510), 1(490) |
| VBF_HToZZ.root | h4lTree | l4elCutBased | 5 | 0.0 | 4.0 | 1.116 | 0(644), 1(55), 2(43), 3(57), 4(201) |
| VBF_HToZZ.root | h4lTree | l4elMvaWP80 | 2 | 0.0 | 1.0 | 0.293 | 0(707), 1(293) |
| VBF_HToZZ.root | h4lTree | l4elMvaWP90 | 2 | 0.0 | 1.0 | 0.361 | 0(639), 1(361) |
| VBF_HToZZ.root | h4lTree | l4miniRelIso | 379 | 0.0 | 0.9145793318748474 | 0.03405133634805679 | 0.0(622), 0.001102209324017167(1), 0.0011848207795992494(1), 0.0012524958001449704(1), 0.001309364102780819(1), 0.0015962389297783375(1), 0.0016837531002238393(1), 0.0018626523669809103(1), 0.002041829749941826(1), 0.003253767965361476(1), 0.0035786733496934175(1), 0.0038279432337731123(1), ... |
| VBF_HToZZ.root | h4lTree | l4muGlobal | 2 | 0.0 | 1.0 | 0.571 | 0(429), 1(571) |
| VBF_HToZZ.root | h4lTree | l4muMedium | 2 | 0.0 | 1.0 | 0.568 | 0(432), 1(568) |
| VBF_HToZZ.root | h4lTree | l4muPF | 2 | 0.0 | 1.0 | 0.578 | 0(422), 1(578) |
| VBF_HToZZ.root | h4lTree | l4muTight | 2 | 0.0 | 1.0 | 0.557 | 0(443), 1(557) |
| VBF_HToZZ.root | h4lTree | l4pdgId | 4 | -13.0 | 13.0 | 0.24 | -13(284), -11(206), 11(216), 13(294) |
| VBF_HToZZ.root | h4lTree | l4zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| VBF_HToZZ.root | h4lTree | lumi | 6 | 91.0 | 188.0 | 147.928 | 91(174), 92(162), 165(158), 166(175), 187(158), 188(173) |
| VBF_HToZZ.root | h4lTree | nPV | 34 | 4.0 | 38.0 | 17.597 | 4(3), 5(8), 6(11), 7(7), 8(11), 9(28), 10(49), 11(39), 12(49), 13(54), 14(74), 15(65) |
| VBF_HToZZ.root | h4lTree | pvNdof | 560 | 0.76171875 | 275.0 | 79.0152359008789 | 0.76171875(1), 5.59375(1), 5.65625(1), 7.4375(1), 8.375(1), 8.4375(1), 9.0625(1), 9.21875(1), 9.25(1), 9.625(1), 9.84375(1), 10.75(1), ... |
| VBF_HToZZ.root | h4lTree | run | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| VBF_HToZZ.root | h4lTree | trigBits | 37 | 0.0 | 1843.0 | 569.664 | 0(26), 1(3), 3(39), 16(7), 17(1), 19(1), 32(38), 48(168), 256(6), 257(3), 259(310), 512(5) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WMHToZZ.root | Metadata | nEvents | 1 | 193088.0 | 193088.0 | 193088.0 | 193088(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WMHToZZ.root | h4lTree | event | 1000 | 3076.0 | 178175.0 | 67633.19 | 3076(1), 3089(1), 3093(1), 3107(1), 3108(1), 3120(1), 3123(1), 3130(1), 3138(1), 3146(1), 3183(1), 3195(1), ... |
| WMHToZZ.root | h4lTree | finalState | 3 | 0.0 | 2.0 | 1.12 | 0(329), 1(222), 2(449) |
| WMHToZZ.root | h4lTree | l1charge | 2 | -1.0 | 1.0 | -0.02 | -1(510), 1(490) |
| WMHToZZ.root | h4lTree | l1elCutBased | 5 | 0.0 | 4.0 | 1.589 | 0(565), 1(17), 2(28), 3(44), 4(346) |
| WMHToZZ.root | h4lTree | l1elMvaWP80 | 2 | 0.0 | 1.0 | 0.347 | 0(653), 1(347) |
| WMHToZZ.root | h4lTree | l1elMvaWP90 | 2 | 0.0 | 1.0 | 0.407 | 0(593), 1(407) |
| WMHToZZ.root | h4lTree | l1miniRelIso | 321 | 0.0 | 1.6822960376739502 | 0.021777888759970665 | 0.0(680), 0.00010466926323715597(1), 0.0002447590813972056(1), 0.0002727907267399132(1), 0.00028557656332850456(1), 0.0005255257128737867(1), 0.0009286999120377004(1), 0.0009393025538884103(1), 0.0013934363378211856(1), 0.0015484843170270324(1), 0.0016598515212535858(1), 0.001968325348570943(1), ... |
| WMHToZZ.root | h4lTree | l1muGlobal | 2 | 0.0 | 1.0 | 0.528 | 0(472), 1(528) |
| WMHToZZ.root | h4lTree | l1muMedium | 2 | 0.0 | 1.0 | 0.531 | 0(469), 1(531) |
| WMHToZZ.root | h4lTree | l1muPF | 2 | 0.0 | 1.0 | 0.534 | 0(466), 1(534) |
| WMHToZZ.root | h4lTree | l1muTight | 2 | 0.0 | 1.0 | 0.515 | 0(485), 1(515) |
| WMHToZZ.root | h4lTree | l1pdgId | 4 | -13.0 | 13.0 | 0.196 | -13(273), -11(217), 11(249), 13(261) |
| WMHToZZ.root | h4lTree | l1zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| WMHToZZ.root | h4lTree | l2charge | 2 | -1.0 | 1.0 | 0.02 | -1(490), 1(510) |
| WMHToZZ.root | h4lTree | l2elCutBased | 5 | 0.0 | 4.0 | 1.5 | 0(570), 1(24), 2(49), 3(50), 4(307) |
| WMHToZZ.root | h4lTree | l2elMvaWP80 | 2 | 0.0 | 1.0 | 0.338 | 0(662), 1(338) |
| WMHToZZ.root | h4lTree | l2elMvaWP90 | 2 | 0.0 | 1.0 | 0.405 | 0(595), 1(405) |
| WMHToZZ.root | h4lTree | l2miniRelIso | 388 | 0.0 | 1.1679307222366333 | 0.023817550390958786 | 0.0(613), 8.540109411114827e-05(1), 0.0004764330806210637(1), 0.0009120873874053359(1), 0.0009706474957056344(1), 0.0011972481152042747(1), 0.0017582506407052279(1), 0.0017604060703888535(1), 0.0019172014435753226(1), 0.0019822160247713327(1), 0.0022080654744058847(1), 0.002264630515128374(1), ... |
| WMHToZZ.root | h4lTree | l2muGlobal | 2 | 0.0 | 1.0 | 0.526 | 0(474), 1(526) |
| WMHToZZ.root | h4lTree | l2muMedium | 2 | 0.0 | 1.0 | 0.532 | 0(468), 1(532) |
| WMHToZZ.root | h4lTree | l2muPF | 2 | 0.0 | 1.0 | 0.534 | 0(466), 1(534) |
| WMHToZZ.root | h4lTree | l2muTight | 2 | 0.0 | 1.0 | 0.519 | 0(481), 1(519) |
| WMHToZZ.root | h4lTree | l2pdgId | 4 | -13.0 | 13.0 | -0.196 | -13(261), -11(249), 11(217), 13(273) |
| WMHToZZ.root | h4lTree | l2zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| WMHToZZ.root | h4lTree | l3charge | 2 | -1.0 | 1.0 | -0.046 | -1(523), 1(477) |
| WMHToZZ.root | h4lTree | l3elCutBased | 5 | 0.0 | 4.0 | 1.373 | 0(604), 1(19), 2(53), 3(48), 4(276) |
| WMHToZZ.root | h4lTree | l3elMvaWP80 | 2 | 0.0 | 1.0 | 0.319 | 0(681), 1(319) |
| WMHToZZ.root | h4lTree | l3elMvaWP90 | 2 | 0.0 | 1.0 | 0.374 | 0(626), 1(374) |
| WMHToZZ.root | h4lTree | l3miniRelIso | 386 | 0.0 | 1.4057406187057495 | 0.023648010566830635 | 0.0(615), 0.00028470810502767563(1), 0.00034138551563955843(1), 0.0003780478145927191(1), 0.0009403108269907534(1), 0.001000064192339778(1), 0.0019472031854093075(1), 0.0024678674526512623(1), 0.0026914826594293118(1), 0.0029199442360550165(1), 0.0032835507299751043(1), 0.003554349998012185(1), ... |
| WMHToZZ.root | h4lTree | l3muGlobal | 2 | 0.0 | 1.0 | 0.562 | 0(438), 1(562) |
| WMHToZZ.root | h4lTree | l3muMedium | 2 | 0.0 | 1.0 | 0.567 | 0(433), 1(567) |
| WMHToZZ.root | h4lTree | l3muPF | 2 | 0.0 | 1.0 | 0.572 | 0(428), 1(572) |
| WMHToZZ.root | h4lTree | l3muTight | 2 | 0.0 | 1.0 | 0.553 | 0(447), 1(553) |
| WMHToZZ.root | h4lTree | l3pdgId | 4 | -13.0 | 13.0 | 0.532 | -13(280), -11(197), 11(230), 13(293) |
| WMHToZZ.root | h4lTree | l3zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| WMHToZZ.root | h4lTree | l4charge | 2 | -1.0 | 1.0 | 0.046 | -1(477), 1(523) |
| WMHToZZ.root | h4lTree | l4elCutBased | 5 | 0.0 | 4.0 | 1.091 | 0(636), 1(63), 2(55), 3(66), 4(180) |
| WMHToZZ.root | h4lTree | l4elMvaWP80 | 2 | 0.0 | 1.0 | 0.288 | 0(712), 1(288) |
| WMHToZZ.root | h4lTree | l4elMvaWP90 | 2 | 0.0 | 1.0 | 0.358 | 0(642), 1(358) |
| WMHToZZ.root | h4lTree | l4miniRelIso | 392 | 0.0 | 1.9011173248291016 | 0.03855033218860626 | 0.0(609), 0.00011495104263303801(1), 0.00025775079848244786(1), 0.0005880317185074091(1), 0.0010939915664494038(1), 0.0017536974046379328(1), 0.001865530270151794(1), 0.0022307669278234243(1), 0.0023072119802236557(1), 0.002426604274660349(1), 0.0032366944942623377(1), 0.0033616633154451847(1), ... |
| WMHToZZ.root | h4lTree | l4muGlobal | 2 | 0.0 | 1.0 | 0.57 | 0(430), 1(570) |
| WMHToZZ.root | h4lTree | l4muMedium | 2 | 0.0 | 1.0 | 0.571 | 0(429), 1(571) |
| WMHToZZ.root | h4lTree | l4muPF | 2 | 0.0 | 1.0 | 0.573 | 0(427), 1(573) |
| WMHToZZ.root | h4lTree | l4muTight | 2 | 0.0 | 1.0 | 0.562 | 0(438), 1(562) |
| WMHToZZ.root | h4lTree | l4pdgId | 4 | -13.0 | 13.0 | -0.532 | -13(293), -11(230), 11(197), 13(280) |
| WMHToZZ.root | h4lTree | l4zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| WMHToZZ.root | h4lTree | lumi | 9 | 5.0 | 232.0 | 88.575 | 5(110), 6(111), 26(131), 70(119), 78(131), 79(41), 82(133), 226(118), 232(106) |
| WMHToZZ.root | h4lTree | nPV | 35 | 3.0 | 46.0 | 17.269 | 3(2), 4(2), 5(3), 6(6), 7(8), 8(17), 9(39), 10(29), 11(50), 12(62), 13(61), 14(55) |
| WMHToZZ.root | h4lTree | pvNdof | 540 | 2.1484375 | 229.5 | 91.21589660644531 | 2.1484375(1), 8.875(1), 9.21875(1), 9.9375(1), 11.5625(1), 12.25(1), 12.65625(1), 13.03125(1), 15.90625(1), 15.9375(1), 18.125(1), 18.5(2), ... |
| WMHToZZ.root | h4lTree | run | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| WMHToZZ.root | h4lTree | trigBits | 44 | 0.0 | 1843.0 | 674.897 | 0(18), 1(1), 3(20), 16(9), 19(2), 32(40), 48(159), 256(12), 257(5), 259(275), 512(9), 528(9) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WPHToZZ.root | Metadata | nEvents | 1 | 294744.0 | 294744.0 | 294744.0 | 294744(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WPHToZZ.root | h4lTree | event | 1000 | 2639.0 | 251430.0 | 128261.09 | 2639(1), 2652(1), 2660(1), 2673(1), 2679(1), 2680(1), 2683(1), 2684(1), 2695(1), 2696(1), 2708(1), 2710(1), ... |
| WPHToZZ.root | h4lTree | finalState | 3 | 0.0 | 2.0 | 1.191 | 0(300), 1(209), 2(491) |
| WPHToZZ.root | h4lTree | l1charge | 2 | -1.0 | 1.0 | 0.028 | -1(486), 1(514) |
| WPHToZZ.root | h4lTree | l1elCutBased | 5 | 0.0 | 4.0 | 1.655 | 0(548), 1(21), 2(28), 3(34), 4(369) |
| WPHToZZ.root | h4lTree | l1elMvaWP80 | 2 | 0.0 | 1.0 | 0.364 | 0(636), 1(364) |
| WPHToZZ.root | h4lTree | l1elMvaWP90 | 2 | 0.0 | 1.0 | 0.419 | 0(581), 1(419) |
| WPHToZZ.root | h4lTree | l1miniRelIso | 315 | 0.0 | 1.6087011098861694 | 0.01944543793797493 | 0.0(686), 6.886286428198218e-05(1), 0.0002758283808361739(1), 0.0007193334167823195(1), 0.0007689683116041124(1), 0.0014961606357246637(1), 0.0016381441382691264(1), 0.0016453253338113427(1), 0.0018295528134331107(1), 0.001861618016846478(1), 0.0020558941178023815(1), 0.00272171339020133(1), ... |
| WPHToZZ.root | h4lTree | l1muGlobal | 2 | 0.0 | 1.0 | 0.519 | 0(481), 1(519) |
| WPHToZZ.root | h4lTree | l1muMedium | 2 | 0.0 | 1.0 | 0.521 | 0(479), 1(521) |
| WPHToZZ.root | h4lTree | l1muPF | 2 | 0.0 | 1.0 | 0.524 | 0(476), 1(524) |
| WPHToZZ.root | h4lTree | l1muTight | 2 | 0.0 | 1.0 | 0.509 | 0(491), 1(509) |
| WPHToZZ.root | h4lTree | l1pdgId | 4 | -13.0 | 13.0 | -0.304 | -13(261), -11(253), 11(223), 13(263) |
| WPHToZZ.root | h4lTree | l1zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| WPHToZZ.root | h4lTree | l2charge | 2 | -1.0 | 1.0 | -0.028 | -1(514), 1(486) |
| WPHToZZ.root | h4lTree | l2elCutBased | 5 | 0.0 | 4.0 | 1.489 | 0(570), 1(26), 2(45), 3(63), 4(296) |
| WPHToZZ.root | h4lTree | l2elMvaWP80 | 2 | 0.0 | 1.0 | 0.345 | 0(655), 1(345) |
| WPHToZZ.root | h4lTree | l2elMvaWP90 | 2 | 0.0 | 1.0 | 0.412 | 0(588), 1(412) |
| WPHToZZ.root | h4lTree | l2miniRelIso | 408 | 0.0 | 1.147377371788025 | 0.025817645713686943 | 0.0(593), 6.230910366866738e-05(1), 0.00012982777843717486(1), 0.00013463177310768515(1), 0.0006056813872419298(1), 0.0008354814490303397(1), 0.0011281458428129554(1), 0.0011583465384319425(1), 0.0011936449445784092(1), 0.0012097535654902458(1), 0.0014721598709002137(1), 0.0017168037593364716(1), ... |
| WPHToZZ.root | h4lTree | l2muGlobal | 2 | 0.0 | 1.0 | 0.514 | 0(486), 1(514) |
| WPHToZZ.root | h4lTree | l2muMedium | 2 | 0.0 | 1.0 | 0.52 | 0(480), 1(520) |
| WPHToZZ.root | h4lTree | l2muPF | 2 | 0.0 | 1.0 | 0.523 | 0(477), 1(523) |
| WPHToZZ.root | h4lTree | l2muTight | 2 | 0.0 | 1.0 | 0.506 | 0(494), 1(506) |
| WPHToZZ.root | h4lTree | l2pdgId | 4 | -13.0 | 13.0 | 0.304 | -13(263), -11(223), 11(253), 13(261) |
| WPHToZZ.root | h4lTree | l2zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| WPHToZZ.root | h4lTree | l3charge | 2 | -1.0 | 1.0 | 0.046 | -1(477), 1(523) |
| WPHToZZ.root | h4lTree | l3elCutBased | 5 | 0.0 | 4.0 | 1.307 | 0(612), 1(36), 2(50), 3(37), 4(265) |
| WPHToZZ.root | h4lTree | l3elMvaWP80 | 2 | 0.0 | 1.0 | 0.32 | 0(680), 1(320) |
| WPHToZZ.root | h4lTree | l3elMvaWP90 | 2 | 0.0 | 1.0 | 0.378 | 0(622), 1(378) |
| WPHToZZ.root | h4lTree | l3miniRelIso | 402 | 0.0 | 1.765234351158142 | 0.033633481711149216 | 0.0(599), 0.0003046211786568165(1), 0.0007720362627878785(1), 0.0008325370727106929(1), 0.0008404874824918807(1), 0.0008454744820483029(1), 0.0009445106261409819(1), 0.0009564092033542693(1), 0.0013326508924365044(1), 0.0015671269502490759(1), 0.002076411619782448(1), 0.002179319504648447(1), ... |
| WPHToZZ.root | h4lTree | l3muGlobal | 2 | 0.0 | 1.0 | 0.559 | 0(441), 1(559) |
| WPHToZZ.root | h4lTree | l3muMedium | 2 | 0.0 | 1.0 | 0.562 | 0(438), 1(562) |
| WPHToZZ.root | h4lTree | l3muPF | 2 | 0.0 | 1.0 | 0.566 | 0(434), 1(566) |
| WPHToZZ.root | h4lTree | l3muTight | 2 | 0.0 | 1.0 | 0.549 | 0(451), 1(549) |
| WPHToZZ.root | h4lTree | l3pdgId | 4 | -13.0 | 13.0 | -0.604 | -13(308), -11(215), 11(218), 13(259) |
| WPHToZZ.root | h4lTree | l3zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| WPHToZZ.root | h4lTree | l4charge | 2 | -1.0 | 1.0 | -0.046 | -1(523), 1(477) |
| WPHToZZ.root | h4lTree | l4elCutBased | 5 | 0.0 | 4.0 | 1.133 | 0(630), 1(51), 2(68), 3(58), 4(193) |
| WPHToZZ.root | h4lTree | l4elMvaWP80 | 2 | 0.0 | 1.0 | 0.279 | 0(721), 1(279) |
| WPHToZZ.root | h4lTree | l4elMvaWP90 | 2 | 0.0 | 1.0 | 0.361 | 0(639), 1(361) |
| WPHToZZ.root | h4lTree | l4miniRelIso | 382 | 0.0 | 2.732473611831665 | 0.04188308119773865 | 0.0(619), 0.00022980841458775103(1), 0.0020070530008524656(1), 0.0024833125062286854(1), 0.0026823757216334343(1), 0.004075145348906517(1), 0.004176286514848471(1), 0.0048657129518687725(1), 0.006103814113885164(1), 0.006569914519786835(1), 0.007394056301563978(1), 0.007531378883868456(1), ... |
| WPHToZZ.root | h4lTree | l4muGlobal | 2 | 0.0 | 1.0 | 0.561 | 0(439), 1(561) |
| WPHToZZ.root | h4lTree | l4muMedium | 2 | 0.0 | 1.0 | 0.562 | 0(438), 1(562) |
| WPHToZZ.root | h4lTree | l4muPF | 2 | 0.0 | 1.0 | 0.566 | 0(434), 1(566) |
| WPHToZZ.root | h4lTree | l4muTight | 2 | 0.0 | 1.0 | 0.554 | 0(446), 1(554) |
| WPHToZZ.root | h4lTree | l4pdgId | 4 | -13.0 | 13.0 | 0.604 | -13(259), -11(218), 11(215), 13(308) |
| WPHToZZ.root | h4lTree | l4zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| WPHToZZ.root | h4lTree | lumi | 11 | 5.0 | 383.0 | 195.742 | 5(102), 66(91), 67(82), 69(81), 72(94), 248(92), 302(98), 304(97), 310(98), 342(100), 383(65) |
| WPHToZZ.root | h4lTree | nPV | 37 | 3.0 | 40.0 | 17.685 | 3(3), 4(2), 5(7), 6(8), 7(14), 8(20), 9(29), 10(30), 11(39), 12(41), 13(63), 14(57) |
| WPHToZZ.root | h4lTree | pvNdof | 508 | 7.5 | 259.0 | 91.22284698486328 | 7.5(1), 8.34375(1), 8.9375(1), 11.8125(1), 12.46875(1), 12.8125(1), 12.84375(1), 13.65625(1), 13.9375(1), 14.6875(1), 15.0(1), 15.21875(1), ... |
| WPHToZZ.root | h4lTree | run | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| WPHToZZ.root | h4lTree | trigBits | 41 | 0.0 | 1843.0 | 694.683 | 0(20), 3(41), 16(10), 32(22), 48(145), 256(7), 257(7), 259(262), 512(5), 528(11), 544(19), 560(84) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ZHToZZ.root | Metadata | nEvents | 1 | 486281.0 | 486281.0 | 486281.0 | 486281(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ZHToZZ.root | h4lTree | event | 1000 | 297320.0 | 3142752.0 | 1904870.103 | 297320(1), 297343(1), 297362(1), 297365(1), 297367(1), 297384(1), 297388(1), 297395(1), 297433(1), 297470(1), 297613(1), 477025(1), ... |
| ZHToZZ.root | h4lTree | finalState | 3 | 0.0 | 2.0 | 1.158 | 0(301), 1(240), 2(459) |
| ZHToZZ.root | h4lTree | l1charge | 2 | -1.0 | 1.0 | 0.03 | -1(485), 1(515) |
| ZHToZZ.root | h4lTree | l1elCutBased | 5 | 0.0 | 4.0 | 1.75 | 0(530), 1(8), 2(29), 3(48), 4(385) |
| ZHToZZ.root | h4lTree | l1elMvaWP80 | 2 | 0.0 | 1.0 | 0.383 | 0(617), 1(383) |
| ZHToZZ.root | h4lTree | l1elMvaWP90 | 2 | 0.0 | 1.0 | 0.445 | 0(555), 1(445) |
| ZHToZZ.root | h4lTree | l1miniRelIso | 281 | 0.0 | 1.3499994277954102 | 0.010434737429022789 | 0.0(720), 2.4612700144643895e-05(1), 3.222974555683322e-05(1), 0.0003249109722673893(1), 0.00038806567317806184(1), 0.0005276884767226875(1), 0.0006319982348941267(1), 0.0009200411150231957(1), 0.001201139879412949(1), 0.0013117709895595908(1), 0.0016940785571932793(1), 0.0017692039255052805(1), ... |
| ZHToZZ.root | h4lTree | l1muGlobal | 2 | 0.0 | 1.0 | 0.506 | 0(494), 1(506) |
| ZHToZZ.root | h4lTree | l1muMedium | 2 | 0.0 | 1.0 | 0.508 | 0(492), 1(508) |
| ZHToZZ.root | h4lTree | l1muPF | 2 | 0.0 | 1.0 | 0.51 | 0(490), 1(510) |
| ZHToZZ.root | h4lTree | l1muTight | 2 | 0.0 | 1.0 | 0.503 | 0(497), 1(503) |
| ZHToZZ.root | h4lTree | l1pdgId | 4 | -13.0 | 13.0 | -0.378 | -13(267), -11(248), 11(242), 13(243) |
| ZHToZZ.root | h4lTree | l1zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| ZHToZZ.root | h4lTree | l2charge | 2 | -1.0 | 1.0 | -0.03 | -1(515), 1(485) |
| ZHToZZ.root | h4lTree | l2elCutBased | 5 | 0.0 | 4.0 | 1.564 | 0(547), 1(32), 2(47), 3(58), 4(316) |
| ZHToZZ.root | h4lTree | l2elMvaWP80 | 2 | 0.0 | 1.0 | 0.358 | 0(642), 1(358) |
| ZHToZZ.root | h4lTree | l2elMvaWP90 | 2 | 0.0 | 1.0 | 0.422 | 0(578), 1(422) |
| ZHToZZ.root | h4lTree | l2miniRelIso | 423 | 0.0 | 1.2880128622055054 | 0.025409862399101257 | 0.0(578), 0.00034743151627480984(1), 0.0006020713481120765(1), 0.0007589667220599949(1), 0.0008783373050391674(1), 0.0011380048235878348(1), 0.001250831875950098(1), 0.0012850509956479073(1), 0.0014632572419941425(1), 0.0020082909613847733(1), 0.00202616723254323(1), 0.0020317533053457737(1), ... |
| ZHToZZ.root | h4lTree | l2muGlobal | 2 | 0.0 | 1.0 | 0.504 | 0(496), 1(504) |
| ZHToZZ.root | h4lTree | l2muMedium | 2 | 0.0 | 1.0 | 0.504 | 0(496), 1(504) |
| ZHToZZ.root | h4lTree | l2muPF | 2 | 0.0 | 1.0 | 0.509 | 0(491), 1(509) |
| ZHToZZ.root | h4lTree | l2muTight | 2 | 0.0 | 1.0 | 0.499 | 0(501), 1(499) |
| ZHToZZ.root | h4lTree | l2pdgId | 4 | -13.0 | 13.0 | 0.378 | -13(243), -11(242), 11(248), 13(267) |
| ZHToZZ.root | h4lTree | l2zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| ZHToZZ.root | h4lTree | l3charge | 2 | -1.0 | 1.0 | -0.018 | -1(509), 1(491) |
| ZHToZZ.root | h4lTree | l3elCutBased | 5 | 0.0 | 4.0 | 1.372 | 0(596), 1(31), 2(52), 3(47), 4(274) |
| ZHToZZ.root | h4lTree | l3elMvaWP80 | 2 | 0.0 | 1.0 | 0.32 | 0(680), 1(320) |
| ZHToZZ.root | h4lTree | l3elMvaWP90 | 2 | 0.0 | 1.0 | 0.371 | 0(629), 1(371) |
| ZHToZZ.root | h4lTree | l3miniRelIso | 399 | 0.0 | 2.46919584274292 | 0.03761681541800499 | 0.0(602), 0.00043569892295636237(1), 0.0005290803383104503(1), 0.0008061982225626707(1), 0.0011486605508252978(1), 0.0011922208359465003(1), 0.0012561623007059097(1), 0.0015416991664096713(1), 0.0016902416246011853(1), 0.001928082201629877(1), 0.0022279706317931414(1), 0.00228366837836802(1), ... |
| ZHToZZ.root | h4lTree | l3muGlobal | 2 | 0.0 | 1.0 | 0.541 | 0(459), 1(541) |
| ZHToZZ.root | h4lTree | l3muMedium | 2 | 0.0 | 1.0 | 0.539 | 0(461), 1(539) |
| ZHToZZ.root | h4lTree | l3muPF | 2 | 0.0 | 1.0 | 0.549 | 0(451), 1(549) |
| ZHToZZ.root | h4lTree | l3muTight | 2 | 0.0 | 1.0 | 0.528 | 0(472), 1(528) |
| ZHToZZ.root | h4lTree | l3pdgId | 4 | -13.0 | 13.0 | 0.224 | -13(269), -11(222), 11(227), 13(282) |
| ZHToZZ.root | h4lTree | l3zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| ZHToZZ.root | h4lTree | l4charge | 2 | -1.0 | 1.0 | 0.018 | -1(491), 1(509) |
| ZHToZZ.root | h4lTree | l4elCutBased | 5 | 0.0 | 4.0 | 1.243 | 0(611), 1(46), 2(55), 3(65), 4(223) |
| ZHToZZ.root | h4lTree | l4elMvaWP80 | 2 | 0.0 | 1.0 | 0.317 | 0(683), 1(317) |
| ZHToZZ.root | h4lTree | l4elMvaWP90 | 2 | 0.0 | 1.0 | 0.382 | 0(618), 1(382) |
| ZHToZZ.root | h4lTree | l4miniRelIso | 404 | 0.0 | 2.321380138397217 | 0.04061572253704071 | 0.0(597), 1.3295829376147594e-05(1), 6.907289935043082e-05(1), 0.00010555339395068586(1), 0.0002688739914447069(1), 0.001483233878389001(1), 0.0015789233148097992(1), 0.0018603010103106499(1), 0.0019779419526457787(1), 0.0022698191460222006(1), 0.0027745661791414022(1), 0.0031550393905490637(1), ... |
| ZHToZZ.root | h4lTree | l4muGlobal | 2 | 0.0 | 1.0 | 0.547 | 0(453), 1(547) |
| ZHToZZ.root | h4lTree | l4muMedium | 2 | 0.0 | 1.0 | 0.543 | 0(457), 1(543) |
| ZHToZZ.root | h4lTree | l4muPF | 2 | 0.0 | 1.0 | 0.549 | 0(451), 1(549) |
| ZHToZZ.root | h4lTree | l4muTight | 2 | 0.0 | 1.0 | 0.536 | 0(464), 1(536) |
| ZHToZZ.root | h4lTree | l4pdgId | 4 | -13.0 | 13.0 | -0.224 | -13(282), -11(227), 11(222), 13(269) |
| ZHToZZ.root | h4lTree | l4zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| ZHToZZ.root | h4lTree | lumi | 52 | 327.0 | 3446.0 | 2089.169 | 327(11), 524(18), 741(19), 785(15), 786(12), 801(20), 858(21), 1089(19), 1341(23), 1342(22), 1346(14), 1349(19), ... |
| ZHToZZ.root | h4lTree | nPV | 36 | 4.0 | 43.0 | 17.438 | 4(4), 5(7), 6(12), 7(8), 8(25), 9(22), 10(36), 11(57), 12(48), 13(57), 14(53), 15(73) |
| ZHToZZ.root | h4lTree | pvNdof | 504 | 0.80078125 | 258.0 | 89.43417358398438 | 0.80078125(1), 1.9921875(1), 7.96875(1), 9.1875(1), 10.5(1), 11.21875(1), 11.4375(1), 11.5(1), 11.6875(1), 13.5(1), 13.71875(1), 13.75(1), ... |
| ZHToZZ.root | h4lTree | run | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| ZHToZZ.root | h4lTree | trigBits | 36 | 0.0 | 1843.0 | 671.231 | 0(12), 1(1), 3(20), 16(2), 32(22), 48(219), 256(8), 257(3), 259(274), 512(9), 528(5), 544(9) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ZZTo4L.root | Metadata | nEvents | 1 | 52104000.0 | 52104000.0 | 52104000.0 | 52104000(1) |

| File | Tree | Branch | N unique | Min | Max | Mean | Values(counts) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ZZTo4L.root | h4lTree | event | 1000 | 2530030.0 | 46950935.0 | 14863485.822 | 2530030(1), 2530071(1), 2530072(1), 2530107(1), 2530130(1), 2530136(1), 2530160(1), 2530177(1), 2530178(1), 2530217(1), 2530242(1), 2530277(1), ... |
| ZZTo4L.root | h4lTree | finalState | 3 | 0.0 | 2.0 | 1.164 | 0(335), 1(166), 2(499) |
| ZZTo4L.root | h4lTree | l1charge | 2 | -1.0 | 1.0 | -0.054 | -1(527), 1(473) |
| ZZTo4L.root | h4lTree | l1elCutBased | 5 | 0.0 | 4.0 | 1.481 | 0(599), 1(9), 2(28), 3(40), 4(324) |
| ZZTo4L.root | h4lTree | l1elMvaWP80 | 2 | 0.0 | 1.0 | 0.328 | 0(672), 1(328) |
| ZZTo4L.root | h4lTree | l1elMvaWP90 | 2 | 0.0 | 1.0 | 0.371 | 0(629), 1(371) |
| ZZTo4L.root | h4lTree | l1miniRelIso | 309 | 0.0 | 1.1439801454544067 | 0.013224679976701736 | 0.0(692), 0.00018014645320363343(1), 0.0002534915693104267(1), 0.0004175411013420671(1), 0.000966920459177345(1), 0.001092381658963859(1), 0.001455719000659883(1), 0.0016288411570712924(1), 0.0016376815037801862(1), 0.0017180853756144643(1), 0.0018272562883794308(1), 0.002078017219901085(1), ... |
| ZZTo4L.root | h4lTree | l1muGlobal | 2 | 0.0 | 1.0 | 0.573 | 0(427), 1(573) |
| ZZTo4L.root | h4lTree | l1muMedium | 2 | 0.0 | 1.0 | 0.575 | 0(425), 1(575) |
| ZZTo4L.root | h4lTree | l1muPF | 2 | 0.0 | 1.0 | 0.581 | 0(419), 1(581) |
| ZZTo4L.root | h4lTree | l1muTight | 2 | 0.0 | 1.0 | 0.564 | 0(436), 1(564) |
| ZZTo4L.root | h4lTree | l1pdgId | 4 | -13.0 | 13.0 | 0.68 | -13(269), -11(204), 11(215), 13(312) |
| ZZTo4L.root | h4lTree | l1zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| ZZTo4L.root | h4lTree | l2charge | 2 | -1.0 | 1.0 | 0.054 | -1(473), 1(527) |
| ZZTo4L.root | h4lTree | l2elCutBased | 5 | 0.0 | 4.0 | 1.353 | 0(607), 1(25), 2(43), 3(58), 4(267) |
| ZZTo4L.root | h4lTree | l2elMvaWP80 | 2 | 0.0 | 1.0 | 0.318 | 0(682), 1(318) |
| ZZTo4L.root | h4lTree | l2elMvaWP90 | 2 | 0.0 | 1.0 | 0.368 | 0(632), 1(368) |
| ZZTo4L.root | h4lTree | l2miniRelIso | 403 | 0.0 | 0.9889469742774963 | 0.022294679656624794 | 0.0(598), 7.2693575930316e-05(1), 0.0007108738063834608(1), 0.0007562406826764345(1), 0.0009609617409296334(1), 0.0010065962560474873(1), 0.001475364901125431(1), 0.0015115223359316587(1), 0.0015422855503857136(1), 0.0015705848345533013(1), 0.0018822858110070229(1), 0.0027448004111647606(1), ... |
| ZZTo4L.root | h4lTree | l2muGlobal | 2 | 0.0 | 1.0 | 0.575 | 0(425), 1(575) |
| ZZTo4L.root | h4lTree | l2muMedium | 2 | 0.0 | 1.0 | 0.572 | 0(428), 1(572) |
| ZZTo4L.root | h4lTree | l2muPF | 2 | 0.0 | 1.0 | 0.581 | 0(419), 1(581) |
| ZZTo4L.root | h4lTree | l2muTight | 2 | 0.0 | 1.0 | 0.562 | 0(438), 1(562) |
| ZZTo4L.root | h4lTree | l2pdgId | 4 | -13.0 | 13.0 | -0.68 | -13(312), -11(215), 11(204), 13(269) |
| ZZTo4L.root | h4lTree | l2zId | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| ZZTo4L.root | h4lTree | l3charge | 2 | -1.0 | 1.0 | 0.016 | -1(492), 1(508) |
| ZZTo4L.root | h4lTree | l3elCutBased | 5 | 0.0 | 4.0 | 1.35 | 0(623), 1(17), 2(32), 3(43), 4(285) |
| ZZTo4L.root | h4lTree | l3elMvaWP80 | 2 | 0.0 | 1.0 | 0.315 | 0(685), 1(315) |
| ZZTo4L.root | h4lTree | l3elMvaWP90 | 2 | 0.0 | 1.0 | 0.363 | 0(637), 1(363) |
| ZZTo4L.root | h4lTree | l3miniRelIso | 353 | 0.0 | 1.0073710680007935 | 0.02027459256350994 | 0.0(648), 0.000148916311445646(1), 0.0005660973256453872(1), 0.0012814293149858713(1), 0.00136207090690732(1), 0.001402194146066904(1), 0.0018042813753709197(1), 0.0019229614408686757(1), 0.0019856011494994164(1), 0.0023657234851270914(1), 0.0023742292542010546(1), 0.0026028375141322613(1), ... |
| ZZTo4L.root | h4lTree | l3muGlobal | 2 | 0.0 | 1.0 | 0.58 | 0(420), 1(580) |
| ZZTo4L.root | h4lTree | l3muMedium | 2 | 0.0 | 1.0 | 0.586 | 0(414), 1(586) |
| ZZTo4L.root | h4lTree | l3muPF | 2 | 0.0 | 1.0 | 0.588 | 0(412), 1(588) |
| ZZTo4L.root | h4lTree | l3muTight | 2 | 0.0 | 1.0 | 0.572 | 0(428), 1(572) |
| ZZTo4L.root | h4lTree | l3pdgId | 4 | -13.0 | 13.0 | -0.22 | -13(305), -11(203), 11(209), 13(283) |
| ZZTo4L.root | h4lTree | l3zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| ZZTo4L.root | h4lTree | l4charge | 2 | -1.0 | 1.0 | -0.016 | -1(508), 1(492) |
| ZZTo4L.root | h4lTree | l4elCutBased | 5 | 0.0 | 4.0 | 1.159 | 0(644), 1(37), 2(50), 3(54), 4(215) |
| ZZTo4L.root | h4lTree | l4elMvaWP80 | 2 | 0.0 | 1.0 | 0.296 | 0(704), 1(296) |
| ZZTo4L.root | h4lTree | l4elMvaWP90 | 2 | 0.0 | 1.0 | 0.353 | 0(647), 1(353) |
| ZZTo4L.root | h4lTree | l4miniRelIso | 382 | 0.0 | 1.8853482007980347 | 0.03294013813138008 | 0.0(619), 1.0562953320913948e-05(1), 0.00037278883974067867(1), 0.000406275677960366(1), 0.0012602809583768249(1), 0.0014086796436458826(1), 0.0017786159878596663(1), 0.0018461118452250957(1), 0.0024086711928248405(1), 0.0032424151431769133(1), 0.003463962348178029(1), 0.0036648751702159643(1), ... |
| ZZTo4L.root | h4lTree | l4muGlobal | 2 | 0.0 | 1.0 | 0.578 | 0(422), 1(578) |
| ZZTo4L.root | h4lTree | l4muMedium | 2 | 0.0 | 1.0 | 0.581 | 0(419), 1(581) |
| ZZTo4L.root | h4lTree | l4muPF | 2 | 0.0 | 1.0 | 0.587 | 0(413), 1(587) |
| ZZTo4L.root | h4lTree | l4muTight | 2 | 0.0 | 1.0 | 0.563 | 0(437), 1(563) |
| ZZTo4L.root | h4lTree | l4pdgId | 4 | -13.0 | 13.0 | 0.22 | -13(283), -11(209), 11(203), 13(305) |
| ZZTo4L.root | h4lTree | l4zId | 1 | 2.0 | 2.0 | 2.0 | 2(1000) |
| ZZTo4L.root | h4lTree | lumi | 30 | 2531.0 | 46951.0 | 14863.998 | 2531(29), 2532(34), 2547(27), 2612(44), 2614(36), 2615(40), 2683(34), 2775(28), 2788(22), 2789(28), 2849(30), 2850(38) |
| ZZTo4L.root | h4lTree | nPV | 35 | 1.0 | 37.0 | 17.672 | 1(1), 2(1), 3(1), 4(1), 5(2), 6(9), 7(13), 8(29), 9(22), 10(34), 11(41), 12(46) |
| ZZTo4L.root | h4lTree | pvNdof | 550 | 1.609375 | 229.5 | 76.42709350585938 | 1.609375(1), 2.9375(1), 3.390625(1), 4.046875(1), 4.28125(1), 6.359375(1), 6.484375(1), 7.921875(1), 8.875(1), 9.125(1), 9.5625(1), 10.875(2), ... |
| ZZTo4L.root | h4lTree | run | 1 | 1.0 | 1.0 | 1.0 | 1(1000) |
| ZZTo4L.root | h4lTree | trigBits | 32 | 0.0 | 1843.0 | 653.985 | 0(37), 1(5), 3(38), 16(9), 32(28), 48(137), 256(20), 257(5), 259(300), 512(6), 528(11), 544(30) |


### Integer/Flag Interpretation and Residual Ambiguities

Targeted decoding attempts:

- Read the local ntuplizer `h4l_ntuplize.py` in this analysis root. It defines the custom `finalState`, `zId`, and `trigBits` encodings and copies NanoAOD lepton-ID branches into the flat ntuple.
- Checked the branch inventory and small-slice unique-value survey for every primary ROOT file. The observed values are consistent with the local ntuplizer definitions.
- Checked public NanoAOD branch context for `Electron_cutBased` using the CMS NanoAOD workbook (https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD). The local ntuplizer copies `Electron_cutBased` for electrons, sets it to `0` for muon rows, and in generator-dressed-lepton fallback sets generated electrons to `4`.

Decoded codes needed by Phase 2:

| Branch family | Observed values | Interpretation | Phase 2 handling |
| --- | --- | --- | --- |
| `finalState` | `0`, `1`, `2` | Local ntuplizer sets `0` for four-muon candidates, `1` for four-electron candidates, and `2` for mixed two-electron/two-muon candidates. | Use for channel splitting only after confirming the file provenance remains this ntuplizer. |
| `l1zId` ... `l4zId` | `1`, `2` | Local ntuplizer stores the selected candidate as Z1 leptons first and Z2 leptons second, then writes `zId=[1, 1, 2, 2]`; `l1/l2` are Z1 and `l3/l4` are Z2. | Safe for reconstructing which selected leptons belong to Z1 vs Z2; it is not an external truth label. |
| `l1elCutBased` ... `l4elCutBased` | `0`, `1`, `2`, `3`, `4` | For electron rows this is the NanoAOD `Electron_cutBased` working-point integer (`0` fail/no WP, `1` veto, `2` loose, `3` medium, `4` tight). For muon rows the local ntuplizer writes `0`, so `0` is not automatically a failed electron. | Apply electron WP logic only where `abs(lNpdgId)==11`; do not treat all zeros as failed electrons. |
| `lNmuMedium`, `lNmuTight`, `lNmuGlobal`, `lNmuPF`, `lNelMvaWP80`, `lNelMvaWP90` | `0`, `1` | Boolean object-ID/pass flags copied from NanoAOD or assigned by the local generator-dressed-lepton fallback. | Use as boolean flags; Phase 2 should require object flavor consistency before applying an electron or muon flag. |
| `trigBits` | Bitmask values, including `0`, `1`, `3`, `16`, `32`, `48`, `259`, `1843` | Local ntuplizer ORs one bit per HLT path; `trigBits=0` means none of the listed HLT paths fired in the stored event. | Decode by bit operations; do not compare only to a single integer value. |

Trigger bit map from `h4l_ntuplize.py`:

| Bit | Mask value | HLT path suffix |
| --- | --- | --- |
| 0 | 1 | HLT_IsoMu24 |
| 1 | 2 | HLT_IsoMu27 |
| 2 | 4 | HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 |
| 3 | 8 | HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 |
| 4 | 16 | HLT_Ele32_WPTight_Gsf |
| 5 | 32 | HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL |
| 6 | 64 | HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ |
| 7 | 128 | HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ |
| 8 | 256 | HLT_TripleMu_12_10_5 |
| 9 | 512 | HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ |
| 10 | 1024 | HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ |

Residual ambiguity: Phase 1 did not prove that every provided ROOT file was produced by this exact local `h4l_ntuplize.py` revision. The custom branch names and observed values match the script, so the interpretation is the working Phase 2 assumption. If Phase 2 changes data source or finds provenance metadata that contradicts this script, it must revise the code map before using channel, ID, or trigger categories.


## Data Quality Assessment

| File | Tree | Entries loaded | Numeric branches | NaN count | Inf count |
| --- | --- | --- | --- | --- | --- |
| cms_10fb_13TeV.root | Metadata | 1 | 2 | 0 | 0 |
| cms_10fb_13TeV.root | h4lTree | 854 | 108 | 0 | 0 |
| DYJetsToLL.root | Metadata | 1 | 1 | 0 | 0 |
| DYJetsToLL.root | h4lTree | 463 | 111 | 0 | 0 |
| GGZZ2E2Mu.root | Metadata | 1 | 1 | 0 | 0 |
| GGZZ2E2Mu.root | h4lTree | 1000 | 111 | 0 | 0 |
| GGZZ4E.root | Metadata | 1 | 1 | 0 | 0 |
| GGZZ4E.root | h4lTree | 1000 | 111 | 0 | 0 |
| GGZZ4Mu.root | Metadata | 1 | 1 | 0 | 0 |
| GGZZ4Mu.root | h4lTree | 1000 | 111 | 0 | 0 |
| GluGluToHToZZ.root | Metadata | 1 | 1 | 0 | 0 |
| GluGluToHToZZ.root | h4lTree | 1000 | 111 | 0 | 0 |
| TTBar.root | Metadata | 1 | 1 | 0 | 0 |
| TTBar.root | h4lTree | 639 | 111 | 0 | 0 |
| VBF_HToZZ.root | Metadata | 1 | 1 | 0 | 0 |
| VBF_HToZZ.root | h4lTree | 1000 | 111 | 0 | 0 |
| WMHToZZ.root | Metadata | 1 | 1 | 0 | 0 |
| WMHToZZ.root | h4lTree | 1000 | 111 | 0 | 0 |
| WPHToZZ.root | Metadata | 1 | 1 | 0 | 0 |
| WPHToZZ.root | h4lTree | 1000 | 111 | 0 | 0 |
| ZHToZZ.root | Metadata | 1 | 1 | 0 | 0 |
| ZHToZZ.root | h4lTree | 1000 | 111 | 0 | 0 |
| ZZTo4L.root | Metadata | 1 | 1 | 0 | 0 |
| ZZTo4L.root | h4lTree | 1000 | 111 | 0 | 0 |

No full-event production processing was performed in Phase 1. The quality survey loaded at most 1000 entries per primary tree and counted NaN/inf values after flattening numeric branches.

### Visible Extremes and Outlier Assessment

The NaN/inf check is clean in the 1000-entry slices, but the integer/range survey shows expected tails that Phase 2 should not ignore:

- Lepton `pfRelIso03` values are bounded just below the local ntuplizer threshold of `0.35`, which is consistent with the object selection. This is acceptable and supports the inference that the ntuples are already object-selected.
- Lepton `miniRelIso` has long tails in the same slices: the largest observed values are about `6.04` in `TTBar.root`, `5.33` in `TTBar.root`, and `4.78` in both the data and DY slices. This is not immediately a NaN/inf pathology because the stored selection cut is on `pfRelIso03`, not `miniRelIso`. Treat these tails as acceptable for Phase 1, but Phase 2 should avoid using `miniRelIso` as a tight modeling observable without a dedicated data/MC tail check.
- Very small `pvNdof` values appear in several slices, with a minimum about `0.296` in `TTBar.root` and values below `1` in data, DY, VBF, and ZH samples. Because `pvNdof` is copied from the input PV branch and no PV-quality cut is apparent in the local ntuplizer, these values are unresolved rather than automatically suspicious. Phase 2 should either avoid using `pvNdof` in selections or add an explicit PV-quality validation if it becomes an input variable.
- The stored `nPV` ranges are broad but finite and plausible for 13 TeV pileup-like content in these small slices; no discontinuity or sentinel value is visible.


## Truth-Level Information

Truth-level support is assessed from branch names and tree content in the metadata inventory. The only `pdgId`-like branches found in the primary files are reconstructed lepton flavor identifiers (`l1pdgId` through `l4pdgId`); no primary branches matching generator/truth tokens (`gen`, `truth`, `lhe`, `mother`, `status`) were found. Phase 2 must not assume truth matching or particle-level closure is available from these ntuples without adding an external method or source.

## Pre-Applied Selections

The ntuples are not raw CMS MiniAOD/NanoAOD; they are flat ntuples produced by `h4l_ntuplize.py`. Therefore the `Events` tree entries are already after ntuplizer-level object/event construction. MC files include `Metadata` generated-event counts for normalization denominators; the ratio of `Events` rows to generated metadata rows is a first diagnostic of preselection/skimming. Data do not include a public inclusive denominator in Phase 1, so no data preselection efficiency is inferred from the target observable.

### Likely Content Boundary From Branches and Ntuplizer Code

The available branch content and the local `h4l_ntuplize.py` code imply that the flat `h4lTree` is a selected-candidate ntuple, not an event record with all reconstructed objects:

- Candidate boundary: each row contains one best four-lepton candidate with `m4l`, `mZ1`, `mZ2`, four selected leptons, and Z assignment labels. Alternate candidates and unselected leptons are not retained.
- Object boundary: selected muons/electrons have already passed pT/eta, impact-parameter, SIP3D, and `pfRelIso03` requirements in the ntuplizer. The stored ID/isolation variables are post-object-selection diagnostics, not raw object collections.
- Pairing boundary: the ntuplizer requires two same-flavor opposite-sign Z candidates, applies Z-mass and low-mass opposite-sign-pair requirements, chooses the Z1/Z2 pairing internally, and writes only that choice.
- Trigger boundary: `trigBits` records the listed HLT path decisions, but the local ntuplizer records the bitmask after candidate construction and does not itself reject rows solely because `trigBits==0`. Phase 2 must decide whether and how to impose trigger requirements.
- Missing-content boundary: no jet collections, MET, all-object collections, generator/truth records, or precomputed MELA/angular discriminants are present in the primary branch inventory. VBF categorization, truth-level closure, and matrix-element discriminants therefore require external recovery, recomputation from available lepton four-vectors, or formal downscoping.


## Exploration Figures

| Figure ID | PNG | Caption |
| --- | --- | --- |
| phase1_m4l_small_slice_shapes | figures/m4l_small_slice_shapes.png | $m_{4\ell}$ [GeV] small-slice shape comparison. The distributions use at most 1000 entries per primary ROOT file and are area-normalized only for Phase 1 shape reconnaissance, not for yield validation. Large differences here flag candidate variables for Phase 2/3 data-MC quality checks rather than final selection conclusions. |
| phase1_z1_mass_small_slice_shapes | figures/z1_mass_small_slice_shapes.png | $m_{Z1}$ [GeV] small-slice shape comparison. The distributions use at most 1000 entries per primary ROOT file and are area-normalized only for Phase 1 shape reconnaissance, not for yield validation. Large differences here flag candidate variables for Phase 2/3 data-MC quality checks rather than final selection conclusions. |
| phase1_z2_mass_small_slice_shapes | figures/z2_mass_small_slice_shapes.png | $m_{Z2}$ [GeV] small-slice shape comparison. The distributions use at most 1000 entries per primary ROOT file and are area-normalized only for Phase 1 shape reconnaissance, not for yield validation. Large differences here flag candidate variables for Phase 2/3 data-MC quality checks rather than final selection conclusions. |
| phase1_pt4l_small_slice_shapes | figures/pt4l_small_slice_shapes.png | $p_T^{4\ell}$ [GeV] small-slice shape comparison. The distributions use at most 1000 entries per primary ROOT file and are area-normalized only for Phase 1 shape reconnaissance, not for yield validation. Large differences here flag candidate variables for Phase 2/3 data-MC quality checks rather than final selection conclusions. |
| phase1_eta4l_small_slice_shapes | figures/eta4l_small_slice_shapes.png | $\eta_{4\ell}$ small-slice shape comparison. The distributions use at most 1000 entries per primary ROOT file and are area-normalized only for Phase 1 shape reconnaissance, not for yield validation. Large differences here flag candidate variables for Phase 2/3 data-MC quality checks rather than final selection conclusions. |
| phase1_leading_lepton_pt_small_slice_shapes | figures/leading_lepton_pt_small_slice_shapes.png | Leading lepton $p_T$ [GeV] small-slice shape comparison. The distributions use at most 1000 entries per primary ROOT file and are area-normalized only for Phase 1 shape reconnaissance, not for yield validation. Large differences here flag candidate variables for Phase 2/3 data-MC quality checks rather than final selection conclusions. |

## Code Reference

- `pixi run p1-metadata`
- `pixi run p1-recon-slice`
- `pixi run p1-preselection`
- `pixi run p1-hists`
- `pixi run p1-plots`
- `pixi run p1-artifacts`

## Open Issues for Phase 2

- Validate prompt-provided effective cross sections against public campaign metadata where possible; Phase 1 records them as user-provided, not independently verified.
- Decide whether downstream work should use the larger user-specified source files or the local copies; Phase 1 recommends the user-specified paths because they are the stated prompt inputs.
- If a required angular discriminator branch is absent, Phase 2/3 must compute angular observables from available four-lepton kinematics or document infeasibility.
