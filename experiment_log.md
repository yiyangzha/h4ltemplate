# Experiment Log

## 2026-05-29T20:45:39Z — Phase 3 executor plan magnus_d784

- Read the required Phase 3 startup context before code or ROOT data work:
  toggles, root and phase CLAUDE files, prompt, paths, executor definition,
  methodology, Phase 2 strategy, commitments, Phase 2 boundary records, and
  Phase 1 deliverables.
- Confirmed MCP literature toggles are disabled; Phase 3 will not call MCP
  tools and will use public fallback only if a source lookup is needed.
- Confirmed boundary commit `1790221` and clean worktree at session start.
- Created `phase3_selection/plan.md` and
  `phase3_selection/logs/executor_magnus_d784_20260529T204533Z.md`.
- Initial implementation decision: keep the scaffolded Phase 3 pixi task names
  but add the missing scripts, insert a dedicated `validate_inputs.py` task,
  and extend the root `all` chain through Phase 3 once the scripts exist.

## 2026-05-29T19:40:45Z — Phase 2 strategy executor viktor_dfa6

- Read required Phase 2 context, Phase 1 artifacts, Phase 1 review trail,
  applicable conventions, and methodology files.
- Confirmed MCP literature tools are disabled and used public web/CMS/arXiv/
  HEPData/PDG fallback routes only.
- Created `phase2_strategy/plan.md` before writing strategy prose.
- Public fallback searches run: CMS-HIG-16-041 mass window/signal strength,
  CMS-HIG-16-041 HEPData, CMS-HIG-19-001 signal strength/fiducial cross
  section, PDG Higgs/gauge summary, H->4l systematics, and H->ZZ->4l angular
  variable definitions.
- Wrote `phase2_strategy/outputs/STRATEGY.md` as a detector-level binned
  simultaneous template-likelihood strategy, not a closed-form extraction.
- Binding decisions: use primary prompt ROOT paths; fit `105 < m4l < 140 GeV`;
  require VBF jet recovery or formal downscope; attempt angular variables only
  through validated lepton-four-vector reconstruction; require data/MC
  validation before any MVA/NN training.
- Updated `COMMITMENTS.md` with Phase 2 binding systematics, validation tests,
  flagship figures, cross-checks, and `[REF]` entries.

## 2026-05-29 — Phase 2 VERIFY self-critique fixes

- Re-read `STRATEGY.md` and `COMMITMENTS.md` in critic mode for VERIFY
  Follow-up 2.
- Strengthened fit-window source evidence by citing the exact CMS public-page
  figure descriptions for `105 < m4l < 140 GeV`.
- Added method-parity limitation [L5] and decision [D9] requiring a Phase 4a
  parametric mass-shape cross-check or documented infeasibility.
- Strengthened VBF recovery/downscope gates and angular-NN promotion gates.
- Fixed `COMMITMENTS.md` so Jet/VBF is an unresolved decision gate, not a
  prematurely marked formal downscope.
- Added a HEPData source-ID note because Phase 1 artifacts and the CMS public
  page use different record identifiers/trails.

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

## 2026-05-29T19:33:00Z — Phase 1 PASS boundary

- Fixer `petra_11e2` resolved all Phase 1 review findings and committed `68a1505`.
- Verification arbiter `sally_b946` marked all findings FIXED in `PHASE1_FIX_VERIFICATION_sally_b946_2026-05-29.md`.
- Fresh Phase 1 reviewer `theo_6ec8` returned PASS in `PHASE1_REVIEW2_theo_6ec8_2026-05-29.md`.
- Orchestrator regression/maximality check written to `REGRESSION_CHECK_phase1.md`; no Phase 1 blockers remain.
- Updated `pixi.toml` `all` task to run the current Phase 1 chain only; future executors must extend it as they add scripts.
- Validation after update: `pixi run all` passed, `pixi run lint-plots` passed, and figure registry smoke test found 6 entries/12 files with no missing, empty, stale, or orphan files.
- Carry Phase 2 risks forward: primary vs local ROOT copies differ; user-provided MC cross sections need validation; no jet/VBF branches; no precomputed MELA/angular branches; no truth-level branches.

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

## 2026-05-29 — Phase 2 traceability anchor fix

- Session `nora_fec7` resolved the remaining Category B traceability finding
  from arbiter `zelda_7b85` by adding explicit `[SP#]`, `[SP*]`, `[VT#]`,
  `[FIG#]`, and `[REF-MATRIX]` anchors to
  `phase2_strategy/outputs/STRATEGY.md`.
- Verification scan found every non-decision tag used in `COMMITMENTS.md`
  explicitly present in `STRATEGY.md`; `git diff --check` passed.
- No substantive physics strategy content changed beyond traceability labels
  and namespace notes.

## 2026-05-29T20:38:06Z — Phase 2 PASS boundary

- Targeted verifier `otto_d91d` confirmed the final traceability fix:
  all non-decision tags used in `COMMITMENTS.md` have explicit anchors in
  `STRATEGY.md`.
- Phase 2 now has no unresolved A/B findings after two review iterations.
- Orchestrator regression/maximality check written to
  `REGRESSION_CHECK_phase2.md`.
- Session summary written to `SESSION_SUMMARY_phase2.md`.
- Phase 3 can start from the binding `STRATEGY.md` and `COMMITMENTS.md`.

## 2026-05-29 — Phase 2 strategy fixes (fiona_8d6e)

- Resolved the Phase 2 arbiter Required Fix List in scoped strategy files.
  Updated `phase2_strategy/outputs/STRATEGY.md` with a binding simultaneous
  category mass-extraction attempt with `mu` profiled, mass-shape/morphing
  closure and downgrade rules, `mu = 5` injection validation, quantitative
  sideband/DY/TTBar rules, current-`paths.json` VBF downscope requirements,
  angular/NN prefit viability and overtraining/boundary checks, a row-by-row
  shape-fit convention coverage matrix, fallback systematics evidence rules,
  and final AN comparability requirements including the HEPData
  `ins1608162`/`ins1608166` cleanup.
- Updated `COMMITMENTS.md` with explicit [D1]-[D9] carryover entries, proof
  artifacts for every decision, origin tags for generic systematic/
  validation/figure/cross-check items, mass-fit and signal-injection
  commitments, and final AN comparability matrix commitments. Wrote fixer log
  and fix report under `phase2_strategy/`.

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

## 2026-05-29 — Phase 3 baseline selection and provenance

- Built Phase 3 primary-path provenance, MC normalization, cutflow, sideband diagnostics, S1 fit-ready histograms, and compact broad-window event arrays using primary prompt ROOT files only.

## 2026-05-29 — Phase 3 VERIFY and Level 2 plot validation

- Executor `magnus_d784` completed formal VERIFY Follow-up 1 and Follow-up 2.
  The plan check found and fixed residual `np.histogram` usage and missing
  planned diagnostics (`3f427e1`, `e248213`).
- Self-critique found and fixed input-validation MC overlay/normalization,
  S2-rejection wording, VBF evidence quantification, and Phase 4 handoff
  wording (`c3e7c8e`).
- Per-figure validators found plot-label, cutflow-readability, mass-legend,
  and model-name presentation issues. Fix commits: `0bf8908`, `34155e3`,
  `63227ca`, and `c7d6adf`.
- Final Level 2 status: all 29 figures in `phase3_selection/outputs/FIGURES.json`
  have PASS validation on the final committed image set. Summary:
  `phase3_selection/review/validation/PERFIG_VALIDATION_SUMMARY_2026-05-29.md`.

## 2026-05-29 — Phase 3 review PASS boundary

- Phase 3 initial review returned ITERATE: plot label issue in
  `sideband_dy_ttbar_diagnostics`, low-count final-state binning handoff
  wording, non-standard JSON `NaN` values, and missing cut-motivation
  diagnostics.
- Executor `magnus_d784` resolved all review findings in commit `01b0066`.
- Verification arbiter `sally_2377` marked all targeted findings FIXED in
  `PHASE3_FIX_VERIFICATION_sally_2377_2026-05-29.md`.
- Fresh Phase 3 critical reviewer `ursula_0b8b` returned PASS with no A/B
  findings. Fresh Level 3 plot validator `vera_6cf0` returned PASS for all
  30 registered figures.
- Regression/maximality check written to `REGRESSION_CHECK_phase3.md`; no
  regression trigger remains. Phase 4a can begin with a conditional low-count
  final-state handoff.

## 2026-05-29 — Phase 3 VBF recovery/downscope gate

- Checked primary and local branch inventories plus ntuplizer provenance for jet/VBF content. Decision: formal VBF downscope; no lepton-only category will be labeled VBF.

## 2026-05-29 — Phase 3 angular reconstruction closure

- Recomputed broad-window four-lepton and Z-candidate masses from retained lepton four-vectors, computed detector-level angular candidates, and wrote physical-range closure outputs.

## 2026-05-29 — Phase 3 input-variable modeling gate

- Computed D7 data/MC shape gates for 14 candidate S2 variables; 2 passed before classifier training.

## 2026-05-29 — Phase 3 S2 classifier attempt

- Trained logistic, BDT, and small NN alternatives with fixed seed; best model `small_nn` promotion decision: False.

## 2026-05-29 — Phase 3 approach comparison

- Compared S1 and S2 on common expected precision and validation gates; selected `S1_reference_like_final_state_categories`.

## 2026-05-29 — Phase 3 S2 classifier attempt

- Trained logistic, BDT, and small NN alternatives with fixed seed; best model `small_nn` promotion decision: False.

## 2026-05-29 — Phase 3 approach comparison

- Compared S1 and S2 on common expected precision and validation gates; selected `S1_reference_like_final_state_categories`.

## 2026-05-29 — Phase 3 input-validation figures

- Produced 14 D7 input-validation figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection figures

- Produced 11 selection/sideband/MVA diagnostic figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection figures

- Produced 11 selection/sideband/MVA diagnostic figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 input-validation figures

- Produced 14 D7 input-validation figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection figures

- Produced 11 selection/sideband/MVA diagnostic figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection artifact

- Built `phase3_selection/outputs/SELECTION.md` from Phase 3 JSON/NPZ outputs.

## 2026-05-29 — Phase 3 commitment update

- Updated `COMMITMENTS.md` for Phase 3-resolved proof artifacts and formal VBF downscope items.

## 2026-05-29 — Phase 3 review iteration fixes

- Resolved review findings A1/B1/B2/B3 by replacing raw sideband legend labels, making Phase 3 JSON strict with undefined MVA score-gate reasons, marking S1 final-state binning as a conditional low-count Phase 4 handoff with per-bin evidence, and adding cut-motivation diagnostics plus a registered figure.

## 2026-05-29 — Phase 3 MVA label presentation fix

- Replaced code-style classifier labels in ROC figures, registry captions, and `SELECTION.md` with presentation names (`BDT`, `small NN`, `logistic`) while preserving machine-readable model keys in metadata.

## 2026-05-29 — Phase 3 mass-plot legend layout fix

- Moved mass-stack data/MC legends out of the experiment-label region and regenerated the m4l stack figures plus the Phase 3 figure registry/artifact.

## 2026-05-29 — Phase 3 final cutflow readability fix

- Redesigned `cutflow_summary` as a horizontal log-yield cutflow with concise step labels and registry metadata preserving the full cut-step mapping and endpoint counts.

## 2026-05-29 — Phase 3 VERIFY self-critique fixes

- Re-read Phase 3 selection artifacts and figures as Follow-up 2. Fixed MC stack omissions in validation plots, aligned D7 plot normalization with the shape gate, added per-model S2 gate evidence, quantified VBF downscope evidence, and clarified Phase 4 category handoff boundaries.

## 2026-05-29 — Phase 3 Level 2 plot validation fixes

- Fixed blocking per-figure validation findings by replacing the mixed-plot `Open Data+Sim` label with explicit `Open Data and Open Simulation` wording, removing broad-window text from the top-right experiment label area, and regenerating all Phase 3 input/selection figures plus the figure registry.

## 2026-05-29 — Phase 3 selection artifact

- Built `phase3_selection/outputs/SELECTION.md` from Phase 3 JSON/NPZ outputs.

## 2026-05-29 — Phase 3 baseline selection and provenance

- Built Phase 3 primary-path provenance, MC normalization, cutflow, sideband diagnostics, S1 fit-ready histograms, and compact broad-window event arrays using primary prompt ROOT files only.

## 2026-05-29 — Phase 3 VBF recovery/downscope gate

- Checked primary and local branch inventories plus ntuplizer provenance for jet/VBF content. Decision: formal VBF downscope; no lepton-only category will be labeled VBF.

## 2026-05-29 — Phase 3 angular reconstruction closure

- Recomputed broad-window four-lepton and Z-candidate masses from retained lepton four-vectors, computed detector-level angular candidates, and wrote physical-range closure outputs.

## 2026-05-29 — Phase 3 input-variable modeling gate

- Computed D7 data/MC shape gates for 14 candidate S2 variables; 2 passed before classifier training.

## 2026-05-29 — Phase 3 S2 classifier attempt

- Trained logistic, BDT, and small NN alternatives with fixed seed; best model `small_nn` promotion decision: False.

## 2026-05-29 — Phase 3 approach comparison

- Compared S1 and S2 on common expected precision and validation gates; selected `S1_reference_like_final_state_categories`.

## 2026-05-29 — Phase 3 input-validation figures

- Produced 14 D7 input-validation figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection figures

- Produced 11 selection/sideband/MVA diagnostic figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection artifact

- Built `phase3_selection/outputs/SELECTION.md` from Phase 3 JSON/NPZ outputs.

## 2026-05-29 — Phase 3 commitment update

- Updated `COMMITMENTS.md` for Phase 3-resolved proof artifacts and formal VBF downscope items.

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

## 2026-05-29 — Phase 3 baseline selection and provenance

- Built Phase 3 primary-path provenance, MC normalization, cutflow, sideband diagnostics, S1 fit-ready histograms, and compact broad-window event arrays using primary prompt ROOT files only.

## 2026-05-29 — Phase 3 VBF recovery/downscope gate

- Checked primary and local branch inventories plus ntuplizer provenance for jet/VBF content. Decision: formal VBF downscope; no lepton-only category will be labeled VBF.

## 2026-05-29 — Phase 3 angular reconstruction closure

- Recomputed broad-window four-lepton and Z-candidate masses from retained lepton four-vectors, computed detector-level angular candidates, and wrote physical-range closure outputs.

## 2026-05-29 — Phase 3 input-variable modeling gate

- Computed D7 data/MC shape gates for 14 candidate S2 variables; 2 passed before classifier training.

## 2026-05-29 — Phase 3 S2 classifier attempt

- Trained logistic, BDT, and small NN alternatives with fixed seed; best model `small_nn` promotion decision: False.

## 2026-05-29 — Phase 3 approach comparison

- Compared S1 and S2 on common expected precision and validation gates; selected `S1_reference_like_final_state_categories`.

## 2026-05-29 — Phase 3 input-validation figures

- Produced 14 D7 input-validation figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection figures

- Produced 11 selection/sideband/MVA diagnostic figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection artifact

- Built `phase3_selection/outputs/SELECTION.md` from Phase 3 JSON/NPZ outputs.

## 2026-05-29 — Phase 3 commitment update

- Updated `COMMITMENTS.md` for Phase 3-resolved proof artifacts and formal VBF downscope items.

## 2026-05-29 — Phase 3 selection figures

- Produced 15 selection/sideband/MVA diagnostic figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection artifact

- Built `phase3_selection/outputs/SELECTION.md` from Phase 3 JSON/NPZ outputs.

## 2026-05-29 — Phase 3 baseline selection and provenance

- Built Phase 3 primary-path provenance, MC normalization, cutflow, cut-motivation diagnostics, sideband diagnostics, S1 fit-ready histograms, and compact broad-window event arrays using primary prompt ROOT files only.

## 2026-05-29 — Phase 3 VBF recovery/downscope gate

- Checked primary and local branch inventories plus ntuplizer provenance for jet/VBF content. Decision: formal VBF downscope; no lepton-only category will be labeled VBF.

## 2026-05-29 — Phase 3 angular reconstruction closure

- Recomputed broad-window four-lepton and Z-candidate masses from retained lepton four-vectors, computed detector-level angular candidates, and wrote physical-range closure outputs.

## 2026-05-29 — Phase 3 input-variable modeling gate

- Computed D7 data/MC shape gates for 14 candidate S2 variables; 2 passed before classifier training.

## 2026-05-29 — Phase 3 S2 classifier attempt

- Trained logistic, BDT, and small NN alternatives with fixed seed; best model `small_nn` promotion decision: False.

## 2026-05-29 — Phase 3 approach comparison

- Compared S1 and S2 on common expected precision and validation gates; selected `S1_reference_like_final_state_categories`.

## 2026-05-29 — Phase 3 input-validation figures

- Produced 14 D7 input-validation figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection figures

- Produced 16 selection/sideband/MVA diagnostic figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection artifact

- Built `phase3_selection/outputs/SELECTION.md` from Phase 3 JSON/NPZ outputs.

## 2026-05-29 — Phase 3 commitment update

- Updated `COMMITMENTS.md` for Phase 3-resolved proof artifacts and formal VBF downscope items.

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

## 2026-05-29 — Phase 3 baseline selection and provenance

- Built Phase 3 primary-path provenance, MC normalization, cutflow, cut-motivation diagnostics, sideband diagnostics, S1 fit-ready histograms, and compact broad-window event arrays using primary prompt ROOT files only.

## 2026-05-29 — Phase 3 VBF recovery/downscope gate

- Checked primary and local branch inventories plus ntuplizer provenance for jet/VBF content. Decision: formal VBF downscope; no lepton-only category will be labeled VBF.

## 2026-05-29 — Phase 3 angular reconstruction closure

- Recomputed broad-window four-lepton and Z-candidate masses from retained lepton four-vectors, computed detector-level angular candidates, and wrote physical-range closure outputs.

## 2026-05-29 — Phase 3 input-variable modeling gate

- Computed D7 data/MC shape gates for 14 candidate S2 variables; 2 passed before classifier training.

## 2026-05-29 — Phase 3 S2 classifier attempt

- Trained logistic, BDT, and small NN alternatives with fixed seed; best model `small_nn` promotion decision: False.

## 2026-05-29 — Phase 3 approach comparison

- Compared S1 and S2 on common expected precision and validation gates; selected `S1_reference_like_final_state_categories`.

## 2026-05-29 — Phase 3 input-validation figures

- Produced 14 D7 input-validation figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection figures

- Produced 16 selection/sideband/MVA diagnostic figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection artifact

- Built `phase3_selection/outputs/SELECTION.md` from Phase 3 JSON/NPZ outputs.

## 2026-05-29 — Phase 3 commitment update

- Updated `COMMITMENTS.md` for Phase 3-resolved proof artifacts and formal VBF downscope items.

## 2026-05-30 — Phase 4a expected inference workspace

- Executor `edmund_69a2` built the expected pyhf model from Phase 3 fit inputs using Asimov observations only.
- Expected `mu = 1 +/- 0.5747` with final-state categories before review.
- Low-count toy validation used 80 toys with seed 4269; success fraction 1.000, median bias -0.06065.
- Updated the shifted-template mass-profile closure to fit each mass hypothesis to Asimov templates with `mu` profiled. Nominal best mass grid point is 125.0 GeV; injected 124, 125, and 126 GeV closure recovers the injected grid point.

## 2026-05-30 — Phase 4a expected plots

- Produced 10 expected-inference figures and registered them in `phase4_inference/4a_expected/outputs/FIGURES.json`.

## 2026-05-30 — Phase 4a regression gate and corruption follow-up

- Applied the user-requested broad-window update: MVA training/evaluation now records `70 < m4l < 170 GeV`; m4l plots include broad `70 < m4l < 170 GeV` display; signal-strength inference remains `105 < m4l < 140 GeV`.
- Added `expected_systematic_shifts.json`, `expected_systematic_shift_summary`, and broad mass-scan metadata over `110-140 GeV` with Z/sideband-adjacent exclusions documented.
- The final-state `m4l_scale_factor_0.8` corruption sensitivity did not reject after three attempts, so it is marked `documented_low_count_infeasible` rather than passed.
- Regression gate `klaus_a64b` passed and `REGRESSION_CHECK_phase4a.md` records the Phase 4a boundary checklist.

## 2026-05-30 — Doc 4a expected analysis note

- Note writer `odette_354d` produced `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex` and compiled `analysis_note/ANALYSIS_NOTE_doc4a_v1.pdf`.
- VERIFY follow-ups fixed a thin Statistical Method section and caption/prose issues; final note has 66 pages, 49 staged figures, 14 tables, and 10 display equations.
- Doc 4a review found one Category A rendering issue and B-level framing issues; fixer `wanda_5bec` resolved them in commit `8e7dd78`.
- Targeted arbiter `alfred_5984` verified all Doc 4a review fixes. Doc 4a is passed and the analysis advances to Phase 4b.

## 2026-05-30 — Phase 4a per-figure validation

- Completed Level 2 per-figure validation for all 10 registered expected-inference figures.
- Initial per-figure failures for `expected_binning_stability` and `expected_reference_comparison` were fixed in commits `1213c39` and `23f3001`, followed by full plot refresh commit `5edd995`.
- Final summary `phase4_inference/4a_expected/review/validation/PERFIG4A_VALIDATION_SUMMARY_2026-05-30.md` reports PASS, with `pixi run lint-plots` and the figure-registry smoke test passing.
- Resolved watcher layout blockers for the m4l template, signal-injection, and binning-stability figures; `pixi run lint-plots` and the figure-registry smoke test passed.
- Split the binning stability display into a single-panel uncertainty figure plus a separately registered low-count-bin summary. Watcher recheck `vera_ee63` reported PASS with zero unresolved blockers.

## 2026-05-30 — Phase 4a expected inference artifact

- Built `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` from expected-result JSON files.

## 2026-05-30 — Phase 4a commitment update

- Updated `COMMITMENTS.md` for Phase 4a expected-inference evidence and formal classifier-migration downscope.

## 2026-05-30 — Phase 4a blocking review fixes

- Fixer `fiona_aebe` resolved the Phase 4a `ITERATE` findings from the
  critical and plot-validation reviews.
- Replaced the inclusive mass-profile closure with a simultaneous final-state
  category shifted-template scan over `4mu`, `4e`, and `2e2mu`, with `mu`
  profiled and injected-mass closure recorded in
  `analysis_note/results/expected_mass_scan.json`.
- Added `analysis_note/results/systematics_sources.json` with SP2
  prompt-effective-cross-section evidence, SP6 pileup/PV documentation,
  fallback flags, affected templates/processes, and evaluation methods.
- Made grouped MC-stat covariance entries internally consistent and updated
  `COMMITMENTS.md` to state the grouped approximation rather than full
  bin-by-bin `staterror` profiling.
- Regenerated the full Phase 4a expected figure set after replacing custom
  final-state panel labels with `mh.label.exp_label(...)` and moving the
  `expected_mu_profile_scan` legend away from the profile curve.
- Verification passed: `pixi run p4a-all`, `pixi run lint-plots`, figure
  registry smoke test, JSON sanity checks, and targeted visual inspection of
  `expected_m4l_final_state_templates.png` and
  `expected_mu_profile_scan.png`.

## 2026-05-30 — Phase 4a VERIFY Follow-up 2 self-critique

- Re-read the expected artifact, result JSON, commitments, watcher feedback, and all current PNGs.
- Fixed referee-facing ambiguity by labelling chi2=0/p=1 as Asimov self-consistency rather than independent GoF validation.
- Labelled grouped MC-stat nuisances as an approximation to per-bin `staterror` profiling and added JSON fields documenting the implementation.
- Added expected-only caveats for low-count category retention and mass-profile non-promotion.
- Added systematic variation-basis metadata, including explicit fallback-prior status where official inputs are unavailable.
- Rerendered `expected_binning_stability.png` with extra x-axis padding and no data-overlapping legend; figure registry smoke test after rerender found 10 entries, 20 registered files, 0 missing/empty/orphan.

## 2026-05-30 — Phase 4a expected inference workspace

- Executor `edmund_69a2` built the expected pyhf model from Phase 3 fit inputs using Asimov observations only.
- Expected `mu = 1 +/- 0.5747` with final-state categories before review.
- Low-count toy validation used 80 toys with seed 4269; success fraction 1.000, median bias -0.06065.

## 2026-05-30 — Phase 4a expected plots

- Produced 10 expected-inference figures and registered them in `phase4_inference/4a_expected/outputs/FIGURES.json`.

## 2026-05-30 — Phase 4a expected inference artifact

- Built `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` from expected-result JSON files.

## 2026-05-30 — Phase 4a commitment update

- Updated `COMMITMENTS.md` for Phase 4a expected-inference evidence and formal classifier-migration downscope.

## 2026-05-30 — Phase 4a expected inference workspace

- Executor `edmund_69a2` built the expected pyhf model from Phase 3 fit inputs using Asimov observations only.
- Expected `mu = 1 +/- 0.5747` with final-state categories before review.
- Low-count toy validation used 80 toys with seed 4269; success fraction 1.000, median bias -0.06065.

## 2026-05-30 — Phase 4a expected plots

- Produced 10 expected-inference figures and registered them in `phase4_inference/4a_expected/outputs/FIGURES.json`.

## 2026-05-30 — Phase 4a expected inference artifact

- Built `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` from expected-result JSON files.

## 2026-05-30 — Phase 4a commitment update

- Updated `COMMITMENTS.md` for Phase 4a expected-inference evidence and formal classifier-migration downscope.

## 2026-05-30 — Phase 4a expected inference workspace

- Executor `edmund_69a2` built the expected pyhf model from Phase 3 fit inputs using Asimov observations only.
- Expected `mu = 1 +/- 0.5747` with final-state categories before review.
- Low-count toy validation used 80 toys with seed 4269; success fraction 1.000, median bias -0.06065.

## 2026-05-30 — Phase 4a expected plots

- Produced 10 expected-inference figures and registered them in `phase4_inference/4a_expected/outputs/FIGURES.json`.

## 2026-05-30 — Phase 4a expected inference artifact

- Built `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` from expected-result JSON files.

## 2026-05-30 — Phase 4a commitment update

- Updated `COMMITMENTS.md` for Phase 4a expected-inference evidence and formal classifier-migration downscope.

## 2026-05-30 — Phase 4a expected binning-stability layout fix

- Regenerated `expected_binning_stability` with a shorter x-axis label and wider right margin to resolve right-edge clipping.

## 2026-05-30 — Phase 4a expected reference-comparison label fix

- Regenerated `expected_reference_comparison` with publication-standard reference labels and caption metadata clarifying that the 3.19 precision ratio is relative to CMS-HIG-16-041 only.

## 2026-05-30 — Phase 4a expected plots

- Produced 10 expected-inference figures and registered them in `phase4_inference/4a_expected/outputs/FIGURES.json`.

## 2026-05-30 — Phase 4a expected inference workspace

- Executor `edmund_69a2` built the expected pyhf model from Phase 3 fit inputs using Asimov observations only.
- Expected `mu = 1 +/- 0.5747` with final-state categories before review.
- Low-count toy validation used 80 toys with seed 4269; success fraction 1.000, median bias -0.06065.

## 2026-05-30 — Phase 4a expected inference workspace

- Executor `edmund_69a2` built the expected pyhf model from Phase 3 fit inputs using Asimov observations only.
- Expected `mu = 1 +/- 0.5747` with final-state categories before review.
- Low-count toy validation used 80 toys with seed 4269; success fraction 1.000, median bias -0.06065.

## 2026-05-30 — Phase 4a expected inference workspace

- Executor `edmund_69a2` built the expected pyhf model from Phase 3 fit inputs using Asimov observations only.
- Expected `mu = 1 +/- 0.5747` with final-state categories before review.
- Low-count toy validation used 80 toys with seed 4269; success fraction 1.000, median bias -0.06065.

## 2026-05-30 — Phase 4a expected plots

- Produced 10 expected-inference figures and registered them in `phase4_inference/4a_expected/outputs/FIGURES.json`.

## 2026-05-30 — Phase 4a expected inference artifact

- Built `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` from expected-result JSON files.

## 2026-05-30 — Phase 4a commitment update

- Updated `COMMITMENTS.md` for Phase 4a expected-inference evidence and formal classifier-migration downscope.

## 2026-05-30 — Phase 4a commitment update

- Updated `COMMITMENTS.md` for Phase 4a expected-inference evidence and formal classifier-migration downscope.

## 2026-05-29 — Phase 3 baseline selection and provenance

- Built Phase 3 primary-path provenance, MC normalization, cutflow, cut-motivation diagnostics, sideband diagnostics, S1 fit-ready histograms, and compact broad-window event arrays using primary prompt ROOT files only.

## 2026-05-29 — Phase 3 VBF recovery/downscope gate

- Checked primary and local branch inventories plus ntuplizer provenance for jet/VBF content. Decision: formal VBF downscope; no lepton-only category will be labeled VBF.

## 2026-05-29 — Phase 3 angular reconstruction closure

- Recomputed broad-window four-lepton and Z-candidate masses from retained lepton four-vectors, computed detector-level angular candidates, and wrote physical-range closure outputs.

## 2026-05-29 — Phase 3 input-variable modeling gate

- Computed D7 data/MC shape gates for 14 candidate S2 variables; 2 passed before classifier training.

## 2026-05-29 — Phase 3 S2 classifier attempt

- Trained logistic, BDT, and small NN alternatives with fixed seed; best model `small_nn` promotion decision: False.

## 2026-05-29 — Phase 3 approach comparison

- Compared S1 and S2 on common expected precision and validation gates; selected `S1_reference_like_final_state_categories`.

## 2026-05-29 — Phase 3 input-validation figures

- Produced 14 D7 input-validation figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection figures

- Produced 17 selection/sideband/MVA diagnostic figures and updated `FIGURES.json`.

## 2026-05-29 — Phase 3 selection artifact

- Built `phase3_selection/outputs/SELECTION.md` from Phase 3 JSON/NPZ outputs.

## 2026-05-29 — Phase 3 commitment update

- Updated `COMMITMENTS.md` for Phase 3-resolved proof artifacts and formal VBF downscope items.

## 2026-05-30 — Phase 4a expected inference workspace

- Executor `edmund_69a2` built the expected pyhf model from Phase 3 fit inputs using Asimov observations only.
- Expected `mu = 1 +/- 0.5747` with final-state categories before review.
- Low-count toy validation used 80 toys with seed 4269; success fraction 1.000, median bias -0.06065.

## 2026-05-30 — Phase 4a expected plots

- Produced 12 expected-inference figures and registered them in `phase4_inference/4a_expected/outputs/FIGURES.json`.

## 2026-05-30 — Phase 4a corruption follow-up (hana_c6cf)

- Tested three final-state-aligned diagnostics for the non-rejecting `m4l_scale_factor_0.8` corruption: profiled Poisson deviance (`p = 0.45954`), profiled per-channel shape-only Poisson deviance (`p = 0.60486`), and profiled Pearson chi2 (`p = 0.15844`).
- Did not use the raw unprofiled Pearson diagnostic (`p = 0.026715`) to pass the gate because it drops the nominal profiled workspace treatment and is less reliable for low-count bins.
- Marked the Phase 4a corruption criterion as `documented_low_count_infeasible`, not passed, and fixed VT12 injected-mass wording to `115, 125, 135 GeV`.

## 2026-05-30 — Phase 4a expected inference artifact

- Built `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` from expected-result JSON files.

## 2026-05-30 — Phase 4a commitment update

- Updated `COMMITMENTS.md` for Phase 4a expected-inference evidence and formal classifier-migration downscope.

## 2026-05-30 — Phase 4a expected plots

- Produced 12 expected-inference figures and registered them in `phase4_inference/4a_expected/outputs/FIGURES.json`.

## 2026-05-30 — Phase 4a expected inference artifact

- Built `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` from expected-result JSON files.

## 2026-05-30 — Phase 4a commitment update

- Updated `COMMITMENTS.md` for Phase 4a expected-inference evidence and formal classifier-migration downscope.

## 2026-05-30 — Phase 4a expected inference workspace

- Executor `edmund_69a2` built the expected pyhf model from Phase 3 fit inputs using Asimov observations only.
- Expected `mu = 1 +/- 0.5747` with final-state categories before review.
- Low-count toy validation used 80 toys with seed 4269; success fraction 1.000, median bias -0.06065.

## 2026-05-30 — Phase 4a expected plots

- Produced 12 expected-inference figures and registered them in `phase4_inference/4a_expected/outputs/FIGURES.json`.

## 2026-05-30 — Phase 4a expected inference artifact

- Built `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` from expected-result JSON files.

## 2026-05-30 — Phase 4a commitment update

- Updated `COMMITMENTS.md` for Phase 4a expected-inference evidence and formal classifier-migration downscope.
## 2026-05-30 — Targeted Phase 3/4a regression update (hana_c6cf)

- Updated Phase 3 MVA training metadata to explicitly use the broad `70 < m4l < 170 GeV` selected event table and keep `m4l` out of classifier inputs.
- Added a tuned BDT trial as the targeted improvement attempt; S2 still does not pass all gates, so S1 remains the nominal handoff.
- Regenerated Phase 3 with `pixi run p3-all`.
- Updated Phase 4a expected inference to retain the `105 < m4l < 140 GeV` fit window, add a broad expected `m4l` display, broaden the shifted-template mass scan to `110-140 GeV`, add per-systematic shifted-bin payloads, and mark grouped MC-stat as a formal downscope/approximation.
- Re-ran corruption sensitivity in the final-state simultaneous workspace. The `+20%` mass-response corruption is rejected, but the `-20%` direction is not (`p = 0.4595`); this is documented as a quantitative low-count limitation rather than claimed as a pass.
- Verification: `pixi run p4a-all`, `pixi run lint-plots`, registry smoke tests, and JSON sanity checks completed.

## 2026-05-30 — Phase 4a expected inference workspace

- Executor `edmund_69a2` built the expected pyhf model from Phase 3 fit inputs using Asimov observations only.
- Expected `mu = 1 +/- 0.5747` with final-state categories before review.
- Low-count toy validation used 80 toys with seed 4269; success fraction 1.000, median bias -0.06065.

## 2026-05-30 — Phase 4a expected inference artifact

- Built `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` from expected-result JSON files.

## 2026-05-30 — Phase 4a commitment update

- Updated `COMMITMENTS.md` for Phase 4a expected-inference evidence and formal classifier-migration downscope.

## 2026-05-30 — Phase 4a expected plots

- Produced 12 expected-inference figures and registered them in `phase4_inference/4a_expected/outputs/FIGURES.json`.
