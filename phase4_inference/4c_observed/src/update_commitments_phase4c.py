from __future__ import annotations

from observed_common import ANALYSIS_ROOT, append_experiment, append_session, ensure_dirs, setup_logging


REPLACEMENTS = {
    "Proof: `analysis_note/results/expected_mass_scan.json` records the simultaneous `4mu`, `4e`, and `2e2mu` category shifted-template mass scan with `mu` profiled, active nuisance metadata, and injected-mass closure.": "Proof: `analysis_note/results/expected_mass_scan.json` records expected shifted-template closure, and `analysis_note/results/observed_mass_scan.json` records the full-data observed shifted-template mass scan with `mu` profiled at each mass hypothesis. Both are approximated detector-level evidence, not official calibrated CMS-quality mass measurements.",
    "Proof: `analysis_note/results/expected_mass_scan.json` contains the category-simultaneous shifted-template mass-profile scan and injected-mass closure with `mu` profiled.": "Proof: `analysis_note/results/expected_mass_scan.json` contains expected shifted-template closure, and `analysis_note/results/observed_mass_scan.json` contains the full-data observed category-simultaneous mass-profile scan with `mu` profiled.",
    "- [ ] [D2][SP3][VT9] Full bin-by-bin MC statistical uncertainty terms for all\n  fit templates. Status: formally downscoped in Phase 4a, not completed.": "- [D] [D2][SP3][VT9] Full bin-by-bin MC statistical uncertainty terms for all\n  fit templates. Status: formally downscoped in Phase 4a and retained in Phase 4c.",
    "- [x] [D9][VT12] Mass-template closure if any mass estimator or morphing scan\n  is reported. Proof: `expected_mass_scan.json` records injected masses 115, 125, and 135 GeV, recovered grid masses, bias threshold verdicts, and per-mass scan rows.": "- [x] [D9][VT12] Mass-template closure if any mass estimator or morphing scan\n  is reported. Proof: `expected_mass_scan.json` records injected masses 115, 125, and 135 GeV, recovered grid masses, bias threshold verdicts, and per-mass scan rows; `observed_mass_scan.json` reports the full-data observed scan separately without assuming M125.",
    "- [ ] [REF-MATRIX] Fiducial cross section: classify as matched only if a\n  documented acceptance/fiducial conversion is implemented with cited\n  branching-fraction and acceptance inputs; otherwise approximated or\n  unavailable.": "- [D] [REF-MATRIX] Fiducial cross section: unavailable in the final result because no reviewed acceptance/fiducial conversion with cited branching-fraction and acceptance inputs was implemented; Phase 4c reports detector-level signal strength only.",
    "- [ ] [REF-MATRIX] Width: classify as unavailable unless a validated width\n  likelihood/shape interpretation is implemented; no pull required when\n  unavailable.": "- [D] [REF-MATRIX] Width: unavailable in the final result because no validated width likelihood/shape interpretation was implemented; no pull is reported.",
    "- [ ] [REF-MATRIX][D4] Production-sensitive categories: classify as matched\n  only for categories with comparable observables and acceptance; otherwise\n  approximated/not directly comparable.": "- [D] [REF-MATRIX][D4] Production-sensitive categories: not directly comparable because Phase 4c retains final-state S1 categories only and no reviewed production-sensitive category is promoted.",
    "- [ ] [REF-MATRIX][A3] VBF categories: classify as unavailable/not measured\n  unless real jet recovery passes; lepton-only proxies are not VBF matches.": "- [D] [REF-MATRIX][A3] VBF categories: unavailable/not measured because real jet recovery did not pass and no lepton-only proxy is labeled as VBF.",
    "- [ ] [REF-MATRIX][D6] Reducible-background treatment: classify as\n  approximated because DY+jets MC replaces official data-driven Z+X unless a\n  later reviewed method changes this.": "- [D] [REF-MATRIX][D6] Reducible-background treatment: approximated because DY+jets MC remains the nominal fake proxy and no later reviewed data-driven Z+X method replaced it.",
    "- [x] [REF-MATRIX][D9] Mass: Phase 4a category-simultaneous shifted-template scan with `mu` profiled passes expected injected-mass closure, but the final AN must classify it as approximated detector-level mass-profile evidence rather than an official-quality matched CMS mass measurement because independent mass-hypothesis MC and official calibration inputs are unavailable.": "- [x] [REF-MATRIX][D9] Mass: Phase 4a category-simultaneous shifted-template scan with `mu` profiled passes expected injected-mass closure, and Phase 4c adds a full-data observed shifted-template mass scan. The final AN must classify the mass result as approximated detector-level mass-profile evidence rather than an official-quality matched CMS mass measurement because independent mass-hypothesis MC and official calibration/morphing inputs are unavailable.",
}


def main() -> None:
    ensure_dirs()
    logger = setup_logging()
    path = ANALYSIS_ROOT / "COMMITMENTS.md"
    text = path.read_text()
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    path.write_text(text)
    remaining = [line for line in text.splitlines() if line.startswith("- [ ]")]
    append_session(
        "Commitments updated for Phase 4c\n\n"
        f"- Remaining unchecked top-level checklist items: {len(remaining)}.\n"
        "- Marked final unavailable comparison products as formal downscopes."
    )
    append_experiment(
        "## 2026-05-30 — Phase 4c commitments update\n\n"
        "- Marked remaining feasible final commitments resolved or formally downscoped.\n"
        f"- Remaining unchecked top-level checklist items after update: {len(remaining)}."
    )
    logger.info("Updated %s; remaining unchecked items: %d", path, len(remaining))


if __name__ == "__main__":
    main()
