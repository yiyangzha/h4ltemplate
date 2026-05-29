from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import uproot

from selection_common import (
    BROAD_M4L_BINS,
    BROAD_WINDOW,
    FINAL_STATE_LABELS,
    FIT_WINDOW,
    HIGH_SIDEBAND,
    LOW_SIDEBAND,
    M4L_BINS,
    OUT,
    SAMPLE_INFO,
    append_experiment,
    append_session,
    ensure_dirs,
    final_state_from_pdgs,
    finite_all,
    hist_counts,
    in_range,
    leading,
    lepton_abs_eta_arrays,
    lepton_pt_arrays,
    now,
    poisson_sumw2,
    primary_files,
    sample_group,
    sample_stack,
    sample_weight,
    setup_logging,
    write_json,
)


LEPTON_BRANCHES = [
    f"l{i}{suffix}"
    for i in range(1, 5)
    for suffix in (
        "pt",
        "eta",
        "phi",
        "mass",
        "charge",
        "pdgId",
        "zId",
        "elCutBased",
        "elMvaWP80",
        "elMvaWP90",
        "muPF",
        "muMedium",
        "muTight",
        "muGlobal",
        "pfRelIso03",
        "miniRelIso",
        "sip3d",
    )
]
EVENT_BRANCHES = ["m4l", "mZ1", "mZ2", "pt4l", "eta4l", "phi4l", "y4l", "finalState", "trigBits", "nPV", "pvNdof"]
BRANCHES = EVENT_BRANCHES + LEPTON_BRANCHES
CUT_MOTIVATION_CUTS = [
    {
        "key": "trigger_bitmask_nonzero",
        "label": "Trigger bitmask",
        "denominator_step": "finite_core",
        "definition": "Events with trigBits != 0 divided by finite-core candidates.",
    },
    {
        "key": "flavor_matched_lepton_id",
        "label": "Flavor-matched lepton ID",
        "denominator_step": "valid_final_state",
        "definition": "Events passing flavor-matched electron/muon ID divided by valid final-state candidates.",
    },
    {
        "key": "z_pair_sanity",
        "label": "Z-pair sanity",
        "denominator_step": "flavor_matched_lepton_id",
        "definition": "Events passing retained Z-pair charge/flavor/mass sanity divided by flavor-ID-selected candidates.",
    },
]


def metadata_generated(root_file: uproot.ReadOnlyDirectory) -> float | None:
    if "Metadata" not in root_file:
        return None
    metadata = root_file["Metadata"]
    if "nEvents" not in metadata.keys():
        return None
    return float(np.sum(metadata["nEvents"].array(library="np")))


def tree_entries(root_file: uproot.ReadOnlyDirectory) -> dict[str, int]:
    entries = {}
    for key in root_file.keys():
        clean = key.split(";")[0]
        obj = root_file[key]
        if hasattr(obj, "num_entries"):
            entries[clean] = int(obj.num_entries)
    return entries


def branch_list(root_file: uproot.ReadOnlyDirectory) -> list[str]:
    return list(root_file["h4lTree"].keys())


def read_arrays(path: Path) -> dict[str, np.ndarray]:
    with uproot.open(path) as root_file:
        tree = root_file["h4lTree"]
        available = set(tree.keys())
        missing = sorted(set(BRANCHES) - available)
        if missing:
            raise RuntimeError(f"{path} missing required branches: {missing}")
        return tree.arrays(BRANCHES, library="np")


def id_mask(arrays: dict[str, np.ndarray]) -> np.ndarray:
    mask = np.ones(len(arrays["m4l"]), dtype=bool)
    for idx in range(1, 5):
        pdg = np.abs(arrays[f"l{idx}pdgId"]).astype(int)
        electron = pdg == 11
        muon = pdg == 13
        electron_ok = arrays[f"l{idx}elCutBased"].astype(int) >= 1
        muon_ok = (arrays[f"l{idx}muPF"].astype(int) == 1) & (arrays[f"l{idx}muMedium"].astype(int) == 1)
        mask &= (electron & electron_ok) | (muon & muon_ok)
    return mask


def z_sanity_mask(arrays: dict[str, np.ndarray]) -> np.ndarray:
    mask = (arrays["mZ1"] > 0) & (arrays["mZ2"] > 0)
    for zid in (1, 2):
        z_members = np.vstack([arrays[f"l{i}zId"].astype(int) == zid for i in range(1, 5)]).T
        charge = np.vstack([arrays[f"l{i}charge"].astype(int) for i in range(1, 5)]).T
        pdg = np.vstack([np.abs(arrays[f"l{i}pdgId"]).astype(int) for i in range(1, 5)]).T
        member_count = np.sum(z_members, axis=1)
        charge_sum = np.sum(np.where(z_members, charge, 0), axis=1)
        flavors = np.where(z_members, pdg, 0)
        flavor_sum = np.sum(flavors, axis=1)
        flavor_max = np.max(flavors, axis=1)
        same_flavor = flavor_sum == 2 * flavor_max
        mask &= (member_count == 2) & (charge_sum == 0) & same_flavor
    return mask


def masks(arrays: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    finite = finite_all(arrays, ["m4l", "mZ1", "mZ2", "pt4l", "eta4l", "y4l"] + LEPTON_BRANCHES)
    trigger = arrays["trigBits"].astype(int) != 0
    channel = np.isin(final_state_from_pdgs(arrays), FINAL_STATE_LABELS)
    obj_id = id_mask(arrays)
    z_sanity = z_sanity_mask(arrays)
    broad = in_range(arrays["m4l"].astype(float), *BROAD_WINDOW, right_inclusive=True)
    fit = in_range(arrays["m4l"].astype(float), *FIT_WINDOW)
    cumulative = {
        "all": np.ones(len(arrays["m4l"]), dtype=bool),
        "finite_core": finite,
        "trigger_bitmask_nonzero": finite & trigger,
        "valid_final_state": finite & trigger & channel,
        "flavor_matched_lepton_id": finite & trigger & channel & obj_id,
        "z_pair_sanity": finite & trigger & channel & obj_id & z_sanity,
        "broad_validation_window_70_170": finite & trigger & channel & obj_id & z_sanity & broad,
        "fit_window_105_140": finite & trigger & channel & obj_id & z_sanity & fit,
    }
    return cumulative


def event_features(arrays: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    pts = lepton_pt_arrays(arrays)
    abs_etas = lepton_abs_eta_arrays(arrays)
    return {
        "m4l": arrays["m4l"].astype(float),
        "mZ1": arrays["mZ1"].astype(float),
        "mZ2": arrays["mZ2"].astype(float),
        "pt4l": arrays["pt4l"].astype(float),
        "eta4l": arrays["eta4l"].astype(float),
        "y4l": arrays["y4l"].astype(float),
        "lead_lepton_pt": leading(pts, 0),
        "sublead_lepton_pt": leading(pts, 1),
        "lead_abs_eta": leading(abs_etas, 0),
        "sublead_abs_eta": leading(abs_etas, 1),
        "max_pf_rel_iso03": np.max(np.vstack([arrays[f"l{i}pfRelIso03"].astype(float) for i in range(1, 5)]).T, axis=1),
        "max_sip3d": np.max(np.vstack([arrays[f"l{i}sip3d"].astype(float) for i in range(1, 5)]).T, axis=1),
        "nPV": arrays["nPV"].astype(float),
        "pvNdof": arrays["pvNdof"].astype(float),
    }


def histogram_payload(
    name: str,
    arrays: dict[str, np.ndarray],
    selected: np.ndarray,
    channels: np.ndarray,
    weight: float,
    edges: np.ndarray,
) -> dict[str, Any]:
    payload = {}
    values = arrays["m4l"].astype(float)
    weights = np.full(len(values), weight, dtype=float)
    for category in ("inclusive", *FINAL_STATE_LABELS):
        cat_mask = selected if category == "inclusive" else selected & (channels == category)
        counts, sumw2 = hist_counts(values[cat_mask], weights[cat_mask], edges)
        payload[category] = {
            "counts": counts,
            "sumw2": sumw2,
            "raw_entries": int(np.sum(cat_mask)),
            "weighted_yield": float(np.sum(counts)),
            "sample": name,
            "group": sample_group(name),
            "stack": sample_stack(name),
        }
    return payload


def summarize_sidebands(name: str, arrays: dict[str, np.ndarray], selected_base: np.ndarray, weight: float) -> dict[str, float]:
    values = arrays["m4l"].astype(float)
    weights = np.full(len(values), weight, dtype=float)
    regions = {
        "low_sideband_70_105": selected_base & (values >= LOW_SIDEBAND[0]) & (values < LOW_SIDEBAND[1]),
        "signal_window_105_140": selected_base & (values > FIT_WINDOW[0]) & (values < FIT_WINDOW[1]),
        "high_sideband_140_170": selected_base & (values > HIGH_SIDEBAND[0]) & (values <= HIGH_SIDEBAND[1]),
    }
    return {
        region: {
            "raw_entries": int(np.sum(mask)),
            "weighted_yield": float(np.sum(weights[mask])),
            "sumw2": poisson_sumw2(weights[mask]),
        }
        for region, mask in regions.items()
    }


def cut_motivation_diagnostics(created: str, cutflow: dict[str, Any]) -> dict[str, Any]:
    accumulators: dict[str, dict[str, dict[str, dict[str, float | int]]]] = {}

    def ensure(process: str, channel: str, cut_key: str) -> dict[str, float | int]:
        return accumulators.setdefault(process, {}).setdefault(channel, {}).setdefault(
            cut_key,
            {
                "numerator_raw_entries": 0,
                "denominator_raw_entries": 0,
                "numerator_weighted_yield": 0.0,
                "denominator_weighted_yield": 0.0,
            },
        )

    def add(process: str, channel: str, cut_key: str, numerator: dict[str, Any], denominator: dict[str, Any]) -> None:
        slot = ensure(process, channel, cut_key)
        slot["numerator_raw_entries"] += int(numerator["raw_entries"])
        slot["denominator_raw_entries"] += int(denominator["raw_entries"])
        slot["numerator_weighted_yield"] += float(numerator["weighted_yield"])
        slot["denominator_weighted_yield"] += float(denominator["weighted_yield"])

    for sample, payload in cutflow["samples"].items():
        process = "Open data" if sample == "cms_10fb_13TeV.root" else sample_stack(sample)
        aggregate_processes = [process] if process == "Open data" else [process, "Open simulation total"]
        for channel in FINAL_STATE_LABELS:
            rows = {item["step"]: item for item in payload["by_channel"][channel]}
            for cut in CUT_MOTIVATION_CUTS:
                numerator = rows[cut["key"]]
                denominator = rows[cut["denominator_step"]]
                for aggregate_process in aggregate_processes:
                    add(aggregate_process, channel, cut["key"], numerator, denominator)

    def finalize(record: dict[str, float | int]) -> dict[str, Any]:
        denominator = float(record["denominator_weighted_yield"])
        efficiency = None if denominator <= 0.0 else float(record["numerator_weighted_yield"]) / denominator
        return {
            **record,
            "efficiency": efficiency,
            "undefined_reason": None if efficiency is not None else "zero denominator",
        }

    by_process = {
        process: {
            channel: {cut_key: finalize(record) for cut_key, record in cuts.items()}
            for channel, cuts in channels.items()
        }
        for process, channels in sorted(accumulators.items())
    }
    return {
        "created_utc": created,
        "cuts": CUT_MOTIVATION_CUTS,
        "channels": list(FINAL_STATE_LABELS),
        "efficiency_definition": "step weighted yield divided by the predeclared denominator-step weighted yield; data weights are one",
        "by_process": by_process,
        "data_mc_summary": {
            process: by_process[process]
            for process in ("Open data", "Open simulation total")
            if process in by_process
        },
    }


def main() -> None:
    ensure_dirs()
    log = setup_logging()
    created = now()
    provenance = {"created_utc": created, "files": [], "primary_paths_only_for_nominal": True}
    normalization = {"created_utc": created, "lumi_pb_user_prompt": 10_000.0, "records": []}
    cutflow: dict[str, Any] = {"created_utc": created, "steps": list(masks_stub()), "samples": {}}
    sidebands: dict[str, Any] = {"created_utc": created, "samples": {}, "ttbar_decision": {}}
    fit_inputs_s1: dict[str, Any] = {
        "created_utc": created,
        "approach": "S1_reference_like_cut_and_channel_fit",
        "fit_window": list(FIT_WINDOW),
        "bin_edges": M4L_BINS.tolist(),
        "broad_window_edges": BROAD_M4L_BINS.tolist(),
        "samples": {},
        "categories": ["inclusive", *FINAL_STATE_LABELS],
    }
    compact: dict[str, list[np.ndarray]] = defaultdict(list)
    compact_meta: list[dict[str, Any]] = []

    for file_info in primary_files():
        path = Path(file_info["path"])
        name = file_info["name"]
        log.info("Processing %s", name)
        with uproot.open(path) as root_file:
            generated = metadata_generated(root_file)
            entries = tree_entries(root_file)
            branches = branch_list(root_file)
        weight = sample_weight(name, generated)
        arrays = read_arrays(path)
        selected_masks = masks(arrays)
        channels = final_state_from_pdgs(arrays)
        features = event_features(arrays)
        final_mask = selected_masks["fit_window_105_140"]
        broad_mask = selected_masks["broad_validation_window_70_170"]

        provenance["files"].append(
            {
                "role": file_info["role"],
                "kind": file_info["kind"],
                "name": name,
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "tree_entries": entries,
                "metadata_generated_events": generated,
                "branch_count_h4lTree": len(branches),
                "jet_like_branches": [b for b in branches if "jet" in b.lower() or "vbf" in b.lower()],
                "used_for_nominal": True,
            }
        )
        normalization["records"].append(
            {
                "sample": name,
                "kind": file_info["kind"],
                "group": sample_group(name),
                "metadata_generated_events": generated,
                "xsec_pb_user_prompt": SAMPLE_INFO.get(name, {}).get("xsec_pb"),
                "lumi_pb_user_prompt": 10_000.0,
                "nominal_weight": weight,
                "expected_yield_before_detector_acceptance": None if name == "cms_10fb_13TeV.root" else SAMPLE_INFO[name]["xsec_pb"] * 10_000.0,
                "weight_formula": "sigma_eff_pb * L_pb / sum_Metadata_nEvents for MC; 1 for data",
            }
        )
        cutflow["samples"][name] = cutflow_record(arrays, selected_masks, channels, weight)
        sidebands["samples"][name] = summarize_sidebands(name, arrays, selected_masks["z_pair_sanity"], weight)
        fit_inputs_s1["samples"][name] = {
            "fit_window": histogram_payload(name, arrays, final_mask, channels, weight, M4L_BINS),
            "broad_window": histogram_payload(name, arrays, broad_mask, channels, weight, BROAD_M4L_BINS),
            "weight": weight,
            "group": sample_group(name),
            "stack": sample_stack(name),
        }

        keep = broad_mask
        for key, values in features.items():
            compact[key].append(values[keep].astype(float))
        compact["channel_code"].append(np.array([{"4mu": 0, "4e": 1, "2e2mu": 2}.get(v, -1) for v in channels[keep]], dtype=np.int16))
        compact["is_data"].append(np.full(np.sum(keep), name == "cms_10fb_13TeV.root", dtype=bool))
        compact["is_signal"].append(np.full(np.sum(keep), bool(SAMPLE_INFO.get(name, {}).get("is_signal", False)), dtype=bool))
        compact["weight"].append(np.full(np.sum(keep), weight, dtype=float))
        compact["sample_index"].append(np.full(np.sum(keep), len(compact_meta), dtype=np.int16))
        compact_meta.append({"sample": name, "group": sample_group(name), "stack": sample_stack(name), "weight": weight})

    sidebands["ttbar_decision"] = ttbar_decision(sidebands)
    cut_motivation = cut_motivation_diagnostics(created, cutflow)
    category_schema = {
        "created_utc": created,
        "nominal_categories": list(FINAL_STATE_LABELS),
        "inclusive_category_available_for_diagnostics": True,
        "vbf_label_used": False,
        "classifier_categories_promoted": False,
        "fit_window": list(FIT_WINDOW),
    }
    npz_payload = {key: np.concatenate(value) for key, value in compact.items()}
    npz_payload["sample_meta_json"] = np.array([str(compact_meta)], dtype=object)
    np.savez_compressed(OUT / "selection_events.npz", **npz_payload)
    write_json(OUT / "selection_provenance.json", provenance)
    write_json(OUT / "normalization.json", normalization)
    write_json(OUT / "cutflow.json", cutflow)
    write_json(OUT / "cut_motivation_diagnostics.json", cut_motivation)
    write_json(OUT / "sideband_fake_diagnostics.json", sidebands)
    write_json(OUT / "category_schema_s1.json", category_schema)
    write_json(OUT / "fit_inputs_s1.json", fit_inputs_s1)
    append_session(
        f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} selection table\n\n"
        "- Wrote Phase 3 provenance, normalization, cutflow, cut-motivation diagnostics, sideband diagnostics, "
        "S1 category schema, S1 fit inputs, and compact broad-window event arrays."
    )
    append_experiment(
        "## 2026-05-29 — Phase 3 baseline selection and provenance\n\n"
        "- Built Phase 3 primary-path provenance, MC normalization, cutflow, cut-motivation diagnostics, "
        "sideband diagnostics, S1 fit-ready histograms, and compact broad-window event arrays using primary prompt ROOT files only."
    )


def masks_stub() -> list[str]:
    return [
        "all",
        "finite_core",
        "trigger_bitmask_nonzero",
        "valid_final_state",
        "flavor_matched_lepton_id",
        "z_pair_sanity",
        "broad_validation_window_70_170",
        "fit_window_105_140",
    ]


def cutflow_record(arrays: dict[str, np.ndarray], selected_masks: dict[str, np.ndarray], channels: np.ndarray, weight: float) -> dict[str, Any]:
    record = {"all_channels": [], "by_channel": {}}
    previous = None
    for step in masks_stub():
        mask = selected_masks[step]
        raw = int(np.sum(mask))
        weighted = float(raw * weight)
        monotonic = True if previous is None else raw <= previous
        record["all_channels"].append({"step": step, "raw_entries": raw, "weighted_yield": weighted, "monotonic": monotonic})
        previous = raw
    for channel in FINAL_STATE_LABELS:
        record["by_channel"][channel] = []
        previous_channel = None
        channel_mask = channels == channel
        for step in masks_stub():
            mask = selected_masks[step] & channel_mask
            raw = int(np.sum(mask))
            monotonic = True if previous_channel is None else raw <= previous_channel
            record["by_channel"][channel].append(
                {"step": step, "raw_entries": raw, "weighted_yield": float(raw * weight), "monotonic": monotonic}
            )
            previous_channel = raw
    return record


def ttbar_decision(sidebands: dict[str, Any]) -> dict[str, Any]:
    dy = sidebands["samples"].get("DYJetsToLL.root", {})
    tt = sidebands["samples"].get("TTBar.root", {})
    ratios = {}
    promote = False
    for region in ("signal_window_105_140", "low_sideband_70_105", "high_sideband_140_170"):
        dy_yield = dy.get(region, {}).get("weighted_yield", 0.0)
        tt_yield = tt.get(region, {}).get("weighted_yield", 0.0)
        ratio = None if dy_yield <= 0 else tt_yield / dy_yield
        ratios[region] = ratio
        if region == "signal_window_105_140" and ratio is not None and ratio >= 0.10:
            promote = True
        if region != "signal_window_105_140" and ratio is not None and ratio >= 0.20:
            promote = True
    return {
        "ratios_ttbar_over_dy": ratios,
        "promote_ttbar_to_nominal": promote,
        "rule": "promote if TTBar/DY >= 10% in signal window or >= 20% in either sideband",
    }


if __name__ == "__main__":
    main()
