# Phase 1 Fix Report

Session: `petra_11e2`
Date: 2026-05-29

## Resolution Summary

| Finding | Status | Evidence |
| --- | --- | --- |
| A1 density y-axis labels | RESOLVED | `plot_exploration.py` now labels densities as `(1/N) dN/dx`, with GeV^-1 for mass/pT and unitless eta density. All six PNG/PDF figures and `FIGURES.json` were regenerated. |
| A2 integer/flag decoding | RESOLVED | `DATA_RECONNAISSANCE.md` now has `Integer/Flag Interpretation and Residual Ambiguities` decoding `finalState`, electron `elCutBased`, `zId`, and `trigBits`, with targeted attempts and a provenance caveat. |
| A3 uncited later CMS numbers | RESOLVED | `LITERATURE_SURVEY.md`, `INPUT_INVENTORY.md`, source index, and `retrieval_log.md` now cite CMS-HIG-19-001 / EPJC 81 (2021) 488, arXiv:2103.04956, DOI 10.1140/epjc/s10052-021-09200-x, with search trail. |
| B1 data-quality extremes | RESOLVED | `DATA_RECONNAISSANCE.md` now assesses isolation tails, small `pvNdof`, and `nPV` ranges as acceptable/unresolved with Phase 2 handling. |
| B2 preselection/content boundary | RESOLVED | `DATA_RECONNAISSANCE.md` now summarizes likely selected-candidate, object, pairing, trigger, and missing-content boundaries. |
| B3 literature survey depth | RESOLVED | `LITERATURE_SURVEY.md` now includes CMS-HIG-19-001 as an additional cited reference analysis and lists methodological differences Phase 2 should account for. |
| C1 validation-note inaccuracies | RESOLVED | All six figure-validation notes were refreshed for regenerated density-label figures; eta x-axis and `Normalized entities` inaccuracies were corrected. |

## Files Changed

- `phase1_exploration/src/plot_exploration.py`
- `phase1_exploration/src/build_phase1_artifacts.py`
- `phase1_exploration/outputs/DATA_RECONNAISSANCE.md`
- `phase1_exploration/outputs/INPUT_INVENTORY.md`
- `phase1_exploration/outputs/LITERATURE_SURVEY.md`
- `phase1_exploration/outputs/FIGURES.json`
- `phase1_exploration/outputs/figures/*.png`
- `phase1_exploration/outputs/figures/*.pdf`
- `phase1_exploration/retrieval_log.md`
- `phase1_exploration/review/validation/FIGURE_VALIDATION_*.md`
- `phase1_exploration/logs/fixer_petra_11e2_20260529T190832Z.md`
- `experiment_log.md`

## Commands Run

```bash
pixi run py -m py_compile phase1_exploration/src/plot_exploration.py phase1_exploration/src/build_phase1_artifacts.py
pixi run p1-plots
pixi run p1-artifacts
pixi run lint-plots
pixi run py - <<'PY'
# figure registry smoke test
PY
```

## Validation Output

- `pixi run py -m py_compile ...`: passed.
- `pixi run p1-plots`: completed; regenerated 6 figures and `FIGURES.json`.
- `pixi run p1-artifacts`: completed; regenerated Phase 1 markdown artifacts and retrieval log.
- `pixi run lint-plots`: `No plotting violations found in 8 file(s).`
- Figure registry smoke test:
  - `figures_registered=6`
  - `missing=[]`
  - `empty=[]`
  - `stale=[]`
  - `orphan_pngs=[]`
- Visual check: `m4l_small_slice_shapes.png` shows `(1/N) dN/dm4l [GeV^-1]`; `eta4l_small_slice_shapes.png` shows `(1/N) dN/deta4l`.
- Stale-label grep: no stale `Normalized entries`, `Normalized entities`, or `n_{4\\ell}` references remain outside review/fix-report documentation.

## Commit Note

The fixes were tightly coupled through the artifact generator: A2, A3, B1, B2, and B3 all live in `build_phase1_artifacts.py` and regenerate the same markdown outputs, while A1 regenerates the common figure registry consumed by that artifact build. I therefore made one scoped final commit instead of per-finding commits to avoid intermediate commits with internally inconsistent regenerated artifacts.

## Remaining Risks

- The flag interpretation assumes the provided ROOT files were produced by the local `h4l_ntuplize.py` revision. The branch names and values match, but Phase 2 should revise the map if it changes data source or finds contradictory provenance metadata.
- Small `pvNdof` values are documented as unresolved for selection use; Phase 2 should not use `pvNdof` without a dedicated validation.
