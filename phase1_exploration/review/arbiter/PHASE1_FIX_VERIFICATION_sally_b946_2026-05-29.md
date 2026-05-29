# Phase 1 Fix Verification

Session: `sally_b946`
Date: 2026-05-29

## Overall Verdict

ALL FIXED

This is a targeted verification of the findings in `PHASE1_REVIEW_odette_a6bb_2026-05-29.md` against the fixer report `FIX_REPORT_petra_11e2_2026-05-29.md` and current disk state. I did not perform a broad fresh review.

## Finding Verification

| Finding | Status | Evidence |
| --- | --- | --- |
| A1 density y-axis labels | FIXED | `phase1_exploration/src/plot_exploration.py:31-40` defines density labels for all six plotted observables, using `[GeV$^{-1}$]` for mass and pT variables and unitless density for `eta4l`; `plot_exploration.py:94` applies `density_ylabel(name)`. I inspected all six regenerated PNGs and confirmed y-axis labels are density-form labels: `(1/N)dN/dm4l [GeV^-1]`, `(1/N)dN/dmZ1 [GeV^-1]`, `(1/N)dN/dmZ2 [GeV^-1]`, `(1/N)dN/dpT4l [GeV^-1]`, `(1/N)dN/deta4l`, and `(1/N)dN/dpTlead [GeV^-1]`. Grep over current outputs, source, retrieval log, and `FIGURE_VALIDATION_*.md` found zero current instances of `Normalized entries`, `Normalized entities`, or `n_{4\\ell}` outside historical review text. |
| A2 integer/flag decoding | FIXED | `DATA_RECONNAISSANCE.md:3901-3935` now includes `Integer/Flag Interpretation and Residual Ambiguities`, targeted decoding attempts, decoded `finalState`, `zId`, electron `elCutBased`, boolean lepton-ID flags, and `trigBits`, plus the trigger bit map. The residual ambiguity is explicitly scoped to ROOT-file provenance against the local `h4l_ntuplize.py` revision. |
| A3 later CMS numeric citation | FIXED | `LITERATURE_SURVEY.md:24` now ties the 137 fb^-1 numbers to CMS-HIG-19-001 / EPJC 81 (2021) 488, names arXiv:2103.04956, and records the search trail. `LITERATURE_SURVEY.md:44`, `INPUT_INVENTORY.md:15-16`, and `retrieval_log.md:4,6` give the source pointer and retained CMS public page. |
| B1 data-quality extremes | FIXED | `DATA_RECONNAISSANCE.md:3969-3976` now assesses `pfRelIso03`, `miniRelIso` tails, very small `pvNdof`, and `nPV` ranges rather than only NaN/inf counts. The prose distinguishes acceptable Phase 1 behavior from Phase 2 caution/avoidance. |
| B2 preselection/content boundary | FIXED | `DATA_RECONNAISSANCE.md:3983-3995` now characterizes selected-candidate, object, pairing, trigger, and missing-content boundaries inferred from branch content and ntuplizer behavior. |
| B3 literature survey depth | FIXED | `LITERATURE_SURVEY.md:24-26` adds CMS-HIG-19-001 as an additional public comparison and states Phase 2-relevant methodological differences: full Run 2 statistics, lepton calibration/systematics, data-driven reducible background, and production/differential categorization depending on absent object content. |
| C1 figure validation notes | FIXED | All six `phase1_exploration/review/validation/FIGURE_VALIDATION_*.md` files are refreshed for the regenerated density-label figures. The stale `Normalized entities` and `n_{4\\ell}` text no longer appears in the current per-figure notes. |

## Pattern Search

Command scope: `phase1_exploration/outputs/*.md`, `phase1_exploration/outputs/FIGURES.json`, `phase1_exploration/review/validation/FIGURE_VALIDATION_*.md`, `phase1_exploration/src/plot_exploration.py`, `phase1_exploration/src/build_phase1_artifacts.py`, and `phase1_exploration/retrieval_log.md`.

Search terms: `Normalized entries`, `Normalized entities`, `n_{4\\ell}`.

Result: no matches in current outputs/current figure-validation notes/source/retrieval log. Matches exist only in the historical review file when the broader `review/validation` directory is searched.

## Claimed Command Verification

- `pixi run lint-plots`: PASS, `No plotting violations found in 8 file(s).`
- Figure registry smoke test: PASS, `figures_registered=6`, `missing=[]`, `empty=[]`, `stale=[]`, `orphan_pngs=[]`.
- `git diff --check`: PASS, no output.

## Next Fixer Actions

None. All listed findings are fixed.
