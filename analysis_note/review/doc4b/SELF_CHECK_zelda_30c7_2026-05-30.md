# Doc 4b Self-Check

Session: `zelda_30c7`  
Date: 2026-05-30

## Compile

- Command: `pixi run tectonic --keep-logs analysis_note/ANALYSIS_NOTE_doc4b_v1.tex`
- PDF: `analysis_note/ANALYSIS_NOTE_doc4b_v1.pdf`
- Page count: 74 pages, from `analysis_note/ANALYSIS_NOTE_doc4b_v1.log`
- BibTeX: PASS. `analysis_note/ANALYSIS_NOTE_doc4b_v1.blg` was written.
- Undefined citations/cross-references: PASS. Grep found no `??`, `Citation`, or `undefined` in source/log.
- Overfull boxes: PASS. Grep found no `Overfull` in source/log.
- Remaining TeX warnings: underfull hboxes in wrapped tables/paragraphs only.

## Figure and Table Checks

- Figure references: 56 total, 56 unique, 0 missing or empty.
- Required Phase 4b figures included: PASS.
  - `partial_m4l_broad_inclusive`
  - `partial_m4l_70_170_categories`
  - `partial_expected_mu_comparison`
  - `partial_nuisance_pulls`
  - `partial_nuisance_impacts`
  - `partial_binning_stability`
  - `partial_split_consistency`
- Tables: 18.
- Display equations: 11.

## Key Number Consistency

Verified the Doc 4b headline values against `analysis_note/results/partial_parameters.json`, `partial_validation.json`, and `partial_covariance.json`:

- Fit window: `70 < m4l < 170 GeV`, including the Z peak.
- Fixed seed: `9417`.
- Events: `20 / 203`.
- Effective luminosity: `1.0 fb^-1`.
- 10% result: `mu = 0.0 +1.3548619813595435`, lower interval at the physical boundary.
- GoF: `chi2/ndf = 31.755141641709276 / 38`, `p = 0.752432307059706`.
- Poisson deviance: `26.768200301302684`, deviance p-value `0.9137772503189814`.
- Expected-vs-partial pull: `-0.679474677941247`, compatible within two sigma.
- Normalization policy: MC scaled to partial luminosity by `0.1`; no data-integral normalization.

Numbers consistency lint: verified the headline partial-result values across the abstract, Change Log, Results tables, Comparison, Conclusions, and Cross-check text. No stale expected-only claims remain where they conflict with the 10% result.

## Stale-Window Check

- Targeted grep for claims that the 10% observed/partial fit uses `105-140`: PASS, no matches.
- The note still discusses `105-140` where appropriate for the Phase 4a expected baseline and earlier CMS-like instruction; those mentions are explicitly separated from the Phase 4b 10% result.

## Limitations Preserved

- The 10% best fit lands at the physical boundary `mu=0`.
- The deterministic split is a proxy, not a CMS run-period validation.
- VBF categories remain downscoped because jet/VBF information is unavailable.
- MVA/NN categories remain rejected and are not used nominally.
- DY+jets remains the reducible fake-background proxy rather than a full data-driven fake-rate estimate.
- Grouped MC-stat treatment remains an approximation, not full bin-by-bin HistFactory `staterror`.
- No full observed-data result is reported yet; Phase 4c remains pending.

## Commands Run

- `pixi run tectonic --keep-logs analysis_note/ANALYSIS_NOTE_doc4b_v1.tex`
- `pixi run py - <<'PY' ... figure/table/equation/page checks ... PY`
- `grep -nE '\\?\\?|Citation|undefined|Overfull' analysis_note/ANALYSIS_NOTE_doc4b_v1.log analysis_note/ANALYSIS_NOTE_doc4b_v1.tex || true`
- `grep -nE '10\\\\% (observed|partial|fit).*105|10% (observed|partial|fit).*105|uses .*105.*10\\\\%|uses .*105.*10%' analysis_note/ANALYSIS_NOTE_doc4b_v1.tex || true`
- `git diff --check`

## Verdict

PASS. Doc 4b TeX and PDF are ready for commit.
