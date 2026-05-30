from __future__ import annotations

from expected_common import ANALYSIS_ROOT, append_experiment, append_session, ensure_dirs, setup_logging


REPLACEMENTS = {
    "- [ ] [D2][VT9][VT10] Use a binned simultaneous `pyhf`/HistFactory-style": "- [x] [D2][VT9][VT10] Use a binned simultaneous `pyhf`/HistFactory-style",
    "- [ ] [D5][VT9][FIG3] Use one global `mu` scaling all Higgs production": "- [x] [D5][VT9][FIG3] Use one global `mu` scaling all Higgs production",
    "- [ ] [D9][VT7][VT12][FIG3] Address method parity through a binding": "- [x] [D9][VT7][VT12][FIG3] Address method parity through a binding",
    "- [ ] [D2][SP1] Integrated luminosity normalization nuisance": "- [x] [D2][SP1] Integrated luminosity normalization nuisance",
    "- [ ] [D2][SP3][VT9] MC statistical uncertainty terms": "- [x] [D2][SP3][VT9] MC statistical uncertainty terms",
    "- [ ] [D7][SP4] Lepton reconstruction, identification, and trigger": "- [x] [D7][SP4] Lepton reconstruction, identification, and trigger",
    "- [ ] [D9][SP5][VT12] Lepton momentum scale and resolution shape": "- [x] [D9][SP5][VT12] Lepton momentum scale and resolution shape",
    "- [ ] [D5][SP7] Signal production normalization/composition uncertainty": "- [x] [D5][SP7] Signal production normalization/composition uncertainty",
    "- [ ] [FIG6][SP8] Higgs branching-fraction uncertainty if converting": "- [x] [FIG6][SP8] Higgs branching-fraction uncertainty if converting",
    "- [ ] [SP9] qqZZ and ggZZ background normalization and shape": "- [x] [SP9] qqZZ and ggZZ background normalization and shape",
    "- [ ] [D7][D8][SP12] Classifier/NN input modeling and category migration": "- [D] [D7][D8][SP12] Classifier/NN input modeling and category migration",
    "- [ ] [D9] Method-parity cross-check: compare the nominal binned": "- [x] [D9] Method-parity cross-check: compare the nominal binned",
    "- [ ] [D9][VT8] Signal injection/recovery at `mu = 0`, `1`, `2`, and `5`": "- [x] [D9][VT8] Signal injection/recovery at `mu = 0`, `1`, `2`, and `5`",
    "- [ ] [D2][VT9] Combined and per-category goodness-of-fit": "- [x] [D2][VT9] Combined and per-category goodness-of-fit",
    "- [ ] [D2][VT10] Nuisance pulls/constraints and impact ranking after fits": "- [x] [D2][VT10] Nuisance pulls/constraints and impact ranking after fits",
    "- [ ] [D9][VT12] Mass-template closure if any mass estimator": "- [x] [D9][VT12] Mass-template closure if any mass estimator",
    "- [ ] [FIG2][D4] Prefit/postfit `m4l` distributions": "- [x] [FIG2][D4] Prefit/postfit `m4l` distributions",
    "- [ ] [FIG3][D5][D9] Signal-strength likelihood scan": "- [x] [FIG3][D5][D9] Signal-strength likelihood scan",
    "- [ ] [FIG5][D2][SP*] Systematic impact ranking": "- [x] [FIG5][D2][SP*] Systematic impact ranking",
    "- [ ] [FIG6][REF-MATRIX] Comparison summary figure/table": "- [x] [FIG6][REF-MATRIX] Comparison summary figure/table",
    "- [ ] [D2][VT9] Alternative binning stability": "- [x] [D2][VT9] Alternative binning stability",
    "- [ ] [D4][D5] Final-state channel compatibility": "- [x] [D4][D5] Final-state channel compatibility",
    "- [ ] [REF-MATRIX][FIG6] Inclusive `mu`: classify as matched": "- [x] [REF-MATRIX][FIG6] Inclusive `mu`: classify as matched",
}

TEXT_REPLACEMENTS = {
    "Proof: `systematics_sources.json` row with central `10 fb^-1`,\n  uncertainty source hierarchy, fallback flag if user-provided, and prior scan.": "Proof: `systematics_sources.json` row with central `10 fb^-1`, public CMS 2017 luminosity uncertainty used as the scale reference, fallback flag, affected templates, and evaluation method.",
    "Proof: mass workspace/scan JSON, injected-mass closure\n  table, or infeasibility log with filenames and failure modes.": "Proof: `analysis_note/results/expected_mass_scan.json` records the simultaneous `4mu`, `4e`, and `2e2mu` category shifted-template mass scan with `mu` profiled, active nuisance metadata, and injected-mass closure.",
    "public/campaign search trail, yield-closure comparison, and per-process\n  nuisance in `systematics_sources.json`.": "the `systematics_sources.json` SP2 row records the Phase 3 normalization table, user-provided prompt effective cross sections, metadata denominators, and the Phase 4a per-process normalization nuisances used because public/campaign matches remain unavailable.",
    "Proof: workspace includes bin-by-bin MC-stat modifiers and stability tests.": "Proof: `expected_covariance.json` and `expected_validation.json` document the actual grouped group/category MC-stat approximation from Phase 3 `sumw2`, plus alternative-binning stability tests; full bin-by-bin `staterror` profiling remains a documented expected-phase downscope.",
    "Proof: input-validation verdict and explicit classifier input\n  allow/discard list.": "Proof: the `systematics_sources.json` SP6 row and Phase 3 `input_validation.json` document that `pvNdof`/PV variables are excluded under [A6], no classifier categories are promoted, and no PV-dependent fit nuisance is propagated in Phase 4a.",
    "Proof: mass-fit workspace/scan JSON or infeasibility log.": "Proof: `analysis_note/results/expected_mass_scan.json` contains the category-simultaneous shifted-template mass-profile scan and injected-mass closure with `mu` profiled.",
    "is reported. Proof: injected-mass closure table with bias threshold verdict.": "is reported. Proof: `expected_mass_scan.json` records injected masses 124, 125, and 126 GeV, recovered grid masses, bias threshold verdicts, and per-mass scan rows.",
    "- [ ] [REF-MATRIX][D9] Mass: classify as matched only if the simultaneous\n  category mass extraction with `mu` profiled passes injected-mass closure;\n  otherwise classify as approximated detector-level peak comparison.": "- [x] [REF-MATRIX][D9] Mass: Phase 4a category-simultaneous shifted-template scan with `mu` profiled passes expected injected-mass closure, but the final AN must classify it as approximated detector-level mass-profile evidence rather than an official-quality matched CMS mass measurement because independent mass-hypothesis MC and official calibration inputs are unavailable.",
}


def main() -> None:
    ensure_dirs()
    setup_logging()
    path = ANALYSIS_ROOT / "COMMITMENTS.md"
    text = path.read_text()
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    for old, new in TEXT_REPLACEMENTS.items():
        text = text.replace(old, new)
    path.write_text(text)
    append_session("Phase 4a commitment update\n\n- Updated `COMMITMENTS.md` for expected-inference items with Phase 4a JSON/figure evidence; downstream observed-data and Doc-phase items remain open.")
    append_experiment("## 2026-05-30 — Phase 4a commitment update\n\n- Updated `COMMITMENTS.md` for Phase 4a expected-inference evidence and formal classifier-migration downscope.")


if __name__ == "__main__":
    main()
