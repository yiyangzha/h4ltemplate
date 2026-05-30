from __future__ import annotations

import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np

from plot_utils import data_mc_comparison, save_and_register
from selection_common import (
    FINAL_STATE_LABELS,
    OUT,
    STACK_ORDER,
    VARIABLE_LABELS,
    append_experiment,
    append_session,
    hist_counts,
    model_display_name,
    read_json,
    sample_display_name,
    setup_logging,
    write_json,
)


def plot_cutflow_summary() -> int:
    cutflow = read_json(OUT / "cutflow.json")
    steps = cutflow["steps"]
    display_labels = {
        "all": "All",
        "finite_core": "Finite core",
        "trigger_bitmask_nonzero": "Trigger > 0",
        "valid_final_state": "Valid FS",
        "flavor_matched_lepton_id": "Flavor ID",
        "z_pair_sanity": "Z pairing",
        "broad_validation_window_70_170": "70-170",
        "fit_window_70_170": "70-170 fit",
    }
    y = np.arange(len(steps), dtype=float)[::-1]
    data_counts = []
    mc_weighted = []
    for step in steps:
        data_total = 0.0
        mc_total = 0.0
        for sample, payload in cutflow["samples"].items():
            row = next(item for item in payload["all_channels"] if item["step"] == step)
            if sample.startswith("cms_"):
                data_total += row["raw_entries"]
            else:
                mc_total += row["weighted_yield"]
        data_counts.append(data_total)
        mc_weighted.append(mc_total)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(data_counts, y, marker="o", color="black", label="Data raw events")
    ax.plot(mc_weighted, y, marker="s", color="#0072B2", label="MC weighted yield")
    ax.set_yticks(y, [display_labels.get(step, step) for step in steps])
    ax.set_xlabel("Events")
    ax.set_ylabel("Cumulative selection step")
    ax.set_xscale("log")
    visible_top = max(max(data_counts), max(mc_weighted))
    if visible_top > 0.0:
        ax.set_xlim(right=visible_top * 2.5)
    ax.legend(loc="lower right", fontsize="x-small")
    mh.label.exp_label(
        exp="CMS",
        text="",
        loc=2,
        data=True,
        llabel="Open Data and Open Simulation",
        rlabel=r"$13$ TeV, 10 fb$^{-1}$",
        ax=ax,
    )
    caption = (
        "Cumulative Phase 3 cutflow for data raw counts and prompt-normalized MC weighted yields. "
        "The rendered step labels are abbreviated for readability; `70-170 fit` is the current Phase 4c fit window. "
        "Every sample-level cutflow is monotonic, and the fit-window endpoint is computed from the active 70-170 GeV selection."
    )
    metadata = {
        "steps": steps,
        "display_labels": {step: display_labels.get(step, step) for step in steps},
        "endpoint": {"data_raw": data_counts[-1], "mc_weighted": mc_weighted[-1]},
    }
    save_and_register(
        fig,
        "cutflow_summary",
        caption,
        "phase3_selection/outputs/cutflow.json",
        metadata,
    )
    return 1


def plot_cut_motivation() -> int:
    diagnostics = read_json(OUT / "cut_motivation_diagnostics.json")
    summary = diagnostics["data_mc_summary"]
    rows = []
    labels = []
    for cut in diagnostics["cuts"]:
        cut_key = cut["key"]
        short_label = {
            "trigger_bitmask_nonzero": "Trigger",
            "flavor_matched_lepton_id": "Lepton ID",
            "z_pair_sanity": "Z pairing",
        }.get(cut_key, cut["label"])
        for channel in diagnostics["channels"]:
            labels.append(f"{short_label} {channel}")
            rows.append(
                (
                    summary.get("Open data", {}).get(channel, {}).get(cut_key, {}).get("efficiency"),
                    summary.get("Open simulation total", {}).get(channel, {}).get(cut_key, {}).get("efficiency"),
                )
            )
    y = np.arange(len(rows), dtype=float)[::-1]
    data_eff = np.asarray([np.nan if item[0] is None else item[0] for item in rows], dtype=float)
    mc_eff = np.asarray([np.nan if item[1] is None else item[1] for item in rows], dtype=float)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.errorbar(data_eff, y, marker="o", linestyle="None", color="black", label="Open data")
    ax.errorbar(mc_eff, y, marker="s", linestyle="None", color="#0072B2", label="Open simulation")
    ax.set_yticks(y, labels)
    ax.set_xlim(0.0, 1.08)
    ax.set_xlabel("Step efficiency")
    ax.set_ylabel("Cut and final state")
    ax.legend(loc="lower left", fontsize="x-small")
    mh.label.exp_label(
        exp="CMS",
        text="",
        loc=2,
        data=True,
        llabel="Open Data and Open Simulation",
        rlabel=r"$13$ TeV, 10 fb$^{-1}$",
        ax=ax,
    )
    caption = (
        "Trigger, flavor-matched lepton-ID, and Z-pair sanity efficiencies by final state. "
        "Efficiencies are ratios to the previous predeclared selection step; data uses raw events and MC uses prompt-normalized weighted yields."
    )
    save_and_register(
        fig,
        "cut_motivation_efficiencies",
        caption,
        "phase3_selection/outputs/cut_motivation_diagnostics.json",
        {"cuts": diagnostics["cuts"], "channels": diagnostics["channels"]},
    )
    return 1


def mc_stack_from_fit(fit_inputs: dict, window: str, category: str) -> tuple[np.ndarray, dict[str, np.ndarray], np.ndarray]:
    data_counts = None
    stacks = {name: None for name in STACK_ORDER}
    edges = np.asarray(fit_inputs["bin_edges" if window == "fit_window" else "broad_window_edges"], dtype=float)
    for sample_payload in fit_inputs["samples"].values():
        item = sample_payload[window][category]
        counts = np.asarray(item["counts"], dtype=float)
        stack = item["stack"]
        if stack == "Data":
            data_counts = counts
        elif stack in stacks:
            stacks[stack] = counts if stacks[stack] is None else stacks[stack] + counts
    return data_counts if data_counts is not None else np.zeros(len(edges) - 1), {k: v for k, v in stacks.items() if v is not None}, edges


def plot_m4l_windows() -> int:
    fit_inputs = read_json(OUT / "fit_inputs_s1.json")
    comparison = read_json(OUT / "approach_comparison.json")
    s1_viability = comparison["approaches"]["S1_reference_like_cut_and_channel_fit"]["final_state_bin_viability"]
    made = 0
    for window, label in (("broad_window", "broad validation"), ("fit_window", "fit")):
        data, stacks, edges = mc_stack_from_fit(fit_inputs, window, "inclusive")
        fig = data_mc_comparison(
            edges,
            data,
            stacks,
            r"$m_{4\ell}$ [GeV]",
            "Events",
            r"$13$ TeV, 10 fb$^{-1}$",
            legend_loc="center right",
        )
        caption = (
            f"Inclusive four-lepton mass distribution in the {label} window. "
            "MC is normalized with prompt effective cross sections and Metadata denominators, while DY+jets remains the nominal fake proxy. "
            "The lower panel shows pulls and the fit-window version is the handoff input for downstream template fits."
        )
        save_and_register(fig, f"m4l_{window}_inclusive", caption, "phase3_selection/outputs/fit_inputs_s1.json", {"window": window, "category": "inclusive"})
        made += 1
    for channel in FINAL_STATE_LABELS:
        data, stacks, edges = mc_stack_from_fit(fit_inputs, "fit_window", channel)
        fig = data_mc_comparison(
            edges,
            data,
            stacks,
            r"$m_{4\ell}$ [GeV]",
            "Events",
            r"$13$ TeV, 10 fb$^{-1}$",
            legend_loc="center right",
        )
        caption = (
            f"Four-lepton mass distribution for the {channel} final-state category in `70 < m4l < 170 GeV`. "
            "These final-state categories are the conditional Phase 4 simultaneous-fit handoff because the classifier split failed the promotion gates and no real VBF category is available; "
            "Phase 4 must validate low-count Poisson/toy behavior and MC-stat stability before reporting fit results."
        )
        save_and_register(
            fig,
            f"m4l_fit_{channel}",
            caption,
            "phase3_selection/outputs/fit_inputs_s1.json",
            {"window": "fit_window", "category": channel, "low_count_evidence": s1_viability["by_category"][channel]},
        )
        made += 1
    return made


def plot_sidebands() -> int:
    sidebands = read_json(OUT / "sideband_fake_diagnostics.json")
    regions = ["low_sideband_70_105", "higgs_peak_control_105_140", "high_sideband_140_170"]
    x = np.arange(len(regions), dtype=float)
    fig = __import__("matplotlib.pyplot").pyplot.subplots(figsize=(10, 10))[0]
    ax = fig.axes[0]
    for sample, marker in (("DYJetsToLL.root", "o"), ("TTBar.root", "s")):
        y = np.array([sidebands["samples"][sample][region]["weighted_yield"] for region in regions], dtype=float)
        err = np.sqrt(np.array([sidebands["samples"][sample][region]["sumw2"] for region in regions], dtype=float))
        ax.errorbar(x, y, yerr=err, marker=marker, linestyle="-", label=sample_display_name(sample))
    ax.set_xticks(x, ["Low sideband", "Higgs-peak control", "High sideband"])
    ax.set_ylabel("Expected events")
    ax.set_xlabel("Region")
    ax.legend(loc="upper right", fontsize="x-small")
    __import__("mplhep").label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV, 10 fb$^{-1}$", ax=ax)
    caption = (
        "DY+jets fake proxy and TTBar diagnostic reducible-background checks across the predeclared sideband and Higgs-peak control regions. "
        f"TTBar diagnostic / DY+jets fake-proxy ratios are {sidebands['ttbar_decision']['ratios_ttbar_over_dy']}, so TTBar is not promoted to the nominal fake model by the Phase 2 thresholds."
    )
    save_and_register(fig, "sideband_dy_ttbar_diagnostics", caption, "phase3_selection/outputs/sideband_fake_diagnostics.json", sidebands["ttbar_decision"])
    return 1


def plot_angular_closure() -> int:
    closure = read_json(OUT / "angular_closure.json")
    quantities = ["m4l", "mZ1", "mZ2"]
    max_medians = []
    for quantity in quantities:
        max_medians.append(max(item["median_abs_diff_GeV"][quantity] for item in closure["samples"]))
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.errorbar(np.arange(len(quantities)), max_medians, marker="o", linestyle="None", color="#009E73", label="Observed closure")
    ax.axhline(0.1, color="#D55E00", linestyle="--", label="0.1 GeV gate")
    ax.set_xticks(np.arange(len(quantities)), [r"$m_{4\ell}$", r"$m_{Z1}$", r"$m_{Z2}$"])
    ax.set_ylabel("Max sample median absolute difference [GeV]")
    ax.set_xlabel("Recomputed quantity")
    ax.set_yscale("log")
    ax.legend(loc="upper right", fontsize="x-small")
    mh.label.exp_label(
        exp="CMS",
        text="",
        loc=2,
        data=True,
        llabel="Open Data and Open Simulation",
        rlabel=r"$13$ TeV",
        ax=ax,
    )
    caption = (
        "Angular reconstruction closure summary showing the maximum per-sample median absolute mass difference for recomputed four-vector quantities. "
        "All medians are far below the 0.1 GeV closure gate and all angular physical-range checks have zero out-of-range entries."
    )
    save_and_register(fig, "angular_closure_median_deltas", caption, "phase3_selection/outputs/angular_closure.json", {"overall_pass": closure["overall_pass"]})
    return 1


def plot_vbf_downscope_evidence() -> int:
    evidence = read_json(OUT / "vbf_recovery_downscope.json")
    checks = evidence["primary_and_local_branch_checks"]
    checked_files = len(checks)
    files_with_jet_vbf = sum(1 for item in checks if item["jet_or_vbf_like_branches"])
    allowed_upstream = len(evidence["join_check"]["allowed_upstream_sources"])
    safe_join = int(evidence["join_check"]["safe_event_key_join_possible"])
    values = [checked_files, files_with_jet_vbf, allowed_upstream, safe_join]
    labels = ["ROOT files\nchecked", "Files with\njet/VBF branches", "Allowed upstream\njoin sources", "Safe event-key\njoin"]
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.errorbar(np.arange(len(values)), values, marker="o", linestyle="None", color="black")
    ax.set_xticks(np.arange(len(values)), labels)
    ax.set_ylabel("Count")
    ax.set_xlabel("VBF recovery evidence")
    visible_top = max(values)
    if visible_top > 0:
        ax.set_ylim(top=visible_top * 1.55)
    mh.label.exp_label(
        exp="CMS",
        text="",
        loc=2,
        data=True,
        llabel="Open Data and Open Simulation",
        rlabel=r"$13$ TeV",
        ax=ax,
    )
    caption = (
        "VBF recovery and downscope evidence from branch inventories and allowed join sources. "
        "No checked flat ntuple contains real jet or VBF discriminator branches, no allowed upstream join source exists, and no lepton-only category is labeled VBF."
    )
    save_and_register(fig, "vbf_downscope_evidence", caption, "phase3_selection/outputs/vbf_recovery_downscope.json", {"decision": evidence["decision"]})
    return 1


def plot_category_viability() -> int:
    comparison = read_json(OUT / "approach_comparison.json")
    viability = comparison["approaches"]["S1_reference_like_cut_and_channel_fit"]["final_state_bin_viability"]
    low_summary = viability["summary"]
    channels = FINAL_STATE_LABELS
    signal = []
    background = []
    data = []
    for channel in channels:
        item = viability["by_category"][channel]
        signal.append(float(np.sum(item["signal_expected_by_bin"])))
        background.append(float(np.sum(item["background_expected_by_bin"])))
        data.append(float(np.sum(item["data_observed_by_bin"])))
    x = np.arange(len(channels), dtype=float)
    width = 0.25
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.errorbar(x - width, signal, marker="s", linestyle="None", color="#009E73", label="Signal")
    ax.errorbar(x, background, marker="^", linestyle="None", color="#0072B2", label="Background")
    ax.errorbar(x + width, data, yerr=np.sqrt(data), marker="o", linestyle="None", color="black", label="Data")
    ax.set_xticks(x, channels)
    ax.set_ylabel("Events in 70 < m4l < 170 GeV")
    ax.set_xlabel("Final-state category")
    visible_top = max(max(signal), max(background), max(np.asarray(data) + np.sqrt(data)))
    if visible_top > 0.0:
        ax.set_ylim(top=visible_top * 1.35)
    ax.legend(loc="upper right", fontsize="x-small")
    mh.label.exp_label(
        exp="CMS",
        text="",
        loc=2,
        data=True,
        llabel="Open Data and Open Simulation",
        rlabel=r"$13$ TeV, 10 fb$^{-1}$",
        ax=ax,
    )
    caption = (
        "S1 final-state category viability summary for the broad MVA comparison window. "
        f"The categories are retained only as a conditional Phase 4 handoff: {low_summary['final_state_bins_below_5_expected']}/"
        f"{low_summary['final_state_total_bins']} final-state bins have S+B below five expected events, while S2 classifier categories fail low-stat viability."
    )
    save_and_register(
        fig,
        "category_viability_s1",
        caption,
        "phase3_selection/outputs/approach_comparison.json",
        {"channels": channels, "low_count_summary": low_summary},
    )
    return 1


def plot_approach_and_mva() -> int:
    made = 0
    comparison = read_json(OUT / "approach_comparison.json")
    metrics = read_json(OUT / "mva_metrics.json")
    active_roc_ids = {f"mva_roc_{model_name}" for model_name in metrics.get("models", {})}
    registry_path = OUT / "FIGURES.json"
    if registry_path.exists():
        registry = read_json(registry_path)
        kept = []
        for item in registry:
            if item["id"].startswith("mva_roc_") and item["id"] not in active_roc_ids:
                for key in ("png", "pdf"):
                    stale = OUT / item[key]
                    if stale.exists():
                        stale.unlink()
                continue
            kept.append(item)
        write_json(registry_path, kept)
    fig = __import__("matplotlib.pyplot").pyplot.subplots(figsize=(10, 10))[0]
    ax = fig.axes[0]
    labels = ["S1", "S2 best split"]
    values = [
        comparison["approaches"]["S1_reference_like_cut_and_channel_fit"]["asimov_mu_uncertainty_proxy"],
        comparison["approaches"]["S2_angular_kinematic_classifier_categories"]["best_high_score_mu_uncertainty_proxy"],
    ]
    ax.errorbar(np.arange(2), values, marker="o", linestyle="None", color="black")
    ax.set_xticks(np.arange(2), labels)
    ax.set_ylabel(r"Expected $\mu$ uncertainty proxy")
    ax.set_xlabel("Selection approach")
    __import__("mplhep").label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV", ax=ax)
    caption = (
        "S1 and S2 approach comparison using the common Asimov counting precision proxy. "
        f"The nominal choice is `{comparison['selected_configuration']}` because {comparison['selection_reason']}"
    )
    save_and_register(fig, "approach_comparison_mu_proxy", caption, "phase3_selection/outputs/approach_comparison.json", comparison)
    made += 1
    for model_name, model in metrics.get("models", {}).items():
        fig = __import__("matplotlib.pyplot").pyplot.subplots(figsize=(10, 10))[0]
        ax = fig.axes[0]
        roc = model["roc"]
        label_name = model_display_name(model_name)
        roc_label = "{} AUC={:.3f}".format(label_name, model["auc"])
        ax.plot(roc["fpr"], roc["tpr"], label=roc_label)
        ax.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random")
        ax.set_xlabel("Background efficiency")
        ax.set_ylabel("Signal efficiency")
        ax.legend(loc="lower right", fontsize="x-small")
        __import__("mplhep").label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV", ax=ax)
        caption = (
            f"{label_name} classifier ROC curve for the S2 attempt. "
            "The repaired classifier has useful separation, but score-shape, mass-sculpting, or low-stat category gates prevent promotion to nominal Phase 4 categories."
        )
        save_and_register(
            fig,
            f"mva_roc_{model_name}",
            caption,
            "phase3_selection/outputs/mva_metrics.json",
            {"model": model_name, "model_label": label_name},
        )
        made += 1
    if (OUT / "mva_scores.npz").exists():
        scores = np.load(OUT / "mva_scores.npz", allow_pickle=True)
        events = np.load(OUT / "selection_events.npz", allow_pickle=True)
        best = scores["best_score"].astype(float)
        edges = np.linspace(0, 1, 11)
        is_data = events["is_data"].astype(bool)
        weights = events["weight"].astype(float)
        data, _ = hist_counts(best[is_data], np.ones(np.sum(is_data), dtype=float), edges)
        mc, _ = hist_counts(best[~is_data], weights[~is_data], edges)
        fig = data_mc_comparison(edges, data, {"MC prediction": mc}, "Classifier score", "Events", r"$13$ TeV, 10 fb$^{-1}$")
        caption = (
            "Best S2 classifier score data/MC comparison in the broad validation window. "
            "The score-shape gate and low-stat category viability failed, so this diagnostic is preserved as rejected-approach evidence rather than used in the nominal fit."
        )
        best_model = str(scores["best_model"][0])
        save_and_register(
            fig,
            "mva_best_score_datamc",
            caption,
            "phase3_selection/outputs/mva_scores.npz",
            {"best_model": best_model, "best_model_label": model_display_name(best_model)},
        )
        made += 1
    return made


def main() -> None:
    setup_logging()
    made = plot_cutflow_summary()
    made += plot_cut_motivation()
    made += plot_m4l_windows()
    made += plot_sidebands()
    made += plot_angular_closure()
    made += plot_vbf_downscope_evidence()
    made += plot_category_viability()
    made += plot_approach_and_mva()
    append_session(f"2026-05-29 selection plots\n\n- Wrote {made} selection, sideband, and approach-comparison figures.")
    append_experiment(f"## 2026-05-29 — Phase 3 selection figures\n\n- Produced {made} selection/sideband/MVA diagnostic figures and updated `FIGURES.json`.")


if __name__ == "__main__":
    main()
