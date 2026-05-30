# Phase 4a Plot Watcher Feedback

- Session: `nora_2930`
- Executor session monitored: `edmund_69a2`
- Phase: `phase4_inference/4a_expected`
- Status: `SETTLED_WITH_UNRESOLVED_BLOCKER`

## Scope

This file records early watcher feedback while the Phase 4a executor is
producing figures. Entries here are not the final blocking plot-validation
review; they are immediate PASS/FAIL checks intended to be acted on while the
executor still has the plotting context loaded.

## Handoff

- Replaces earlier watcher `celeste_1743`, which exited before any Phase 4a
  figures appeared.
- Prior watcher state: `outputs/FIGURES.json` remained empty, no Phase 4a PNGs
  were produced, and the executor log had no `FIGURE_READY:` lines through
  `2026-05-30T00:31:55Z`.

## Poll History

- 2026-05-30T00:35:00Z: replacement watcher started. `outputs/FIGURES.json`
  is still empty (`[]`), `outputs/figures/` contains no PNGs, and
  `outputs/INFERENCE_EXPECTED.md` is absent. Executor log still has no
  `FIGURE_READY:` lines.
- 2026-05-30T00:35:56Z: no figure-production change. `outputs/FIGURES.json`
  remains empty, `outputs/figures/` still contains zero files, and
  `outputs/INFERENCE_EXPECTED.md` is still absent. Executor code is advancing
  (`src/expected_common.py` mtime `00:33:12Z`,
  `src/run_expected_inference.py` mtime `00:33:38Z`), but the executor log
  remains unchanged since `00:25:06Z` with no `FIGURE_READY:` lines.
- 2026-05-30T00:36:52Z: still no Phase 4a figures or registry entries.
  `outputs/FIGURES.json` remains `[]`, `outputs/figures/` still contains zero
  files, and `outputs/INFERENCE_EXPECTED.md` is absent. Executor code continues
  to move (`src/run_expected_inference.py` mtime `00:36:44Z`), but the executor
  log still has no `FIGURE_READY:` notifications.
- 2026-05-30T00:37:52Z: no new plot artifacts yet. Registry remains empty,
  figures directory remains empty, and the inference artifact is still absent.
  The executor continues touching `src/run_expected_inference.py`
  (`00:36:54Z`), so the watch remains active rather than closing as stalled.
- 2026-05-30T00:39:08Z: executor produced machine-readable Phase 4a result
  JSON files in `analysis_note/results/` (`expected_parameters.json`,
  `expected_covariance.json`, `expected_systematics.json`,
  `expected_validation.json`, `expected_mass_scan.json`; all `00:37:53Z`), but
  there are still no Phase 4a figures, no registry entries, no
  `FIGURE_READY:` lines, and no `outputs/INFERENCE_EXPECTED.md`. This now
  looks like plot-stage lag or missing figure emission rather than total
  executor inactivity.
- 2026-05-30T00:40:28Z: plotting-code stage is now visible because
  `src/make_expected_plots.py` appeared with mtime `00:40:17Z`. However,
  there are still no rendered Phase 4a figures, no `FIGURE_READY:` lines, no
  registry entries, and no inference artifact yet. Watch remains active for the
  first emitted PNG.
- 2026-05-30T00:41:22Z: first figure batch arrived. `outputs/FIGURES.json`
  now registers 9 figures, `outputs/figures/` contains 9 PNG/PDF pairs, and
  the executor log contains 9 `FIGURE_READY:` lines from `00:41:10Z` through
  `00:41:13Z`. Visual inspection completed for all 9 current PNGs. Immediate
  watcher findings are listed below.
- 2026-05-30T00:43:50Z: the executor performed a second full figure write
  (`FIGURE_READY:` lines `00:42:18Z` through `00:42:22Z`) after reading the
  watcher file, but the current rendered PNGs still show the same three layout
  blockers listed below. `outputs/INFERENCE_EXPECTED.md` is still absent.
- 2026-05-30T00:45:13Z: no new `FIGURE_READY:` lines or figure mtimes appeared
  after the `00:42:22Z` refresh, but `src/make_expected_plots.py` changed again
  at `00:45:05Z`. The inference artifact is still absent, so the watch remains
  open.
- 2026-05-30T00:46:28Z: a third full figure write arrived (`FIGURE_READY:`
  lines `00:45:20Z` through `00:45:24Z`). Re-inspection of the newest PNGs
  shows that `expected_m4l_final_state_templates.png` and
  `expected_signal_injection_recovery.png` are now acceptable. The remaining
  blocker is `expected_binning_stability.png`. `outputs/INFERENCE_EXPECTED.md`
  is still absent.
- 2026-05-30T00:49:27Z: a fourth full figure write arrived (`FIGURE_READY:`
  lines `00:48:27Z` through `00:48:30Z`). The executor log again shows watcher
  feedback checks after each save. The current blocker remains
  `expected_binning_stability.png`, and `outputs/INFERENCE_EXPECTED.md` is
  still absent.
- 2026-05-30T00:54:43Z: no new `FIGURE_READY:` lines, no figure mtime changes,
  and no `outputs/INFERENCE_EXPECTED.md` appeared during repeated idle polling
  after the `00:48:30Z` batch. The current rendered figure set is treated as
  settled for this watcher run, with one unresolved figure blocker and a
  missing phase artifact from the executor.

## Figure Status

- `expected_m4l_final_state_templates.png` — `PASS`
  - Latest render improved the panel legend/layout. The current PNG no longer
    has the earlier right-edge clipping or label/data collision that blocked
    the first batch.

- `expected_mu_profile_scan.png` — `PASS`
  - Curve, sigma guides, and text are readable. No overlap or ratio-panel issue
    seen.

- `expected_nuisance_impacts.png` — `PASS`
  - Labels are readable and the ranking is visually clear. No legend or label
    collision seen in the rendered PNG.

- `expected_uncertainty_breakdown.png` — `PASS`
  - Clean, readable point-only summary. No overlap or clipping issue seen.

- `expected_signal_injection_recovery.png` — `PASS`
  - Latest render moved the legend clear of the experiment label and points.
    Current layout is readable.

- `expected_low_count_validation.png` — `PASS`
  - Threshold line and points are readable; no visible overlap or clipping
    problem in the current rendering.

- `expected_binning_stability.png` — `FAIL`
  - The current two-panel layout is still too cramped. The shared central
    x-axis label and the lower panel compete for the same vertical space, and
    the overall composition will read poorly at AN scale.
  - Fix now: split this into two separate figures or make the 2-row layout
    substantially taller with cleaner spacing between panels. The current
    stacked presentation is still not publication-ready.

- `expected_mass_profile_attempt.png` — `PASS`
  - Profile curve and axis text are readable with no obvious overlap.

- `expected_reference_comparison.png` — `PASS`
  - Reference markers, uncertainty bars, and SM expectation line are readable.
    No immediate publication-quality blocker seen.

## Running Totals

- Inspected: `9`
- PASS: `8`
- FAIL: `1`
- Unresolved blockers: `1`

## Current Blocker

One current figure still needs a layout fix before the watcher would call this
batch clean:

1. `expected_binning_stability.png`

## Watcher Closeout

The live watch is ending on a settled figure batch rather than a clean Phase 4a
artifact handoff. The executor produced and repeatedly refreshed 9 registered
figures, but never wrote `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md`
during this watcher run. The current visual state is:

- `8` figures PASS
- `1` figure FAIL: `expected_binning_stability.png`

If the executor resumes and emits new `FIGURE_READY:` lines or writes the
missing inference artifact, the watcher should be resumed from this file.
