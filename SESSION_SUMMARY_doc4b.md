# Session Summary Doc 4b

Date: 2026-05-30

Doc 4b updated the analysis note with fixed-seed 10% observed-data results.

Primary outputs:

- `analysis_note/ANALYSIS_NOTE_doc4b_v1.tex`
- `analysis_note/ANALYSIS_NOTE_doc4b_v1.pdf`

Doc 4b result:

- Fit window: `70 < m4l < 170 GeV`, including the Z peak, per user-requested Phase 4b override.
- Seed: `9417`.
- Subsample: `20 / 203` selected events, effective luminosity `1.0 fb^-1`.
- `mu = 0.0 +1.3548619813595435`, lower interval at the physical boundary.
- GoF: `chi2/ndf = 31.755141641709276 / 38`, `p = 0.752432307059706`.
- Expected-vs-partial pull: `-0.679474677941247`.

Gate status:

- Doc 4b VERIFY passed after stale fit-window wording was fixed.
- Compact gate `tomoko_c890` passed.
- Human gate was auto-approved per the user's directive and archived in `analysis_note/review/HUMAN_GATE_doc4b_2026-05-30.md`.

Next step: Phase 4c full-data inference using the current broad `70 < m4l < 170 GeV` fit-window instruction unless superseded by a later user instruction.
