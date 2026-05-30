PASS

# Doc 4a BibTeX Validation

Session: `viktor_eac3`  
Date: `2026-05-30`

Validated:
- `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex`
- `references.bib`
- `analysis_note/ANALYSIS_NOTE_doc4a_v1.log`

## Summary

- Cited keys found in LaTeX: 16
- Matching BibTeX entries present: 16 / 16
- Missing cited entries: 0
- Duplicate BibTeX keys: 0
- Undefined citation warnings in LaTeX log: 0 found

## Per-key status

| Key | Entry present | Metadata plausibility | Status |
|---|---|---:|---|
| `ATLASDiscovery2012` | yes | plausible DOI/arXiv/title/year combination | PASS |
| `CMS-HIG-16-041` | yes | plausible DOI/arXiv/title/year combination | PASS |
| `CMS-HIG-19-001` | yes | plausible DOI/arXiv/title/year combination | PASS |
| `CMSDetector` | yes | plausible DOI/title/year combination | PASS |
| `CMSDiscovery2012` | yes | plausible DOI/arXiv/title/year combination | PASS |
| `CMSOpenData` | yes | plausible portal citation | PASS |
| `Cowan2011` | yes | plausible DOI/arXiv/title/year combination | PASS |
| `GEANT4` | yes | plausible DOI/title/year combination | PASS |
| `HistFactory` | yes | plausible CERN report metadata | PASS |
| `Minuit` | yes | plausible DOI/title/year combination | PASS |
| `PDG2024` | yes | plausible DOI/title/year combination | PASS |
| `POWHEG` | yes | plausible DOI/arXiv/title/year combination | PASS |
| `PYTHIA8` | yes | plausible DOI/arXiv/title/year combination | PASS |
| `ScikitLearn` | yes | plausible journal/title/year/url combination | PASS |
| `XGBoost` | yes | plausible DOI/arXiv/title/year combination | PASS |
| `pyhf_joss` | yes | plausible DOI/title/year combination | PASS |

## Findings

### (C) Unused bibliography entry

- `CMS-LUM-20-001` exists in `references.bib` but is not cited in `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex`.

## Verdict basis

No Category A issues found. I found no missing or obviously fabricated citations, and the LaTeX log shows no undefined citation warnings. The only issue is one orphaned BibTeX entry, which is non-blocking.
