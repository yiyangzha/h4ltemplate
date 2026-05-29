# Phase 1 Self-Critique After VERIFY Follow-up 2

Session: `albert_0f97`
Timestamp: 2026-05-29T18:43:00Z

## Figure Critiques and Fixes

- `m4l_small_slice_shapes.png`: Criticism: the previous connected lines
  between sparse small-slice bin estimates visually implied interpolation or
  smooth model shapes. Fix: regenerated the figure with marker-only error
  bars for every sample and changed the experiment label to `Open Data+Sim`
  because the plot contains both data and simulation.
- `z1_mass_small_slice_shapes.png`: Criticism: the line-connected MC shapes
  overemphasized bin-to-bin fluctuations and made the small-slice comparison
  look more precise than it is. Fix: regenerated with marker-only error bars.
- `z2_mass_small_slice_shapes.png`: Criticism: the off-shell structure and
  sparse high-mass bins were visually distorted by connecting lines. Fix:
  regenerated with marker-only error bars.
- `pt4l_small_slice_shapes.png`: Criticism: connecting low-statistics tail
  bins made the tail look like a continuous prediction rather than a slice
  diagnostic. Fix: regenerated with marker-only error bars.
- `eta4l_small_slice_shapes.png`: Criticism: the broad eta distribution had
  strong bin-to-bin fluctuations that were made harder to judge by lines
  crossing between samples. Fix: regenerated with marker-only error bars.
- `leading_lepton_pt_small_slice_shapes.png`: Criticism: the tail comparison
  was visually overinterpretable with connected points. Fix: regenerated with
  marker-only error bars.

## Artifact Critiques and Fixes

- Criticism: `DATA_RECONNAISSANCE.md` said MELA/angular discriminants were
  found because the branch-name search matched `phi` branches. That was too
  broad: azimuthal primitives exist, but precomputed MELA/angular
  discriminants do not. Fix: split the capability table into `Angular
  primitives` and `Precomputed MELA/angular discriminants`, with the latter
  explicitly `NOT FOUND`.
- Criticism: the primary-vs-local copy mismatch was only described in prose,
  even though the file sizes and entry counts materially differ. Fix: added a
  `Primary vs Local Copy Check` table with primary/local sizes, tree-entry
  dictionaries, and a verdict for each matched file.
- Criticism: the plot labels previously said only `CMS Open Data` even though
  the figures overlay MC. Fix: changed to `CMS Open Data+Sim`.

## Claim Evidence Review

- Claim: every ROOT file/tree/branch was inventoried. Evidence: `root_metadata.json`
  contains 24 ROOT files, 48 trees, and 2688 branch entries; the generated
  artifact renders the complete inventory.
- Claim: small-slice data quality was checked. Evidence: `slice_recon.json`
  reports 1342 numeric branch summaries, 621 unique-value surveys,
  `nan_count_total=0`, and `inf_count_total=0`.
- Claim: truth-level branches are absent. Evidence: primary branch search for
  `gen`, `truth`, `lhe`, `mother`, and `status` returned no matches.
- Claim: VBF jet observables are absent. Evidence: primary branch search for
  `jet`, `mjj`, `j1`, `j2`, and `deta` returned no matches.
- Claim: precomputed angular/MELA discriminants are absent. Evidence: primary
  branch search finds only `l1phi`, `l2phi`, `l3phi`, `l4phi`, and `phi4l`;
  no `D_bkg_kin`, `Dsig`, `KD`, `costheta`, `cosTheta`, or `mela` branches.

## Regenerated Files

- `phase1_exploration/outputs/FIGURES.json`
- all six PDF/PNG files in `phase1_exploration/outputs/figures/`
- `phase1_exploration/outputs/DATA_RECONNAISSANCE.md`

## Remaining Limitations

- Literature source extraction uses public web/HEPData/CMS/PDG fallback routes
  because MCP tools are disabled. The artifacts cite retained public URLs, but
  Phase 2 should still verify any exact table/page-level values it promotes to
  binding inputs.
- VBF categorization and NN angular discriminators remain feasibility risks:
  no jet branches and no precomputed angular/MELA discriminants are present in
  the primary ntuples.

