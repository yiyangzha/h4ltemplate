from __future__ import annotations

from pathlib import Path

from selection_common import ROOT, append_experiment, append_session


REPLACEMENTS = {
    "- [ ] [D1][VT1] Use primary prompt data/MC paths": "- [x] [D1][VT1] Use primary prompt data/MC paths",
    "- [ ] [D3][VT1][VT3] Enforce `105 < m4l < 140 GeV`": "- [x] [D3][VT1][VT3] Enforce `105 < m4l < 140 GeV`",
    "- [ ] [D4][VT6][VT13] Nominal categories are final states": "- [x] [D4][VT6][VT13] Nominal categories are final states",
    "- [ ] [D6][VT2][SP10] Use DY+jets MC as the default": "- [x] [D6][VT2][SP10] Use DY+jets MC as the default",
    "- [ ] [D7][VT4][FIG4] Apply the input-modeling gate": "- [x] [D7][VT4][FIG4] Apply the input-modeling gate",
    "- [ ] [D8][VT5][SP13] Attempt the angular NN only after": "- [x] [D8][VT5][SP13] Attempt the angular NN only after",
    "- [ ] [A2][SP2] Prompt effective cross-section validation": "- [x] [A2][SP2] Prompt effective cross-section validation",
    "- [ ] [A6][SP6] Pileup/PV modeling validation": "- [x] [A6][SP6] Pileup/PV modeling validation",
    "- [ ] [D6][SP10] DY+jets fake-proxy normalization": "- [x] [D6][SP10] DY+jets fake-proxy normalization",
    "- [ ] [L2][SP11] TTBar omission/inclusion cross-check": "- [x] [L2][SP11] TTBar omission/inclusion cross-check",
    "- [ ] [D8][SP13] Angular reconstruction uncertainty": "- [x] [D8][SP13] Angular reconstruction uncertainty",
    "- [ ] [A3] Jet/VBF decision gate": "- [D] [A3] Jet/VBF decision gate",
    "- [ ] [D1][VT1] File provenance check": "- [x] [D1][VT1] File provenance check",
    "- [ ] [D6][VT2] MC normalization check": "- [x] [D6][VT2] MC normalization check",
    "- [ ] [D3][VT3] Selection cutflow monotonicity": "- [x] [D3][VT3] Selection cutflow monotonicity",
    "- [ ] [D7][VT4] Candidate-variable data/MC validation": "- [x] [D7][VT4] Candidate-variable data/MC validation",
    "- [ ] [D7][VT4] Enforce input gate": "- [x] [D7][VT4] Enforce input gate",
    "- [ ] [D8][VT5] Angular reconstruction closure": "- [x] [D8][VT5] Angular reconstruction closure",
    "- [ ] [D4][VT6] S1 cut-based versus S2": "- [x] [D4][VT6] S1 cut-based versus S2",
    "- [ ] [A3][D4] VBF downscope review gate": "- [D] [A3][D4] VBF downscope review gate",
    "- [ ] [D7][D8][VT13] Angular/NN promotion gate": "- [x] [D7][D8][VT13] Angular/NN promotion gate",
    "- [ ] [FIG1][D6] Inclusive `m4l` stacked": "- [x] [FIG1][D6] Inclusive `m4l` stacked",
    "- [ ] [FIG4][D7][D8] Classifier/angular input validation": "- [x] [FIG4][D7][D8] Classifier/angular input validation",
    "- [ ] [A1][D1][VT1] Primary-vs-local ROOT copy freeze": "- [x] [A1][D1][VT1] Primary-vs-local ROOT copy freeze",
    "- [ ] [A3][D4] VBF recovery attempt": "- [D] [A3][D4] VBF recovery attempt",
    "- [ ] [A4][D8][VT5] Angular variables recomputed": "- [x] [A4][D8][VT5] Angular variables recomputed",
    "- [ ] [D8][VT5] Stored-vs-recomputed four-vector closure": "- [x] [D8][VT5] Stored-vs-recomputed four-vector closure",
    "- [ ] [L2][D6][SP11] TTBar reducible-background diagnostic": "- [x] [L2][D6][SP11] TTBar reducible-background diagnostic",
    "- [ ] [D6][SP10] Sideband background normalization": "- [x] [D6][SP10] Sideband background normalization",
    "- [ ] [D7][D8] Classifier mass-sculpting check": "- [x] [D7][D8] Classifier mass-sculpting check",
}


def main() -> None:
    path = ROOT / "COMMITMENTS.md"
    text = path.read_text()
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    path.write_text(text)
    append_session("2026-05-29 commitment update\n\n- Updated Phase 3-resolved and formally downscoped commitments in `COMMITMENTS.md`.")
    append_experiment("## 2026-05-29 — Phase 3 commitment update\n\n- Updated `COMMITMENTS.md` for Phase 3-resolved proof artifacts and formal VBF downscope items.")


if __name__ == "__main__":
    main()
