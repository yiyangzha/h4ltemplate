# Phase 1 Review

Session: `odette_a6bb`  
Date: `2026-05-29`

## Verdict

ITERATE

Phase 1 is close, and the core artifact set exists, but I do not pass it yet. I independently checked the required artifacts, reread the VERIFY/self-review chain, reran `pixi run lint-plots`, read every Phase 1 PNG, and inspected the Phase 1 scripts. The main blockers are:

1. all six figures have a mechanical y-axis labeling error,
2. the integer/flag survey is enumerated but not actually interpreted,
3. `LITERATURE_SURVEY.md` introduces uncited numeric results for a later CMS result.

## Checks That Passed

- Required Phase 1 artifacts exist: `DATA_RECONNAISSANCE.md`, `INPUT_INVENTORY.md`, `LITERATURE_SURVEY.md`, and `FIGURES.json`.
- The MCP-disabled path was respected throughout: `INPUT_INVENTORY.md:32-34`, `LITERATURE_SURVEY.md:8-10`, and `retrieval_log.md:3-8` all consistently document `MCP_ALPHAXIV=false` and `MCP_LEP_CORPUS=false`.
- The ROOT inventory and branch schema are materially present, including the Phase 2-relevant capability summary at `DATA_RECONNAISSANCE.md:3190-3203`.
- The key Phase 2 risks are surfaced: no jet/VBF branches, no precomputed MELA/angular discriminants, and no truth-level branches (`DATA_RECONNAISSANCE.md:3198-3203`, `3932-3938`, `3960-3964`).
- `FIGURES.json` registers six figures (`FIGURES.json:1-122`), and I confirmed all six PNGs/PDFs exist on disk and render cleanly.
- `pixi run lint-plots` passes.

## A Findings

### A1. All six figures label a density as `Normalized entries`, which is mechanically wrong.

Evidence:

- `phase1_exploration/src/plot_exploration.py:67-70` computes
  `density = counts / (total * widths)` and `yerr = sqrt(counts) / (total * widths)`.
- `phase1_exploration/src/plot_exploration.py:81-82` then labels the y-axis as `Normalized entries`.

That label is incorrect for every rendered plot I checked:

- `m4l_small_slice_shapes.png`
- `z1_mass_small_slice_shapes.png`
- `z2_mass_small_slice_shapes.png`
- `pt4l_small_slice_shapes.png`
- `eta4l_small_slice_shapes.png`
- `leading_lepton_pt_small_slice_shapes.png`

For the mass and `p_T` plots, the y-axis should carry inverse-GeV units if the current density definition is kept. For `eta4l`, the problem is still present: the code plots a bin-width-normalized density, not raw normalized entries.

Concrete fix:

- Either keep the current normalization and relabel to a density form, e.g. `1/N dN/dx` with units where needed, or
- drop the division by `widths` and truly plot normalized per-bin entries.

This is also a contradiction of the figure-validation PASS notes, which treat the current y-axis label as correct.

### A2. The integer/flag survey is listed, but the non-trivial codes are not understood or documented.

Evidence:

- The survey exists at `DATA_RECONNAISSANCE.md:3205-3898`.
- Representative non-trivial codes are present, but not decoded:
  - `finalState` at `3213`, `3269`, `3327`
  - electron cut-based working-point integers at `3215`, `3226`, `3237`, `3248`
  - `zId` flags at `3224`, `3246`
  - `trigBits` bitmasks at `3260`, `3318`, `3840`, `3898`
- After the large table block, the document moves directly to `## Data Quality Assessment` at `3901` with no interpretation section for these codes.

Phase 1 required more than printing distinct values. Phase 2 will need to know what these branch values mean before it can safely use them in selection logic, category definitions, or trigger/ID handling.

Concrete fix:

- Add a short interpretation subsection after the unique-value survey that decodes the important flags and integers, or explicitly documents which ones remain unresolved after targeted investigation.
- At minimum: decode `finalState`, the electron cut-based scale, `zId`, and the structure/meaning of `trigBits`.

### A3. `LITERATURE_SURVEY.md` includes uncited numeric results for a later CMS publication.

Evidence:

- `LITERATURE_SURVEY.md:24` quotes `mu = 0.94 +/- 0.07 (stat) +0.09/-0.08 (syst)` and `2.84 +0.23/-0.22 (stat) +0.26/-0.21 (syst) fb at mH = 125.38 GeV`.
- The source index at `LITERATURE_SURVEY.md:37-44` lists only CMS-HIG-16-041, HEPData-80189, CMS-LUM-20-001, and PDG-2024. There is no citation for the later 137 fb^-1 CMS result.

Under the analysis rules, uncited numeric inputs are not acceptable.

Concrete fix:

- Add the specific paper/HEPData citation and section/table pointer for the later CMS result, plus the search trail that found it, or
- remove the uncited numbers.

## B Findings

### B1. The data-quality section is narrower than the claims made for it.

Evidence:

- `DATA_RECONNAISSANCE.md:3901-3930` reports only entry counts plus total NaN/inf counts.
- The same artifact already surfaces extreme values that deserve explicit comment, for example:
  - large lepton isolation tails at `3251`, `3307`, `3887`
  - very small `pvNdof` values at `3259`, `3316`, `3838`, `3896`

I am not asserting these values are wrong. I am saying the document currently jumps from “we checked data quality” to a NaN/inf summary without explaining whether these extremes are expected, acceptable, or suspicious.

Concrete fix:

- Add a short prose assessment of the obvious outliers/extremes already visible in the slice tables/JSON and state whether they are expected detector/reconstruction behavior.

### B2. The preselection discussion identifies that the ntuples are skimmed, but it does not yet characterize what was probably pre-applied.

Evidence:

- `DATA_RECONNAISSANCE.md:3936-3938` says the files are flat ntuples and therefore already after ntuplizer-level object/event construction.
- That is useful, but it stops short of inferring what content boundaries or likely object/event requirements are already baked in.

Phase 2 can still proceed, but strategy work will benefit from a tighter statement of what the current ntuples can and cannot represent.

Concrete fix:

- Expand the preselection section with a short “likely content boundary” summary derived from branch availability and event content.

### B3. The literature survey is usable as a seed, but thin for Phase 2 strategy.

Evidence:

- The search trail at `LITERATURE_SURVEY.md:8-10` is shallow.
- The document does identify the key reference analysis and one later comparison, but it does not yet give a robust set of reference analyses or a systematic-method summary.

Concrete fix:

- Add at least one more cited reference analysis or public comparison result and a short note on the methodological differences Phase 2 should care about.

## C Findings

### C1. Two of the existing per-figure validation notes contain small factual inaccuracies.

I confirm the overall visual quality judgments, but I contradict parts of the written notes:

- `FIGURE_VALIDATION_lena_cc50.md:15` says the eta plot x-axis label is `n_{4\ell}`. The rendered label is `\eta_{4\ell}`.
- `FIGURE_VALIDATION_hana_1b43.md:19` says `Normalized entities`; the rendered label says `Normalized entries`.

If the figures are regenerated for A1, refresh these notes as well.

## Figure-by-Figure Check

I visually inspected every PNG in `phase1_exploration/outputs/figures/`.

- `m4l_small_slice_shapes.png`: visual PASS. Readable, no label overlap, legend placement acceptable. Mechanical FAIL under A1.
- `z1_mass_small_slice_shapes.png`: visual PASS. Readable, legend clear, no clipping. Mechanical FAIL under A1.
- `z2_mass_small_slice_shapes.png`: visual PASS. Readable, no obvious rendering defects. Mechanical FAIL under A1.
- `pt4l_small_slice_shapes.png`: visual PASS. Tail remains readable; no overlap issues. Mechanical FAIL under A1.
- `eta4l_small_slice_shapes.png`: visual PASS. Readable and coherent; no overlap issues. Mechanical FAIL under A1 because the axis still labels a density as entries.
- `leading_lepton_pt_small_slice_shapes.png`: visual PASS. Busy but still legible. Mechanical FAIL under A1.

## Per-Figure Validation Cross-Check

- `FIGURE_VALIDATION_hana_1b43.md`: mostly confirmed visually, but I contradict the implied axis-label correctness because of A1.
- `FIGURE_VALIDATION_hugo_9313.md`: visual PASS confirmed; axis-label correctness contradicted by A1.
- `FIGURE_VALIDATION_ingrid_cf26.md`: visual PASS confirmed; axis-label correctness contradicted by A1.
- `FIGURE_VALIDATION_jasper_8a6a.md`: visual PASS confirmed; axis-label correctness contradicted by A1.
- `FIGURE_VALIDATION_lena_cc50.md`: visual PASS confirmed, but the quoted x-axis label is wrong and axis-label correctness is contradicted by A1.
- `FIGURE_VALIDATION_magnus_b4f3.md`: visual PASS confirmed; axis-label correctness contradicted by A1.

## Phase 2 Readiness

After the A findings are resolved, the Phase 1 outputs should be adequate to seed Phase 2. The important strategic risks are already visible:

- no jet/VBF branches in the current ntuples,
- no precomputed angular/MELA branches,
- no truth-level information,
- primary and local copies differ materially.

Those are the right issues for Phase 2 to confront. The current review verdict is ITERATE because the remaining problems are local and should be fixed before the strategy phase starts building on them.
