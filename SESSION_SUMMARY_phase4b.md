# Session Summary Phase 4b

Date: 2026-05-30

Phase 4b produced fixed-seed 10% data inference after the user requested a
Phase 4b fit-window override to `70 < m4l < 170 GeV`, including the Z peak.
This supersedes the previous Phase 4b `105 < m4l < 140 GeV` instruction.

Primary artifact:

- `phase4_inference/4b_partial/outputs/INFERENCE_PARTIAL.md`

Machine-readable outputs:

- `analysis_note/results/partial_parameters.json`
- `analysis_note/results/partial_validation.json`
- `analysis_note/results/partial_covariance.json`
- `analysis_note/results/partial_systematics.json`
- `analysis_note/results/partial_systematic_shifts.json`

Headline 10% result:

- Fit window: `70 < m4l < 170 GeV`.
- Fixed seed: `9417`.
- Subsample: `20 / 203` selected data events, effective luminosity `1.0 fb^-1`.
- `mu = 0.0 +1.3548619813595435`; the lower interval is at the configured physical boundary.
- GoF: `chi2/ndf = 31.755141641709276 / 38`, `p = 0.752432307059706`.

Notes:

- This is a user-requested Phase 4b override and should be carried into Doc 4b.
- No fresh Phase 4b review was run after the override, per the user instruction: "No need to review again, just re-make plots and results quickly."
- Plot watcher fallback initially failed pre-override figures, but the executor reran and registered the final seven Phase 4b figures.
