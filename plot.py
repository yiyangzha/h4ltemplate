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
        "Missing Python dependency. Install/use an environment with uproot, awkward, numpy, and matplotlib."
    ) from exc

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BLUE = "#5790fc"
RED = "#e42536"
GRAY = "#9c9ca1"
Z_MASS = 91.1876
UINT64 = np.uint64
MASK64 = (1 << 64) - 1


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


def bin_edges(modify_cfg: Mapping, plot_cfg: Mapping) -> Dict[str, np.ndarray]:
    eff_binning = modify_cfg.get("efficiency", {}).get("binning", {})
    pt_edges = np.asarray(eff_binning.get("pt", [5, 10, 20, 30, 40, 50, 80, 120, 200]), dtype=float)
    abs_eta_edges = np.asarray(eff_binning.get("abs_eta", [0.0, 0.8, 1.2, 1.4442, 1.566, 2.0, 2.5]), dtype=float)
    signed_eta = sorted(set([-float(x) for x in abs_eta_edges[:0:-1]] + [float(x) for x in abs_eta_edges]))

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
    plt.rcParams.update(
        {
            "figure.figsize": (7.0, 6.0),
            "font.family": "DejaVu Sans",
            "font.size": 12,
            "axes.linewidth": 1.2,
            "axes.grid": False,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "legend.frameon": False,
            "savefig.bbox": "tight",
        }
    )


def add_cms_label(ax, right_text: str = "Simulation") -> None:
    ax.text(0.0, 1.02, "CMS", transform=ax.transAxes, fontsize=16, fontweight="bold", va="bottom")
    ax.text(0.13, 1.02, "Preliminary", transform=ax.transAxes, fontsize=12, va="bottom")
    ax.text(1.0, 1.02, right_text, transform=ax.transAxes, fontsize=12, ha="right", va="bottom")


def bin_index(values: np.ndarray, edges: np.ndarray) -> np.ndarray:
    idx = np.searchsorted(edges, values, side="right") - 1
    return np.clip(idx, 0, len(edges) - 2)


def flat_eff_bin(cfg: Mapping, pt: np.ndarray, eta: np.ndarray, energy: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    eff_binning = cfg.get("efficiency", {}).get("binning", {})
    pt_edges = np.asarray(eff_binning.get("pt", [5, 10, 20, 30, 40, 50, 80, 120, 200]), dtype=float)
    eta_edges = np.asarray(eff_binning.get("abs_eta", [0.0, 0.8, 1.2, 1.4442, 1.566, 2.0, 2.5]), dtype=float)
    energy_edges = eff_binning.get("energy")

    pt_bin = bin_index(pt, pt_edges)
    eta_bin = bin_index(np.abs(eta), eta_edges)
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
    return flat, pt_bin, eta_bin


def n_eff_bins(cfg: Mapping) -> int:
    eff_binning = cfg.get("efficiency", {}).get("binning", {})
    n_pt = len(eff_binning.get("pt", [5, 10, 20, 30, 40, 50, 80, 120, 200])) - 1
    n_eta = len(eff_binning.get("abs_eta", [0.0, 0.8, 1.2, 1.4442, 1.566, 2.0, 2.5])) - 1
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
    charge,
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
        prefix = flavor_prefix(flavor)
        requested.append(f"{prefix}_genPartIdx")
        requested.extend(selected_efficiency_branches(plot_cfg, cfg, flavor).keys())
        requested.extend(selected_event_efficiency_branches(plot_cfg, cfg, flavor).keys())
    requested.extend(event_id_branches(cfg).values())
    requested.extend(["GenPart_pdgId", "GenPart_statusFlags"])
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
        for start in range(0, tree.num_entries, chunk_size):
            stop = min(tree.num_entries, start + chunk_size)
            arrays = read_arrays(tree, requested, start, stop, f"{path} base-efficiency")
            for flavor in ("muon", "electron"):
                br = lepton_branches(cfg, flavor)
                if br["pt"] not in arrays or br["eta"] not in arrays:
                    continue
                pt = arrays[br["pt"]]
                eta = arrays[br["eta"]]
                flat_pt, _ = flatten_jagged(pt)
                flat_eta, _ = flatten_jagged(eta)
                energy = None
                if cfg.get("efficiency", {}).get("binning", {}).get("energy"):
                    if br.get("energy") and br["energy"] in arrays:
                        energy, _ = flatten_jagged(arrays[br["energy"]])
                    else:
                        energy = flat_pt * np.cosh(flat_eta)
                flat_bin, _, _ = flat_eff_bin(cfg, flat_pt, flat_eta, energy)
                for branch, ecfg in selected_efficiency_branches(plot_cfg, cfg, flavor).items():
                    if branch not in arrays:
                        continue
                    passed = ak.to_numpy(ak.flatten(pass_mask(arrays[branch], ecfg), axis=1)).astype(float)
                    maps[(flavor, branch)]["total"] += np.bincount(flat_bin, minlength=n_eff_bins(cfg))
                    maps[(flavor, branch)]["pass"] += np.bincount(flat_bin, weights=passed, minlength=n_eff_bins(cfg))

                for branch, ecfg in selected_event_efficiency_branches(plot_cfg, cfg, flavor).items():
                    if branch not in arrays:
                        continue
                    leading = leading_event_values(pt, eta, None)
                    if len(leading["pt"]) == 0:
                        continue
                    event_pass = ak.to_numpy(pass_mask(arrays[branch], ecfg)).astype(float)
                    valid_events = ak.to_numpy(ak.num(pt, axis=1) > 0).astype(bool)
                    passed = event_pass[valid_events]
                    event_bin, _, _ = flat_eff_bin(cfg, leading["pt"], leading["eta"])
                    maps[(flavor, branch)]["total"] += np.bincount(event_bin, minlength=n_eff_bins(cfg))
                    maps[(flavor, branch)]["pass"] += np.bincount(event_bin, weights=passed, minlength=n_eff_bins(cfg))
    return maps


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
    flat_bin, pt_bin, eta_bin = flat_eff_bin(cfg, flat_pt, flat_eta, flat_energy)
    passed = base_map["pass"][flat_bin]
    total = base_map["total"][flat_bin]
    global_total = float(np.sum(base_map["total"]))
    global_pass = float(np.sum(base_map["pass"]))
    global_eff = global_pass / global_total if global_total > 0 else 0.0
    base = np.where(total > 0, passed / np.maximum(total, 1.0), global_eff)

    distortion = branch_cfg.get("distortion", {})
    prob = base * float(distortion.get("global_factor", 1.0))
    eta_factors = distortion.get("eta_factors", [])
    if eta_factors:
        eta_arr = np.asarray(eta_factors, dtype=float)
        valid = eta_bin < len(eta_arr)
        prob = np.where(valid, prob * eta_arr[np.clip(eta_bin, 0, len(eta_arr) - 1)], prob)
    pt_factors = distortion.get("pt_factors", [])
    if pt_factors:
        pt_arr = np.asarray(pt_factors, dtype=float)
        valid = pt_bin < len(pt_arr)
        prob = np.where(valid, prob * pt_arr[np.clip(pt_bin, 0, len(pt_arr) - 1)], prob)
    bin_factors = distortion.get("bin_factors", [])
    if bin_factors:
        for ieta, row in enumerate(bin_factors):
            row_arr = np.asarray(row, dtype=float)
            for ipt, factor in enumerate(row_arr):
                prob = np.where((eta_bin == ieta) & (pt_bin == ipt), prob * factor, prob)

    pt_ref = float(distortion.get("pt_reference", cfg.get("scale", {}).get("pt_reference", 45.0)))
    prob *= 1.0 + float(distortion.get("pt_slope_log", 0.0)) * np.log(np.maximum(flat_pt, 1.0e-9) / max(pt_ref, 1.0e-9))
    prob = np.clip(np.where(np.isfinite(prob), prob, 0.0), 0.0, 1.0)
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
    flat_bin, pt_bin, eta_bin = flat_eff_bin(cfg, pt, eta)
    passed = base_map["pass"][flat_bin]
    total = base_map["total"][flat_bin]
    global_total = float(np.sum(base_map["total"]))
    global_pass = float(np.sum(base_map["pass"]))
    global_eff = global_pass / global_total if global_total > 0 else 0.0
    base = np.where(total > 0, passed / np.maximum(total, 1.0), global_eff)

    distortion = branch_cfg.get("distortion", {})
    prob = base * float(distortion.get("global_factor", 1.0))
    eta_factors = distortion.get("eta_factors", [])
    if eta_factors:
        eta_arr = np.asarray(eta_factors, dtype=float)
        valid = eta_bin < len(eta_arr)
        prob = np.where(valid, prob * eta_arr[np.clip(eta_bin, 0, len(eta_arr) - 1)], prob)
    pt_factors = distortion.get("pt_factors", [])
    if pt_factors:
        pt_arr = np.asarray(pt_factors, dtype=float)
        valid = pt_bin < len(pt_arr)
        prob = np.where(valid, prob * pt_arr[np.clip(pt_bin, 0, len(pt_arr) - 1)], prob)
    pt_ref = float(distortion.get("pt_reference", cfg.get("scale", {}).get("pt_reference", 45.0)))
    prob *= 1.0 + float(distortion.get("pt_slope_log", 0.0)) * np.log(np.maximum(pt, 1.0e-9) / max(pt_ref, 1.0e-9))
    return np.clip(np.where(np.isfinite(prob), prob, 0.0), 0.0, 1.0)


def mc_truth_mask(arrays: Mapping[str, ak.Array], flavor: str, pt_like):
    prefix = flavor_prefix(flavor)
    idx_name = f"{prefix}_genPartIdx"
    if idx_name not in arrays or "GenPart_pdgId" not in arrays:
        print(f"[WARN] Missing MC truth branches for {flavor}; using all reconstructed leptons as MC-truth denominator")
        return ak.ones_like(pt_like, dtype=bool)

    gen_idx = arrays[idx_name]
    gen_pdg = arrays["GenPart_pdgId"]
    gen_count = ak.num(gen_pdg, axis=1)
    valid = (gen_idx >= 0) & (gen_idx < gen_count)
    safe_idx = ak.where(valid, gen_idx, 0)
    padded_pdg = ak.pad_none(gen_pdg, 1, clip=False)
    matched_pdg = ak.fill_none(padded_pdg[safe_idx], 0)
    mask = valid & (abs(matched_pdg) == (13 if flavor == "muon" else 11))

    if "GenPart_statusFlags" in arrays:
        flags = ak.fill_none(ak.pad_none(arrays["GenPart_statusFlags"], 1, clip=False)[safe_idx], 0)
        prompt = ((flags & 1) != 0) | ((flags & (1 << 8)) != 0)
        mask = mask & prompt
    return mask


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
) -> None:
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
) -> None:
    if key not in store:
        store[key] = {"num": np.zeros(len(edges) - 1), "den": np.zeros(len(edges) - 1)}
    values = np.asarray(values, dtype=float)
    probabilities = np.asarray(probabilities, dtype=float)
    finite = np.isfinite(values) & np.isfinite(probabilities)
    store[key]["den"] += np.histogram(values[finite], bins=edges)[0]
    store[key]["num"] += np.histogram(values[finite], bins=edges, weights=probabilities[finite])[0]


def add_hist_counts(store: MutableMapping[Tuple, np.ndarray], key: Tuple, values, edges: np.ndarray) -> None:
    vals = to_numpy_flat(values)
    if key not in store:
        store[key] = np.zeros(len(edges) - 1)
    store[key] += np.histogram(vals, bins=edges)[0]


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


def tnp_probes(arrays: Mapping[str, ak.Array], br: Mapping[str, str], passed) -> Dict[str, np.ndarray]:
    required = [br.get("pt"), br.get("eta"), br.get("phi"), br.get("mass")]
    if any(name not in arrays for name in required):
        return {"pt": np.array([]), "eta": np.array([]), "phi": np.array([]), "pass": np.array([], dtype=bool)}

    pts = ak.to_list(arrays[br["pt"]])
    etas = ak.to_list(arrays[br["eta"]])
    phis = ak.to_list(arrays[br["phi"]])
    masses = ak.to_list(arrays[br["mass"]])
    charges = ak.to_list(arrays[br["charge"]]) if br.get("charge") in arrays else None
    passes = ak.to_list(passed)

    out = {"pt": [], "eta": [], "phi": [], "pass": []}
    for iev, event_pts in enumerate(pts):
        n = len(event_pts)
        if n < 2:
            continue
        best = None
        best_delta = None
        for i in range(n):
            for j in range(i + 1, n):
                if charges is not None and charges[iev][i] * charges[iev][j] >= 0:
                    continue
                mass, _, _, _ = system_kinematics(
                    (event_pts[i], etas[iev][i], phis[iev][i], masses[iev][i]),
                    (event_pts[j], etas[iev][j], phis[iev][j], masses[iev][j]),
                )
                if not (60.0 <= mass <= 120.0):
                    continue
                delta = abs(mass - Z_MASS)
                if best_delta is None or delta < best_delta:
                    best = (i, j)
                    best_delta = delta
        if best is None:
            continue
        i, j = best
        for tag, probe in ((i, j), (j, i)):
            if event_pts[tag] < 20.0 or not passes[iev][tag]:
                continue
            out["pt"].append(event_pts[probe])
            out["eta"].append(etas[iev][probe])
            out["phi"].append(phis[iev][probe])
            out["pass"].append(bool(passes[iev][probe]))
    return {key: np.asarray(value) for key, value in out.items()}


def tnp_event_probes(arrays: Mapping[str, ak.Array], br: Mapping[str, str], event_passed) -> Dict[str, np.ndarray]:
    required = [br.get("pt"), br.get("eta"), br.get("phi"), br.get("mass")]
    if any(name not in arrays for name in required):
        return {"pt": np.array([]), "eta": np.array([]), "phi": np.array([]), "pass": np.array([], dtype=bool)}

    pts = ak.to_list(arrays[br["pt"]])
    etas = ak.to_list(arrays[br["eta"]])
    phis = ak.to_list(arrays[br["phi"]])
    masses = ak.to_list(arrays[br["mass"]])
    charges = ak.to_list(arrays[br["charge"]]) if br.get("charge") in arrays else None
    event_pass = ak.to_numpy(event_passed).astype(bool)

    out = {"pt": [], "eta": [], "phi": [], "pass": []}
    for iev, event_pts in enumerate(pts):
        n = len(event_pts)
        if n < 2:
            continue
        best = None
        best_delta = None
        for i in range(n):
            for j in range(i + 1, n):
                if charges is not None and charges[iev][i] * charges[iev][j] >= 0:
                    continue
                mass, _, _, _ = system_kinematics(
                    (event_pts[i], etas[iev][i], phis[iev][i], masses[iev][i]),
                    (event_pts[j], etas[iev][j], phis[iev][j], masses[iev][j]),
                )
                if not (60.0 <= mass <= 120.0):
                    continue
                delta = abs(mass - Z_MASS)
                if best_delta is None or delta < best_delta:
                    best = (i, j)
                    best_delta = delta
        if best is None:
            continue
        for probe in best:
            out["pt"].append(event_pts[probe])
            out["eta"].append(etas[iev][probe])
            out["phi"].append(phis[iev][probe])
            out["pass"].append(bool(event_pass[iev]))
    return {key: np.asarray(value) for key, value in out.items()}


def add_tnp_efficiency(
    store: MutableMapping[Tuple, Dict[str, np.ndarray]],
    key_base: Tuple,
    probes: Mapping[str, np.ndarray],
    edges_by_var: Mapping[str, np.ndarray],
    variables: Sequence[str],
) -> None:
    for var in variables:
        edges = edges_by_var[var]
        key = key_base + (var,)
        if key not in store:
            store[key] = {"num": np.zeros(len(edges) - 1), "den": np.zeros(len(edges) - 1)}
        vals = probes[var]
        passed = probes["pass"].astype(float)
        finite = np.isfinite(vals)
        store[key]["den"] += np.histogram(vals[finite], bins=edges)[0]
        store[key]["num"] += np.histogram(vals[finite], bins=edges, weights=passed[finite])[0]


def leading_dilepton_values(pt, eta, phi, mass) -> Dict[str, np.ndarray]:
    pts = ak.to_list(pt)
    etas = ak.to_list(eta)
    phis = ak.to_list(phi)
    masses = ak.to_list(mass)
    out = {"mass": [], "pt": [], "eta": [], "phi": []}
    for iev, event_pts in enumerate(pts):
        if len(event_pts) < 2:
            continue
        order = sorted(range(len(event_pts)), key=lambda idx: event_pts[idx], reverse=True)
        i, j = order[0], order[1]
        values = system_kinematics(
            (event_pts[i], etas[iev][i], phis[iev][i], masses[iev][i]),
            (event_pts[j], etas[iev][j], phis[iev][j], masses[iev][j]),
        )
        for key, value in zip(("mass", "pt", "eta", "phi"), values):
            out[key].append(value)
    return {key: np.asarray(value) for key, value in out.items()}


def normalize_hist(counts: np.ndarray, edges: np.ndarray, normalize: bool) -> np.ndarray:
    if not normalize:
        return counts
    total = float(np.sum(counts))
    if total <= 0:
        return counts
    widths = np.diff(edges)
    return counts / (total * widths)


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
        "input": (BLUE, "-", "Input"),
        "expected": (GRAY, "--", "Expected"),
        "output": (RED, "-", "Output"),
    }
    for sample, (color, linestyle, label) in styles.items():
        counts = hist_store.get(key_base + (sample,), np.zeros(len(edges) - 1))
        values = normalize_hist(counts, edges, normalize)
        ax.step(edges, step_values(values), where="post", color=color, linestyle=linestyle, linewidth=1.8, label=label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    add_cms_label(ax)
    fig.savefig(figdir / filename)
    plt.close(fig)


def efficiency_values(counts: Mapping[str, np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
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
        ("input", "mc_truth", BLUE, "o", "Input MC truth"),
        ("input", "tnp", BLUE, "s", "Input TnP"),
        ("output", "mc_truth", RED, "o", "Output MC truth"),
        ("output", "tnp", RED, "s", "Output TnP"),
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
            label=label,
        )

    expected_key = (flavor, branch, "expected", var)
    if expected_key in expected_store:
        expected, _ = efficiency_values(expected_store[expected_key])
        valid = np.isfinite(expected)
        first_label = True
        for lo, hi, y, keep in zip(edges[:-1], edges[1:], expected, valid):
            if not keep:
                continue
            ax.hlines(
                y,
                lo,
                hi,
                colors=GRAY,
                linestyles="--",
                linewidth=1.8,
                label="Expected" if first_label else None,
            )
            first_label = False

    ax.set_xlabel(xlabel)
    ax.set_ylabel("A.U.")
    ax.set_ylim(0.0, 1.15)
    ax.legend(fontsize=10)
    add_cms_label(ax)
    fig.savefig(figdir / filename)
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
    labels = {
        "mass": f"{flavor} leading dilepton mass [GeV]",
        "pt": f"{flavor} leading dilepton pT [GeV]",
        "eta": f"{flavor} leading dilepton eta",
        "phi": f"{flavor} leading dilepton phi",
    }
    return labels.get(var, f"{flavor} leading dilepton {var}")


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
    flavors_to_process = set(lepton_specs) | set(dilepton_specs) | {item["flavor"] for item in eff_specs}

    print("[INFO] Stage A: learning one merged input efficiency map from all input ROOT files")
    base_maps = build_base_efficiency_maps(modify_cfg, plot_cfg, [src for src, _ in pairs], chunk_size)

    eff_store: Dict[Tuple, Dict[str, np.ndarray]] = {}
    expected_eff_store: Dict[Tuple, Dict[str, np.ndarray]] = {}
    hist_store: Dict[Tuple, np.ndarray] = {}
    dilepton_store: Dict[Tuple, np.ndarray] = {}

    requested = branch_requests(modify_cfg, plot_cfg)
    print("[INFO] Stage B: comparing all input/output ROOT pairs and merging them into common plots")
    for input_path, output_path in pairs:
        if not output_path.exists():
            raise RuntimeError(f"Expected output file does not exist: {output_path}")
        input_tree = open_tree(input_path, tree_name)
        output_tree = open_tree(output_path, tree_name)
        if input_tree.num_entries != output_tree.num_entries:
            raise RuntimeError(f"Entry mismatch: {input_path} has {input_tree.num_entries}, {output_path} has {output_tree.num_entries}")

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
                pt_in = arr_in[br["pt"]]
                eta_in = arr_in[br["eta"]]
                phi_in = arr_in[br["phi"]]
                mass_in = arr_in[br["mass"]]
                pt_out = arr_out[br["pt"]]
                eta_out = arr_out[br["eta"]]
                phi_out = arr_out[br["phi"]]
                mass_out = arr_out[br["mass"]]
                pt_exp, pt_scaled = expected_pt_arrays(modify_cfg, arr_in, flavor, start, pt_in, eta_in, charge_in)

                energy_in = awkward_energy(pt_in, eta_in, mass_in)
                energy_exp = awkward_energy(pt_exp, eta_in, mass_in)
                energy_out = awkward_energy(pt_out, eta_out, mass_out)
                rel_shift_in = ak.zeros_like(pt_in)
                rel_shift_exp = ak.where(pt_in > 0, pt_exp / pt_in - 1.0, np.nan)
                rel_shift_out = ak.where(pt_in > 0, pt_out / pt_in - 1.0, np.nan)
                smear_in = ak.zeros_like(pt_in)
                smear_exp = ak.where(pt_scaled > 0, (pt_exp - pt_scaled) / pt_scaled, np.nan)
                smear_out = ak.where(pt_scaled > 0, (pt_out - pt_scaled) / pt_scaled, np.nan)

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
                    for sample, pt, eta, phi, mass in (
                        ("input", pt_in, eta_in, phi_in, mass_in),
                        ("expected", pt_exp, eta_in, phi_in, mass_in),
                        ("output", pt_out, eta_out, phi_out, mass_out),
                    ):
                        values = leading_dilepton_values(pt, eta, phi, mass)
                        for var in dilepton_specs.get(flavor, []):
                            if var not in values or var not in dilepton_edges:
                                print(f"[WARN] Unsupported dilepton distribution {flavor}.{var}; skipping")
                                continue
                            add_hist_counts(dilepton_store, (flavor, var, sample), values[var], dilepton_edges[var])

                selected_eff = selected_efficiency_branches(plot_cfg, modify_cfg, flavor)
                selected_event_eff = selected_event_efficiency_branches(plot_cfg, modify_cfg, flavor)
                if selected_eff or selected_event_eff:
                    truth_in = mc_truth_mask(arr_in, flavor, pt_in)
                    truth_out = mc_truth_mask(arr_out, flavor, pt_out)

                for branch, ecfg in selected_eff.items():
                    if branch not in arr_in or branch not in arr_out:
                        continue
                    pass_in = pass_mask(arr_in[branch], ecfg)
                    pass_out = pass_mask(arr_out[branch], ecfg)
                    variables = eff_variables.get((flavor, branch), [])
                    for sample, truth, passed, pt, eta, phi in (
                        ("input", truth_in, pass_in, pt_in, eta_in, phi_in),
                        ("output", truth_out, pass_out, pt_out, eta_out, phi_out),
                    ):
                        values_by_var = {"pt": pt, "eta": eta, "phi": phi}
                        for var in variables:
                            if var not in values_by_var or var not in eff_edges:
                                print(f"[WARN] Unsupported efficiency variable {flavor}.{branch}.{var}; skipping")
                                continue
                            add_efficiency_counts(
                                eff_store,
                                (flavor, branch, sample, "mc_truth", var),
                                values_by_var[var],
                                truth,
                                passed,
                                eff_edges[var],
                            )

                    tnp_in = tnp_probes(arr_in, br, pass_in)
                    tnp_out = tnp_probes(arr_out, br, pass_out)
                    add_tnp_efficiency(eff_store, (flavor, branch, "input", "tnp"), tnp_in, eff_edges, variables)
                    add_tnp_efficiency(eff_store, (flavor, branch, "output", "tnp"), tnp_out, eff_edges, variables)

                    base_map = base_maps.get((flavor, branch))
                    if base_map is not None:
                        exp_probs = distorted_probability(modify_cfg, base_map, ecfg, pt_exp, eta_in)
                        values_by_var = {"pt": pt_exp, "eta": eta_in, "phi": phi_in}
                        for var in variables:
                            if var not in values_by_var or var not in eff_edges:
                                continue
                            add_expected_counts(
                                expected_eff_store,
                                (flavor, branch, "expected", var),
                                values_by_var[var],
                                exp_probs,
                                eff_edges[var],
                            )

                if selected_event_eff:
                    leading_in = leading_event_values(pt_in, eta_in, phi_in, truth_in)
                    leading_out = leading_event_values(pt_out, eta_out, phi_out, truth_out)
                    leading_exp = leading_event_values(pt_exp, eta_in, phi_in)
                    valid_in = ak.to_numpy(ak.num(pt_in, axis=1) > 0).astype(bool)
                    valid_out = ak.to_numpy(ak.num(pt_out, axis=1) > 0).astype(bool)
                    for branch, ecfg in selected_event_eff.items():
                        if branch not in arr_in or branch not in arr_out:
                            continue
                        pass_in_event = ak.to_numpy(pass_mask(arr_in[branch], ecfg)).astype(bool)[valid_in]
                        pass_out_event = ak.to_numpy(pass_mask(arr_out[branch], ecfg)).astype(bool)[valid_out]
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

                        tnp_in = tnp_event_probes(arr_in, br, pass_mask(arr_in[branch], ecfg))
                        tnp_out = tnp_event_probes(arr_out, br, pass_mask(arr_out[branch], ecfg))
                        add_tnp_efficiency(eff_store, (flavor, branch, "input", "tnp"), tnp_in, eff_edges, variables)
                        add_tnp_efficiency(eff_store, (flavor, branch, "output", "tnp"), tnp_out, eff_edges, variables)

                        base_map = base_maps.get((flavor, branch))
                        if base_map is not None and len(leading_exp["pt"]):
                            exp_probs = distorted_probability_flat(modify_cfg, base_map, ecfg, leading_exp["pt"], leading_exp["eta"])
                            values_by_var = {"pt": leading_exp["pt"], "eta": leading_exp["eta"], "phi": leading_exp["phi"]}
                            for var in variables:
                                if var not in values_by_var or var not in eff_edges:
                                    continue
                                add_expected_counts_flat(
                                    expected_eff_store,
                                    (flavor, branch, "expected", var),
                                    values_by_var[var],
                                    exp_probs,
                                    eff_edges[var],
                                )

    print(f"[INFO] Writing plots to {figdir}")
    for flavor, variables in lepton_specs.items():
        for var in variables:
            if var not in hist_edges:
                continue
            plot_hist_comparison(
                figdir,
                f"dist_{flavor}_{var}.pdf",
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
                f"dilepton_{flavor}_{var}.pdf",
                dilepton_store,
                (flavor, var),
                dilepton_edges[var],
                dilepton_distribution_label(flavor, var),
                "Events",
                normalize=False,
            )

    for spec in eff_specs:
        flavor = spec["flavor"]
        branch = spec["branch"]
        for var in spec["variables"]:
            if var not in eff_edges:
                continue
            plot_efficiency(
                figdir,
                f"eff_{flavor}_{sanitize(branch)}_{var}.pdf",
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
