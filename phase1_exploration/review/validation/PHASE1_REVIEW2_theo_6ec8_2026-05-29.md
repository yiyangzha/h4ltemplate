# Phase 1 Review

Session: `theo_6ec8`  
Date: `2026-05-29`

## Verdict

PASS

This is a fresh Phase 1 review after the ITERATE fix cycle, not only a targeted fix verification. I read the current Phase 1 artifacts and prior review chain in full, reran `pixi run lint-plots` myself, inspected the current plotting script, and visually checked every current Phase 1 PNG. I find the previous blockers fixed, and the current Phase 1 outputs are sufficient to seed Phase 2 strategy work.

## Checks That Passed

- Required Phase 1 artifacts exist and are complete enough for strategy input: `DATA_RECONNAISSANCE.md`, `INPUT_INVENTORY.md`, `LITERATURE_SURVEY.md`, and `FIGURES.json` are all present and populated. The reconnaissance artifact contains the required summary, sample inventory/MC coverage, branch schema, capability scan, integer/flag survey plus interpretation, data-quality section, truth-level assessment, preselection/content boundary, figure registry, and Phase 2 open issues ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:6`](../../outputs/DATA_RECONNAISSANCE.md), [`:28`](../../outputs/DATA_RECONNAISSANCE.md), [`:47`](../../outputs/DATA_RECONNAISSANCE.md), [`:3190`](../../outputs/DATA_RECONNAISSANCE.md), [`:3205`](../../outputs/DATA_RECONNAISSANCE.md), [`:3901`](../../outputs/DATA_RECONNAISSANCE.md), [`:3938`](../../outputs/DATA_RECONNAISSANCE.md), [`:3979`](../../outputs/DATA_RECONNAISSANCE.md), [`:3983`](../../outputs/DATA_RECONNAISSANCE.md), [`:3998`](../../outputs/DATA_RECONNAISSANCE.md), [`:4018`](../../outputs/DATA_RECONNAISSANCE.md)).
- Sample inventory and MC coverage are documented with event entries, metadata denominators, prompt-provided effective cross sections, nominal weights, generators, tune, and `sqrt(s)` ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:28-45`](../../outputs/DATA_RECONNAISSANCE.md)).
- The branch schema is materially complete. The artifact inventories every file, tree, branch, type, interpretation, and entry count; the primary data file alone shows the expected full structure, and the same pattern is repeated for the remaining primary and local files ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:49-175`](../../outputs/DATA_RECONNAISSANCE.md)).
- The integer/flag survey is no longer only a dump. It now includes an interpretation section that decodes `finalState`, `zId`, electron cut-based working points, boolean ID flags, and the `trigBits` bitmask, with an explicit provenance caveat for Phase 2 ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:3901-3935`](../../outputs/DATA_RECONNAISSANCE.md)).
- Data quality is documented at the right Phase 1 level: the slice-based NaN/inf scan is clean, and the visible outlier discussion now covers `pfRelIso03`, `miniRelIso`, `pvNdof`, and `nPV` ranges instead of claiming “checked” without interpretation ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:3938-3976`](../../outputs/DATA_RECONNAISSANCE.md)).
- Truth-level support and content boundaries are stated clearly. The artifact explicitly says no truth/generator branches were found and documents that the ntuple is a selected-candidate flat ntuple with no jet collections, MET, all-object collections, truth records, or precomputed MELA/angular discriminants ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:3979-3995`](../../outputs/DATA_RECONNAISSANCE.md)).
- The main Phase 2 feasibility risks are surfaced where they belong: no jet/VBF observables in the primary branch inventory, no precomputed MELA/angular discriminants, no truth-level branches, differing primary vs local copies, and prompt-provided cross sections still awaiting public validation ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:10-26`](../../outputs/DATA_RECONNAISSANCE.md), [`:3190-3203`](../../outputs/DATA_RECONNAISSANCE.md), [`:4018-4022`](../../outputs/DATA_RECONNAISSANCE.md), [`phase1_exploration/outputs/INPUT_INVENTORY.md:22-33`](../../outputs/INPUT_INVENTORY.md)).
- The MCP-disabled path is respected consistently. `TOGGLES.md` sets `MCP_ALPHAXIV=false` and `MCP_LEP_CORPUS=false` ([`TOGGLES.md:34-72`](../../../TOGGLES.md)); the literature artifacts record that no MCP tools were used and show the public-web fallback search trail ([`phase1_exploration/outputs/LITERATURE_SURVEY.md:6-10`](../../outputs/LITERATURE_SURVEY.md), [`phase1_exploration/outputs/INPUT_INVENTORY.md:34-36`](../../outputs/INPUT_INVENTORY.md), [`phase1_exploration/retrieval_log.md:1-10`](../../retrieval_log.md)).
- The CMS-HIG-16-041 and CMS-HIG-19-001 numbers called out in the previous review are now backed by explicit public-source provenance in both the literature survey and input inventory. The HIG-19-001 signal-strength and fiducial-cross-section values are cited on disk with a retained public page and search trail ([`phase1_exploration/outputs/LITERATURE_SURVEY.md:22-26`](../../outputs/LITERATURE_SURVEY.md), [`:39-48`](../../outputs/LITERATURE_SURVEY.md), [`phase1_exploration/outputs/INPUT_INVENTORY.md:15-16`](../../outputs/INPUT_INVENTORY.md)).
- Figure registry coverage is coherent: `FIGURES.json` registers six current Phase 1 figures with matching captions and observable names ([`phase1_exploration/outputs/FIGURES.json:1-122`](../../outputs/FIGURES.json)).

## Previous Findings Rechecked

- A1 fixed: the plotting script now computes densities with explicit propagated `yerr` and labels the y-axis in density form for each observable ([`phase1_exploration/src/plot_exploration.py:31-40`](../../src/plot_exploration.py), [`:81-95`](../../src/plot_exploration.py)).
- A2 fixed: the integer/flag interpretation block is present and usable for Phase 2 ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:3901-3935`](../../outputs/DATA_RECONNAISSANCE.md)).
- A3 fixed: the later CMS result is now cited in `LITERATURE_SURVEY.md`, `INPUT_INVENTORY.md`, and the retrieval log ([`phase1_exploration/outputs/LITERATURE_SURVEY.md:24`](../../outputs/LITERATURE_SURVEY.md), [`phase1_exploration/outputs/INPUT_INVENTORY.md:15-16`](../../outputs/INPUT_INVENTORY.md), [`phase1_exploration/retrieval_log.md:4-6`](../../retrieval_log.md)).
- B1 and B2 fixed: the data-quality extremes and the likely content boundary are now described explicitly instead of only implied ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:3969-3976`](../../outputs/DATA_RECONNAISSANCE.md), [`:3987-3995`](../../outputs/DATA_RECONNAISSANCE.md)).
- B3 fixed: the literature survey now includes an additional useful public comparison and explains why it matters for Phase 2 ([`phase1_exploration/outputs/LITERATURE_SURVEY.md:22-26`](../../outputs/LITERATURE_SURVEY.md)).
- C1 fixed: the current figure-validation notes are refreshed and consistent with the regenerated figures ([`phase1_exploration/review/validation/FIGURE_VALIDATION_hana_1b43.md:1-20`](./FIGURE_VALIDATION_hana_1b43.md), [`FIGURE_VALIDATION_hugo_9313.md:1-24`](./FIGURE_VALIDATION_hugo_9313.md), [`FIGURE_VALIDATION_ingrid_cf26.md:1-22`](./FIGURE_VALIDATION_ingrid_cf26.md), [`FIGURE_VALIDATION_jasper_8a6a.md:1-20`](./FIGURE_VALIDATION_jasper_8a6a.md), [`FIGURE_VALIDATION_lena_cc50.md:1-21`](./FIGURE_VALIDATION_lena_cc50.md), [`FIGURE_VALIDATION_magnus_b4f3.md:1-21`](./FIGURE_VALIDATION_magnus_b4f3.md)).

## Plot-Code Check

I reran `pixi run lint-plots` and got `No plotting violations found in 8 file(s).`

The current plotting implementation also passes direct mechanical inspection against the validator checklist:

- `mh.style.use("CMS")` is applied ([`phase1_exploration/src/plot_exploration.py:12`](../../src/plot_exploration.py)).
- Single-panel figures use `figsize=(10, 10)` ([`phase1_exploration/src/plot_exploration.py:62`](../../src/plot_exploration.py)).
- No `set_title`, `tight_layout`, `constrained_layout`, or colorbar misuse is present.
- Axis labels are set explicitly, with units where applicable, and the normalized distributions use explicit propagated uncertainties through `ax.errorbar(...)` rather than the `sqrt(N)` trap ([`phase1_exploration/src/plot_exploration.py:81-95`](../../src/plot_exploration.py)).
- Legend font size is relative, not absolute, and `mpl_magic(ax)` is called to keep the legend out of the data ([`phase1_exploration/src/plot_exploration.py:95-96`](../../src/plot_exploration.py)).
- The experiment label is present and clearly marked as open data/simulation context rather than an official CMS result ([`phase1_exploration/src/plot_exploration.py:97-105`](../../src/plot_exploration.py)).
- Both PDF and PNG outputs are saved with `bbox_inches="tight", dpi=200, transparent=True`, and the figure is closed afterward ([`phase1_exploration/src/plot_exploration.py:106-110`](../../src/plot_exploration.py)).

## Figure-by-Figure Check

I visually inspected every current PNG in `phase1_exploration/outputs/figures/`.

- `m4l_small_slice_shapes.png`: PASS. Density label is corrected, text is legible, the legend sits in an empty upper-right region, and no label or point overlap is visible.
- `z1_mass_small_slice_shapes.png`: PASS. Readable at rendered size, density label is correct, and the plot remains visually clean despite the narrow Z peak.
- `z2_mass_small_slice_shapes.png`: PASS. Readable, no clipping or legend collision, and the denser low-mass region is still interpretable.
- `pt4l_small_slice_shapes.png`: PASS. Tail remains legible, the error bars look reasonable for sparse normalized slices, and there is no obvious rendering artifact.
- `eta4l_small_slice_shapes.png`: PASS. The corrected unitless-density label is present, the broad y-range is still readable, and the legend stays off the plotted points.
- `leading_lepton_pt_small_slice_shapes.png`: PASS. This is the busiest of the six, but the text is readable, the legend is acceptable, and I do not see malformed or suspiciously uniform error bars.

## Residual Risks for Phase 2

These are real constraints, but they are documented strategy inputs rather than Phase 1 blockers:

- The primary and local ROOT copies differ materially in size and tree entries. Phase 2 must freeze one source choice and not mix them ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:10-26`](../../outputs/DATA_RECONNAISSANCE.md)).
- The effective MC cross sections are still user-provided inputs, not independently validated campaign metadata. Phase 2 should verify them before treating yield normalization as settled ([`phase1_exploration/outputs/INPUT_INVENTORY.md:22-33`](../../outputs/INPUT_INVENTORY.md), [`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:4020`](../../outputs/DATA_RECONNAISSANCE.md)).
- No jet/VBF branches are present in the primary ntuples. Any VBF-like categorization will require external recovery or a formal downscope ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:3198-3203`](../../outputs/DATA_RECONNAISSANCE.md), [`:3995`](../../outputs/DATA_RECONNAISSANCE.md)).
- No precomputed angular/MELA branches are present, but per-lepton four-vector inputs are. Phase 2 can still test whether the requested angular discriminator is recomputable from the retained kinematics ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:3196-3200`](../../outputs/DATA_RECONNAISSANCE.md), [`:4022`](../../outputs/DATA_RECONNAISSANCE.md)).
- No truth-level branches are present, so truth-matching and particle-level closure cannot be assumed from these ntuples alone ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:3201`](../../outputs/DATA_RECONNAISSANCE.md), [`:3979-3981`](../../outputs/DATA_RECONNAISSANCE.md)).
- The `miniRelIso` tails and very small `pvNdof` values are acceptable for Phase 1 discovery, but they should not become strategy inputs without dedicated validation ([`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:3971-3976`](../../outputs/DATA_RECONNAISSANCE.md)).

## Conclusion

I do not find remaining Phase 1 blockers. The fixes from the previous ITERATE cycle are present in the current artifacts, the figures and plotting code are now mechanically sound, and the documented risks are exactly the ones Phase 2 should pick up.
