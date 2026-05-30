# Doc 4a Self-Critique

Session: `odette_354d`  
Date: 2026-05-30

## Referee-Style Criticisms and Fixes

### Expected-only staging

Potential criticism: a reader could mistake the note for an observed-data result because the note discusses CMS Open Data and includes data/MC selection plots.

Finding: addressed in the abstract, Change Log, Expected Results, Statistical Method, and figure captions. The expected result is explicitly Asimov-only and no observed Open Data counts are used as pseudo-data.

Fix applied: none needed.

### CMS-HIG-16-041 comparison

Potential criticism: the note could imply that the result was tuned to CMS-HIG-16-041 because the expected central value is near the CMS value.

Finding: the comparison section states that CMS-HIG-16-041 and CMS-HIG-19-001 are not fit inputs and that the pull is contextual only. The precision ratio is quantitative: 3.193 relative to CMS-HIG-16-041.

Fix applied: none needed.

### VBF and MVA/NN downscopes

Potential criticism: mentioning VBF signal templates could be mistaken for a VBF category measurement.

Finding: the note distinguishes VBF signal component templates from VBF event categories. It states no VBF category exists, no lepton-only category is labeled VBF, and no jet/VBF systematics are propagated.

Fix applied: corrected an awkward approach-comparison caption so it clearly says S2 failed promotion gates and S1 is nominal.

### Low-count corruption sensitivity

Potential criticism: the +20% corruption rejection could be over-read as a symmetric corruption-sensitivity pass.

Finding: the Cross-checks section, low-count figure caption, corruption table caption, Conclusions, Known Limitations, and Limitation Index all state that the -20% test is `documented_low_count_infeasible` after three final-state-aligned attempts and is not passed.

Fix applied: none needed.

### Grouped MC-stat downscope

Potential criticism: grouped MC-stat normalization nuisances might be read as full HistFactory bin-by-bin staterror.

Finding: the Corrections, Systematics, Conclusions, and Limitation Index explicitly call this a grouped approximation/downscope, not full bin-by-bin `staterror`.

Fix applied: none needed.

### Figure/caption window clarity

Potential criticism: a broad-window appendix caption could blur the 70--170 GeV validation display and 105--140 GeV inference window.

Finding: one appendix caption used loose wording about the fit-window handoff.

Fix applied: revised the caption to state that the broad display is sideband/validation context only and that separate 105--140 GeV templates define inference.

### Text quality

Potential criticism: a typo in the signal-production subsection could distract from the systematic explanation.

Finding: `Signal productionn` typo.

Fix applied: corrected to `Signal production`.

## Final Critic Verdict

After the fixes above, the strongest remaining limitations are physics limitations already documented in the note: expected-only staging, no VBF category, rejected MVA/NN categories, DY+jets fake proxy, grouped MC-stat approximation, and the non-passing -20% corruption sensitivity. These are supported by Phase 3/4a JSON/artifact evidence rather than asserted as prose-only claims.
