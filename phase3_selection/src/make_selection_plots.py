from __future__ import annotations

import numpy as np
from scipy.stats import chi2

from plot_utils import data_mc_comparison, save_and_register
from selection_common import (
    FINAL_STATE_LABELS,
    OUT,
    STACK_ORDER,
    VARIABLE_LABELS,
    append_experiment,
    append_session,
    read_json,
    setup_logging,
)


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
    made = 0
    for window, label in (("broad_window", "broad validation"), ("fit_window", "fit")):
        data, stacks, edges = mc_stack_from_fit(fit_inputs, window, "inclusive")
        fig = data_mc_comparison(edges, data, stacks, r"$m_{4\ell}$ [GeV]", "Events", r"$13$ TeV, 10 fb$^{-1}$")
        caption = (
            f"Inclusive four-lepton mass distribution in the {label} window. "
            "MC is normalized with prompt effective cross sections and Metadata denominators, while DY+jets remains the nominal fake proxy. "
            "The lower panel shows pulls and the fit-window version is the handoff input for downstream template fits."
        )
        save_and_register(fig, f"m4l_{window}_inclusive", caption, "phase3_selection/outputs/fit_inputs_s1.json", {"window": window, "category": "inclusive"})
        made += 1
    for channel in FINAL_STATE_LABELS:
        data, stacks, edges = mc_stack_from_fit(fit_inputs, "fit_window", channel)
        fig = data_mc_comparison(edges, data, stacks, r"$m_{4\ell}$ [GeV]", "Events", r"$13$ TeV, 10 fb$^{-1}$")
        caption = (
            f"Four-lepton mass distribution for the {channel} final-state category in `105 < m4l < 140 GeV`. "
            "These final-state categories are the nominal Phase 4 simultaneous-fit categories because the classifier split failed the promotion gates and no real VBF category is available."
        )
        save_and_register(fig, f"m4l_fit_{channel}", caption, "phase3_selection/outputs/fit_inputs_s1.json", {"window": "fit_window", "category": channel})
        made += 1
    return made


def plot_sidebands() -> int:
    sidebands = read_json(OUT / "sideband_fake_diagnostics.json")
    regions = ["low_sideband_70_105", "signal_window_105_140", "high_sideband_140_170"]
    x = np.arange(len(regions), dtype=float)
    fig = __import__("matplotlib.pyplot").pyplot.subplots(figsize=(10, 10))[0]
    ax = fig.axes[0]
    for sample, marker in (("DYJetsToLL.root", "o"), ("TTBar.root", "s")):
        y = np.array([sidebands["samples"][sample][region]["weighted_yield"] for region in regions], dtype=float)
        err = np.sqrt(np.array([sidebands["samples"][sample][region]["sumw2"] for region in regions], dtype=float))
        ax.errorbar(x, y, yerr=err, marker=marker, linestyle="-", label=sample.replace(".root", ""))
    ax.set_xticks(x, ["Low sideband", "Signal window", "High sideband"])
    ax.set_ylabel("Expected events")
    ax.set_xlabel("Region")
    ax.legend(loc="upper right", fontsize="x-small")
    __import__("mplhep").label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV, 10 fb$^{-1}$", ax=ax)
    caption = (
        "DY+jets and TTBar reducible-background diagnostics across the predeclared sideband and signal regions. "
        f"TTBar/DY ratios are {sidebands['ttbar_decision']['ratios_ttbar_over_dy']}, so TTBar is not promoted to the nominal fake model by the Phase 2 thresholds."
    )
    save_and_register(fig, "sideband_dy_ttbar_diagnostics", caption, "phase3_selection/outputs/sideband_fake_diagnostics.json", sidebands["ttbar_decision"])
    return 1


def plot_approach_and_mva() -> int:
    made = 0
    comparison = read_json(OUT / "approach_comparison.json")
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
    metrics = read_json(OUT / "mva_metrics.json")
    for model_name, model in metrics.get("models", {}).items():
        fig = __import__("matplotlib.pyplot").pyplot.subplots(figsize=(10, 10))[0]
        ax = fig.axes[0]
        roc = model["roc"]
        label_name = model_name.replace("_", " ")
        roc_label = "{} AUC={:.3f}".format(label_name, model["auc"])
        ax.plot(roc["fpr"], roc["tpr"], label=roc_label)
        ax.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random")
        ax.set_xlabel("Background efficiency")
        ax.set_ylabel("Signal efficiency")
        ax.legend(loc="lower right", fontsize="x-small")
        __import__("mplhep").label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV", ax=ax)
        caption = (
            f"{model_name} classifier ROC curve for the S2 attempt. "
            "The weak separation and failed category-viability gates prevent promotion to nominal Phase 4 categories."
        )
        save_and_register(fig, f"mva_roc_{model_name}", caption, "phase3_selection/outputs/mva_metrics.json", {"model": model_name})
        made += 1
    if (OUT / "mva_scores.npz").exists():
        scores = np.load(OUT / "mva_scores.npz", allow_pickle=True)
        events = np.load(OUT / "selection_events.npz", allow_pickle=True)
        best = scores["best_score"].astype(float)
        edges = np.linspace(0, 1, 11)
        is_data = events["is_data"].astype(bool)
        weights = events["weight"].astype(float)
        data, _ = np.histogram(best[is_data], bins=edges)
        mc, _ = np.histogram(best[~is_data], bins=edges, weights=weights[~is_data])
        fig = data_mc_comparison(edges, data, {"MC prediction": mc}, "Classifier score", "Events", r"$13$ TeV, broad window")
        caption = (
            "Best S2 classifier score data/MC comparison in the broad validation window. "
            "The score-shape gate and low-stat category viability failed, so this diagnostic is preserved as rejected-approach evidence rather than used in the nominal fit."
        )
        save_and_register(fig, "mva_best_score_datamc", caption, "phase3_selection/outputs/mva_scores.npz", {"best_model": str(scores["best_model"][0])})
        made += 1
    return made


def main() -> None:
    setup_logging()
    made = plot_m4l_windows()
    made += plot_sidebands()
    made += plot_approach_and_mva()
    append_session(f"2026-05-29 selection plots\n\n- Wrote {made} selection, sideband, and approach-comparison figures.")
    append_experiment(f"## 2026-05-29 — Phase 3 selection figures\n\n- Produced {made} selection/sideband/MVA diagnostic figures and updated `FIGURES.json`.")


if __name__ == "__main__":
    main()
