#!/usr/bin/env python3
"""
Validate and plot NanoAOD modifications produced by modify_nanoaod.cpp.

This script intentionally does not rewrite ROOT files. It reads a plotting
config with explicit input/output ROOT file pairs, then uses the
modify_nanoaod.cpp config only for branch names and expected modification
parameters.
"""

from __future__ import annotations

import argparse
import glob
import itertools
import json
import math
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

import numpy as np

try:
    import awkward as ak
    import uproot
except ImportError as exc:
    raise SystemExit(
        "Missing Python dependency. Use an environment with uproot, awkward, numpy, matplotlib, mplhep, and PyROOT."
    ) from exc

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, TwoSlopeNorm

try:
    import ROOT
    import mplhep as hep
except ImportError as exc:
    raise SystemExit(
        "Missing Python dependency. Use an environment with uproot, awkward, numpy, matplotlib, mplhep, and PyROOT."
    ) from exc

ROOT.gROOT.SetBatch(True)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)


BLUE = "#5790fc"
RED = "#e42536"
GRAY = "#9c9ca1"
Z_MASS = 91.1876
MASS_FIT_MIN = 55.0
MASS_FIT_MAX = 135.0
MASS_FIT_ALT_MAX = 100.0
MASS_PEAK_SEARCH_MIN = 75.0
MASS_PEAK_SEARCH_MAX = 115.0
UINT64 = np.uint64
MASK64 = (1 << 64) - 1
TNP_FIT_COUNTER = itertools.count()
TNP_MIN_FIT_ALL = 40
TNP_MIN_FIT_EACH = 5
TNP_SINGLE_CB_MIN_ALL = 120
TNP_SINGLE_CB_MIN_PASS = 20
TNP_DOUBLE_CB_MIN_ALL = 600
TNP_DOUBLE_CB_MIN_PASS = 80
TNP_CHI2_BINS = 40
TNP_MAX_CHI2_NDF = 8.0
MIN_EFF_BIN_TOTAL = 20
TRUTH_MATCH_DR = 0.1
GEN_TRUTH_BRANCHES = [
    "nGenPart",
    "GenPart_pt",
    "GenPart_eta",
    "GenPart_phi",
    "GenPart_pdgId",
    "GenPart_genPartIdxMother",
    "GenPart_statusFlags",
]


def load_config(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def resolve_path(raw: str, base_dir: Path) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else base_dir / path


def flavor_prefix(flavor: str) -> str:
    return "Muon" if flavor == "muon" else "Electron"


def lepton_branches(cfg: Mapping, flavor: str) -> Mapping[str, str]:
    defaults = {
        "muon": {
            "n": "nMuon",
            "pt": "Muon_pt",
            "eta": "Muon_eta",
            "phi": "Muon_phi",
            "mass": "Muon_mass",
            "charge": "Muon_charge",
        },
        "electron": {
            "n": "nElectron",
            "pt": "Electron_pt",
            "eta": "Electron_eta",
            "phi": "Electron_phi",
            "mass": "Electron_mass",
            "charge": "Electron_charge",
        },
    }[flavor].copy()
    defaults.update(cfg.get("branches", {}).get(flavor, {}))
    return defaults


def event_id_branches(cfg: Mapping) -> Mapping[str, str]:
    defaults = {"run": "run", "luminosityBlock": "luminosityBlock", "event": "event"}
    defaults.update(cfg.get("branches", {}).get("event_id", {}))
    return defaults


def efficiency_branch_cfgs(cfg: Mapping, flavor: str) -> Mapping[str, Mapping]:
    eff = cfg.get("efficiency", {})
    key = "muon_branches" if flavor == "muon" else "electron_branches"
    return eff.get(key, {})


def event_efficiency_branch_cfgs(cfg: Mapping) -> Mapping[str, Mapping]:
    return cfg.get("efficiency", {}).get("event_branches", {})


def sanitize(name: str) -> str:
    out = []
    for char in name:
        out.append(char if char.isalnum() or char in "._-" else "_")
    return "".join(out)


def efficiency_specs(plot_cfg: Mapping, modify_cfg: Mapping) -> List[Dict]:
    specs = []
    default_variables = ["pt", "eta", "phi"]
    configured = plot_cfg.get("efficiencies")
    if configured:
        for item in configured:
            flavor = item["flavor"]
            variables = item.get("variables", default_variables)
            for branch in item.get("branches", []):
                specs.append({
                    "level": item.get("level", "lepton"),
                    "flavor": flavor,
                    "branch": branch,
                    "variables": list(variables),
                })
        return specs

    for flavor in ("muon", "electron"):
        for branch in efficiency_branch_cfgs(modify_cfg, flavor):
            specs.append({"level": "lepton", "flavor": flavor, "branch": branch, "variables": default_variables.copy()})
    for branch, cfg in event_efficiency_branch_cfgs(modify_cfg).items():
        specs.append({
            "level": "event",
            "flavor": cfg.get("reference_flavor", "muon"),
            "branch": branch,
            "variables": default_variables.copy(),
        })
    return specs


def lepton_distribution_specs(plot_cfg: Mapping) -> List[Dict]:
    configured = plot_cfg.get("distributions", {}).get("lepton")
    if configured:
        return [
            {
                "flavor": item["flavor"],
                "variables": list(item.get("variables", ["pt", "energy", "relative_pt_shift", "smear_response"])),
            }
            for item in configured
        ]
    return [
        {"flavor": "muon", "variables": ["pt", "energy", "relative_pt_shift", "smear_response"]},
        {"flavor": "electron", "variables": ["pt", "energy", "relative_pt_shift", "smear_response"]},
    ]


def dilepton_distribution_specs(plot_cfg: Mapping) -> List[Dict]:
    configured = plot_cfg.get("distributions", {}).get("dilepton")
    if configured:
        return [
            {
                "flavor": item["flavor"],
                "variables": list(item.get("variables", ["mass", "pt", "eta", "phi"])),
            }
            for item in configured
        ]
    return [
        {"flavor": "muon", "variables": ["mass", "pt", "eta", "phi"]},
        {"flavor": "electron", "variables": ["mass", "pt", "eta", "phi"]},
    ]


def selected_efficiency_branches(plot_cfg: Mapping, modify_cfg: Mapping, flavor: str) -> Dict[str, Mapping]:
    selected = {
        spec["branch"]
        for spec in efficiency_specs(plot_cfg, modify_cfg)
        if spec["level"] == "lepton" and spec["flavor"] == flavor
    }
    all_cfgs = efficiency_branch_cfgs(modify_cfg, flavor)
    return {branch: all_cfgs[branch] for branch in selected if branch in all_cfgs}


def selected_event_efficiency_branches(plot_cfg: Mapping, modify_cfg: Mapping, flavor: str) -> Dict[str, Mapping]:
    selected = {
        spec["branch"]
        for spec in efficiency_specs(plot_cfg, modify_cfg)
        if spec["level"] == "event" and spec["flavor"] == flavor
    }
    all_cfgs = event_efficiency_branch_cfgs(modify_cfg)
    return {branch: all_cfgs[branch] for branch in selected if branch in all_cfgs}


def selected_tnp_fit_branches(plot_cfg: Mapping, modify_cfg: Mapping, flavor: str) -> set:
    tnp_cfg = plot_cfg.get("tnp_fits", {})
    configured = tnp_cfg.get("branches")
    if configured is None:
        return set(selected_efficiency_branches(plot_cfg, modify_cfg, flavor))
    if isinstance(configured, Mapping):
        return set(configured.get(flavor, []))
    return set(configured)


def selected_tnp_fit_variables(plot_cfg: Mapping, variables: Sequence[str]) -> List[str]:
    configured = plot_cfg.get("tnp_fits", {}).get("variables")
    if configured is None:
        return list(variables)
    allowed = set(configured)
    return [var for var in variables if var in allowed]


def tnp_tag_id_branch(flavor: str) -> str:
    return "Muon_mediumId" if flavor == "muon" else "Electron_cutBased"


def tnp_tag_id_cfg(cfg: Mapping, flavor: str) -> Mapping:
    branch = tnp_tag_id_branch(flavor)
    all_cfgs = efficiency_branch_cfgs(cfg, flavor)
    if branch in all_cfgs:
        return all_cfgs[branch]
    if flavor == "muon":
        return {"type": "bool"}
    return {"type": "int_wp", "pass_threshold": 3}


def fnv1a64(text: str) -> int:
    h = 1469598103934665603
    for byte in text.encode():
        h ^= byte
        h = (h * 1099511628211) & MASK64
    return h


def short_hash_hex(text: str) -> str:
    return f"{fnv1a64(text) & 0xFFFFFFFF:08x}"


def contains_glob_meta(path: str) -> bool:
    return any(char in path for char in "*?[")


def path_entries(section: Mapping) -> List[str]:
    entries: List[str] = []
    if "path" in section:
        entries.append(section["path"])
    if "file" in section:
        entries.append(section["file"])
    entries.extend(section.get("paths", []))
    entries.extend(section.get("files", []))
    return entries


def expand_root_paths(section: Mapping, base_dir: Path, allow_missing_file: bool = False) -> List[Path]:
    recursive = bool(section.get("recursive", False))
    files = set()
    for raw in path_entries(section):
        path = resolve_path(raw, base_dir)
        raw_pattern = str(path)
        if contains_glob_meta(raw):
            for match in glob.glob(raw_pattern, recursive=recursive):
                matched = Path(match)
                if matched.is_file() and matched.suffix == ".root":
                    files.add(matched.resolve())
            continue
        if path.is_dir():
            iterator = path.rglob("*.root") if recursive else path.glob("*.root")
            for match in iterator:
                if match.is_file():
                    files.add(match.resolve())
            continue
        if path.suffix == ".root" and (allow_missing_file or path.exists()):
            files.add(path.resolve())
    return sorted(files)


def output_directory_from_config(output_cfg: Mapping, base_dir: Path, modify_cfg: Mapping) -> Optional[Path]:
    if "directory" in output_cfg:
        return resolve_path(output_cfg["directory"], base_dir)
    entries = path_entries(output_cfg)
    if len(entries) == 1 and not contains_glob_meta(entries[0]):
        candidate = resolve_path(entries[0], base_dir)
        if candidate.suffix != ".root":
            return candidate
        if candidate.is_dir():
            return candidate
    if not entries:
        modify_output = modify_cfg.get("output", {})
        return resolve_path(modify_output.get("directory", "modified"), base_dir)
    return None


def make_expected_outputs(inputs: Sequence[Path], out_dir: Path, suffix: str) -> List[Path]:
    outputs = []
    used = set()
    for src in inputs:
        ext = src.suffix or ".root"
        out = out_dir / f"{src.stem}{suffix}{ext}"
        resolved = out.resolve()
        if resolved in used:
            out = out_dir / f"{src.stem}_{short_hash_hex(str(src))}{suffix}{ext}"
            resolved = out.resolve()
        used.add(resolved)
        outputs.append(out)
    return outputs


def match_outputs_by_suffix(inputs: Sequence[Path], outputs: Sequence[Path], suffix: str) -> Optional[List[Path]]:
    by_name = {out.name: out for out in outputs}
    matched = []
    for src in inputs:
        expected_name = f"{src.stem}{suffix}{src.suffix or '.root'}"
        out = by_name.get(expected_name)
        if out is None:
            return None
        matched.append(out)
    return matched


def file_pairs(plot_cfg: Mapping, modify_cfg: Mapping, base_dir: Path) -> List[Tuple[Path, Path]]:
    suffix = plot_cfg.get("output", {}).get("suffix", modify_cfg.get("output", {}).get("suffix", "_modified"))

    if "files" in plot_cfg:
        pairs: List[Tuple[Path, Path]] = []
        for item in plot_cfg["files"]:
            if "input" not in item or "output" not in item:
                raise ValueError("Each config_plot.json files entry must contain input and output")
            input_cfg = {"path": item["input"], "recursive": item.get("recursive", False)}
            output_cfg = {"path": item["output"], "recursive": item.get("recursive", False), "suffix": item.get("suffix", suffix)}
            inputs = expand_root_paths(input_cfg, base_dir, allow_missing_file=True)
            out_dir = output_directory_from_config(output_cfg, base_dir, modify_cfg)
            if out_dir is not None:
                outputs = make_expected_outputs(inputs, out_dir, output_cfg["suffix"])
            else:
                outputs = expand_root_paths(output_cfg, base_dir, allow_missing_file=True)
                matched = match_outputs_by_suffix(inputs, outputs, output_cfg["suffix"])
                if matched is not None:
                    outputs = matched
            if len(inputs) != len(outputs):
                raise ValueError(f"Cannot pair input/output files for config_plot files entry {item}")
            pairs.extend(zip(inputs, outputs))
        return pairs

    input_cfg = plot_cfg.get("input", {})
    output_cfg = plot_cfg.get("output", {})
    inputs = expand_root_paths(input_cfg, base_dir, allow_missing_file=True)
    if not inputs:
        raise ValueError("config_plot.json input did not match any ROOT files")

    out_dir = output_directory_from_config(output_cfg, base_dir, modify_cfg)
    if out_dir is not None:
        outputs = make_expected_outputs(inputs, out_dir, suffix)
    else:
        outputs = expand_root_paths(output_cfg, base_dir, allow_missing_file=True)
        matched = match_outputs_by_suffix(inputs, outputs, suffix)
        if matched is not None:
            outputs = matched
        elif len(outputs) != len(inputs):
            raise ValueError(
                "config_plot.json output must be a directory+suffix, or must match the number of input ROOT files"
            )
    if len(inputs) != len(outputs):
        raise ValueError("config_plot.json input/output ROOT file counts do not match")
    return list(zip(inputs, outputs))


def open_tree(path: Path, tree_name: str):
    root_file = uproot.open(path)
    if tree_name not in root_file:
        raise RuntimeError(f"{path} does not contain tree {tree_name!r}")
    return root_file[tree_name]


def existing_branches(tree, requested: Iterable[str]) -> List[str]:
    keys = set(tree.keys())
    out = []
    for name in requested:
        if name and name in keys and name not in out:
            out.append(name)
    return out


def warn_missing(tree, requested: Iterable[str], context: str) -> None:
    keys = set(tree.keys())
    for name in sorted(set(x for x in requested if x)):
        if name not in keys:
            print(f"[WARN] {context}: missing branch {name}")


def print_progress(label: str, done: int, total: int, last_bucket: int) -> int:
    if total <= 0:
        return last_bucket
    bucket = min(20, int(math.floor(20.0 * float(done) / float(total))))
    if bucket == last_bucket and done != total:
        return last_bucket
    percent = 100.0 * float(done) / float(total)
    print(f"[INFO] {label}: {percent:5.1f}% ({done}/{total})", flush=True)
    return bucket


def read_arrays(tree, branches: Iterable[str], start: int, stop: int, context: str) -> Dict[str, ak.Array]:
    wanted = list(dict.fromkeys(b for b in branches if b))
    warn_missing(tree, wanted, context)
    present = existing_branches(tree, wanted)
    if not present:
        return {}
    return tree.arrays(present, entry_start=start, entry_stop=stop, library="ak", how=dict)


def to_numpy_flat(values) -> np.ndarray:
    if values is None:
        return np.array([], dtype=float)
    if isinstance(values, ak.Array):
        if values.ndim > 1:
            flat = ak.flatten(values, axis=1)
        else:
            flat = values
        arr = ak.to_numpy(flat)
    else:
        arr = np.asarray(values)
    arr = np.asarray(arr, dtype=float)
    return arr[np.isfinite(arr)]


def flatten_jagged(values) -> Tuple[np.ndarray, np.ndarray]:
    counts = ak.to_numpy(ak.num(values, axis=1)).astype(np.int64)
    if int(np.sum(counts)) == 0:
        return np.array([], dtype=float), counts
    return ak.to_numpy(ak.flatten(values, axis=1)), counts


def unflatten_like(flat: np.ndarray, counts: np.ndarray) -> ak.Array:
    return ak.unflatten(flat, counts)


def signed_eta_edges_from_abs(abs_eta_edges: Sequence[float]) -> List[float]:
    abs_edges = [float(x) for x in abs_eta_edges]
    return [-x for x in reversed(abs_edges) if x > 0.0] + abs_edges


def bin_edges(modify_cfg: Mapping, plot_cfg: Mapping) -> Dict[str, np.ndarray]:
    eff_binning = modify_cfg.get("efficiency", {}).get("binning", {})
    pt_edges = np.asarray(eff_binning.get("pt", [5, 10, 20, 30, 40, 50, 80, 120, 200]), dtype=float)
    abs_eta_edges = np.asarray(eff_binning.get("abs_eta", [0.0, 0.8, 1.2, 1.4442, 1.566, 2.0, 2.5]), dtype=float)
    signed_eta = eff_binning.get("eta", signed_eta_edges_from_abs(abs_eta_edges))

    hist_pt = np.unique(np.concatenate(([0.0], pt_edges, [max(300.0, pt_edges[-1] * 1.5)])))
    validation = plot_cfg.get("binning", {})
    return {
        "eff_pt": np.asarray(validation.get("eff_pt", pt_edges), dtype=float),
        "eff_eta": np.asarray(validation.get("eff_eta", signed_eta), dtype=float),
        "eff_phi": np.asarray(validation.get("eff_phi", np.linspace(-math.pi, math.pi, 17)), dtype=float),
        "hist_pt": np.asarray(validation.get("lepton_pt", hist_pt), dtype=float),
        "hist_energy": np.asarray(validation.get("lepton_energy", [0, 10, 20, 30, 40, 50, 80, 120, 200, 300, 500]), dtype=float),
        "hist_shift": np.asarray(validation.get("relative_shift", np.linspace(-0.05, 0.05, 61)), dtype=float),
        "hist_smear": np.asarray(validation.get("smear_response", np.linspace(-0.05, 0.05, 61)), dtype=float),
        "dilepton_mass": np.asarray(validation.get("dilepton_mass", np.linspace(50, 130, 81)), dtype=float),
        "dilepton_pt": np.asarray(validation.get("dilepton_pt", np.linspace(0, 300, 61)), dtype=float),
        "dilepton_eta": np.asarray(validation.get("dilepton_eta", np.linspace(-5, 5, 41)), dtype=float),
        "dilepton_phi": np.asarray(validation.get("dilepton_phi", np.linspace(-math.pi, math.pi, 41)), dtype=float),
    }


def cms_style() -> None:
    hep.style.use("CMS")
    plt.rcParams.update(
        {
            "figure.figsize": (7.0, 6.0),
            "font.family": "DejaVu Sans",
            "font.size": 15,
            "axes.labelsize": 17,
            "axes.linewidth": 1.2,
            "axes.grid": False,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "legend.frameon": False,
            "legend.fontsize": 13,
            "savefig.bbox": "tight",
        }
    )


def add_cms_label(ax, right_text: str = "Simulation") -> None:
    del right_text
    hep.cms.label("Preliminary", data=False, com=13, ax=ax)


def bin_index(values: np.ndarray, edges: np.ndarray) -> np.ndarray:
    idx = np.searchsorted(edges, values, side="right") - 1
    return np.clip(idx, 0, len(edges) - 2)


def flat_eff_bin(
    cfg: Mapping, pt: np.ndarray, eta: np.ndarray, energy: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    eff_binning = cfg.get("efficiency", {}).get("binning", {})
    pt_edges = np.asarray(eff_binning.get("pt", [5, 10, 20, 30, 40, 50, 80, 120, 200]), dtype=float)
    abs_eta_edges = np.asarray(eff_binning.get("abs_eta", [0.0, 0.8, 1.2, 1.4442, 1.566, 2.0, 2.5]), dtype=float)
    eta_edges = np.asarray(eff_binning.get("eta", signed_eta_edges_from_abs(abs_eta_edges)), dtype=float)
    energy_edges = eff_binning.get("energy")

    pt_bin = bin_index(pt, pt_edges)
    eta_bin = bin_index(eta, eta_edges)
    abs_eta_bin = bin_index(np.abs(eta), abs_eta_edges)
    n_pt = len(pt_edges) - 1
    n_eta = len(eta_edges) - 1
    if energy_edges:
        e_edges = np.asarray(energy_edges, dtype=float)
        if energy is None:
            energy = np.maximum(pt, 0.0) * np.cosh(eta)
        energy_bin = bin_index(energy, e_edges)
        flat = (energy_bin * n_eta + eta_bin) * n_pt + pt_bin
    else:
        flat = eta_bin * n_pt + pt_bin
    return flat, pt_bin, eta_bin, abs_eta_bin


def n_eff_bins(cfg: Mapping) -> int:
    eff_binning = cfg.get("efficiency", {}).get("binning", {})
    n_pt = len(eff_binning.get("pt", [5, 10, 20, 30, 40, 50, 80, 120, 200])) - 1
    abs_eta_edges = eff_binning.get("abs_eta", [0.0, 0.8, 1.2, 1.4442, 1.566, 2.0, 2.5])
    n_eta = len(eff_binning.get("eta", signed_eta_edges_from_abs(abs_eta_edges))) - 1
    n_energy = max(1, len(eff_binning.get("energy", [])) - 1)
    return n_pt * n_eta * n_energy


def pass_mask(values, eff_cfg: Mapping):
    eff_type = eff_cfg.get("type", "bool")
    if eff_type == "int_wp":
        return values >= int(eff_cfg.get("pass_threshold", 1))
    if eff_type == "float_max":
        return values <= float(eff_cfg.get("max", eff_cfg.get("pass_threshold", 0.15)))
    return values != 0


def lepton_energy(pt, eta, mass):
    return np.sqrt((pt * np.cosh(eta)) ** 2 + mass**2)


def awkward_energy(pt, eta, mass):
    return np.sqrt((pt * np.cosh(eta)) ** 2 + mass**2)


def splitmix64_np(x: np.ndarray) -> np.ndarray:
    x = x.astype(UINT64) + UINT64(0x9E3779B97F4A7C15)
    x = (x ^ (x >> UINT64(30))) * UINT64(0xBF58476D1CE4E5B9)
    x = (x ^ (x >> UINT64(27))) * UINT64(0x94D049BB133111EB)
    return x ^ (x >> UINT64(31))


def uniform01_np(key: np.ndarray) -> np.ndarray:
    x = splitmix64_np(key)
    return ((x >> UINT64(11)).astype(np.float64)) * (1.0 / 9007199254740992.0)


def normal01_np(key: np.ndarray) -> np.ndarray:
    u1 = np.maximum(uniform01_np(key), np.finfo(float).tiny)
    u2 = uniform01_np(key ^ UINT64(0xD1B54A32D192ED03))
    return np.sqrt(-2.0 * np.log(u1)) * np.cos(2.0 * math.pi * u2)


def hash_combine_np(seed: np.ndarray, value: np.ndarray) -> np.ndarray:
    value = value.astype(UINT64)
    return seed ^ (value + UINT64(0x9E3779B97F4A7C15) + (seed << UINT64(6)) + (seed >> UINT64(2)))


def object_keys(
    cfg: Mapping,
    arrays: Mapping[str, ak.Array],
    pt_like,
    start_entry: int,
    flavor: str,
    stream: str,
) -> np.ndarray:
    flat_pt, counts = flatten_jagged(pt_like)
    n = len(flat_pt)
    event_ids = event_id_branches(cfg)
    n_events = len(counts)

    def scalar_branch(name: str) -> np.ndarray:
        if name in arrays:
            return ak.to_numpy(arrays[name]).astype(np.uint64)
        return np.zeros(n_events, dtype=np.uint64)

    run = scalar_branch(event_ids["run"])
    lumi = scalar_branch(event_ids["luminosityBlock"])
    event = scalar_branch(event_ids["event"])
    entries = np.arange(start_entry, start_entry + n_events, dtype=np.uint64)
    object_index = ak.to_numpy(ak.flatten(ak.local_index(pt_like, axis=1), axis=1)).astype(np.uint64)

    run_obj = np.repeat(run, counts)
    lumi_obj = np.repeat(lumi, counts)
    event_obj = np.repeat(event, counts)
    entry_obj = np.repeat(entries, counts)
    zero_event = (run_obj == 0) & (lumi_obj == 0) & (event_obj == 0)

    seed = np.full(n, UINT64(int(cfg.get("global", {}).get("seed", 314159))), dtype=np.uint64)
    for value in (run_obj, lumi_obj, event_obj):
        seed = hash_combine_np(seed, value)
    seed = np.where(zero_event, hash_combine_np(seed, entry_obj), seed)
    seed = hash_combine_np(seed, object_index)
    seed = hash_combine_np(seed, np.full(n, 13 if flavor == "muon" else 11, dtype=np.uint64))
    seed = hash_combine_np(seed, np.full(n, fnv1a64(stream), dtype=np.uint64))
    return seed


def region_shift(regions: Mapping, eta: np.ndarray, pt: np.ndarray, charge: np.ndarray, pt_ref: float) -> np.ndarray:
    shift = np.zeros_like(pt, dtype=float)
    abs_eta = np.abs(eta)
    for params in regions.values():
        mask = (abs_eta >= float(params.get("abs_eta_min", 0.0))) & (
            abs_eta < float(params.get("abs_eta_max", np.inf))
        )
        log_term = np.log(np.maximum(pt, 1.0e-9) / max(pt_ref, 1.0e-9))
        shift = np.where(
            mask,
            float(params.get("constant", 0.0))
            + float(params.get("pt_slope_log", 0.0)) * log_term
            + float(params.get("charge_asymmetry", 0.0)) * charge,
            shift,
        )
    return shift


def region_sigma(regions: Mapping, eta: np.ndarray, pt: np.ndarray, pt_ref: float) -> np.ndarray:
    sigma = np.zeros_like(pt, dtype=float)
    abs_eta = np.abs(eta)
    for params in regions.values():
        mask = (abs_eta >= float(params.get("abs_eta_min", 0.0))) & (
            abs_eta < float(params.get("abs_eta_max", np.inf))
        )
        log_term = np.log(np.maximum(pt, 1.0e-9) / max(pt_ref, 1.0e-9))
        value = float(params.get("sigma", 0.0)) + float(params.get("pt_slope_log", 0.0)) * log_term
        sigma = np.where(mask, np.maximum(value, 0.0), sigma)
    return sigma


def expected_pt_arrays(
    cfg: Mapping,
    arrays: Mapping[str, ak.Array],
    flavor: str,
    start_entry: int,
    pt,
    eta,
    phi,
    mass,
    charge,
    protect_boson_mass: bool = False,
) -> Tuple[ak.Array, ak.Array]:
    flat_pt, counts = flatten_jagged(pt)
    flat_eta, _ = flatten_jagged(eta)
    if charge is None:
        flat_charge = np.zeros_like(flat_pt)
    else:
        flat_charge, _ = flatten_jagged(charge)

    scale_cfg = cfg.get("scale", {})
    pt_ref = float(scale_cfg.get("pt_reference", 45.0))
    scaled = flat_pt.copy().astype(float)
    if scale_cfg.get("enabled", True):
        shift = region_shift(scale_cfg.get(flavor, {}), flat_eta, flat_pt, flat_charge, pt_ref)
        scaled = flat_pt * (1.0 + shift)
    if protect_boson_mass:
        scaled = protect_boson_pair_center_pts(arrays, flavor, scaled, counts, pt, eta, phi, mass, charge)

    new_pt = scaled.copy()
    res_cfg = cfg.get("resolution", {})
    if res_cfg.get("enabled", True) and len(flat_pt):
        sigma = region_sigma(res_cfg.get(flavor, {}), flat_eta, flat_pt, pt_ref)
        keys = object_keys(cfg, arrays, pt, start_entry, flavor, "resolution")
        new_pt = scaled * (1.0 + normal01_np(keys) * sigma)

    new_pt = np.where(np.isfinite(new_pt) & (new_pt > 0.0), new_pt, 0.0)
    return unflatten_like(new_pt, counts), unflatten_like(scaled, counts)


def branch_requests(cfg: Mapping, plot_cfg: Mapping) -> List[str]:
    requested = []
    for flavor in ("muon", "electron"):
        br = lepton_branches(cfg, flavor)
        requested.extend(br.values())
        requested.append(tnp_tag_id_branch(flavor))
        requested.extend(selected_efficiency_branches(plot_cfg, cfg, flavor).keys())
        requested.extend(selected_event_efficiency_branches(plot_cfg, cfg, flavor).keys())
    requested.extend(event_id_branches(cfg).values())
    requested.extend(GEN_TRUTH_BRANCHES)
    return list(dict.fromkeys(x for x in requested if x))


def build_base_efficiency_maps(
    cfg: Mapping,
    plot_cfg: Mapping,
    inputs: Sequence[Path],
    chunk_size: int,
) -> Dict[Tuple[str, str], Dict[str, np.ndarray]]:
    maps: Dict[Tuple[str, str], Dict[str, np.ndarray]] = {}
    for flavor in ("muon", "electron"):
        for branch in selected_efficiency_branches(plot_cfg, cfg, flavor):
            maps[(flavor, branch)] = {
                "pass": np.zeros(n_eff_bins(cfg), dtype=float),
                "total": np.zeros(n_eff_bins(cfg), dtype=float),
            }
        for branch in selected_event_efficiency_branches(plot_cfg, cfg, flavor):
            maps[(flavor, branch)] = {
                "pass": np.zeros(n_eff_bins(cfg), dtype=float),
                "total": np.zeros(n_eff_bins(cfg), dtype=float),
            }

    if not cfg.get("efficiency", {}).get("enabled", True):
        return maps

    tree_name = cfg.get("global", {}).get("tree_name", "Events")
    for path in inputs:
        tree = open_tree(path, tree_name)
        requested = branch_requests(cfg, plot_cfg)
        progress_bucket = -1
        progress_bucket = print_progress(f"Base efficiency {path}", 0, tree.num_entries, progress_bucket)
        for start in range(0, tree.num_entries, chunk_size):
            stop = min(tree.num_entries, start + chunk_size)
            arrays = read_arrays(tree, requested, start, stop, f"{path} base-efficiency")
            for flavor in ("muon", "electron"):
                br = lepton_branches(cfg, flavor)
                if br["pt"] not in arrays or br["eta"] not in arrays:
                    continue
                pt = arrays[br["pt"]]
                eta = arrays[br["eta"]]
                energy = None
                if cfg.get("efficiency", {}).get("binning", {}).get("energy"):
                    if br.get("energy") and br["energy"] in arrays:
                        energy = arrays[br["energy"]]
                    else:
                        energy = pt * np.cosh(eta)
                leading = gen_matched_boson_leading_values(
                    arrays,
                    flavor,
                    pt,
                    eta,
                    arrays.get(br.get("phi")),
                    energy=energy,
                )
                if len(leading["pt"]) == 0:
                    continue
                flat_energy = leading["energy"] if energy is not None else None
                flat_bin, _, _, _ = flat_eff_bin(cfg, leading["pt"], leading["eta"], flat_energy)
                denom = leading["denom"].astype(bool)
                for branch, ecfg in selected_efficiency_branches(plot_cfg, cfg, flavor).items():
                    if branch not in arrays:
                        continue
                    passed = matched_object_values(pass_mask(arrays[branch], ecfg), leading["event"], leading["index"])
                    maps[(flavor, branch)]["total"] += np.bincount(flat_bin[denom], minlength=n_eff_bins(cfg))
                    maps[(flavor, branch)]["pass"] += np.bincount(
                        flat_bin[denom], weights=passed[denom].astype(float), minlength=n_eff_bins(cfg)
                    )

                for branch, ecfg in selected_event_efficiency_branches(plot_cfg, cfg, flavor).items():
                    if branch not in arrays:
                        continue
                    event_pass = ak.to_numpy(pass_mask(arrays[branch], ecfg)).astype(float)
                    passed = event_pass[leading["event"]]
                    maps[(flavor, branch)]["total"] += np.bincount(flat_bin[denom], minlength=n_eff_bins(cfg))
                    maps[(flavor, branch)]["pass"] += np.bincount(
                        flat_bin[denom], weights=passed[denom], minlength=n_eff_bins(cfg)
                    )
            progress_bucket = print_progress(f"Base efficiency {path}", stop, tree.num_entries, progress_bucket)
    return maps


def map_efficiency_values(base_map: Mapping[str, np.ndarray], flat_bin: np.ndarray) -> np.ndarray:
    passed = base_map["pass"][flat_bin]
    total = base_map["total"][flat_bin]
    global_total = float(np.sum(base_map["total"]))
    global_pass = float(np.sum(base_map["pass"]))
    global_eff = global_pass / global_total if global_total > 0 else 0.0
    use_bin = (total >= MIN_EFF_BIN_TOTAL) | ((total > 0) & (global_total < MIN_EFF_BIN_TOTAL))
    return np.where(use_bin, passed / np.maximum(total, 1.0), global_eff)


def small_smooth_factor(value: float) -> float:
    if not np.isfinite(value):
        return 1.0
    return float(np.clip(value, 0.95, 1.05))


def smoothed_factor_array(factors: Sequence[float], indices: np.ndarray) -> np.ndarray:
    if not factors:
        return np.ones_like(indices, dtype=float)
    raw = np.asarray([small_smooth_factor(float(x)) for x in factors], dtype=float)
    smooth = np.ones_like(raw, dtype=float)
    for i in range(len(raw)):
        lo = max(0, i - 1)
        hi = min(len(raw), i + 2)
        weights = np.ones(hi - lo, dtype=float)
        weights[i - lo] = 2.0
        smooth[i] = float(np.sum(raw[lo:hi] * weights) / np.sum(weights))
    valid = (indices >= 0) & (indices < len(smooth))
    clipped = np.clip(indices, 0, len(smooth) - 1)
    return np.where(valid, smooth[clipped], 1.0)


def apply_constrained_distortion(
    cfg: Mapping,
    branch_cfg: Mapping,
    base: np.ndarray,
    flat_pt: np.ndarray,
    eta_bin: np.ndarray,
    abs_eta_bin: np.ndarray,
) -> np.ndarray:
    del cfg, eta_bin, abs_eta_bin
    distortion = branch_cfg.get("distortion", {})
    prob = base * small_smooth_factor(float(distortion.get("global_factor", 1.0)))
    turnon_amp = float(distortion.get("pt_turnon_amplitude", 0.0))
    if turnon_amp != 0.0:
        width = max(float(distortion.get("pt_turnon_width", 8.0)), 1.0e-3)
        shifted_width = max(width * float(np.clip(distortion.get("pt_turnon_width_scale", 1.0), 0.5, 2.0)), 1.0e-3)
        center = float(distortion.get("pt_turnon_center", 25.0))
        shift = float(np.clip(distortion.get("pt_turnon_shift", 0.0), -10.0, 10.0))
        nominal = 1.0 / (1.0 + np.exp(-np.clip((flat_pt - center) / width, -40.0, 40.0)))
        shifted = 1.0 / (1.0 + np.exp(-np.clip((flat_pt - center - shift) / shifted_width, -40.0, 40.0)))
        prob *= 1.0 + float(np.clip(turnon_amp, -0.20, 0.20)) * (shifted - nominal)
    prob = np.clip(np.where(np.isfinite(prob), prob, 0.0), 0.0, 1.0)
    return prob


def distorted_probability(
    cfg: Mapping,
    base_map: Mapping[str, np.ndarray],
    branch_cfg: Mapping,
    pt,
    eta,
    energy=None,
):
    flat_pt, counts = flatten_jagged(pt)
    flat_eta, _ = flatten_jagged(eta)
    flat_energy = None
    if energy is not None:
        flat_energy, _ = flatten_jagged(energy)
    flat_bin, _, eta_bin, abs_eta_bin = flat_eff_bin(cfg, flat_pt, flat_eta, flat_energy)
    base = map_efficiency_values(base_map, flat_bin)
    prob = apply_constrained_distortion(cfg, branch_cfg, base, flat_pt, eta_bin, abs_eta_bin)
    return unflatten_like(prob, counts)


def distorted_probability_flat(
    cfg: Mapping,
    base_map: Mapping[str, np.ndarray],
    branch_cfg: Mapping,
    pt: np.ndarray,
    eta: np.ndarray,
):
    pt = np.asarray(pt, dtype=float)
    eta = np.asarray(eta, dtype=float)
    flat_bin, _, eta_bin, abs_eta_bin = flat_eff_bin(cfg, pt, eta)
    base = map_efficiency_values(base_map, flat_bin)
    return apply_constrained_distortion(cfg, branch_cfg, base, pt, eta_bin, abs_eta_bin)


def empty_truth_values() -> Dict[str, np.ndarray]:
    return {
        "pt": np.array([], dtype=float),
        "eta": np.array([], dtype=float),
        "phi": np.array([], dtype=float),
        "energy": np.array([], dtype=float),
        "pass": np.array([], dtype=bool),
        "denom": np.array([], dtype=bool),
        "event": np.array([], dtype=int),
        "index": np.array([], dtype=int),
    }


def gen_truth_available(arrays: Mapping[str, ak.Array]) -> bool:
    required = ["GenPart_pt", "GenPart_eta", "GenPart_phi", "GenPart_pdgId", "GenPart_genPartIdxMother"]
    return all(name in arrays for name in required)


def lepton_abs_pdg_id(flavor: str) -> int:
    return 13 if flavor == "muon" else 11


def status_flag(flags, index: int, bit: int) -> bool:
    return flags is not None and index < len(flags) and (int(flags[index]) & (1 << bit)) != 0


def prompt_like_gen(flags, index: int) -> bool:
    if flags is None or index >= len(flags):
        return True
    return status_flag(flags, index, 0) or status_flag(flags, index, 8) or status_flag(flags, index, 11)


def has_ancestor_pdg(pdg_ids, mothers, index: int, abs_pdg_id: int, n_gen: int) -> bool:
    if index >= len(mothers):
        return False
    mother = int(mothers[index])
    guard = 0
    while 0 <= mother < n_gen and guard < n_gen:
        if mother >= len(pdg_ids):
            return False
        if abs(int(pdg_ids[mother])) == abs_pdg_id:
            return True
        if mother >= len(mothers):
            return False
        mother = int(mothers[mother])
        guard += 1
    return False


def leading_gen_boson_lepton_index(gen_pts, gen_pdg_ids, gen_mothers, gen_flags, n_gen: int, abs_lepton_pdg_id: int) -> Optional[int]:
    candidates = gen_boson_lepton_indices(gen_pts, gen_pdg_ids, gen_mothers, gen_flags, n_gen, abs_lepton_pdg_id)
    if not candidates:
        return None
    return max(candidates, key=lambda idx: float(gen_pts[idx]))


def gen_boson_lepton_indices(gen_pts, gen_pdg_ids, gen_mothers, gen_flags, n_gen: int, abs_lepton_pdg_id: int) -> List[int]:
    limit = min(n_gen, len(gen_pts), len(gen_pdg_ids), len(gen_mothers))
    candidates = []
    have_last_copy = False
    for idx in range(limit):
        if abs(int(gen_pdg_ids[idx])) != abs_lepton_pdg_id:
            continue
        if not prompt_like_gen(gen_flags, idx):
            continue
        if not has_ancestor_pdg(gen_pdg_ids, gen_mothers, idx, 23, limit) and not has_ancestor_pdg(
            gen_pdg_ids, gen_mothers, idx, 25, limit
        ):
            continue
        try:
            pt = float(gen_pts[idx])
        except (TypeError, ValueError):
            continue
        if not np.isfinite(pt):
            continue
        last_copy = status_flag(gen_flags, idx, 13)
        have_last_copy = have_last_copy or last_copy
        candidates.append((idx, last_copy))
    if have_last_copy:
        candidates = [item for item in candidates if item[1]]
    return [item[0] for item in candidates]


def delta_phi(a: float, b: float) -> float:
    return (a - b + math.pi) % (2.0 * math.pi) - math.pi


def reco_charge_matches_gen(reco_charge: int, gen_pdg_id: int) -> bool:
    if reco_charge == 0 or gen_pdg_id == 0:
        return True
    return reco_charge * gen_pdg_id < 0


def common_pair_scale_for_mass(
    target_mass: float,
    center1: float,
    eta1: float,
    phi1: float,
    mass1: float,
    center2: float,
    eta2: float,
    phi2: float,
    mass2: float,
) -> float:
    if not np.isfinite(target_mass) or target_mass <= 0.0:
        return 1.0

    def mass_at(scale: float) -> float:
        mass, _, _, _ = system_kinematics(
            (center1 * scale, eta1, phi1, mass1),
            (center2 * scale, eta2, phi2, mass2),
        )
        return mass

    at_one = mass_at(1.0)
    if not np.isfinite(at_one) or at_one <= 0.0:
        return 1.0
    if abs(at_one - target_mass) <= 1.0e-9 * max(target_mass, 1.0):
        return 1.0

    lo = 0.0
    hi = 1.0
    if at_one < target_mass:
        lo = 1.0
        hi = 2.0
        for _ in range(32):
            if mass_at(hi) >= target_mass:
                break
            hi *= 2.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if mass_at(mid) < target_mass:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def protect_boson_pair_center_pts(
    arrays: Mapping[str, ak.Array],
    flavor: str,
    center_flat: np.ndarray,
    counts: np.ndarray,
    pt,
    eta,
    phi,
    mass,
    charge,
) -> np.ndarray:
    if phi is None or mass is None or charge is None or not gen_truth_available(arrays):
        return center_flat

    centers = ak.to_list(unflatten_like(center_flat, counts))
    pts = ak.to_list(pt)
    etas = ak.to_list(eta)
    phis = ak.to_list(phi)
    masses = ak.to_list(mass)
    charges = ak.to_list(charge)
    gen_pts = ak.to_list(arrays["GenPart_pt"])
    gen_etas = ak.to_list(arrays["GenPart_eta"])
    gen_phis = ak.to_list(arrays["GenPart_phi"])
    gen_pdg_ids = ak.to_list(arrays["GenPart_pdgId"])
    gen_mothers = ak.to_list(arrays["GenPart_genPartIdxMother"])
    gen_flags = ak.to_list(arrays["GenPart_statusFlags"]) if "GenPart_statusFlags" in arrays else None
    n_gen_values = ak.to_numpy(arrays["nGenPart"]).astype(int) if "nGenPart" in arrays else None
    abs_pdg_id = lepton_abs_pdg_id(flavor)
    max_dr2 = TRUTH_MATCH_DR * TRUTH_MATCH_DR

    for iev, event_pts in enumerate(pts):
        if iev >= len(gen_pts):
            continue
        limit = min(len(event_pts), len(etas[iev]), len(phis[iev]), len(masses[iev]), len(charges[iev]), len(centers[iev]))
        if limit < 2:
            continue
        n_gen = int(n_gen_values[iev]) if n_gen_values is not None and iev < len(n_gen_values) else len(gen_pts[iev])
        gen_flags_event = gen_flags[iev] if gen_flags is not None and iev < len(gen_flags) else None
        gen_indices = gen_boson_lepton_indices(
            gen_pts[iev],
            gen_pdg_ids[iev],
            gen_mothers[iev],
            gen_flags_event,
            n_gen,
            abs_pdg_id,
        )
        if not gen_indices:
            continue

        matched = [False] * limit
        used_reco = set()
        for gen_idx in gen_indices:
            if gen_idx >= len(gen_etas[iev]) or gen_idx >= len(gen_phis[iev]) or gen_idx >= len(gen_pdg_ids[iev]):
                continue
            best = None
            best_dr2 = max_dr2
            gen_eta = float(gen_etas[iev][gen_idx])
            gen_phi = float(gen_phis[iev][gen_idx])
            gen_pdg_id = int(gen_pdg_ids[iev][gen_idx])
            for idx in range(limit):
                if idx in used_reco:
                    continue
                if not reco_charge_matches_gen(int(charges[iev][idx]), gen_pdg_id):
                    continue
                dr2 = (float(etas[iev][idx]) - gen_eta) ** 2 + delta_phi(float(phis[iev][idx]), gen_phi) ** 2
                if np.isfinite(dr2) and dr2 < best_dr2:
                    best = idx
                    best_dr2 = dr2
            if best is not None:
                matched[best] = True
                used_reco.add(best)

        pairs = []
        for i in range(limit):
            if not matched[i] or int(charges[iev][i]) == 0:
                continue
            for j in range(i + 1, limit):
                if matched[j] and int(charges[iev][j]) != 0 and int(charges[iev][i]) * int(charges[iev][j]) < 0:
                    pairs.append((i, j))

        if len(pairs) == 1:
            i, j = pairs[0]
            old_mass, _, _, _ = system_kinematics(
                (float(event_pts[i]), float(etas[iev][i]), float(phis[iev][i]), float(masses[iev][i])),
                (float(event_pts[j]), float(etas[iev][j]), float(phis[iev][j]), float(masses[iev][j])),
            )
            scale = common_pair_scale_for_mass(
                old_mass,
                float(centers[iev][i]),
                float(etas[iev][i]),
                float(phis[iev][i]),
                float(masses[iev][i]),
                float(centers[iev][j]),
                float(etas[iev][j]),
                float(phis[iev][j]),
                float(masses[iev][j]),
            )
            if np.isfinite(scale) and scale > 0.0:
                centers[iev][i] = float(centers[iev][i]) * scale
                centers[iev][j] = float(centers[iev][j]) * scale
        elif len(pairs) > 1:
            protected = {idx for pair in pairs for idx in pair}
            for idx in protected:
                centers[iev][idx] = float(event_pts[idx])

    return ak.to_numpy(ak.flatten(ak.Array(centers), axis=None))


def gen_matched_boson_leading_values(
    arrays: Mapping[str, ak.Array],
    flavor: str,
    pt,
    eta,
    phi,
    passed=None,
    energy=None,
) -> Dict[str, np.ndarray]:
    if phi is None or not gen_truth_available(arrays):
        return empty_truth_values()

    reco_pts = ak.to_list(pt)
    reco_etas = ak.to_list(eta)
    reco_phis = ak.to_list(phi)
    passes = ak.to_list(passed) if passed is not None else None
    energies = ak.to_list(energy) if energy is not None else None
    gen_pts = ak.to_list(arrays["GenPart_pt"])
    gen_etas = ak.to_list(arrays["GenPart_eta"])
    gen_phis = ak.to_list(arrays["GenPart_phi"])
    gen_pdg_ids = ak.to_list(arrays["GenPart_pdgId"])
    gen_mothers = ak.to_list(arrays["GenPart_genPartIdxMother"])
    gen_flags = ak.to_list(arrays["GenPart_statusFlags"]) if "GenPart_statusFlags" in arrays else None
    n_gen_values = ak.to_numpy(arrays["nGenPart"]).astype(int) if "nGenPart" in arrays else None
    abs_pdg_id = lepton_abs_pdg_id(flavor)
    max_dr2 = TRUTH_MATCH_DR * TRUTH_MATCH_DR
    out = {key: [] for key in empty_truth_values()}

    for iev, event_pts in enumerate(reco_pts):
        if iev >= len(gen_pts):
            continue
        n_gen = int(n_gen_values[iev]) if n_gen_values is not None and iev < len(n_gen_values) else len(gen_pts[iev])
        gen_flags_event = gen_flags[iev] if gen_flags is not None and iev < len(gen_flags) else None
        lead_gen = leading_gen_boson_lepton_index(
            gen_pts[iev],
            gen_pdg_ids[iev],
            gen_mothers[iev],
            gen_flags_event,
            n_gen,
            abs_pdg_id,
        )
        if lead_gen is None or lead_gen >= len(gen_etas[iev]) or lead_gen >= len(gen_phis[iev]):
            continue

        limit = min(len(event_pts), len(reco_etas[iev]), len(reco_phis[iev]))
        if passes is not None:
            limit = min(limit, len(passes[iev]))
        if energies is not None:
            limit = min(limit, len(energies[iev]))
        best = None
        best_dr2 = max_dr2
        gen_eta = float(gen_etas[iev][lead_gen])
        gen_phi = float(gen_phis[iev][lead_gen])
        for idx in range(limit):
            dr2 = (float(reco_etas[iev][idx]) - gen_eta) ** 2 + delta_phi(float(reco_phis[iev][idx]), gen_phi) ** 2
            if np.isfinite(dr2) and dr2 < best_dr2:
                best = idx
                best_dr2 = dr2
        if best is None:
            continue

        out["pt"].append(float(event_pts[best]))
        out["eta"].append(float(reco_etas[iev][best]))
        out["phi"].append(float(reco_phis[iev][best]))
        out["energy"].append(float(energies[iev][best]) if energies is not None else 0.0)
        out["pass"].append(bool(passes[iev][best]) if passes is not None else True)
        out["denom"].append(True)
        out["event"].append(iev)
        out["index"].append(best)
    return {
        "pt": np.asarray(out["pt"], dtype=float),
        "eta": np.asarray(out["eta"], dtype=float),
        "phi": np.asarray(out["phi"], dtype=float),
        "energy": np.asarray(out["energy"], dtype=float),
        "pass": np.asarray(out["pass"], dtype=bool),
        "denom": np.asarray(out["denom"], dtype=bool),
        "event": np.asarray(out["event"], dtype=int),
        "index": np.asarray(out["index"], dtype=int),
    }


def leading_event_values(pt, eta, phi, denom_mask=None) -> Dict[str, np.ndarray]:
    pts = ak.to_list(pt)
    etas = ak.to_list(eta)
    phis = ak.to_list(phi) if phi is not None else None
    masks = ak.to_list(denom_mask) if denom_mask is not None else None
    out = {"pt": [], "eta": [], "phi": [], "denom": []}
    for iev, event_pts in enumerate(pts):
        if not event_pts:
            continue
        lead = max(range(len(event_pts)), key=lambda idx: event_pts[idx])
        out["pt"].append(event_pts[lead])
        out["eta"].append(etas[iev][lead])
        out["phi"].append(phis[iev][lead] if phis is not None else 0.0)
        out["denom"].append(bool(masks[iev][lead]) if masks is not None else True)
    return {key: np.asarray(value) for key, value in out.items()}


def os_probe_lepton_values(
    pt,
    eta,
    phi=None,
    charge=None,
    passed=None,
    energy=None,
) -> Dict[str, np.ndarray]:
    pts = ak.to_list(pt)
    etas = ak.to_list(eta)
    phis = ak.to_list(phi) if phi is not None else None
    charges = ak.to_list(charge) if charge is not None else None
    passes = ak.to_list(passed) if passed is not None else None
    energies = ak.to_list(energy) if energy is not None else None
    out = {"pt": [], "eta": [], "phi": [], "energy": [], "pass": [], "denom": []}
    if charges is None:
        return {key: np.asarray(value) for key, value in out.items()}
    for iev, event_pts in enumerate(pts):
        limit = min(len(event_pts), len(charges[iev]))
        if limit < 2:
            continue
        ordered = sorted(range(limit), key=lambda idx: event_pts[idx], reverse=True)
        tag = ordered[0]
        probe = ordered[1]
        tag_charge = int(charges[iev][tag])
        probe_charge = int(charges[iev][probe])
        if tag_charge == 0 or probe_charge == 0 or tag_charge * probe_charge >= 0:
            continue
        out["pt"].append(event_pts[probe])
        out["eta"].append(etas[iev][probe])
        out["phi"].append(phis[iev][probe] if phis is not None else 0.0)
        out["energy"].append(energies[iev][probe] if energies is not None else 0.0)
        out["pass"].append(bool(passes[iev][probe]) if passes is not None else True)
        out["denom"].append(True)
    return {key: np.asarray(value) for key, value in out.items()}


def add_efficiency_counts(
    store: MutableMapping[Tuple, Dict[str, np.ndarray]],
    key: Tuple,
    values,
    denom_mask,
    passed,
    edges: np.ndarray,
) -> None:
    vals = ak.to_numpy(ak.flatten(values[denom_mask], axis=1)) if values is not None else np.array([])
    pass_vals = ak.to_numpy(ak.flatten(passed[denom_mask], axis=1)).astype(float) if values is not None else np.array([])
    if key not in store:
        store[key] = {"num": np.zeros(len(edges) - 1), "den": np.zeros(len(edges) - 1)}
    finite = np.isfinite(vals)
    store[key]["den"] += np.histogram(vals[finite], bins=edges)[0]
    store[key]["num"] += np.histogram(vals[finite], bins=edges, weights=pass_vals[finite])[0]


def add_efficiency_counts_flat(
    store: MutableMapping[Tuple, Dict[str, np.ndarray]],
    key: Tuple,
    values: np.ndarray,
    denom_mask: np.ndarray,
    passed: np.ndarray,
    edges: np.ndarray,
) -> None:
    if key not in store:
        store[key] = {"num": np.zeros(len(edges) - 1), "den": np.zeros(len(edges) - 1)}
    values = np.asarray(values, dtype=float)
    denom_mask = np.asarray(denom_mask, dtype=bool)
    passed = np.asarray(passed, dtype=float)
    finite = np.isfinite(values) & denom_mask
    store[key]["den"] += np.histogram(values[finite], bins=edges)[0]
    store[key]["num"] += np.histogram(values[finite], bins=edges, weights=passed[finite])[0]


def add_expected_counts(
    store: MutableMapping[Tuple, Dict[str, np.ndarray]],
    key: Tuple,
    values,
    probabilities,
    edges: np.ndarray,
    denom_mask=None,
) -> None:
    if denom_mask is not None:
        values = values[denom_mask]
        probabilities = probabilities[denom_mask]
    vals = ak.to_numpy(ak.flatten(values, axis=1))
    probs = ak.to_numpy(ak.flatten(probabilities, axis=1))
    if key not in store:
        store[key] = {"num": np.zeros(len(edges) - 1), "den": np.zeros(len(edges) - 1)}
    finite = np.isfinite(vals) & np.isfinite(probs)
    store[key]["den"] += np.histogram(vals[finite], bins=edges)[0]
    store[key]["num"] += np.histogram(vals[finite], bins=edges, weights=probs[finite])[0]


def add_expected_counts_flat(
    store: MutableMapping[Tuple, Dict[str, np.ndarray]],
    key: Tuple,
    values: np.ndarray,
    probabilities: np.ndarray,
    edges: np.ndarray,
    denom_mask: Optional[np.ndarray] = None,
) -> None:
    if key not in store:
        store[key] = {"num": np.zeros(len(edges) - 1), "den": np.zeros(len(edges) - 1)}
    values = np.asarray(values, dtype=float)
    probabilities = np.asarray(probabilities, dtype=float)
    finite = np.isfinite(values) & np.isfinite(probabilities)
    if denom_mask is not None:
        finite &= np.asarray(denom_mask, dtype=bool)
    store[key]["den"] += np.histogram(values[finite], bins=edges)[0]
    store[key]["num"] += np.histogram(values[finite], bins=edges, weights=probabilities[finite])[0]


def add_hist_counts(store: MutableMapping[Tuple, np.ndarray], key: Tuple, values, edges: np.ndarray) -> None:
    vals = to_numpy_flat(values)
    if key not in store:
        store[key] = np.zeros(len(edges) - 1)
    store[key] += np.histogram(vals, bins=edges)[0]


def correlation_branch_cfgs(plot_cfg: Mapping, modify_cfg: Mapping, flavor: str) -> Dict[str, Mapping]:
    selected = selected_efficiency_branches(plot_cfg, modify_cfg, flavor)
    selected_event = selected_event_efficiency_branches(plot_cfg, modify_cfg, flavor)
    ordered = {}
    for branch, cfg in efficiency_branch_cfgs(modify_cfg, flavor).items():
        if branch in selected:
            ordered[branch] = cfg
    for branch, cfg in event_efficiency_branch_cfgs(modify_cfg).items():
        if branch in selected_event and branch not in ordered:
            ordered[branch] = cfg
    return ordered


def correlation_branch_edges(branch_cfg: Mapping) -> np.ndarray:
    eff_type = branch_cfg.get("type", "bool")
    if eff_type == "bool":
        return np.asarray([-0.5, 0.5, 1.5], dtype=float)
    if eff_type == "int_wp":
        high = max(
            6,
            int(branch_cfg.get("pass_threshold", 1)),
            int(branch_cfg.get("pass_value", branch_cfg.get("pass_threshold", 1))),
            int(branch_cfg.get("fail_value", 0)),
        )
        return np.arange(-0.5, float(high) + 1.5, 1.0, dtype=float)
    threshold = float(branch_cfg.get("max", branch_cfg.get("pass_threshold", 0.15)))
    fail_value = float(branch_cfg.get("fail_value", 2.0 * threshold))
    high = max(1.0, 4.0 * threshold, 2.0 * fail_value)
    return np.linspace(0.0, high, 13, dtype=float)


def correlation_specs(modify_cfg: Mapping, plot_cfg: Mapping, flavor: str, bins: Mapping[str, np.ndarray]) -> List[Dict]:
    branch_cfgs = correlation_branch_cfgs(plot_cfg, modify_cfg, flavor)
    edges_by_var = {
        "energy": bins["hist_energy"],
        "eta": bins["eff_eta"],
        "pt": bins["hist_pt"],
    }
    labels_by_var = {
        "energy": f"{flavor} lepton energy [GeV]",
        "eta": f"{flavor} lepton eta",
        "pt": f"{flavor} lepton pT [GeV]",
    }
    for branch, cfg in branch_cfgs.items():
        edges_by_var[branch] = correlation_branch_edges(cfg)
        labels_by_var[branch] = branch

    pairs = [("energy", "eta"), ("energy", "pt"), ("pt", "eta")]
    pairs.extend(itertools.combinations(branch_cfgs.keys(), 2))
    specs = []
    for xvar, yvar in pairs:
        if xvar not in edges_by_var or yvar not in edges_by_var:
            continue
        specs.append({
            "x": xvar,
            "y": yvar,
            "x_edges": edges_by_var[xvar],
            "y_edges": edges_by_var[yvar],
            "x_label": labels_by_var[xvar],
            "y_label": labels_by_var[yvar],
        })
    return specs


def matched_object_values(values, events: np.ndarray, indices: np.ndarray) -> np.ndarray:
    events = np.asarray(events, dtype=int)
    if isinstance(values, ak.Array) and values.ndim <= 1:
        arr = ak.to_numpy(values)
        out = np.full(len(events), np.nan, dtype=float)
        valid = (events >= 0) & (events < len(arr))
        out[valid] = np.asarray(arr[events[valid]], dtype=float)
        return out

    if isinstance(values, ak.Array):
        indices = np.asarray(indices, dtype=int)
        counts = ak.to_numpy(ak.num(values, axis=1)).astype(np.int64)
        offsets = np.empty(len(counts), dtype=np.int64)
        if len(counts) > 0:
            offsets[0] = 0
            offsets[1:] = np.cumsum(counts[:-1])
        flat = ak.to_numpy(ak.flatten(values, axis=1))
        out = np.full(len(events), np.nan, dtype=float)
        valid_event = (events >= 0) & (events < len(counts))
        valid = np.zeros(len(events), dtype=bool)
        valid[valid_event] = (indices[valid_event] >= 0) & (indices[valid_event] < counts[events[valid_event]])
        flat_indices = offsets[events[valid]] + indices[valid]
        out[valid] = np.asarray(flat[flat_indices], dtype=float)
        return out

    rows = ak.to_list(values)
    out = []
    for event_idx, object_idx in zip(events, np.asarray(indices, dtype=int)):
        if event_idx < 0 or event_idx >= len(rows):
            out.append(np.nan)
            continue
        row = rows[event_idx]
        if object_idx < 0 or object_idx >= len(row):
            out.append(np.nan)
            continue
        out.append(float(row[object_idx]))
    return np.asarray(out, dtype=float)


def add_correlation_counts(
    store: MutableMapping[Tuple, np.ndarray],
    key: Tuple,
    x_values: np.ndarray,
    y_values: np.ndarray,
    x_edges: np.ndarray,
    y_edges: np.ndarray,
) -> None:
    if key not in store:
        store[key] = np.zeros((len(y_edges) - 1, len(x_edges) - 1), dtype=float)
    x_values = np.asarray(x_values, dtype=float)
    y_values = np.asarray(y_values, dtype=float)
    finite = np.isfinite(x_values) & np.isfinite(y_values)
    if not np.any(finite):
        return
    hist, _, _ = np.histogram2d(x_values[finite], y_values[finite], bins=[x_edges, y_edges])
    store[key] += hist.T


def add_correlation_sample(
    store: MutableMapping[Tuple, np.ndarray],
    specs: Sequence[Mapping],
    flavor: str,
    sample: str,
    arrays: Mapping[str, ak.Array],
    leading: Mapping[str, np.ndarray],
    branch_cfgs: Mapping[str, Mapping],
) -> None:
    values_by_var = {
        "pt": np.asarray(leading["pt"], dtype=float),
        "eta": np.asarray(leading["eta"], dtype=float),
        "energy": np.asarray(leading["energy"], dtype=float),
    }
    for branch in branch_cfgs:
        if branch in arrays:
            values_by_var[branch] = matched_object_values(arrays[branch], leading["event"], leading["index"])
    for spec in specs:
        xvar = spec["x"]
        yvar = spec["y"]
        if xvar not in values_by_var or yvar not in values_by_var:
            continue
        add_correlation_counts(
            store,
            (flavor, sample, xvar, yvar),
            values_by_var[xvar],
            values_by_var[yvar],
            spec["x_edges"],
            spec["y_edges"],
        )


def p4_components(pt: float, eta: float, phi: float, mass: float) -> Tuple[float, float, float, float]:
    px = pt * math.cos(phi)
    py = pt * math.sin(phi)
    pz = pt * math.sinh(eta)
    energy = math.sqrt(max((pt * math.cosh(eta)) ** 2 + mass**2, 0.0))
    return energy, px, py, pz


def system_kinematics(l1: Tuple[float, float, float, float], l2: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
    e1, px1, py1, pz1 = p4_components(*l1)
    e2, px2, py2, pz2 = p4_components(*l2)
    e = e1 + e2
    px = px1 + px2
    py = py1 + py2
    pz = pz1 + pz2
    pt = math.hypot(px, py)
    mass2 = e * e - px * px - py * py - pz * pz
    mass = math.sqrt(max(mass2, 0.0))
    eta = math.asinh(pz / pt) if pt > 0 else 0.0
    phi = math.atan2(py, px)
    return mass, pt, eta, phi


def tnp_probes(arrays: Mapping[str, ak.Array], br: Mapping[str, str], probe_passed, tag_passed) -> Dict[str, np.ndarray]:
    required = [br.get("pt"), br.get("eta"), br.get("phi"), br.get("mass"), br.get("charge")]
    if any(name not in arrays for name in required):
        return {
            "pt": np.array([]),
            "eta": np.array([]),
            "phi": np.array([]),
            "mass": np.array([]),
            "pass": np.array([], dtype=bool),
        }

    pts = ak.to_list(arrays[br["pt"]])
    etas = ak.to_list(arrays[br["eta"]])
    phis = ak.to_list(arrays[br["phi"]])
    masses = ak.to_list(arrays[br["mass"]])
    charges = ak.to_list(arrays[br["charge"]])
    probe_passes = ak.to_list(probe_passed)
    tag_passes = ak.to_list(tag_passed)

    out = {"pt": [], "eta": [], "phi": [], "mass": [], "pass": []}
    for iev, event_pts in enumerate(pts):
        limit = min(len(event_pts), len(charges[iev]), len(probe_passes[iev]), len(tag_passes[iev]))
        if limit < 2:
            continue
        ordered = sorted(range(limit), key=lambda idx: event_pts[idx], reverse=True)
        tag = ordered[0]
        probe = ordered[1]
        tag_charge = int(charges[iev][tag])
        probe_charge = int(charges[iev][probe])
        if tag_charge == 0 or probe_charge == 0 or tag_charge * probe_charge >= 0:
            continue
        if not bool(tag_passes[iev][tag]):
            continue
        out["pt"].append(event_pts[probe])
        out["eta"].append(etas[iev][probe])
        out["phi"].append(phis[iev][probe])
        mass, _, _, _ = system_kinematics(
            (event_pts[tag], etas[iev][tag], phis[iev][tag], masses[iev][tag]),
            (event_pts[probe], etas[iev][probe], phis[iev][probe], masses[iev][probe]),
        )
        out["mass"].append(mass)
        out["pass"].append(bool(probe_passes[iev][probe]))
    return {key: np.asarray(value) for key, value in out.items()}


def tnp_probe_base(arrays: Mapping[str, ak.Array], br: Mapping[str, str], tag_passed) -> Dict[str, np.ndarray]:
    required = [br.get("pt"), br.get("eta"), br.get("phi"), br.get("mass"), br.get("charge")]
    if any(name not in arrays for name in required):
        return {
            "pt": np.array([]),
            "eta": np.array([]),
            "phi": np.array([]),
            "mass": np.array([]),
            "event": np.array([], dtype=int),
            "index": np.array([], dtype=int),
        }

    pt = arrays[br["pt"]]
    eta = arrays[br["eta"]]
    phi = arrays[br["phi"]]
    mass = arrays[br["mass"]]
    charge = arrays[br["charge"]]
    has_pair = (
        (ak.num(pt, axis=1) >= 2)
        & (ak.num(eta, axis=1) >= 2)
        & (ak.num(phi, axis=1) >= 2)
        & (ak.num(mass, axis=1) >= 2)
        & (ak.num(charge, axis=1) >= 2)
        & (ak.num(tag_passed, axis=1) >= 2)
    )
    if not bool(ak.any(has_pair)):
        return {
            "pt": np.array([]),
            "eta": np.array([]),
            "phi": np.array([]),
            "mass": np.array([]),
            "event": np.array([], dtype=int),
            "index": np.array([], dtype=int),
        }

    event_indices = np.nonzero(ak.to_numpy(has_pair))[0]
    pt2 = pt[has_pair]
    eta2 = eta[has_pair]
    phi2 = phi[has_pair]
    mass2 = mass[has_pair]
    charge2 = charge[has_pair]
    tag_passed2 = tag_passed[has_pair]
    order = ak.argsort(pt2, axis=1, ascending=False)
    sorted_pt = pt2[order]
    sorted_eta = eta2[order]
    sorted_phi = phi2[order]
    sorted_mass = mass2[order]
    sorted_charge = charge2[order]
    sorted_tag_passed = tag_passed2[order]
    sorted_index = ak.local_index(pt2, axis=1)[order]

    tag_pt = ak.to_numpy(sorted_pt[:, 0]).astype(float)
    tag_eta = ak.to_numpy(sorted_eta[:, 0]).astype(float)
    tag_phi = ak.to_numpy(sorted_phi[:, 0]).astype(float)
    tag_mass = ak.to_numpy(sorted_mass[:, 0]).astype(float)
    tag_charge = ak.to_numpy(sorted_charge[:, 0]).astype(int)
    tag_ok = ak.to_numpy(sorted_tag_passed[:, 0]).astype(bool)
    probe_pt = ak.to_numpy(sorted_pt[:, 1]).astype(float)
    probe_eta = ak.to_numpy(sorted_eta[:, 1]).astype(float)
    probe_phi = ak.to_numpy(sorted_phi[:, 1]).astype(float)
    probe_mass = ak.to_numpy(sorted_mass[:, 1]).astype(float)
    probe_charge = ak.to_numpy(sorted_charge[:, 1]).astype(int)
    probe_index = ak.to_numpy(sorted_index[:, 1]).astype(int)

    valid = (tag_charge != 0) & (probe_charge != 0) & (tag_charge * probe_charge < 0) & tag_ok
    if not np.any(valid):
        return {
            "pt": np.array([]),
            "eta": np.array([]),
            "phi": np.array([]),
            "mass": np.array([]),
            "event": np.array([], dtype=int),
            "index": np.array([], dtype=int),
        }

    e1 = np.sqrt(np.maximum((tag_pt * np.cosh(tag_eta)) ** 2 + tag_mass**2, 0.0))
    e2 = np.sqrt(np.maximum((probe_pt * np.cosh(probe_eta)) ** 2 + probe_mass**2, 0.0))
    px = tag_pt * np.cos(tag_phi) + probe_pt * np.cos(probe_phi)
    py = tag_pt * np.sin(tag_phi) + probe_pt * np.sin(probe_phi)
    pz = tag_pt * np.sinh(tag_eta) + probe_pt * np.sinh(probe_eta)
    energy = e1 + e2
    pair_mass = np.sqrt(np.maximum(energy * energy - px * px - py * py - pz * pz, 0.0))
    return {
        "pt": probe_pt[valid],
        "eta": probe_eta[valid],
        "phi": probe_phi[valid],
        "mass": pair_mass[valid],
        "event": event_indices[valid].astype(int),
        "index": probe_index[valid],
    }


def tnp_probe_with_pass(base: Mapping[str, np.ndarray], probe_passed) -> Dict[str, np.ndarray]:
    passed = matched_object_values(probe_passed, base["event"], base["index"]).astype(bool)
    return {
        "pt": np.asarray(base["pt"], dtype=float),
        "eta": np.asarray(base["eta"], dtype=float),
        "phi": np.asarray(base["phi"], dtype=float),
        "mass": np.asarray(base["mass"], dtype=float),
        "pass": passed,
    }


def tnp_event_probe_with_pass(base: Mapping[str, np.ndarray], event_passed) -> Dict[str, np.ndarray]:
    event_pass = ak.to_numpy(event_passed).astype(bool) if isinstance(event_passed, ak.Array) else np.asarray(event_passed, dtype=bool)
    valid = (base["event"] >= 0) & (base["event"] < len(event_pass))
    passed = np.zeros(len(base["event"]), dtype=bool)
    passed[valid] = event_pass[base["event"][valid]]
    return {
        "pt": np.asarray(base["pt"], dtype=float),
        "eta": np.asarray(base["eta"], dtype=float),
        "phi": np.asarray(base["phi"], dtype=float),
        "mass": np.asarray(base["mass"], dtype=float),
        "pass": passed,
    }


def tnp_event_probes(arrays: Mapping[str, ak.Array], br: Mapping[str, str], event_passed, tag_passed) -> Dict[str, np.ndarray]:
    required = [br.get("pt"), br.get("eta"), br.get("phi"), br.get("mass"), br.get("charge")]
    if any(name not in arrays for name in required):
        return {
            "pt": np.array([]),
            "eta": np.array([]),
            "phi": np.array([]),
            "mass": np.array([]),
            "pass": np.array([], dtype=bool),
        }

    pts = ak.to_list(arrays[br["pt"]])
    etas = ak.to_list(arrays[br["eta"]])
    phis = ak.to_list(arrays[br["phi"]])
    masses = ak.to_list(arrays[br["mass"]])
    charges = ak.to_list(arrays[br["charge"]])
    event_pass = ak.to_numpy(event_passed).astype(bool)
    tag_passes = ak.to_list(tag_passed)

    out = {"pt": [], "eta": [], "phi": [], "mass": [], "pass": []}
    for iev, event_pts in enumerate(pts):
        limit = min(len(event_pts), len(charges[iev]), len(tag_passes[iev]))
        if limit < 2:
            continue
        ordered = sorted(range(limit), key=lambda idx: event_pts[idx], reverse=True)
        tag = ordered[0]
        probe = ordered[1]
        tag_charge = int(charges[iev][tag])
        probe_charge = int(charges[iev][probe])
        if tag_charge == 0 or probe_charge == 0 or tag_charge * probe_charge >= 0:
            continue
        if not bool(tag_passes[iev][tag]):
            continue
        pair_mass, _, _, _ = system_kinematics(
            (event_pts[tag], etas[iev][tag], phis[iev][tag], masses[iev][tag]),
            (event_pts[probe], etas[iev][probe], phis[iev][probe], masses[iev][probe]),
        )
        out["pt"].append(event_pts[probe])
        out["eta"].append(etas[iev][probe])
        out["phi"].append(phis[iev][probe])
        out["mass"].append(pair_mass)
        out["pass"].append(bool(event_pass[iev]))
    return {key: np.asarray(value) for key, value in out.items()}


def add_tnp_mass_candidates(
    store: MutableMapping[Tuple, Dict[str, List[List[np.ndarray]]]],
    key_base: Tuple,
    probes: Mapping[str, np.ndarray],
    edges_by_var: Mapping[str, np.ndarray],
    variables: Sequence[str],
) -> None:
    masses = np.asarray(probes.get("mass", np.array([])), dtype=float)
    passed = np.asarray(probes.get("pass", np.array([])), dtype=bool)
    if len(masses) == 0:
        return
    mass_window = np.isfinite(masses) & (masses >= MASS_FIT_MIN) & (masses <= MASS_FIT_MAX)
    for var in variables:
        if var not in probes or var not in edges_by_var:
            continue
        edges = edges_by_var[var]
        key = key_base + (var,)
        if key not in store:
            store[key] = {
                "pass": [[] for _ in range(len(edges) - 1)],
                "fail": [[] for _ in range(len(edges) - 1)],
            }
        values = np.asarray(probes[var], dtype=float)
        finite = mass_window & np.isfinite(values)
        bins = np.searchsorted(edges, values, side="right") - 1
        in_range = finite & (bins >= 0) & (bins < len(edges) - 1)
        for ibin in range(len(edges) - 1):
            bin_mask = in_range & (bins == ibin)
            if not np.any(bin_mask):
                continue
            store[key]["pass"][ibin].append(masses[bin_mask & passed])
            store[key]["fail"][ibin].append(masses[bin_mask & ~passed])


def make_combined_roodataset(
    name: str,
    mass_var,
    sample,
    pass_masses: np.ndarray,
    fail_masses: np.ndarray,
    fit_min: float,
    fit_max: float,
):
    data = ROOT.RooDataSet(name, name, ROOT.RooArgSet(mass_var, sample))
    args = ROOT.RooArgSet(mass_var, sample)
    for label, masses in (("pass", pass_masses), ("fail", fail_masses)):
        sample.setLabel(label)
        for value in np.asarray(masses, dtype=float):
            if not np.isfinite(value) or value < fit_min or value > fit_max:
                continue
            mass_var.setVal(float(value))
            data.add(args)
    return data


def converged_fit(result) -> bool:
    if result is None:
        return False
    return int(result.status()) == 0 and int(result.covQual()) >= 2


def fit_result_nfloat(result) -> int:
    if result is None:
        return 0
    try:
        return max(0, int(result.floatParsFinal().getSize()))
    except Exception:
        return 0


def projection_chi2_ndf(
    mass,
    sample,
    comb_data,
    sim_pdf,
    label: str,
    uid: str,
    n_float: int,
    fit_min: float,
    fit_max: float,
) -> float:
    frame = mass.frame(ROOT.RooFit.Range(fit_min, fit_max), ROOT.RooFit.Bins(TNP_CHI2_BINS))
    sample_name = sample.GetName()
    mass_name = mass.GetName()
    data_name = f"chi2_data_{label}_{uid}"
    model_name = f"chi2_model_{label}_{uid}"
    sample_set = ROOT.RooArgSet(sample)
    comb_data.plotOn(
        frame,
        ROOT.RooFit.Cut(
            f"{sample_name}=={sample_name}::{label} && {mass_name}>={fit_min:.12g} && {mass_name}<={fit_max:.12g}"
        ),
        ROOT.RooFit.Name(data_name),
    )
    sim_pdf.plotOn(
        frame,
        ROOT.RooFit.Slice(sample, label),
        ROOT.RooFit.ProjWData(sample_set, comb_data),
        ROOT.RooFit.Name(model_name),
    )
    projection_nfloat = max(1, int(math.ceil(0.5 * n_float)))
    chi2 = float(frame.chiSquare(model_name, data_name, projection_nfloat))
    if not np.isfinite(chi2) or chi2 <= 0.0:
        return np.inf
    return chi2


def tnp_fit_quality(result, mass, sample, comb_data, sim_pdf, uid: str) -> Dict[str, float]:
    fit_min = float(mass.getMin("fit_window"))
    fit_max = float(mass.getMax("fit_window"))
    n_float = fit_result_nfloat(result)
    quality = {
        "status": float(result.status()) if result is not None else np.inf,
        "covQual": float(result.covQual()) if result is not None else -1.0,
        "n_float": float(n_float),
        "fit_min": fit_min,
        "fit_max": fit_max,
        "chi2_pass": np.inf,
        "chi2_fail": np.inf,
        "chi2_max": np.inf,
    }
    if not converged_fit(result):
        return quality
    chi2_pass = projection_chi2_ndf(mass, sample, comb_data, sim_pdf, "pass", uid, n_float, fit_min, fit_max)
    chi2_fail = projection_chi2_ndf(mass, sample, comb_data, sim_pdf, "fail", uid, n_float, fit_min, fit_max)
    quality["chi2_pass"] = chi2_pass
    quality["chi2_fail"] = chi2_fail
    quality["chi2_max"] = max(chi2_pass, chi2_fail)
    return quality


def acceptable_fit_quality(quality: Mapping[str, float]) -> bool:
    return (
        int(quality.get("status", 1)) == 0
        and int(quality.get("covQual", 0)) >= 2
        and float(quality.get("chi2_max", np.inf)) <= TNP_MAX_CHI2_NDF
    )


def format_tnp_quality(quality: Mapping[str, float]) -> str:
    if not quality:
        return "fit quality unavailable"
    return (
        f"status={int(quality.get('status', -1))}, covQual={int(quality.get('covQual', -1))}, "
        f"range=[{quality.get('fit_min', MASS_FIT_MIN):.0f},{quality.get('fit_max', MASS_FIT_MAX):.0f}], "
        f"chi2/ndf pass={quality.get('chi2_pass', np.inf):.2f}, "
        f"fail={quality.get('chi2_fail', np.inf):.2f}"
    )


def format_bin_edge(value: float) -> str:
    return sanitize(f"{float(value):g}")


def tnp_fit_plot_path(fit_dir: Path, key: Tuple, ibin: int, edges: Optional[np.ndarray], tier: str) -> Path:
    flavor, branch, sample, _, var = key
    bin_label = f"bin{ibin:03d}"
    if edges is not None and ibin + 1 < len(edges):
        bin_label += f"_{format_bin_edge(edges[ibin])}_to_{format_bin_edge(edges[ibin + 1])}"
    filename = f"fit_{sample}_{flavor}_{sanitize(branch)}_{var}_{bin_label}_{tier}.pdf"
    return fit_dir / filename


def tnp_fit_plot_title(key: Tuple, ibin: int, edges: Optional[np.ndarray], tier: str, n_pass: int, n_fail: int) -> str:
    flavor, branch, sample, _, var = key
    parts = [sample, flavor, branch, var, f"bin {ibin}", tier, f"pass/fail {n_pass}/{n_fail}"]
    if edges is not None and ibin + 1 < len(edges):
        parts.insert(5, f"{edges[ibin]:g} <= {var} < {edges[ibin + 1]:g}")
    return " | ".join(parts)


def mass_peak_and_width(pass_masses: np.ndarray, fail_masses: np.ndarray) -> Tuple[float, float]:
    masses = np.concatenate([pass_masses, fail_masses]) if len(pass_masses) or len(fail_masses) else np.array([])
    masses = masses[np.isfinite(masses) & (masses >= MASS_FIT_MIN) & (masses <= MASS_FIT_MAX)]
    if len(masses) < 10:
        return Z_MASS, 2.0
    peak_masses = masses[(masses >= MASS_PEAK_SEARCH_MIN) & (masses <= MASS_PEAK_SEARCH_MAX)]
    if len(peak_masses) >= 10:
        hist, edges = np.histogram(peak_masses, bins=np.linspace(MASS_PEAK_SEARCH_MIN, MASS_PEAK_SEARCH_MAX, 81))
    else:
        hist, edges = np.histogram(masses, bins=np.linspace(MASS_FIT_MIN, MASS_FIT_MAX, 81))
    if np.sum(hist) <= 0:
        return Z_MASS, 2.0
    imax = int(np.argmax(hist))
    low = max(0, imax - 2)
    high = min(len(hist), imax + 3)
    centers = 0.5 * (edges[:-1] + edges[1:])
    weights = hist[low:high].astype(float)
    peak = float(np.average(centers[low:high], weights=weights)) if np.sum(weights) > 0.0 else float(centers[imax])
    central = masses[(masses >= peak - 15.0) & (masses <= peak + 15.0)]
    if len(central) >= 10:
        q16, q84 = np.percentile(central, [16.0, 84.0])
        width = 0.5 * (q84 - q16)
    else:
        width = np.std(masses)
    return float(np.clip(peak, MASS_FIT_MIN + 3.0, MASS_FIT_MAX - 3.0)), float(np.clip(width, 0.8, 12.0))


def has_high_mass_background_shape(pass_masses: np.ndarray, fail_masses: np.ndarray) -> bool:
    masses = np.concatenate([pass_masses, fail_masses]) if len(pass_masses) or len(fail_masses) else np.array([])
    masses = masses[np.isfinite(masses) & (masses >= MASS_FIT_MIN) & (masses <= MASS_FIT_MAX)]
    if len(masses) < 80:
        return False
    peak = np.count_nonzero((masses >= 90.0) & (masses <= 100.0))
    high = np.count_nonzero((masses > MASS_FIT_ALT_MAX) & (masses <= MASS_FIT_MAX))
    if peak < 20:
        return False
    return (high / peak) > 0.12


def low_side_shoulder_fit_window(pass_masses: np.ndarray, fail_masses: np.ndarray) -> Optional[Tuple[float, float]]:
    masses = np.concatenate([pass_masses, fail_masses]) if len(pass_masses) or len(fail_masses) else np.array([])
    masses = masses[np.isfinite(masses) & (masses >= MASS_FIT_MIN) & (masses <= MASS_FIT_MAX)]
    if len(masses) < 250:
        return None
    hist, edges = np.histogram(masses, bins=np.arange(65.0, 106.0, 1.0))
    if np.sum(hist) <= 0:
        return None
    centers = 0.5 * (edges[:-1] + edges[1:])
    smooth = np.convolve(hist.astype(float), np.array([0.25, 0.5, 0.25]), mode="same")
    peak_mask = (centers >= 84.0) & (centers <= 98.0)
    if not np.any(peak_mask):
        return None
    peak_idx_candidates = np.flatnonzero(peak_mask)
    peak_idx = int(peak_idx_candidates[np.argmax(smooth[peak_idx_candidates])])
    peak_center = float(centers[peak_idx])
    peak_height = float(smooth[peak_idx])
    if peak_height < 30.0:
        return None

    low_mask = (centers >= 68.0) & (centers <= peak_center - 6.0)
    if not np.any(low_mask):
        return None
    low_idx_candidates = np.flatnonzero(low_mask)
    low_idx = int(low_idx_candidates[np.argmax(smooth[low_idx_candidates])])
    low_height = float(smooth[low_idx])
    if low_height < 0.20 * peak_height:
        return None
    valley = float(np.min(smooth[low_idx: peak_idx + 1])) if low_idx < peak_idx else peak_height
    if valley > 0.85 * min(low_height, peak_height):
        return None

    fit_min = max(MASS_FIT_MIN, peak_center - 9.0)
    fit_max = min(MASS_FIT_ALT_MAX, peak_center + 10.0)
    if fit_max - fit_min < 14.0:
        return None
    return float(fit_min), float(fit_max)


def fit_context_from_bin(
    plot_key: Optional[Tuple],
    ibin: Optional[int],
    edges: Optional[np.ndarray],
    pass_masses: np.ndarray,
    fail_masses: np.ndarray,
) -> Dict[str, float]:
    flavor = plot_key[0] if plot_key is not None else "muon"
    var = plot_key[-1] if plot_key is not None else ""
    pt_hint = 45.0
    abs_eta_hint = 0.8
    if edges is not None and ibin is not None and 0 <= ibin and ibin + 1 < len(edges):
        low = float(edges[ibin])
        high = float(edges[ibin + 1])
        center = 0.5 * (low + high)
        if var == "pt":
            pt_hint = max(center, 1.0)
        elif var == "eta":
            if low <= 0.0 <= high:
                abs_eta_hint = 0.25 * (abs(low) + abs(high))
            else:
                abs_eta_hint = abs(center)
    masses = np.concatenate([pass_masses, fail_masses]) if len(pass_masses) or len(fail_masses) else np.array([])
    right_tail = False
    if len(masses) >= 10:
        q10, q90 = np.percentile(masses, [10.0, 90.0])
        right_tail = (q90 - np.median(masses)) > (np.median(masses) - q10)
    mass_peak, mass_width = mass_peak_and_width(pass_masses, fail_masses)
    return {
        "flavor": flavor,
        "pt": float(pt_hint),
        "abs_eta": float(abs_eta_hint),
        "right_tail": float(right_tail),
        "mass_peak": mass_peak,
        "mass_width": mass_width,
        "allow_alt_fit_max": float(has_high_mass_background_shape(pass_masses, fail_masses)),
    }


def signal_shape_hints(context: Mapping[str, float]) -> Dict[str, float]:
    flavor = str(context.get("flavor", "muon"))
    eta_term = float(np.clip(context.get("abs_eta", 0.8) / 2.5, 0.0, 1.6))
    pt_term = float(np.clip((context.get("pt", 45.0) - 45.0) / 160.0, 0.0, 1.8))
    right_tail = bool(context.get("right_tail", 0.0))
    mass_width = float(np.clip(context.get("mass_width", 2.0), 0.8, 12.0))

    if flavor == "electron":
        sigma1 = max(1.05 + 0.55 * eta_term + 0.45 * pt_term, 0.45 * mass_width)
        sigma2 = sigma1 * (5.2 + 0.80 * eta_term + 0.35 * pt_term)
        alpha_l = 0.75 + 0.15 * (not right_tail) - 0.08 * eta_term
        alpha_r = -(0.70 + 0.20 * right_tail - 0.05 * eta_term)
        n_tail = 0.85
        frac = 0.68
        sigma1_bounds = (0.08, 10.0)
        sigma2_bounds = (1.0, 40.0)
        alpha_bound = 0.20
    else:
        sigma1 = max(0.75 + 0.32 * eta_term + 0.28 * pt_term, 0.40 * mass_width)
        sigma2 = sigma1 * (2.6 + 0.25 * eta_term)
        alpha_l = 2.05 + 0.25 * (not right_tail) - 0.10 * eta_term
        alpha_r = -(2.25 + 0.25 * right_tail - 0.10 * eta_term)
        n_tail = 2.4
        frac = 0.72
        sigma1_bounds = (0.25, 6.0)
        sigma2_bounds = (0.8, 18.0)
        alpha_bound = 0.35

    sigma1 = float(np.clip(sigma1, *sigma1_bounds))
    sigma2 = float(np.clip(max(sigma2, sigma1 * 2.2), *sigma2_bounds))
    return {
        "sigma1": sigma1,
        "sigma2": sigma2,
        "alpha_l": float(np.clip(alpha_l, alpha_bound, 8.0)),
        "alpha_r": float(np.clip(alpha_r, -8.0, -alpha_bound)),
        "n_tail": float(n_tail),
        "frac": float(np.clip(frac, 0.0, 1.0)),
        "single_alpha": float(np.clip(alpha_r if right_tail else alpha_l, -8.0, 8.0)),
    }


def initial_bkg_fraction(context: Mapping[str, float], passed: bool) -> float:
    eta_term = float(np.clip(context.get("abs_eta", 0.8) / 2.5, 0.0, 1.5))
    pt_term = float(np.clip((context.get("pt", 45.0) - 45.0) / 160.0, 0.0, 1.5))
    eta_factor = 0.70 + 0.45 * eta_term
    pt_factor = 1.0 / (1.0 + 0.80 * pt_term)
    pass_factor = 0.60 if passed else 1.15
    return float(np.clip(0.05 * eta_factor * pt_factor * pass_factor, 0.005, 0.50))


def save_tnp_fit_plot(
    plot_path: Path,
    title: str,
    tier: str,
    uid: str,
    mass,
    sample,
    comb_data,
    sim_pdf,
    quality: Optional[Mapping[str, float]] = None,
) -> None:
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    frame = mass.frame(ROOT.RooFit.Title(title))
    sample_name = sample.GetName()
    sample_set = ROOT.RooArgSet(sample)
    comb_data.plotOn(
        frame,
        ROOT.RooFit.Cut(f"{sample_name}=={sample_name}::fail"),
        ROOT.RooFit.MarkerColor(ROOT.kRed + 1),
        ROOT.RooFit.LineColor(ROOT.kRed + 1),
        ROOT.RooFit.Name(f"data_fail_{uid}"),
    )
    sim_pdf.plotOn(
        frame,
        ROOT.RooFit.Slice(sample, "fail"),
        ROOT.RooFit.ProjWData(sample_set, comb_data),
        ROOT.RooFit.LineColor(ROOT.kRed + 1),
        ROOT.RooFit.Name(f"model_fail_{uid}"),
    )
    sim_pdf.plotOn(
        frame,
        ROOT.RooFit.Slice(sample, "fail"),
        ROOT.RooFit.ProjWData(sample_set, comb_data),
        ROOT.RooFit.Components(f"bkg_fail_{uid}"),
        ROOT.RooFit.LineColor(ROOT.kRed + 2),
        ROOT.RooFit.LineStyle(ROOT.kDashed),
        ROOT.RooFit.Name(f"bkg_fail_{uid}"),
    )
    comb_data.plotOn(
        frame,
        ROOT.RooFit.Cut(f"{sample_name}=={sample_name}::pass"),
        ROOT.RooFit.MarkerColor(ROOT.kBlue + 1),
        ROOT.RooFit.LineColor(ROOT.kBlue + 1),
        ROOT.RooFit.Name(f"data_pass_{uid}"),
    )
    sim_pdf.plotOn(
        frame,
        ROOT.RooFit.Slice(sample, "pass"),
        ROOT.RooFit.ProjWData(sample_set, comb_data),
        ROOT.RooFit.LineColor(ROOT.kBlue + 1),
        ROOT.RooFit.Name(f"model_pass_{uid}"),
    )
    sim_pdf.plotOn(
        frame,
        ROOT.RooFit.Slice(sample, "pass"),
        ROOT.RooFit.ProjWData(sample_set, comb_data),
        ROOT.RooFit.Components(f"bkg_pass_{uid}"),
        ROOT.RooFit.LineColor(ROOT.kBlue + 2),
        ROOT.RooFit.LineStyle(ROOT.kDashed),
        ROOT.RooFit.Name(f"bkg_pass_{uid}"),
    )

    canvas = ROOT.TCanvas(f"canvas_{uid}", f"canvas_{uid}", 900, 700)
    frame.GetXaxis().SetTitle("m_{ll} [GeV]")
    frame.GetYaxis().SetTitle("Candidates")
    frame.GetXaxis().SetTitleSize(0.052)
    frame.GetYaxis().SetTitleSize(0.052)
    frame.GetXaxis().SetLabelSize(0.044)
    frame.GetYaxis().SetLabelSize(0.044)
    frame.Draw()
    if quality is not None:
        latex = ROOT.TLatex()
        latex.SetNDC(True)
        latex.SetTextSize(0.030)
        latex.DrawLatex(
            0.18,
            0.82,
            f"#chi^{{2}}/ndf pass = {quality.get('chi2_pass', np.inf):.2f}",
        )
        latex.DrawLatex(
            0.18,
            0.77,
            f"#chi^{{2}}/ndf fail = {quality.get('chi2_fail', np.inf):.2f}",
        )
        latex.DrawLatex(
            0.18,
            0.72,
            f"status = {int(quality.get('status', -1))}, covQual = {int(quality.get('covQual', -1))}",
        )
        latex.DrawLatex(
            0.18,
            0.67,
            f"fit range = [{quality.get('fit_min', MASS_FIT_MIN):.0f}, {quality.get('fit_max', MASS_FIT_MAX):.0f}] GeV",
        )
    legend = ROOT.TLegend(0.62, 0.70, 0.88, 0.88)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.034)
    for object_name, label, option in (
        (f"data_fail_{uid}", "fail data", "pe"),
        (f"model_fail_{uid}", f"fail {tier}", "l"),
        (f"bkg_fail_{uid}", "fail bkg exp", "l"),
        (f"data_pass_{uid}", "pass data", "pe"),
        (f"model_pass_{uid}", f"pass {tier}", "l"),
        (f"bkg_pass_{uid}", "pass bkg exp", "l"),
    ):
        obj = frame.findObject(object_name)
        if obj:
            legend.AddEntry(obj, label, option)
    legend.Draw()
    canvas.SaveAs(str(plot_path))


def tnp_fit_model_tier(n_pass: int, n_total: int) -> str:
    if n_total >= TNP_DOUBLE_CB_MIN_ALL and n_pass >= TNP_DOUBLE_CB_MIN_PASS:
        return "double_cb"
    if n_total >= TNP_SINGLE_CB_MIN_ALL and n_pass >= TNP_SINGLE_CB_MIN_PASS:
        return "single_cb"
    return "gaussian"


def tnp_fit_tiers(start_tier: str) -> Sequence[str]:
    tiers = ("double_cb", "single_cb", "gaussian")
    return tiers[tiers.index(start_tier):]


def fit_tnp_signal_efficiency_with_model(
    tier: str,
    uid: str,
    mass,
    sample,
    pass_masses: np.ndarray,
    fail_masses: np.ndarray,
    n_pass: int,
    n_fail: int,
    fit_context: Mapping[str, float],
    fit_min: float,
    fit_max: float,
    plot_path: Optional[Path] = None,
    plot_title: Optional[str] = None,
    save_rejected_plot: bool = True,
) -> Tuple[float, float, Dict[str, float]]:
    n_total = n_pass + n_fail
    mass.setRange("full", MASS_FIT_MIN, MASS_FIT_MAX)
    mass.setRange("fit_window", fit_min, fit_max)
    n_pass_fit = int(np.count_nonzero((pass_masses >= fit_min) & (pass_masses <= fit_max)))
    n_fail_fit = int(np.count_nonzero((fail_masses >= fit_min) & (fail_masses <= fit_max)))
    if min(n_pass_fit, n_fail_fit) < TNP_MIN_FIT_EACH or (n_pass_fit + n_fail_fit) < TNP_MIN_FIT_ALL:
        return np.nan, np.nan, {
            "status": np.inf,
            "covQual": -1.0,
            "fit_min": fit_min,
            "fit_max": fit_max,
            "chi2_pass": np.inf,
            "chi2_fail": np.inf,
            "chi2_max": np.inf,
        }
    comb_data = make_combined_roodataset(
        f"comb_data_{uid}",
        mass,
        sample,
        pass_masses,
        fail_masses,
        fit_min,
        fit_max,
    )
    if comb_data.numEntries() < TNP_MIN_FIT_ALL:
        return np.nan, np.nan, {"status": np.inf, "covQual": -1.0, "fit_min": fit_min, "fit_max": fit_max}
    shape = signal_shape_hints(fit_context)
    bkg_pass_init = initial_bkg_fraction(fit_context, passed=True)
    bkg_fail_init = initial_bkg_fraction(fit_context, passed=False)
    avg_bkg_init = 0.5 * (bkg_pass_init + bkg_fail_init)
    mean_hint = float(np.clip(fit_context.get("mass_peak", Z_MASS), MASS_FIT_MIN + 2.0, MASS_FIT_MAX - 2.0))
    mean_window = float(np.clip(2.5 * fit_context.get("mass_width", 2.0), 5.0, 18.0))
    mean_low = max(MASS_FIT_MIN + 1.0, mean_hint - mean_window)
    mean_high = min(MASS_FIT_MAX - 1.0, mean_hint + mean_window)
    mean = ROOT.RooRealVar(f"mean_{uid}", "mean", mean_hint, mean_low, mean_high)
    slope_pass = ROOT.RooRealVar(f"slope_pass_{uid}", "slope_pass", -0.015, -0.10, 0.03)
    slope_fail = ROOT.RooRealVar(f"slope_fail_{uid}", "slope_fail", -0.015, -0.10, 0.03)

    if tier == "double_cb":
        is_electron = str(fit_context.get("flavor", "muon")) == "electron"
        sigma_small_min, sigma_small_max = (0.05, 10.0) if is_electron else (0.15, 8.0)
        sigma_gap_min, sigma_gap_max = (0.20, 35.0) if is_electron else (0.10, 20.0)
        alpha_bound = 0.15 if is_electron else 0.25
        sigma_small_init = float(np.clip(shape["sigma1"], sigma_small_min, sigma_small_max))
        sigma_gap_init = float(np.clip(shape["sigma2"] - sigma_small_init, sigma_gap_min, sigma_gap_max))
        # Keep the two CB widths ordered separately for pass/fail. Sharing the
        # peak position is stable, but sharing the full resolution model can
        # bias bins where the selected and rejected probes have different tails.
        sigma_small_pass = ROOT.RooRealVar(
            f"sigma_small_pass_{uid}",
            "sigma_small_pass",
            sigma_small_init,
            sigma_small_min,
            sigma_small_max,
        )
        sigma_gap_pass = ROOT.RooRealVar(
            f"sigma_gap_pass_{uid}",
            "sigma_gap_pass",
            sigma_gap_init,
            sigma_gap_min,
            sigma_gap_max,
        )
        sigma_large_pass = ROOT.RooFormulaVar(
            f"sigma_large_pass_{uid}",
            "sigma_large_pass",
            "@0+@1",
            ROOT.RooArgList(sigma_small_pass, sigma_gap_pass),
        )
        sigma_small_fail = ROOT.RooRealVar(
            f"sigma_small_fail_{uid}",
            "sigma_small_fail",
            sigma_small_init,
            sigma_small_min,
            sigma_small_max,
        )
        sigma_gap_fail = ROOT.RooRealVar(
            f"sigma_gap_fail_{uid}",
            "sigma_gap_fail",
            sigma_gap_init,
            sigma_gap_min,
            sigma_gap_max,
        )
        sigma_large_fail = ROOT.RooFormulaVar(
            f"sigma_large_fail_{uid}",
            "sigma_large_fail",
            "@0+@1",
            ROOT.RooArgList(sigma_small_fail, sigma_gap_fail),
        )
        alpha_l = ROOT.RooRealVar(f"alpha_l_{uid}", "alpha_l", shape["alpha_l"], alpha_bound, 10.0)
        alpha_r = ROOT.RooRealVar(f"alpha_r_{uid}", "alpha_r", shape["alpha_r"], -10.0, -alpha_bound)
        n_l = ROOT.RooRealVar(f"n_l_{uid}", "n_l", shape["n_tail"])
        n_r = ROOT.RooRealVar(f"n_r_{uid}", "n_r", shape["n_tail"])
        n_l.setConstant(True)
        n_r.setConstant(True)
        frac_pass = ROOT.RooRealVar(f"frac_pass_{uid}", "frac_pass", shape["frac"], 0.0, 1.0)
        frac_fail = ROOT.RooRealVar(f"frac_fail_{uid}", "frac_fail", shape["frac"], 0.0, 1.0)
        cb_small_pass = ROOT.RooCBShape(f"cb_small_pass_{uid}", "cb_small_pass", mass, mean, sigma_small_pass, alpha_l, n_l)
        cb_large_pass = ROOT.RooCBShape(f"cb_large_pass_{uid}", "cb_large_pass", mass, mean, sigma_large_pass, alpha_r, n_r)
        cb_small_fail = ROOT.RooCBShape(f"cb_small_fail_{uid}", "cb_small_fail", mass, mean, sigma_small_fail, alpha_l, n_l)
        cb_large_fail = ROOT.RooCBShape(f"cb_large_fail_{uid}", "cb_large_fail", mass, mean, sigma_large_fail, alpha_r, n_r)
        signal_pass = ROOT.RooAddPdf(
            f"signal_pass_{uid}",
            "signal_pass",
            ROOT.RooArgList(cb_small_pass, cb_large_pass),
            ROOT.RooArgList(frac_pass),
        )
        signal_fail = ROOT.RooAddPdf(
            f"signal_fail_{uid}",
            "signal_fail",
            ROOT.RooArgList(cb_small_fail, cb_large_fail),
            ROOT.RooArgList(frac_fail),
        )
    elif tier == "single_cb":
        sigma_pass = ROOT.RooRealVar(f"sigma_pass_{uid}", "sigma_pass", shape["sigma1"], 0.15, 12.0)
        sigma_fail = ROOT.RooRealVar(f"sigma_fail_{uid}", "sigma_fail", shape["sigma1"], 0.15, 12.0)
        alpha_init = shape["single_alpha"]
        if alpha_init < 0.0:
            alpha = ROOT.RooRealVar(f"alpha_{uid}", "alpha", alpha_init, -8.0, -0.25)
        else:
            alpha = ROOT.RooRealVar(f"alpha_{uid}", "alpha", alpha_init, 0.25, 8.0)
        n = ROOT.RooRealVar(f"n_{uid}", "n", shape["n_tail"])
        n.setConstant(True)
        signal_pass = ROOT.RooCBShape(f"signal_pass_{uid}", "signal_pass", mass, mean, sigma_pass, alpha, n)
        signal_fail = ROOT.RooCBShape(f"signal_fail_{uid}", "signal_fail", mass, mean, sigma_fail, alpha, n)
    else:
        sigma_pass = ROOT.RooRealVar(f"sigma_pass_{uid}", "sigma_pass", shape["sigma1"], 0.15, 12.0)
        sigma_fail = ROOT.RooRealVar(f"sigma_fail_{uid}", "sigma_fail", shape["sigma1"], 0.15, 12.0)
        signal_pass = ROOT.RooGaussian(f"signal_pass_{uid}", "signal_pass", mass, mean, sigma_pass)
        signal_fail = ROOT.RooGaussian(f"signal_fail_{uid}", "signal_fail", mass, mean, sigma_fail)

    bkg_pass = ROOT.RooExponential(f"bkg_pass_{uid}", "bkg_pass", mass, slope_pass)
    bkg_fail = ROOT.RooExponential(f"bkg_fail_{uid}", "bkg_fail", mass, slope_fail)
    eff = ROOT.RooRealVar(f"tnp_eff_{uid}", "tnp_eff", min(max(n_pass / max(n_total, 1), 0.01), 0.99), 0.0, 1.0)
    nsig_total = ROOT.RooRealVar(
        f"nsig_total_{uid}",
        "nsig_total",
        max(1.0, n_total / (1.0 + avg_bkg_init)),
        0.0,
        1.2 * n_total + 20.0,
    )
    nsig_pass = ROOT.RooFormulaVar(
        f"nsig_pass_{uid}",
        "nsig_pass",
        "@0*@1",
        ROOT.RooArgList(eff, nsig_total),
    )
    nsig_fail = ROOT.RooFormulaVar(
        f"nsig_fail_{uid}",
        "nsig_fail",
        "(1.0-@0)*@1",
        ROOT.RooArgList(eff, nsig_total),
    )
    bkg_frac_pass = ROOT.RooRealVar(f"bkg_frac_pass_{uid}", "bkg_frac_pass", bkg_pass_init, 0.0, 0.5)
    bkg_frac_fail = ROOT.RooRealVar(f"bkg_frac_fail_{uid}", "bkg_frac_fail", bkg_fail_init, 0.0, 0.5)
    nbkg_pass = ROOT.RooFormulaVar(
        f"nbkg_pass_{uid}",
        "nbkg_pass",
        "@0*@1",
        ROOT.RooArgList(bkg_frac_pass, nsig_pass),
    )
    nbkg_fail = ROOT.RooFormulaVar(
        f"nbkg_fail_{uid}",
        "nbkg_fail",
        "@0*@1",
        ROOT.RooArgList(bkg_frac_fail, nsig_fail),
    )
    model_pass = ROOT.RooAddPdf(
        f"model_pass_{uid}",
        "model_pass",
        ROOT.RooArgList(signal_pass, bkg_pass),
        ROOT.RooArgList(nsig_pass, nbkg_pass),
    )
    model_fail = ROOT.RooAddPdf(
        f"model_fail_{uid}",
        "model_fail",
        ROOT.RooArgList(signal_fail, bkg_fail),
        ROOT.RooArgList(nsig_fail, nbkg_fail),
    )
    sim_pdf = ROOT.RooSimultaneous(f"sim_pdf_{uid}", "sim_pdf", sample)
    sim_pdf.addPdf(model_pass, "pass")
    sim_pdf.addPdf(model_fail, "fail")
    model_pass.fixCoefRange("full")
    model_fail.fixCoefRange("full")

    def run_fit(strategy: int):
        return sim_pdf.fitTo(
            comb_data,
            ROOT.RooFit.Save(True),
            ROOT.RooFit.Extended(True),
            ROOT.RooFit.Range("fit_window"),
            ROOT.RooFit.Strategy(strategy),
            ROOT.RooFit.Offset(True),
            ROOT.RooFit.PrintLevel(-1),
            ROOT.RooFit.Warnings(False),
        )

    result = run_fit(1)
    if not converged_fit(result):
        result = run_fit(2)
    quality = tnp_fit_quality(result, mass, sample, comb_data, sim_pdf, uid)
    if not acceptable_fit_quality(quality):
        if plot_path is not None and save_rejected_plot:
            rejected_path = plot_path.parent / "rejected" / plot_path.name
            save_tnp_fit_plot(
                rejected_path,
                f"{plot_title or uid} | rejected | {format_tnp_quality(quality)}",
                tier,
                uid,
                mass,
                sample,
                comb_data,
                sim_pdf,
                quality,
            )
        return np.nan, np.nan, quality

    if plot_path is not None:
        save_tnp_fit_plot(
            plot_path,
            f"{plot_title or uid} | {format_tnp_quality(quality)}",
            tier,
            uid,
            mass,
            sample,
            comb_data,
            sim_pdf,
            quality,
        )

    value = float(eff.getVal())
    error = float(eff.getError())
    if not np.isfinite(value) or not np.isfinite(error):
        return np.nan, np.nan, quality
    return np.clip(value, 0.0, 1.0), max(error, 0.0), quality


def fit_tnp_signal_efficiency(
    pass_masses: np.ndarray,
    fail_masses: np.ndarray,
    plot_dir: Optional[Path] = None,
    plot_key: Optional[Tuple] = None,
    ibin: Optional[int] = None,
    edges: Optional[np.ndarray] = None,
) -> Tuple[float, float]:
    pass_masses = np.asarray(pass_masses, dtype=float)
    fail_masses = np.asarray(fail_masses, dtype=float)
    pass_masses = pass_masses[np.isfinite(pass_masses) & (pass_masses >= MASS_FIT_MIN) & (pass_masses <= MASS_FIT_MAX)]
    fail_masses = fail_masses[np.isfinite(fail_masses) & (fail_masses >= MASS_FIT_MIN) & (fail_masses <= MASS_FIT_MAX)]
    n_pass = len(pass_masses)
    n_fail = len(fail_masses)
    n_total = n_pass + n_fail
    if n_total < TNP_MIN_FIT_ALL or min(n_pass, n_fail) < TNP_MIN_FIT_EACH:
        if plot_key is not None and ibin is not None:
            print(
                f"[WARN] TnP fit skipped for {plot_key} bin {ibin}; "
                f"insufficient fit statistics n_pass={n_pass}, n_fail={n_fail}"
            )
        return np.nan, np.nan
    if n_pass == 0 or n_fail == 0:
        return np.nan, np.nan

    base_uid = str(next(TNP_FIT_COUNTER))
    mass = ROOT.RooRealVar(f"mll_{base_uid}", "m_{ll}", MASS_FIT_MIN, MASS_FIT_MAX)
    mass.setRange("full", MASS_FIT_MIN, MASS_FIT_MAX)
    sample = ROOT.RooCategory(f"sample_{base_uid}", "sample")
    sample.defineType("pass")
    sample.defineType("fail")
    fit_context = fit_context_from_bin(plot_key, ibin, edges, pass_masses, fail_masses)
    best_quality: Optional[Dict[str, float]] = None
    best_tier: Optional[str] = None
    best_window: Optional[Tuple[float, float]] = None

    for tier in tnp_fit_tiers(tnp_fit_model_tier(n_pass, n_total)):
        windows = [(MASS_FIT_MIN, MASS_FIT_MAX)]
        if bool(fit_context.get("allow_alt_fit_max", 0.0)):
            windows.append((MASS_FIT_MIN, MASS_FIT_ALT_MAX))
        core_window = low_side_shoulder_fit_window(pass_masses, fail_masses)
        if core_window is not None and core_window not in windows:
            windows.append(core_window)
        for fit_min, fit_max in windows:
            plot_path = None
            plot_title = None
            if plot_dir is not None and plot_key is not None and ibin is not None:
                plot_path = tnp_fit_plot_path(plot_dir, plot_key, ibin, edges, tier)
                plot_title = (
                    f"{tnp_fit_plot_title(plot_key, ibin, edges, tier, n_pass, n_fail)} "
                    f"| fit {fit_min:g}-{fit_max:g} GeV"
                )
            value, error, quality = fit_tnp_signal_efficiency_with_model(
                tier,
                f"{base_uid}_{tier}_{format_bin_edge(fit_min)}_{format_bin_edge(fit_max)}",
                mass,
                sample,
                pass_masses,
                fail_masses,
                n_pass,
                n_fail,
                fit_context,
                fit_min,
                fit_max,
                plot_path,
                plot_title,
                False,
            )
            if best_quality is None or quality.get("chi2_max", np.inf) < best_quality.get("chi2_max", np.inf):
                best_quality = quality
                best_tier = tier
                best_window = (fit_min, fit_max)
            if np.isfinite(value) and np.isfinite(error):
                return value, error
    if plot_key is not None and ibin is not None:
        print(
            f"[WARN] TnP fit rejected for {plot_key} bin {ibin}; "
            f"best tier={best_tier}, {format_tnp_quality(best_quality or {})}; omitting TnP point"
        )
        if plot_dir is not None and best_tier is not None and best_window is not None:
            fit_min, fit_max = best_window
            plot_path = tnp_fit_plot_path(plot_dir, plot_key, ibin, edges, best_tier)
            plot_title = (
                f"{tnp_fit_plot_title(plot_key, ibin, edges, best_tier, n_pass, n_fail)} "
                f"| fit {fit_min:g}-{fit_max:g} GeV"
            )
            fit_tnp_signal_efficiency_with_model(
                best_tier,
                f"{base_uid}_{best_tier}_{format_bin_edge(fit_min)}_{format_bin_edge(fit_max)}_final_rejected",
                mass,
                sample,
                pass_masses,
                fail_masses,
                n_pass,
                n_fail,
                fit_context,
                fit_min,
                fit_max,
                plot_path,
                plot_title,
                False,
            )
    return np.nan, np.nan


def finalize_tnp_fits(
    eff_store: MutableMapping[Tuple, Dict[str, np.ndarray]],
    tnp_store: Mapping[Tuple, Dict[str, List[List[np.ndarray]]]],
    fit_dir: Optional[Path] = None,
    edges_by_var: Optional[Mapping[str, np.ndarray]] = None,
) -> None:
    if fit_dir is not None:
        fit_dir.mkdir(parents=True, exist_ok=True)
    for key, payload in tnp_store.items():
        n_bins = len(payload["pass"])
        eff = np.full(n_bins, np.nan, dtype=float)
        err = np.full(n_bins, np.nan, dtype=float)
        var_edges = edges_by_var.get(key[-1]) if edges_by_var is not None else None
        for ibin in range(n_bins):
            pass_masses = np.concatenate(payload["pass"][ibin]) if payload["pass"][ibin] else np.array([], dtype=float)
            fail_masses = np.concatenate(payload["fail"][ibin]) if payload["fail"][ibin] else np.array([], dtype=float)
            eff[ibin], err[ibin] = fit_tnp_signal_efficiency(
                pass_masses,
                fail_masses,
                fit_dir,
                key,
                ibin,
                var_edges,
            )
        eff_store[key] = {
            "eff": eff,
            "err": err,
            "num": eff.copy(),
            "den": np.ones_like(eff),
        }


def leading_dilepton_values(pt, eta, phi, mass, charge) -> Dict[str, np.ndarray]:
    out = {"mass": [], "pt": [], "eta": [], "phi": []}
    if charge is None:
        return {key: np.asarray(value) for key, value in out.items()}
    has_pair = (
        (ak.num(pt, axis=1) >= 2)
        & (ak.num(eta, axis=1) >= 2)
        & (ak.num(phi, axis=1) >= 2)
        & (ak.num(mass, axis=1) >= 2)
        & (ak.num(charge, axis=1) >= 2)
    )
    if not bool(ak.any(has_pair)):
        return {key: np.asarray(value) for key, value in out.items()}

    pt2 = pt[has_pair]
    order = ak.argsort(pt2, axis=1, ascending=False)
    leptons = ak.zip(
        {
            "pt": pt2[order],
            "eta": eta[has_pair][order],
            "phi": phi[has_pair][order],
            "mass": mass[has_pair][order],
            "charge": charge[has_pair][order],
        }
    )
    pairs = ak.combinations(leptons, 2, fields=["l1", "l2"])
    os_pair = (
        (pairs.l1.charge != 0)
        & (pairs.l2.charge != 0)
        & (pairs.l1.charge * pairs.l2.charge < 0)
    )
    selected = ak.firsts(pairs[os_pair])
    selected_mask = ~ak.is_none(selected)
    if not bool(ak.any(selected_mask)):
        return {key: np.asarray(value) for key, value in out.items()}

    l1 = selected[selected_mask].l1
    l2 = selected[selected_mask].l2
    pt1 = ak.to_numpy(l1.pt).astype(float)
    eta1 = ak.to_numpy(l1.eta).astype(float)
    phi1 = ak.to_numpy(l1.phi).astype(float)
    mass1 = ak.to_numpy(l1.mass).astype(float)
    pt2 = ak.to_numpy(l2.pt).astype(float)
    eta2 = ak.to_numpy(l2.eta).astype(float)
    phi2 = ak.to_numpy(l2.phi).astype(float)
    mass2 = ak.to_numpy(l2.mass).astype(float)

    e1 = np.sqrt(np.maximum((pt1 * np.cosh(eta1)) ** 2 + mass1**2, 0.0))
    e2 = np.sqrt(np.maximum((pt2 * np.cosh(eta2)) ** 2 + mass2**2, 0.0))
    px = pt1 * np.cos(phi1) + pt2 * np.cos(phi2)
    py = pt1 * np.sin(phi1) + pt2 * np.sin(phi2)
    pz = pt1 * np.sinh(eta1) + pt2 * np.sinh(eta2)
    energy = e1 + e2
    pair_pt = np.hypot(px, py)
    return {
        "mass": np.sqrt(np.maximum(energy * energy - px * px - py * py - pz * pz, 0.0)),
        "pt": pair_pt,
        "eta": np.arcsinh(np.divide(pz, pair_pt, out=np.zeros_like(pz), where=pair_pt > 0.0)),
        "phi": np.arctan2(py, px),
    }


def normalize_hist(counts: np.ndarray, edges: np.ndarray, normalize: bool) -> np.ndarray:
    if not normalize:
        return counts
    total = float(np.sum(counts))
    if total <= 0:
        return counts
    widths = np.diff(edges)
    return counts / (total * widths)


def hist_errors(counts: np.ndarray, edges: np.ndarray, normalize: bool) -> np.ndarray:
    counts = np.asarray(counts, dtype=float)
    errors = np.sqrt(np.maximum(counts, 0.0))
    if not normalize:
        return errors
    total = float(np.sum(counts))
    if total <= 0.0:
        return np.zeros_like(counts, dtype=float)
    return errors / (total * np.diff(edges))


def step_values(values: np.ndarray) -> np.ndarray:
    if len(values) == 0:
        return np.array([])
    return np.r_[values, values[-1]]


def plot_hist_comparison(
    figdir: Path,
    filename: str,
    hist_store: Mapping[Tuple, np.ndarray],
    key_base: Tuple,
    edges: np.ndarray,
    xlabel: str,
    ylabel: str,
    normalize: bool,
) -> None:
    fig, ax = plt.subplots()
    styles = {
        "input": (BLUE, "-", "raw"),
        "output": (RED, "-", "Modified"),
    }
    for sample, (color, linestyle, label) in styles.items():
        counts = hist_store.get(key_base + (sample,), np.zeros(len(edges) - 1))
        values = normalize_hist(counts, edges, normalize)
        errors = hist_errors(counts, edges, normalize)
        ax.fill_between(
            edges,
            step_values(np.maximum(values - errors, 0.0)),
            step_values(values + errors),
            step="post",
            color=color,
            alpha=0.8,
            linewidth=0,
        )
        ax.step(edges, step_values(values), where="post", color=color, linestyle=linestyle, linewidth=1.8, label=label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0.0)
    ax.legend()
    add_cms_label(ax)
    outpath = figdir / filename
    outpath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath)
    plt.close(fig)


def plot_correlation_heatmap(
    outdir: Path,
    filename: str,
    counts: np.ndarray,
    x_edges: np.ndarray,
    y_edges: np.ndarray,
    xlabel: str,
    ylabel: str,
    title: str,
) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    counts = np.asarray(counts, dtype=float)
    vmax = max(1.01, float(np.nanmax(counts)) if counts.size else 1.0)
    masked = np.ma.masked_less_equal(counts, 0.0)
    norm = LogNorm(vmin=1.0, vmax=vmax)

    fig, ax = plt.subplots(figsize=(8.0, 6.8))
    mesh = ax.pcolormesh(x_edges, y_edges, masked, cmap="RdBu_r", norm=norm, shading="auto")
    cbar = fig.colorbar(mesh, ax=ax)
    cbar.set_label("Entries")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
    y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])
    denom = math.log(vmax) if vmax > 1.0 else 1.0
    fontsize = 7 if counts.size <= 120 else 5
    for iy, y_center in enumerate(y_centers):
        for ix, x_center in enumerate(x_centers):
            value = counts[iy, ix]
            label = str(int(round(value)))
            if value >= 1.0 and denom > 0.0:
                strength = math.log(value) / denom
                color = "white" if strength > 0.55 else "black"
            else:
                color = "black"
            ax.text(x_center, y_center, label, ha="center", va="center", color=color, fontsize=fontsize)

    add_cms_label(ax)
    fig.savefig(outdir / filename)
    plt.close(fig)


def plot_correlation_delta_heatmap(
    outdir: Path,
    filename: str,
    delta: np.ndarray,
    x_edges: np.ndarray,
    y_edges: np.ndarray,
    xlabel: str,
    ylabel: str,
    title: str,
) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    delta = np.asarray(delta, dtype=float)
    max_abs = float(np.nanmax(np.abs(delta))) if delta.size else 0.0
    vmax = max(1.0, max_abs)
    norm = TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax)

    fig, ax = plt.subplots(figsize=(8.0, 6.8))
    mesh = ax.pcolormesh(x_edges, y_edges, delta, cmap="RdBu_r", norm=norm, shading="auto")
    cbar = fig.colorbar(mesh, ax=ax)
    cbar.set_label("Modified - raw entries")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
    y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])
    fontsize = 7 if delta.size <= 120 else 5
    for iy, y_center in enumerate(y_centers):
        for ix, x_center in enumerate(x_centers):
            value = delta[iy, ix]
            color = "white" if abs(value) > 0.55 * vmax else "black"
            ax.text(x_center, y_center, f"{int(round(value)):+d}", ha="center", va="center", color=color, fontsize=fontsize)

    add_cms_label(ax)
    fig.savefig(outdir / filename)
    plt.close(fig)


def plot_correlation_outputs(
    figdir: Path,
    store: Mapping[Tuple, np.ndarray],
    specs_by_flavor: Mapping[str, Sequence[Mapping]],
) -> None:
    outdir = figdir / "correlation"
    sample_labels = {"input": "raw", "output": "Modified"}
    for flavor, specs in specs_by_flavor.items():
        for spec in specs:
            xvar = spec["x"]
            yvar = spec["y"]
            for sample in ("input", "output"):
                key = (flavor, sample, xvar, yvar)
                if key not in store:
                    continue
                filename = f"corr_{flavor}_{sample}_{sanitize(xvar)}_{sanitize(yvar)}.pdf"
                title = f"{flavor} {sample_labels[sample]}: {xvar} vs {yvar}"
                plot_correlation_heatmap(
                    outdir / sample,
                    filename,
                    store[key],
                    spec["x_edges"],
                    spec["y_edges"],
                    spec["x_label"],
                    spec["y_label"],
                    title,
                )
            input_key = (flavor, "input", xvar, yvar)
            output_key = (flavor, "output", xvar, yvar)
            if input_key in store and output_key in store:
                filename = f"corr_{flavor}_delta_{sanitize(xvar)}_{sanitize(yvar)}.pdf"
                title = f"{flavor} Modified - raw: {xvar} vs {yvar}"
                plot_correlation_delta_heatmap(
                    outdir / "delta",
                    filename,
                    np.asarray(store[output_key], dtype=float) - np.asarray(store[input_key], dtype=float),
                    spec["x_edges"],
                    spec["y_edges"],
                    spec["x_label"],
                    spec["y_label"],
                    title,
                )


def efficiency_values(counts: Mapping[str, np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
    if "eff" in counts and "err" in counts:
        return np.asarray(counts["eff"], dtype=float), np.asarray(counts["err"], dtype=float)
    den = counts["den"]
    num = counts["num"]
    eff = np.divide(num, den, out=np.full_like(num, np.nan, dtype=float), where=den > 0)
    err = np.sqrt(np.divide(eff * (1.0 - eff), den, out=np.zeros_like(eff), where=den > 0))
    return eff, err


def plot_efficiency(
    figdir: Path,
    filename: str,
    eff_store: Mapping[Tuple, Dict[str, np.ndarray]],
    expected_store: Mapping[Tuple, Dict[str, np.ndarray]],
    flavor: str,
    branch: str,
    var: str,
    edges: np.ndarray,
    xlabel: str,
) -> None:
    fig, ax = plt.subplots()
    centers = 0.5 * (edges[:-1] + edges[1:])

    draw_specs = [
        ("input", "mc_truth", BLUE, "o", "raw MC truth"),
        ("input", "tnp", BLUE, "s", "raw TnP"),
        ("output", "mc_truth", RED, "o", "Modified MC truth"),
        ("output", "tnp", RED, "s", "Modified TnP"),
    ]
    for sample, method, color, marker, label in draw_specs:
        key = (flavor, branch, sample, method, var)
        if key not in eff_store:
            continue
        eff, err = efficiency_values(eff_store[key])
        valid = np.isfinite(eff)
        ax.errorbar(
            centers[valid],
            eff[valid],
            yerr=err[valid],
            linestyle="none",
            marker=marker,
            markersize=5,
            color=color,
            markerfacecolor="none",
            markeredgecolor=color,
            markeredgewidth=1.2,
            elinewidth=1.2,
            capsize=2,
            label=label,
        )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(f"{flavor} {branch} Efficiency")
    ax.set_ylim(0.0, 1.0)
    ax.legend(fontsize=12)
    add_cms_label(ax)
    outpath = figdir / filename
    outpath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath)
    plt.close(fig)


def lepton_distribution_label(flavor: str, var: str) -> str:
    labels = {
        "pt": f"{flavor} lepton pT [GeV]",
        "energy": f"{flavor} lepton energy [GeV]",
        "relative_pt_shift": f"{flavor} relative pT shift",
        "smear_response": f"{flavor} smearing response",
    }
    return labels.get(var, f"{flavor} {var}")


def dilepton_distribution_label(flavor: str, var: str) -> str:
    pair = "di-muon" if flavor == "muon" else "di-electron"
    labels = {
        "mass": f"OS {pair} mass [GeV]",
        "pt": f"OS {pair} pT [GeV]",
        "eta": f"OS {pair} eta",
        "phi": f"OS {pair} phi",
    }
    return labels.get(var, f"OS {pair} {var}")


def efficiency_label(flavor: str, var: str) -> str:
    labels = {
        "pt": f"{flavor} lepton pT [GeV]",
        "eta": f"{flavor} lepton eta",
        "phi": f"{flavor} lepton phi",
    }
    return labels.get(var, f"{flavor} lepton {var}")


def analyze(modify_cfg: Mapping, plot_cfg: Mapping, pairs: Sequence[Tuple[Path, Path]], figdir: Path, chunk_size: int) -> None:
    figdir.mkdir(parents=True, exist_ok=True)
    cms_style()
    tree_name = plot_cfg.get("tree_name", modify_cfg.get("global", {}).get("tree_name", "Events"))
    bins = bin_edges(modify_cfg, plot_cfg)
    eff_edges = {"pt": bins["eff_pt"], "eta": bins["eff_eta"], "phi": bins["eff_phi"]}
    hist_edges = {
        "pt": bins["hist_pt"],
        "energy": bins["hist_energy"],
        "relative_pt_shift": bins["hist_shift"],
        "smear_response": bins["hist_smear"],
    }
    dilepton_edges = {
        "mass": bins["dilepton_mass"],
        "pt": bins["dilepton_pt"],
        "eta": bins["dilepton_eta"],
        "phi": bins["dilepton_phi"],
    }

    eff_specs = efficiency_specs(plot_cfg, modify_cfg)
    eff_variables = {(item["flavor"], item["branch"]): item["variables"] for item in eff_specs}
    lepton_specs = {item["flavor"]: item["variables"] for item in lepton_distribution_specs(plot_cfg)}
    dilepton_specs = {item["flavor"]: item["variables"] for item in dilepton_distribution_specs(plot_cfg)}
    correlation_enabled = bool(plot_cfg.get("correlations", {}).get("enabled", False))
    correlation_specs_by_flavor = {
        flavor: (correlation_specs(modify_cfg, plot_cfg, flavor, bins) if correlation_enabled else [])
        for flavor in ("muon", "electron")
    }
    correlation_branch_cfgs_by_flavor = {
        flavor: correlation_branch_cfgs(plot_cfg, modify_cfg, flavor)
        for flavor in ("muon", "electron")
    }
    flavors_to_process = (
        set(lepton_specs)
        | set(dilepton_specs)
        | {item["flavor"] for item in eff_specs}
        | {flavor for flavor, specs in correlation_specs_by_flavor.items() if specs}
    )
    protect_expected_boson_mass = bool(plot_cfg.get("protect_expected_boson_mass", False))
    if not protect_expected_boson_mass:
        print("[INFO] Fast plotting: expected pT curves skip per-event boson-pair mass protection; output ROOT files remain fully validated")
    if not correlation_enabled:
        print("[INFO] Fast plotting: correlation heatmaps are disabled; set correlations.enabled=true to produce them")

    print("[INFO] Stage A: learning one merged input efficiency map from all input ROOT files")
    base_maps = build_base_efficiency_maps(modify_cfg, plot_cfg, [src for src, _ in pairs], chunk_size)

    eff_store: Dict[Tuple, Dict[str, np.ndarray]] = {}
    expected_eff_store: Dict[Tuple, Dict[str, np.ndarray]] = {}
    tnp_mass_store: Dict[Tuple, Dict[str, List[List[np.ndarray]]]] = {}
    hist_store: Dict[Tuple, np.ndarray] = {}
    dilepton_store: Dict[Tuple, np.ndarray] = {}
    correlation_store: Dict[Tuple, np.ndarray] = {}

    requested = branch_requests(modify_cfg, plot_cfg)
    print("[INFO] Stage B: comparing all input/output ROOT pairs and merging them into common plots")
    for input_path, output_path in pairs:
        if not output_path.exists():
            raise RuntimeError(f"Expected output file does not exist: {output_path}")
        input_tree = open_tree(input_path, tree_name)
        output_tree = open_tree(output_path, tree_name)
        if input_tree.num_entries != output_tree.num_entries:
            raise RuntimeError(f"Entry mismatch: {input_path} has {input_tree.num_entries}, {output_path} has {output_tree.num_entries}")

        progress_label = f"Compare {input_path} -> {output_path}"
        progress_bucket = -1
        progress_bucket = print_progress(progress_label, 0, input_tree.num_entries, progress_bucket)
        for start in range(0, input_tree.num_entries, chunk_size):
            stop = min(input_tree.num_entries, start + chunk_size)
            arr_in = read_arrays(input_tree, requested, start, stop, f"{input_path} input")
            arr_out = read_arrays(output_tree, requested, start, stop, f"{output_path} output")

            for flavor in sorted(flavors_to_process):
                br = lepton_branches(modify_cfg, flavor)
                needed = [br.get("pt"), br.get("eta"), br.get("phi"), br.get("mass")]
                if any(name not in arr_in or name not in arr_out for name in needed):
                    continue
                charge_in = arr_in.get(br.get("charge"))
                charge_out = arr_out.get(br.get("charge"))
                pt_in = arr_in[br["pt"]]
                eta_in = arr_in[br["eta"]]
                phi_in = arr_in[br["phi"]]
                mass_in = arr_in[br["mass"]]
                pt_out = arr_out[br["pt"]]
                eta_out = arr_out[br["eta"]]
                phi_out = arr_out[br["phi"]]
                mass_out = arr_out[br["mass"]]
                pt_exp, pt_scaled = expected_pt_arrays(
                    modify_cfg,
                    arr_in,
                    flavor,
                    start,
                    pt_in,
                    eta_in,
                    phi_in,
                    mass_in,
                    charge_in,
                    protect_expected_boson_mass,
                )

                energy_in = awkward_energy(pt_in, eta_in, mass_in)
                energy_exp = awkward_energy(pt_exp, eta_in, mass_in)
                energy_out = awkward_energy(pt_out, eta_out, mass_out)
                rel_shift_in = ak.zeros_like(pt_in)
                rel_shift_exp = ak.where(pt_in > 0, pt_exp / pt_in - 1.0, np.nan)
                rel_shift_out = ak.where(pt_in > 0, pt_out / pt_in - 1.0, np.nan)
                smear_in = ak.zeros_like(pt_in)
                smear_exp = ak.where(pt_scaled > 0, (pt_exp - pt_scaled) / pt_scaled, np.nan)
                smear_out = ak.where(pt_scaled > 0, (pt_out - pt_scaled) / pt_scaled, np.nan)

                corr_specs = correlation_specs_by_flavor.get(flavor, [])
                leading_in = gen_matched_boson_leading_values(arr_in, flavor, pt_in, eta_in, phi_in, energy=energy_in)
                leading_out = gen_matched_boson_leading_values(arr_out, flavor, pt_out, eta_out, phi_out, energy=energy_out)
                leading_exp = gen_matched_boson_leading_values(arr_in, flavor, pt_exp, eta_in, phi_in, energy=energy_exp)
                if corr_specs:
                    corr_branch_cfgs = correlation_branch_cfgs_by_flavor.get(flavor, {})
                    add_correlation_sample(
                        correlation_store,
                        corr_specs,
                        flavor,
                        "input",
                        arr_in,
                        leading_in,
                        corr_branch_cfgs,
                    )
                    add_correlation_sample(
                        correlation_store,
                        corr_specs,
                        flavor,
                        "output",
                        arr_out,
                        leading_out,
                        corr_branch_cfgs,
                    )

                dist_values = {
                    "pt": (pt_in, pt_exp, pt_out),
                    "energy": (energy_in, energy_exp, energy_out),
                    "relative_pt_shift": (rel_shift_in, rel_shift_exp, rel_shift_out),
                    "smear_response": (smear_in, smear_exp, smear_out),
                }
                for var in lepton_specs.get(flavor, []):
                    if var not in dist_values or var not in hist_edges:
                        print(f"[WARN] Unsupported lepton distribution {flavor}.{var}; skipping")
                        continue
                    vin, vexp, vout = dist_values[var]
                    edges = hist_edges[var]
                    add_hist_counts(hist_store, (flavor, var, "input"), vin, edges)
                    add_hist_counts(hist_store, (flavor, var, "expected"), vexp, edges)
                    add_hist_counts(hist_store, (flavor, var, "output"), vout, edges)

                if dilepton_specs.get(flavor):
                    for sample, pt, eta, phi, mass, charge in (
                        ("input", pt_in, eta_in, phi_in, mass_in, charge_in),
                        ("expected", pt_exp, eta_in, phi_in, mass_in, charge_in),
                        ("output", pt_out, eta_out, phi_out, mass_out, charge_out),
                    ):
                        values = leading_dilepton_values(pt, eta, phi, mass, charge)
                        for var in dilepton_specs.get(flavor, []):
                            if var not in values or var not in dilepton_edges:
                                print(f"[WARN] Unsupported dilepton distribution {flavor}.{var}; skipping")
                                continue
                            add_hist_counts(dilepton_store, (flavor, var, sample), values[var], dilepton_edges[var])

                selected_eff = selected_efficiency_branches(plot_cfg, modify_cfg, flavor)
                selected_event_eff = selected_event_efficiency_branches(plot_cfg, modify_cfg, flavor)
                selected_tnp_eff = selected_tnp_fit_branches(plot_cfg, modify_cfg, flavor)
                tag_branch = tnp_tag_id_branch(flavor)
                tag_cfg = tnp_tag_id_cfg(modify_cfg, flavor)
                tag_pass_in = pass_mask(arr_in[tag_branch], tag_cfg) if tag_branch in arr_in else ak.zeros_like(pt_in, dtype=bool)
                tag_pass_out = pass_mask(arr_out[tag_branch], tag_cfg) if tag_branch in arr_out else ak.zeros_like(pt_out, dtype=bool)
                tnp_base_in = tnp_probe_base(arr_in, br, tag_pass_in)
                tnp_base_out = tnp_probe_base(arr_out, br, tag_pass_out)

                for branch, ecfg in selected_eff.items():
                    if branch not in arr_in or branch not in arr_out:
                        continue
                    pass_in = pass_mask(arr_in[branch], ecfg)
                    pass_out = pass_mask(arr_out[branch], ecfg)
                    pass_in_matched = matched_object_values(pass_in, leading_in["event"], leading_in["index"]).astype(bool)
                    pass_out_matched = matched_object_values(pass_out, leading_out["event"], leading_out["index"]).astype(bool)
                    variables = eff_variables.get((flavor, branch), [])
                    for sample, leading, matched_pass in (
                        ("input", leading_in, pass_in_matched),
                        ("output", leading_out, pass_out_matched),
                    ):
                        values_by_var = {"pt": leading["pt"], "eta": leading["eta"], "phi": leading["phi"]}
                        for var in variables:
                            if var not in values_by_var or var not in eff_edges:
                                print(f"[WARN] Unsupported efficiency variable {flavor}.{branch}.{var}; skipping")
                                continue
                            add_efficiency_counts_flat(
                                eff_store,
                                (flavor, branch, sample, "mc_truth", var),
                                values_by_var[var],
                                leading["denom"],
                                matched_pass,
                                eff_edges[var],
                            )

                    if branch in selected_tnp_eff:
                        tnp_variables = selected_tnp_fit_variables(plot_cfg, variables)
                        tnp_in = tnp_probe_with_pass(tnp_base_in, pass_in)
                        tnp_out = tnp_probe_with_pass(tnp_base_out, pass_out)
                        add_tnp_mass_candidates(tnp_mass_store, (flavor, branch, "input", "tnp"), tnp_in, eff_edges, tnp_variables)
                        add_tnp_mass_candidates(tnp_mass_store, (flavor, branch, "output", "tnp"), tnp_out, eff_edges, tnp_variables)

                    base_map = base_maps.get((flavor, branch))
                    if base_map is not None:
                        exp_probs = distorted_probability_flat(modify_cfg, base_map, ecfg, leading_exp["pt"], leading_exp["eta"])
                        values_by_var = {"pt": leading_exp["pt"], "eta": leading_exp["eta"], "phi": leading_exp["phi"]}
                        values_in_by_var = {"pt": leading_in["pt"], "eta": leading_in["eta"], "phi": leading_in["phi"]}
                        for var in variables:
                            if var not in values_by_var or var not in eff_edges:
                                continue
                            if var in ("pt", "eta"):
                                add_expected_counts_flat(
                                    expected_eff_store,
                                    (flavor, branch, "expected", var),
                                    values_by_var[var],
                                    exp_probs,
                                    eff_edges[var],
                                    leading_exp["denom"],
                                )
                            elif var in values_in_by_var:
                                add_efficiency_counts_flat(
                                    expected_eff_store,
                                    (flavor, branch, "expected", var),
                                    values_in_by_var[var],
                                    leading_in["denom"],
                                    pass_in_matched,
                                    eff_edges[var],
                                )

                if selected_event_eff:
                    for branch, ecfg in selected_event_eff.items():
                        if branch not in arr_in or branch not in arr_out:
                            continue
                        pass_in_all = ak.to_numpy(pass_mask(arr_in[branch], ecfg)).astype(bool)
                        pass_out_all = ak.to_numpy(pass_mask(arr_out[branch], ecfg)).astype(bool)
                        pass_in_event = pass_in_all[leading_in["event"]]
                        pass_out_event = pass_out_all[leading_out["event"]]
                        variables = eff_variables.get((flavor, branch), [])
                        for sample, leading, passed in (
                            ("input", leading_in, pass_in_event),
                            ("output", leading_out, pass_out_event),
                        ):
                            values_by_var = {"pt": leading["pt"], "eta": leading["eta"], "phi": leading["phi"]}
                            for var in variables:
                                if var not in values_by_var or var not in eff_edges:
                                    print(f"[WARN] Unsupported event efficiency variable {flavor}.{branch}.{var}; skipping")
                                    continue
                                add_efficiency_counts_flat(
                                    eff_store,
                                    (flavor, branch, sample, "mc_truth", var),
                                    values_by_var[var],
                                    leading["denom"],
                                    passed,
                                    eff_edges[var],
                                )

                        if branch in selected_tnp_eff:
                            tnp_variables = selected_tnp_fit_variables(plot_cfg, variables)
                            tnp_in = tnp_event_probe_with_pass(tnp_base_in, pass_mask(arr_in[branch], ecfg))
                            tnp_out = tnp_event_probe_with_pass(tnp_base_out, pass_mask(arr_out[branch], ecfg))
                            add_tnp_mass_candidates(tnp_mass_store, (flavor, branch, "input", "tnp"), tnp_in, eff_edges, tnp_variables)
                            add_tnp_mass_candidates(tnp_mass_store, (flavor, branch, "output", "tnp"), tnp_out, eff_edges, tnp_variables)

                        base_map = base_maps.get((flavor, branch))
                        if base_map is not None and len(leading_exp["pt"]):
                            exp_probs = distorted_probability_flat(modify_cfg, base_map, ecfg, leading_exp["pt"], leading_exp["eta"])
                            values_by_var = {"pt": leading_exp["pt"], "eta": leading_exp["eta"], "phi": leading_exp["phi"]}
                            input_values_by_var = {"pt": leading_in["pt"], "eta": leading_in["eta"], "phi": leading_in["phi"]}
                            for var in variables:
                                if var not in values_by_var or var not in eff_edges:
                                    continue
                                if var in ("pt", "eta"):
                                    add_expected_counts_flat(
                                        expected_eff_store,
                                        (flavor, branch, "expected", var),
                                        values_by_var[var],
                                        exp_probs,
                                        eff_edges[var],
                                        leading_exp["denom"],
                                    )
                                elif var in input_values_by_var:
                                    add_efficiency_counts_flat(
                                        expected_eff_store,
                                        (flavor, branch, "expected", var),
                                        input_values_by_var[var],
                                        leading_in["denom"],
                                        pass_in_event,
                                        eff_edges[var],
                                    )
            progress_bucket = print_progress(progress_label, stop, input_tree.num_entries, progress_bucket)

    fit_dir = figdir / "efficiency" / "fit"
    print(f"[INFO] Fitting TnP pass/fail dilepton mass spectra with RooFit and writing fit plots to {fit_dir}")
    finalize_tnp_fits(eff_store, tnp_mass_store, fit_dir, eff_edges)

    print(f"[INFO] Writing plots to {figdir}")
    for flavor, variables in lepton_specs.items():
        for var in variables:
            if var not in hist_edges:
                continue
            plot_hist_comparison(
                figdir,
                f"distributions/lepton/dist_{flavor}_{var}.pdf",
                hist_store,
                (flavor, var),
                hist_edges[var],
                lepton_distribution_label(flavor, var),
                "A.U.",
                normalize=True,
            )

    for flavor, variables in dilepton_specs.items():
        for var in variables:
            if var not in dilepton_edges:
                continue
            plot_hist_comparison(
                figdir,
                f"distributions/dilepton/dilepton_{flavor}_{var}.pdf",
                dilepton_store,
                (flavor, var),
                dilepton_edges[var],
                dilepton_distribution_label(flavor, var),
                "Events",
                normalize=False,
            )

    plot_correlation_outputs(figdir, correlation_store, correlation_specs_by_flavor)

    for spec in eff_specs:
        flavor = spec["flavor"]
        branch = spec["branch"]
        for var in spec["variables"]:
            if var not in eff_edges:
                continue
            plot_efficiency(
                figdir,
                f"efficiency/eff_{flavor}_{sanitize(branch)}_{var}.pdf",
                eff_store,
                expected_eff_store,
                flavor,
                branch,
                var,
                eff_edges[var],
                efficiency_label(flavor, var),
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot NanoAOD modification validation figures.")
    parser.add_argument("--config-plot", "--config", default="config_plot.json", help="Plot configuration JSON")
    parser.add_argument("--figdir", default=None, help="Override output PDF directory")
    parser.add_argument("--chunk-size", type=int, default=100000, help="Events per chunk")
    args = parser.parse_args()

    plot_config_path = Path(args.config_plot)
    plot_cfg = load_config(plot_config_path)
    base_dir = plot_config_path.parent
    modify_config_path = resolve_path(plot_cfg.get("modify_config", "config.json"), base_dir)
    modify_cfg = load_config(modify_config_path)

    pairs = file_pairs(plot_cfg, modify_cfg, base_dir)
    if not pairs:
        raise SystemExit("No input/output ROOT file pairs found in config_plot.json")
    for src, dst in pairs:
        print(f"[INFO] Pair: {src} -> {dst}")

    figdir = Path(args.figdir) if args.figdir else resolve_path(plot_cfg.get("figures", "figures"), base_dir)
    analyze(modify_cfg, plot_cfg, pairs, figdir, args.chunk_size)


if __name__ == "__main__":
    main()
