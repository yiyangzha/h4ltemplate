# Phase 1 Exploration Plan

Session: `albert_0f97`
Started: 2026-05-29T18:18:33Z

## Scope

Produce the Phase 1 exploration and literature artifacts for the CMS Open Data
2017 H->4l mass measurement. MCP literature tools are disabled by
`TOGGLES.md`, so the literature workflow will use public web, INSPIRE/arXiv,
DOI pages, CMS public references, and PDG/public tables where accessible.

The executor owns only `phase1_exploration/**`, root `experiment_log.md`, and
root or phase retrieval/session logs. Later phase artifacts are read-only.

## Workstream A: Data Reconnaissance

1. Inspect filesystem structure under the configured data and MC directories
   from `paths.json`, preferring local copies in this analysis root when they
   mirror the source paths.
2. Write `inspect_root_metadata.py` to structurally inspect every ROOT file
   with `uproot`: file size, keys, every tree, tree entries, and every branch
   with interpretation/type information. This structural scan may cover all
   files, but it will not process full event arrays.
3. Write `recon_small_slice.py` to load only a small slice of approximately
   1000 entries per physics tree and survey branch shapes, NaN/inf counts,
   simple numeric ranges, key candidate variables, and unique values for
   integer/boolean/flag-like branches.
4. Write `check_preselection_and_coverage.py` to combine metadata tree event
   counts with user-provided effective sample cross sections, identify
   generator/process/tune/energy coverage from names and metadata, compare
   data event counts with rough luminosity-scaled expectations where a
   citable or user-provided normalization exists, and flag preselection
   evidence without deriving analysis constants from the target observable.
5. Write `make_exploration_histograms.py` to create compact machine-readable
   histogram summaries for key variables from small slices. Candidate variables
   will be discovered from branch names, prioritizing 4-lepton mass, lepton
   kinematics, jet multiplicity/VBF-like variables, and angular variables.
6. Write `plot_exploration.py` to render publication-quality Phase 1 figures
   from the histogram summaries using `matplotlib`, `mplhep`, and `hist`, save
   both PDF and PNG outputs, and update `outputs/FIGURES.json`. Each PNG will
   be logged as `FIGURE_READY: <path>`.
7. Write `build_phase1_artifacts.py` to assemble
   `DATA_RECONNAISSANCE.md`, `INPUT_INVENTORY.md`, and
   `LITERATURE_SURVEY.md` from JSON summaries and retrieved source notes.

## Workstream B: Literature and Inputs

1. Record MCP-disabled status in the session log and retrieval log; no MCP tool
   calls will be made.
2. Search public sources for the reference CMS analysis
   `JHEP 11 (2017) 047` / `CMS-HIG-16-041`, including paper, arXiv, DOI, and
   public result pages. Extract fit mass window, event categories, fit method,
   published mass/signal-strength/context values, and comparability limits.
3. Search public CMS luminosity references for 2017 pp data luminosity
   information and document whether the prompt's 10 fb^-1 target is a user
   analysis subset rather than a full-year certified luminosity.
4. Search public PDG/CERN/HEP references for needed masses, widths, branching
   fractions, or world-average comparison values. Every numeric input will
   carry source and section/table/page where available.
5. Seed `INPUT_INVENTORY.md` with the user-provided effective MC sample cross
   sections and metadata-generated event counts, explicitly marking user
   prompt values as `FOUND_USER_PROVIDED` until Phase 2/3 validates them
   against public generator records.

## PDF Toolchain Test

Create a temporary `analysis_note/test_build.tex`, run
`pixi run build-pdf analysis_note/test_build.tex` or equivalent tectonic task,
record the result, and remove the stub after a successful compile or after
documenting the failure.

## Self-Checks Before Completion

1. Run all Phase 1 pixi tasks that are implemented:
   `p1-metadata`, `p1-recon-slice`, `p1-preselection`, `p1-hists`,
   `p1-plots`, `p1-pdf-test`, and `p1-artifacts`.
2. Run `pixi run lint-plots`.
3. Verify `outputs/FIGURES.json` entries point to non-empty PDF/PNG files and
   that there are no orphan PNGs in `outputs/figures/`.
4. Grep Phase 1 scripts for forbidden plotting patterns and bare `print()`.
5. Re-read the three output artifacts and verify every Phase 1 checklist item
   is answered, or documented as infeasible with search/attempt evidence.

