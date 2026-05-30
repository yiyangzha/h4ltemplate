# VERIFY_sven_6dea_2026-05-30

Session: `sven_6dea`

Scope: fast plot-only Doc 4c fix for `analysis_note/figures/doc4c_reference_comparison.{pdf,png}`. No Phase 4 inference was rerun and no physics numbers were changed.

## Figure Regeneration

- Regenerated `analysis_note/figures/doc4c_reference_comparison.pdf` and `.png` with a one-off `pixi run py - <<'PY'` command.
- Signal-strength panel uses black square markers for all entries.
- Entries without stat/syst split use one uncapped total horizontal bar.
- CMS-HIG-19-001 signal strength uses an inner capped stat bar and an outer uncapped quadrature total bar.
- Mass panel uses black square markers for all entries.
- This-analysis mass entry uses `best_mass_GeV = 124.75` and `diagnostic_grid_half_step_GeV = 0.125` from `analysis_note/results/observed_mass_scan.json`.
- CMS-HIG-16-041/JHEP mass uses an inner capped stat bar and outer uncapped quadrature total bar.
- PDG 2024 mass uses one uncapped total horizontal bar.
- No legends are present.

## Checks

- `pixi run tectonic --outdir analysis_note analysis_note/ANALYSIS_NOTE_doc4c_v1.tex` completed and wrote `analysis_note/ANALYSIS_NOTE_doc4c_v1.pdf`.
- `grep -n "Comparison to Prior Results and Theory\\|doc4c_reference_comparison" analysis_note/ANALYSIS_NOTE_doc4c_v1.tex` showed:
  - line 681: `\section{Comparison to Prior Results and Theory}`
  - line 714: `\includegraphics[width=0.92\linewidth,height=0.70\textheight,keepaspectratio]{figures/doc4c_reference_comparison.pdf}`
- `ls -l analysis_note/figures/doc4c_reference_comparison.pdf analysis_note/figures/doc4c_reference_comparison.png` after regeneration showed:
  - `analysis_note/figures/doc4c_reference_comparison.pdf`, 19184 bytes, May 30 07:55
  - `analysis_note/figures/doc4c_reference_comparison.png`, 72132 bytes, May 30 07:55
- `pixi run lint-plots` passed: `No plotting violations found in 34 file(s).`

## Worktree Scope

Expected changed files are the regenerated comparison figure files, the compiled Doc 4c PDF from the requested compile step, this verification note, and `experiment_log.md`.
