# Experiment Log

## 2026-05-29T18:13:30Z — Orchestrator resume

- Resumed from disk following `CLAUDE.md` recovery protocol.
- Found clean git worktree before edits; last 20 commits are generic `update` commits ending at `b4429ef`.
- `prompt.md` exists and contains the H=>4L CMS Open Data measurement objective.
- No `SESSION_STATE.md` or exported `*.txt` chat history found.
- `experiment_log.md` and `COMMITMENTS.md` contained no completed phase evidence.
- Required phase artifacts are absent except empty `FIGURES.json` placeholders, so the lifecycle is at Phase 1 EXECUTE.
- MCP verification failed because the manifest tools are not exposed in this Codex session (`alphaxiv.full_text_papers_search`, `lep-corpus.search_lep_corpus` unavailable via tool discovery). Set `MCP_ALPHAXIV=false` and `MCP_LEP_CORPUS=false`; agents must use documented web/fallback literature routes.

## 2026-05-29T18:59:13Z — Phase 1 review ITERATE

- Phase 1 executor `albert_0f97` produced required artifacts and passed VERIFY follow-ups after self-critique fixes.
- Per-figure validators passed all six Phase 1 PNGs.
- Independent Phase 1 review `odette_a6bb` returned ITERATE.
- Blocking findings: all six figures label a bin-width-normalized density as `Normalized entries`; important integer/flag codes are listed but not decoded; `LITERATURE_SURVEY.md` includes uncited numeric results for a later CMS publication.
- B findings: data-quality prose needs outlier/extreme interpretation; preselection/content boundary needs tighter characterization; literature survey is thin for Phase 2 strategy.
- Next step: spawn a fixer agent for all A/B findings, then run verification arbiter before fresh review.

## 2026-05-29T18:18:33Z — Phase 1 executor plan

- Phase 1 executor session `albert_0f97` read the required runtime,
  phase, methodology, prompt, path, and executor files before loading ROOT
  data or searching literature.
- Confirmed MCP literature tools are disabled; Phase 1 will use public
  web/INSPIRE/arXiv/CMS/PDG fallback routes and record search trails.
- Created `phase1_exploration/plan.md` and
  `phase1_exploration/logs/executor_albert_0f97_20260529T181833Z.md`.

## 2026-05-29 — Phase 1 metadata inventory

- Inspected 24 ROOT files structurally with uproot and wrote `phase1_exploration/outputs/root_metadata.json`.

## 2026-05-29 — Phase 1 small-slice reconnaissance

- Surveyed branch ranges, NaN/inf counts, and integer/flag unique values on at most 1000 entries per primary tree.

## 2026-05-29 — Phase 1 coverage check

- Summed MC Metadata generated-event counts where available and computed prompt-luminosity nominal MC weights for downstream validation.

## 2026-05-29 — Phase 1 histogram summaries

- Produced small-slice histogram summaries for available 4l mass, Z mass, jet, and discriminant candidate branches.

## 2026-05-29 — Phase 1 coverage check

- Summed MC Metadata generated-event counts where available and computed prompt-luminosity nominal MC weights for downstream validation.

## 2026-05-29 — Phase 1 histogram summaries

- Produced small-slice histogram summaries for available 4l mass, Z mass, jet, and discriminant candidate branches.

## 2026-05-29 — Phase 1 histogram summaries

- Produced small-slice histogram summaries for available 4l mass, Z mass, jet, and discriminant candidate branches.

## 2026-05-29 — Phase 1 exploration figures

- Produced 6 small-slice exploration figures and updated `phase1_exploration/outputs/FIGURES.json`.

## 2026-05-29 — Phase 1 PDF toolchain test

- Ran `pixi run build-pdf /sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/test_build.tex`; passed=True; temporary stub removed.

## 2026-05-29 — Phase 1 artifacts built

- Built Phase 1 markdown artifacts from metadata, small-slice surveys, coverage checks, figure registry, and public literature source notes.

## 2026-05-29T19:08:32Z — Phase 1 fixer petra_11e2

- Resolved A1 by relabeling all six bin-width-normalized exploration plots as densities and regenerating PNG/PDF figures plus `FIGURES.json`.
- Resolved A2 by adding an integer/flag interpretation section for `finalState`, electron cut-based WP integers, `zId`, and `trigBits`, with a provenance caveat for Phase 2.
- Resolved A3/B3 by citing CMS-HIG-19-001 / EPJC 81 (2021) 488 for the 137 fb^-1 CMS H->4l comparison values and expanding the Phase 2 methodology caveats.
- Resolved B1/B2 by adding data-quality prose for isolation/PV extremes and a preselection/content-boundary summary derived from branch availability and the local ntuplizer code.
- Resolved C1 by refreshing all six per-figure validation notes after figure regeneration.
- Verification: `pixi run py -m py_compile ...`, `pixi run p1-plots`, `pixi run p1-artifacts`, `pixi run lint-plots`, and the FIGURES registry smoke test all passed.

## 2026-05-29T18:35:00Z — Phase 1 self-check

- Final Phase 1 pixi chain passed:
  `p1-metadata`, `p1-recon-slice`, `p1-preselection`, `p1-hists`,
  `p1-plots`, `p1-pdf-test`, `p1-artifacts`, and `lint-plots`.
- Figure registry smoke test found 6 figures with no missing, empty,
  stale, or orphan PNG/PDF entries.
- Self-critique fixed an overlapping plot label and added explicit
  documentation that jet/VBF, truth, and precomputed angular/MELA branches
  are absent in the primary ntuples.

## 2026-05-29T18:43:00Z — Phase 1 VERIFY self-critique fixes

- Re-read Phase 1 figures and artifacts in critic mode for VERIFY Follow-up 2.
- Regenerated all six exploration figures with marker-only error bars; connected
  lines were removed because they over-interpreted sparse small-slice
  histograms.
- Updated figure labeling from `CMS Open Data` to `CMS Open Data+Sim` because
  the figures overlay data and MC.
- Regenerated `DATA_RECONNAISSANCE.md` to add a primary-vs-local copy table
  and to separate angular primitives from absent precomputed MELA/angular
  discriminants.

## 2026-05-29 — Phase 1 exploration figures

- Produced 6 small-slice exploration figures and updated `phase1_exploration/outputs/FIGURES.json`.

## 2026-05-29 — Phase 1 artifacts built

- Built Phase 1 markdown artifacts from metadata, small-slice surveys, coverage checks, figure registry, and public literature source notes.

## 2026-05-29 — Phase 1 artifacts built

- Built Phase 1 markdown artifacts from metadata, small-slice surveys, coverage checks, figure registry, and public literature source notes.

## 2026-05-29 — Phase 1 exploration figures

- Produced 6 small-slice exploration figures and updated `phase1_exploration/outputs/FIGURES.json`.

## 2026-05-29 — Phase 1 artifacts built

- Built Phase 1 markdown artifacts from metadata, small-slice surveys, coverage checks, figure registry, and public literature source notes.

## 2026-05-29 — Phase 1 artifacts built

- Built Phase 1 markdown artifacts from metadata, small-slice surveys, coverage checks, figure registry, and public literature source notes.

## 2026-05-29 — Phase 1 metadata inventory

- Inspected 24 ROOT files structurally with uproot and wrote `phase1_exploration/outputs/root_metadata.json`.

## 2026-05-29 — Phase 1 small-slice reconnaissance

- Surveyed branch ranges, NaN/inf counts, and integer/flag unique values on at most 1000 entries per primary tree.

## 2026-05-29 — Phase 1 coverage check

- Summed MC Metadata generated-event counts where available and computed prompt-luminosity nominal MC weights for downstream validation.

## 2026-05-29 — Phase 1 histogram summaries

- Produced small-slice histogram summaries for available 4l mass, Z mass, jet, and discriminant candidate branches.

## 2026-05-29 — Phase 1 exploration figures

- Produced 6 small-slice exploration figures and updated `phase1_exploration/outputs/FIGURES.json`.

## 2026-05-29 — Phase 1 PDF toolchain test

- Ran `pixi run build-pdf /sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/test_build.tex`; passed=True; temporary stub removed.

## 2026-05-29 — Phase 1 artifacts built

- Built Phase 1 markdown artifacts from metadata, small-slice surveys, coverage checks, figure registry, and public literature source notes.

## 2026-05-29 — Phase 1 exploration figures

- Produced 6 small-slice exploration figures and updated `phase1_exploration/outputs/FIGURES.json`.

## 2026-05-29 — Phase 1 artifacts built

- Built Phase 1 markdown artifacts from metadata, small-slice surveys, coverage checks, figure registry, and public literature source notes.

## 2026-05-29 — Phase 1 exploration figures

- Produced 6 small-slice exploration figures and updated `phase1_exploration/outputs/FIGURES.json`.

## 2026-05-29 — Phase 1 artifacts built

- Built Phase 1 markdown artifacts from metadata, small-slice surveys, coverage checks, figure registry, and public literature source notes.

## 2026-05-29 — Phase 1 artifacts built

- Built Phase 1 markdown artifacts from metadata, small-slice surveys, coverage checks, figure registry, and public literature source notes.
