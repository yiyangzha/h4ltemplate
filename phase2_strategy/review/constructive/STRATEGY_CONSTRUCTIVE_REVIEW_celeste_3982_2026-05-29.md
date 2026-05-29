# Constructive Review — Phase 2 Strategy

Session: `celeste_3982`  
Date: 2026-05-29  
Artifact reviewed: `phase2_strategy/outputs/STRATEGY.md`

## Scope read

Read in full:

- `TOGGLES.md`
- `agents/constructive_reviewer.md`
- `methodology/06-review.md`
- `phase2_strategy/CLAUDE.md`
- `phase2_strategy/outputs/STRATEGY.md`
- `COMMITMENTS.md`
- `phase2_strategy/review/VERIFY_viktor_dfa6.md`
- `phase1_exploration/outputs/DATA_RECONNAISSANCE.md`
- `phase1_exploration/outputs/INPUT_INVENTORY.md`
- `phase1_exploration/outputs/LITERATURE_SURVEY.md`
- `experiment_log.md`

MCP toggles are `false`; no MCP tools were called.

## Verdict

No Category A blocker identified in the current Phase 2 strategy. The nominal inclusive/channel `m4l` template-fit path is coherent, grounded in Phase 1 constraints, and materially improved by the VERIFY self-critique. The remaining gaps are operational rather than conceptual: they would weaken Phase 3 execution and later AN review if left implicit.

`COMMITMENTS.md` is usable by later reviewers, but it is not yet as traceable as it should be for a long Phase 3/4 chain.

## Findings

### B1 — The VBF recovery branch is still underspecified as an operational gate, because the currently allowed inputs do not include any upstream source from which jets could be recovered.

Evidence:

- The strategy correctly states that the primary ntuples contain no jet collections or VBF discriminants (`phase2_strategy/outputs/STRATEGY.md:61-64`).
- Phase 1 independently established the same missing-content boundary: no jets, no all-object collections, no truth, and no precomputed MELA/angular content (`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:3989-3995`).
- The proposed recovery step depends on an allowed upstream join (`phase2_strategy/outputs/STRATEGY.md:251-253`), but `paths.json` currently allows only the flat-ntuple data and MC directories, not upstream NanoAOD or other source files (`paths.json:1-10`).

Why this matters:

Phase 3 can document that recovery is impossible, but today the strategy still presents VBF recovery as a live technical branch without stating its actual precondition: broader allowed inputs. That will make later reviewers ask whether VBF was seriously attempted or was never feasible under the sandboxed input contract.

Recommendation:

Add an explicit precondition to the strategy and commitments: VBF recovery is attempted only if the orchestrator/human expands the allowed-source list before Phase 3 planning; otherwise the default action is immediate formal downscope after documenting the no-jet branch inventory and the `paths.json` allow-list limitation. That keeps the analysis honest and prevents a fake "attempted recovery" narrative.

### B2 — The angular/NN branch needs a minimum-statistics viability gate before category splitting, not only a relative-performance gate.

Evidence:

- The strategy sensibly requires kinematic reconstruction, physical-range checks, input-modelling checks, and a 10% expected-uncertainty improvement before promoting an NN (`phase2_strategy/outputs/STRATEGY.md:275-291`).
- But the current gate is entirely relative; it does not require minimum expected counts per category/bin before the classifier is allowed to define the nominal fit.
- Phase 1 shows the available data sample is only 854 candidate rows total (`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:32,56`), and the expected signal yields for subleading production modes are tiny at 10 fb^-1 (`phase1_exploration/outputs/DATA_RECONNAISSANCE.md:37-42`).
- The strategy’s own precision estimate already anticipates weak statistics and important reducible-background/MC-stat effects (`phase2_strategy/outputs/STRATEGY.md:346-372`).

Why this matters:

With this sample size, an NN can clear a relative Asimov metric while still producing fragile categories, unstable nuisance pulls, or bins below the regime where the chosen asymptotics and shape systematics behave well. That is a process risk, not a theoretical one.

Recommendation:

Before any classifier becomes nominal, require a machine-readable pre-fit viability table with at least:

- expected total events per final category and per `m4l` bin,
- expected signal and background counts per category,
- number of bins below the low-count threshold used by the fit model,
- a hard veto if any proposed nominal category split creates sparsity that forces unstable MC-stat or GoF behavior.

This should sit alongside the current 10% improvement gate, not replace it.

### B3 — The final comparison plan is not yet comprehensive enough for the analysis note; it needs an explicit comparability matrix, not only a summary figure.

Evidence:

- The literature survey is careful that only some CMS outputs are directly comparable for this open-data detector-level analysis (`phase1_exploration/outputs/LITERATURE_SURVEY.md:14-26,34-37`).
- The strategy also acknowledges several non-parities: no official calibrations, DY-only fake proxy, no jet categories, detector-level mass estimator only (`phase2_strategy/outputs/STRATEGY.md:77-95,142-147,431-436`).
- But the flagship comparison plan is currently just one summary figure/table against CMS-HIG-16-041, CMS-HIG-19-001, and PDG (`phase2_strategy/outputs/STRATEGY.md:382-395`).
- `COMMITMENTS.md` records reference values for fiducial cross sections and width constraints as well as `mu` and `mH` (`COMMITMENTS.md:103-143`), even though the current strategy does not commit to measuring all of those quantities.

Why this matters:

Without a bound comparability matrix, the later AN can easily drift into over-comparison: quoting official fiducial or width results next to a detector-level `mu`/peak-estimator analysis without making the matched vs unmatched observables explicit. That would weaken the honesty of the final physics narrative.

Recommendation:

Add a committed Phase 4/Doc deliverable that maps each reference observable or category to one of:

- matched and quantitatively comparable,
- approximated but not directly comparable,
- unavailable / intentionally not measured.

At minimum this matrix should cover inclusive `mu`, mass, fiducial cross section, width, production-sensitive categories, and reducible-background treatment. Quantitative pulls should be required only for the first class.

### B4 — The luminosity systematic plan is still too vague for a binding Phase 2 commitment.

Evidence:

- Phase 1 has a user-provided target luminosity of 10 fb^-1 and a separate public CMS 2017 full-year reference luminosity of 42.12 +/- 0.34 fb^-1 (`phase1_exploration/outputs/INPUT_INVENTORY.md:8-9`).
- The strategy says: "Use the user target luminosity for central value and public CMS 2017 luminosity uncertainty as a scale reference if applicable" (`phase2_strategy/outputs/STRATEGY.md:300`).

Why this matters:

"If applicable" is not a reviewable nuisance prescription. For a detector-level `mu` measurement normalized to prompt effective cross sections, the luminosity treatment needs to be explicit: either the 10 fb^-1 subset is taken as an exact user-defined scale, or a conservative subset-luminosity uncertainty is assigned and justified. Borrowing the full-year CMS luminosity uncertainty without stating why it transfers would be too loose for later review.

Recommendation:

Turn this into a binary Phase 3 decision with evidence:

- either document that the 10 fb^-1 subset inherits a specific luminosity uncertainty from a cited source,
- or explicitly mark the central luminosity as user-provided and assign a conservative normalization envelope as a methodological limitation.

The important part is to remove the current ambiguity before Phase 4 systematics are built.

### C1 — `COMMITMENTS.md` is workable, but later reviewers would benefit from stronger traceability from each checkbox back to the strategy decision or section that created it.

Evidence:

- The file is populated and materially better after VERIFY (`phase2_strategy/review/VERIFY_viktor_dfa6.md:27-40`).
- It already captures major gates, figures, cross-checks, and references (`COMMITMENTS.md:12-143`).
- However, many generic entries do not carry a strategy label or section anchor, unlike items such as `[A3]`, `[D7]`, and `[D9]`.

Why this matters:

By Phase 4c and Doc review, reviewers will need to answer "was this commitment fulfilled, revised, or silently dropped?" Generic lines without an origin anchor slow that audit down and make silent drift easier.

Recommendation:

Keep the current structure, but add a short origin tag to each unlabeled item on the next update, for example:

- `(from STRATEGY Systematic Plan)`
- `(from STRATEGY Validation Tests #6)`
- `(from STRATEGY Flagship Figures #4)`

That would make the file much more reviewer-friendly without changing its content.

## Closing assessment

The strategy is directionally sound and honest about the main open-data limitations. The next iteration should not broaden scope; it should make the existing decision gates more executable and more auditable, especially around VBF feasibility, classifier viability under low statistics, and how the final note will compare detector-level results to official CMS publications.
