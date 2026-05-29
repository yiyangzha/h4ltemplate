from __future__ import annotations

from datetime import datetime, timezone

import awkward as ak
import hist
import numpy as np
import uproot

from phase1_utils import OUT, append_experiment, append_session, ensure_dirs, primary_files, setup_logging, write_json

SLICE = 1000

CANDIDATES = {
    "m4l": {
        "tokens": ("mass4l", "m4l", "zzmass", "fourleptonmass", "mass_4l"),
        "bins": (40, 70.0, 170.0),
        "xlabel": r"$m_{4\ell}$ [GeV]",
    },
    "z1_mass": {
        "tokens": ("z1mass", "massz1", "z1_mass", "z1_m", "mz1"),
        "bins": (40, 40.0, 120.0),
        "xlabel": r"$m_{Z1}$ [GeV]",
    },
    "z2_mass": {
        "tokens": ("z2mass", "massz2", "z2_mass", "z2_m", "mz2"),
        "bins": (40, 0.0, 120.0),
        "xlabel": r"$m_{Z2}$ [GeV]",
    },
    "pt4l": {
        "tokens": ("pt4l", "fourleptonpt"),
        "bins": (40, 0.0, 200.0),
        "xlabel": r"$p_T^{4\ell}$ [GeV]",
    },
    "eta4l": {
        "tokens": ("eta4l", "fourleptoneta"),
        "bins": (40, -5.0, 5.0),
        "xlabel": r"$\eta_{4\ell}$",
    },
    "leading_lepton_pt": {
        "tokens": ("l1pt", "lep1pt", "leadingleptonpt"),
        "bins": (40, 0.0, 200.0),
        "xlabel": r"Leading lepton $p_T$ [GeV]",
    },
    "njets": {
        "tokens": ("njets", "njet", "n_jets", "jetmultiplicity"),
        "bins": (8, -0.5, 7.5),
        "xlabel": "Jet multiplicity",
    },
    "lead_jet_pt": {
        "tokens": ("leadjetpt", "jet1pt", "leadingjetpt", "j1pt"),
        "bins": (40, 0.0, 200.0),
        "xlabel": r"Leading jet $p_T$ [GeV]",
    },
    "d_bkg_kin": {
        "tokens": ("dbkg", "d_bkg", "kinbkg", "dkin", "mela"),
        "bins": (40, 0.0, 1.0),
        "xlabel": "Kinematic background discriminant",
    },
}


def canonical(name: str) -> str:
    return "".join(ch for ch in name.lower() if ch.isalnum())


def find_candidates(branches: list[str]) -> dict[str, str]:
    mapped = {}
    normalized = {branch: canonical(branch) for branch in branches}
    for observable, cfg in CANDIDATES.items():
        for branch, clean in normalized.items():
            if any(token in clean for token in cfg["tokens"]):
                mapped[observable] = branch
                break
    return mapped


def flatten_numeric(array: ak.Array) -> np.ndarray:
    flat = ak.flatten(array, axis=None)
    if len(flat) == 0:
        return np.asarray([])
    try:
        values = np.asarray(ak.to_numpy(flat), dtype=float)
    except (TypeError, ValueError):
        return np.asarray([])
    return values[np.isfinite(values)]


def fill_counts(values: np.ndarray, bins: tuple[int, float, float]) -> tuple[list[float], list[float]]:
    h = hist.Hist(hist.axis.Regular(bins[0], bins[1], bins[2], name="x"))
    h.fill(values)
    return h.axes[0].edges.tolist(), h.values().astype(float).tolist()


def main() -> None:
    ensure_dirs()
    log = setup_logging()
    observables: dict[str, dict] = {key: {"config": cfg, "samples": []} for key, cfg in CANDIDATES.items()}
    discovery = []
    for file_info in primary_files():
        with uproot.open(file_info["path"]) as root_file:
            for key in root_file.keys():
                tree = root_file[key]
                if not hasattr(tree, "arrays") or key.split(";")[0].lower() == "metadata":
                    continue
                branches = list(tree.keys())
                mapping = find_candidates(branches)
                discovery.append({"file": file_info["name"], "tree": key, "mapping": mapping})
                if not mapping:
                    continue
                arrays = tree.arrays(list(mapping.values()), entry_stop=min(SLICE, int(tree.num_entries)), library="ak")
                for observable, branch in mapping.items():
                    values = flatten_numeric(arrays[branch])
                    if len(values) == 0:
                        continue
                    edges, counts = fill_counts(values, CANDIDATES[observable]["bins"])
                    observables[observable]["samples"].append(
                        {
                            "file": file_info["name"],
                            "kind": file_info["kind"],
                            "group": file_info["sample_info"].get("group", file_info["kind"]),
                            "branch": branch,
                            "entries_loaded": int(min(SLICE, int(tree.num_entries))),
                            "values_plotted": int(len(values)),
                            "edges": edges,
                            "counts": counts,
                        }
                    )
                    log.info("Filled %s from %s:%s", observable, file_info["name"], branch)
    write_json(
        OUT / "exploration_histograms.json",
        {"created_utc": datetime.now(timezone.utc).isoformat(), "slice_entries": SLICE, "observables": observables, "discovery": discovery},
    )
    append_session(
        "2026-05-29 exploration histograms\n\n"
        "- Wrote `phase1_exploration/outputs/exploration_histograms.json` from "
        "small-slice candidate variables."
    )
    append_experiment(
        "## 2026-05-29 — Phase 1 histogram summaries\n\n"
        "- Produced small-slice histogram summaries for available 4l mass, Z mass, "
        "jet, and discriminant candidate branches."
    )


if __name__ == "__main__":
    main()
