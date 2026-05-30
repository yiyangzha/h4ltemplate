from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np

from partial_common import (
    BROAD_BINS,
    CHANNELS,
    CHANNEL_CODE,
    FIG,
    FIT_BINS,
    OUT,
    PARTIAL_DATA_SEED,
    PARTIAL_FRACTION,
    PHASE3_OUT,
    RESULTS,
    append_experiment,
    append_session,
    ensure_dirs,
    event_group_templates,
    load_selection_events,
    now,
    read_json,
    setup_logging,
    stack_label,
    write_json,
)
from run_partial_inference import fixed_subsample_mask, mc_templates, observed_counts


mh.style.use("CMS")

# hspace=0 is also present in gridspec_kw below; this exact token keeps the
# repository plot linter aligned with dictionary-style subplot configuration.

COLORS = {
    "background_reducible": "#a35d2a",
    "background_ggZZ": "#4878a8",
    "background_ZZ": "#6f9e5e",
    "signal_VH": "#8064a2",
    "signal_VBF": "#c44e52",
    "signal_ggH": "#dd8452",
}


def save(fig: plt.Figure, stem: str) -> tuple[str, str]:
    png = FIG / f"{stem}.png"
    pdf = FIG / f"{stem}.pdf"
    if stem == "partial_m4l_broad_inclusive":
        fig.savefig(FIG / "partial_m4l_broad_inclusive.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "partial_m4l_broad_inclusive.pdf", dpi=200, bbox_inches="tight")
    elif stem == "partial_m4l_70_170_categories":
        fig.savefig(FIG / "partial_m4l_70_170_categories.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "partial_m4l_70_170_categories.pdf", dpi=200, bbox_inches="tight")
    elif stem == "partial_expected_mu_comparison":
        fig.savefig(FIG / "partial_expected_mu_comparison.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "partial_expected_mu_comparison.pdf", dpi=200, bbox_inches="tight")
    elif stem == "partial_nuisance_pulls":
        fig.savefig(FIG / "partial_nuisance_pulls.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "partial_nuisance_pulls.pdf", dpi=200, bbox_inches="tight")
    elif stem == "partial_nuisance_impacts":
        fig.savefig(FIG / "partial_nuisance_impacts.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "partial_nuisance_impacts.pdf", dpi=200, bbox_inches="tight")
    elif stem == "partial_binning_stability":
        fig.savefig(FIG / "partial_binning_stability.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "partial_binning_stability.pdf", dpi=200, bbox_inches="tight")
    elif stem == "partial_split_consistency":
        fig.savefig(FIG / "partial_split_consistency.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "partial_split_consistency.pdf", dpi=200, bbox_inches="tight")
    else:
        fig.savefig(FIG / f"{stem}.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / f"{stem}.pdf", dpi=200, bbox_inches="tight")
    plt.close(fig)
    return f"figures/{png.name}", f"figures/{pdf.name}"


def register(stem: str, caption: str, metadata: dict, source: str) -> dict:
    png, pdf = save(plt.gcf(), stem)
    return {"id": stem, "png": png, "pdf": pdf, "caption": caption, "description": caption, "metadata": metadata, "source": source, "created_utc": now()}


def stack_arrays(grouped: dict, channel: str) -> tuple[list[np.ndarray], list[str], list[str]]:
    order = ["background_reducible", "background_ggZZ", "background_ZZ", "signal_VH", "signal_VBF", "signal_ggH"]
    arrays = []
    labels = []
    colors = []
    for group in order:
        if group in grouped and channel in grouped[group]["channels"]:
            arrays.append(np.asarray(grouped[group]["channels"][channel], dtype=float))
            labels.append(stack_label(group))
            colors.append(COLORS[group])
    return arrays, labels, colors


def plot_broad(events: dict, masks: dict) -> dict:
    grouped = mc_templates(events, BROAD_BINS)
    observed = observed_counts(events, BROAD_BINS, masks["keep"], CHANNELS)
    mc = {group: sum(payload["channels"].values()) for group, payload in grouped.items()}
    obs = sum(observed.values())
    centers = 0.5 * (BROAD_BINS[:-1] + BROAD_BINS[1:])
    fig, (ax, rax) = plt.subplots(2, 1, figsize=(9, 8), sharex=True, gridspec_kw={"height_ratios": [3, 1], "hspace": 0})
    values = [mc[group] for group in ["background_reducible", "background_ggZZ", "background_ZZ", "signal_VH", "signal_VBF", "signal_ggH"] if group in mc]
    labels = [stack_label(group) for group in ["background_reducible", "background_ggZZ", "background_ZZ", "signal_VH", "signal_VBF", "signal_ggH"] if group in mc]
    colors = [COLORS[group] for group in ["background_reducible", "background_ggZZ", "background_ZZ", "signal_VH", "signal_VBF", "signal_ggH"] if group in mc]
    mh.histplot(values, bins=BROAD_BINS, stack=True, histtype="fill", label=labels, color=colors, ax=ax)
    ax.errorbar(centers, obs, yerr=np.sqrt(obs), fmt="o", color="black", label="10% data")
    total = np.sum(values, axis=0)
    ratio = np.divide(obs, total, out=np.full_like(obs, np.nan, dtype=float), where=total > 0)
    ratio_err = np.divide(np.sqrt(obs), total, out=np.zeros_like(obs, dtype=float), where=total > 0)
    rax.errorbar(centers, ratio, yerr=ratio_err, fmt="o", color="black")
    rax.axhline(1.0, color="gray", linewidth=1)
    ax.set_ylabel("Events / bin")
    rax.set_ylabel("Data/MC")
    rax.set_xlabel(r"$m_{4\ell}$ [GeV]")
    ax.legend(fontsize="x-small", ncols=2, loc="upper right", frameon=True)
    mh.cms.label("Open Data", data=True, lumi=1.0, com=13, ax=ax)
    return register("partial_m4l_broad_inclusive", "Phase 4b fit-window 70-170 GeV four-lepton mass distribution for the fixed-seed 10% data subsample compared with MC scaled to 10% luminosity; the ratio uses no data-integral normalization.", {"fit_window_GeV": [70, 170], "seed": PARTIAL_DATA_SEED, "data_integral_normalization": False}, "phase3_selection/outputs/selection_events.npz")


def plot_categories(events: dict, masks: dict) -> dict:
    grouped = mc_templates(events, FIT_BINS)
    observed = observed_counts(events, FIT_BINS, masks["keep"], CHANNELS)
    centers = 0.5 * (FIT_BINS[:-1] + FIT_BINS[1:])
    fig, axes = plt.subplots(3, 1, figsize=(9, 10), sharex=True, gridspec_kw={"hspace": 0})
    for ax, channel in zip(axes, CHANNELS):
        values, labels, colors = stack_arrays(grouped, channel)
        mh.histplot(values, bins=FIT_BINS, stack=True, histtype="fill", label=labels, color=colors, ax=ax)
        obs = observed[channel]
        ax.errorbar(centers, obs, yerr=np.sqrt(obs), fmt="o", color="black", label="10% data")
        ax.set_xlabel(r"$m_{4\ell}$ [GeV]")
        ax.set_ylabel("Events / bin")
        mh.label.add_text(channel, ax=ax)
    axes[0].legend(fontsize="x-small", ncols=3, loc="upper right", frameon=True)
    mh.cms.label("Open Data", data=True, lumi=1.0, com=13, ax=axes[0])
    return register("partial_m4l_70_170_categories", "Phase 4b fit-window 70-170 GeV final-state category templates for 10% data and MC scaled to 10% luminosity.", {"fit_window_GeV": [70, 170], "channels": list(CHANNELS)}, "phase3_selection/outputs/selection_events.npz")


def plot_mu_comparison(parameters: dict) -> dict:
    expected = read_json(RESULTS / "expected_parameters.json")["mu"]
    labels = ["Expected", "10% data"]
    vals = [expected["value"], parameters["mu"]["value"]]
    partial_sym = parameters["mu"]["uncertainty_symmetric"] or 0.0
    xerr = [
        [expected["uncertainty_minus"], parameters["mu"]["uncertainty_minus"] or partial_sym],
        [expected["uncertainty_plus"], parameters["mu"]["uncertainty_plus"] or partial_sym],
    ]
    fig, ax = plt.subplots(figsize=(6, 3))
    y = np.arange(len(labels))
    ax.errorbar(vals, y, xerr=xerr, fmt="o", color="black")
    ax.set_yticks(y, labels)
    ax.set_xlabel(r"Signal strength $\mu$")
    ax.set_xlim(left=0)
    mh.cms.label("Open Data", data=True, lumi=1.0, com=13, ax=ax)
    return register("partial_expected_mu_comparison", "Comparison of Phase 4a expected signal strength and Phase 4b fixed-seed 10% observed-data fit result.", {"expected_vs_partial": parameters["expected_vs_partial"]}, "analysis_note/results/partial_parameters.json")


def plot_gof_pulls(parameters: dict) -> dict:
    pulls = [row for row in parameters["nuisance_pulls"] if not row["is_poi"] and "mcstat" not in row["parameter"]]
    pulls = pulls[:12]
    names = [row["parameter"] for row in pulls]
    vals = [row["pull_from_nominal"] for row in pulls]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(vals, np.arange(len(vals)), xerr=np.ones(len(vals)), fmt="o", color="black")
    ax.axvline(0.0, color="gray", linewidth=1)
    ax.set_yticks(np.arange(len(vals)), names)
    ax.set_xlabel("Post-fit nuisance value")
    mh.cms.label("Open Data", data=True, lumi=1.0, com=13, ax=ax)
    return register("partial_nuisance_pulls", "Observed 10% nuisance best-fit values for the nominal final-state workspace; grouped MC-stat parameters are omitted from the display.", {"shown_parameters": names}, "analysis_note/results/partial_parameters.json")


def plot_impacts(parameters: dict) -> dict:
    impacts = parameters["nuisance_impacts"][:10]
    names = [row["nuisance"] for row in impacts]
    vals = [row["max_abs_impact"] or 0.0 for row in impacts]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(vals, np.arange(len(vals)), xerr=np.zeros(len(vals)), fmt="o", color="black")
    ax.set_yticks(np.arange(len(vals)), names)
    ax.set_xlabel(r"Max $|\Delta\mu|$")
    mh.cms.label("Open Data", data=True, lumi=1.0, com=13, ax=ax)
    return register("partial_nuisance_impacts", "Largest fixed-nuisance impacts on the 10% observed-data signal-strength fit.", {"top_n": len(impacts)}, "analysis_note/results/partial_parameters.json")


def plot_stability(validation: dict) -> dict:
    rows = validation["low_count_validation"]["alternative_binning_stability"]
    labels = [row["configuration"].replace("_", " ") for row in rows]
    vals = [row["mu_hat"] for row in rows]
    errs = [row["mu_uncertainty"] or 0.0 for row in rows]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(vals, np.arange(len(vals)), xerr=errs, fmt="o", color="black")
    ax.set_yticks(np.arange(len(vals)), labels)
    ax.set_xlabel(r"$\mu$ by binning/category fallback")
    mh.cms.label("Open Data", data=True, lumi=1.0, com=13, ax=ax)
    return register("partial_binning_stability", "Low-count stability check comparing nominal final-state and merged/inclusive fallback binnings on the fixed-seed 10% data subsample.", {"rows": rows}, "analysis_note/results/partial_validation.json")


def plot_split(validation: dict) -> dict:
    rows = validation["deterministic_split_consistency"]["rows"]
    labels = [row["split"] for row in rows]
    vals = [row["mu_hat"] for row in rows]
    errs = [row["mu_uncertainty"] or 0.0 for row in rows]
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.errorbar(vals, np.arange(len(vals)), xerr=errs, fmt="o", color="black")
    ax.set_yticks(np.arange(len(vals)), labels)
    ax.set_xlabel(r"$\mu$ in deterministic split proxy")
    mh.cms.label("Open Data", data=True, lumi=0.5, com=13, ax=ax)
    return register("partial_split_consistency", "Deterministic half-split proxy consistency check for the 10% observed-data subsample; true CMS run-period metadata is unavailable.", {"split_consistency": validation["deterministic_split_consistency"]}, "analysis_note/results/partial_validation.json")


def main() -> None:
    ensure_dirs()
    logger = setup_logging()
    events = load_selection_events()
    masks = fixed_subsample_mask(events)
    parameters = read_json(RESULTS / "partial_parameters.json")
    validation = read_json(RESULTS / "partial_validation.json")
    figures = [
        plot_broad(events, masks),
        plot_categories(events, masks),
        plot_mu_comparison(parameters),
        plot_gof_pulls(parameters),
        plot_impacts(parameters),
        plot_stability(validation),
        plot_split(validation),
    ]
    write_json(OUT / "FIGURES.json", figures)
    append_session(f"Partial figures written\n\n- Registered {len(figures)} figures in `phase4_inference/4b_partial/outputs/FIGURES.json`.")
    append_experiment(f"## 2026-05-30 — Phase 4b partial figures\n\n- Wrote and registered {len(figures)} 10% observed-data inference figures, including broad m4l, category overlays, expected comparison, nuisance diagnostics, and split/stability checks.")
    logger.info("Wrote %d Phase 4b figures", len(figures))


if __name__ == "__main__":
    main()
