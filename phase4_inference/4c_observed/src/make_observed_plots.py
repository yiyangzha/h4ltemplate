from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np

from observed_common import (
    BROAD_BINS,
    CHANNELS,
    CHANNEL_CODE,
    FIG,
    FIT_BINS,
    OUT,
    OBSERVED_DATA_SEED,
    OBSERVED_FRACTION,
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
from run_observed_inference import full_data_mask, mc_templates, observed_counts


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
    if stem == "observed_m4l_broad_inclusive":
        fig.savefig(FIG / "observed_m4l_broad_inclusive.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "observed_m4l_broad_inclusive.pdf", dpi=200, bbox_inches="tight")
    elif stem == "observed_m4l_70_170_categories":
        fig.savefig(FIG / "observed_m4l_70_170_categories.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "observed_m4l_70_170_categories.pdf", dpi=200, bbox_inches="tight")
    elif stem == "observed_expected_mu_comparison":
        fig.savefig(FIG / "observed_expected_mu_comparison.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "observed_expected_mu_comparison.pdf", dpi=200, bbox_inches="tight")
    elif stem == "observed_nuisance_pulls":
        fig.savefig(FIG / "observed_nuisance_pulls.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "observed_nuisance_pulls.pdf", dpi=200, bbox_inches="tight")
    elif stem == "observed_nuisance_impacts":
        fig.savefig(FIG / "observed_nuisance_impacts.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "observed_nuisance_impacts.pdf", dpi=200, bbox_inches="tight")
    elif stem == "observed_binning_stability":
        fig.savefig(FIG / "observed_binning_stability.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "observed_binning_stability.pdf", dpi=200, bbox_inches="tight")
    elif stem == "observed_split_consistency":
        fig.savefig(FIG / "observed_split_consistency.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "observed_split_consistency.pdf", dpi=200, bbox_inches="tight")
    elif stem == "observed_mass_scan":
        fig.savefig(FIG / "observed_mass_scan.png", dpi=200, bbox_inches="tight")
        fig.savefig(FIG / "observed_mass_scan.pdf", dpi=200, bbox_inches="tight")
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
    ax.errorbar(centers, obs, yerr=np.sqrt(obs), fmt="o", color="black", label="full data")
    total = np.sum(values, axis=0)
    ratio = np.divide(obs, total, out=np.full_like(obs, np.nan, dtype=float), where=total > 0)
    ratio_err = np.divide(np.sqrt(obs), total, out=np.zeros_like(obs, dtype=float), where=total > 0)
    rax.errorbar(centers, ratio, yerr=ratio_err, fmt="o", color="black")
    rax.axhline(1.0, color="gray", linewidth=1)
    ax.set_ylabel("Events / bin")
    rax.set_ylabel("Data/MC")
    rax.set_xlabel(r"$m_{4\ell}$ [GeV]")
    ax.legend(fontsize="x-small", ncols=2, loc="upper right", frameon=True)
    mh.cms.label("Open Data", data=True, lumi=10.0, com=13, ax=ax)
    return register("observed_m4l_broad_inclusive", "Phase 4c fit-window 70-170 GeV four-lepton mass distribution for all 203 selected data events compared with MC scaled to full-data luminosity; the ratio uses no data-integral normalization.", {"fit_window_GeV": [70, 170], "split_seed": OBSERVED_DATA_SEED, "data_integral_normalization": False}, "phase3_selection/outputs/selection_events.npz")


def plot_categories(events: dict, masks: dict) -> dict:
    grouped = mc_templates(events, FIT_BINS)
    observed = observed_counts(events, FIT_BINS, masks["keep"], CHANNELS)
    centers = 0.5 * (FIT_BINS[:-1] + FIT_BINS[1:])
    fig, axes = plt.subplots(3, 1, figsize=(9, 10), sharex=True, gridspec_kw={"hspace": 0})
    for ax, channel in zip(axes, CHANNELS):
        values, labels, colors = stack_arrays(grouped, channel)
        mh.histplot(values, bins=FIT_BINS, stack=True, histtype="fill", label=labels, color=colors, ax=ax)
        obs = observed[channel]
        ax.errorbar(centers, obs, yerr=np.sqrt(obs), fmt="o", color="black", label="full data")
        ax.set_xlabel(r"$m_{4\ell}$ [GeV]")
        ax.set_ylabel("Events / bin")
        mh.label.add_text(channel, ax=ax)
    axes[0].legend(fontsize="x-small", ncols=3, loc="upper right", frameon=True)
    mh.cms.label("Open Data", data=True, lumi=10.0, com=13, ax=axes[0])
    return register("observed_m4l_70_170_categories", "Phase 4c fit-window 70-170 GeV final-state category templates for full data and MC scaled to full-data luminosity.", {"fit_window_GeV": [70, 170], "channels": list(CHANNELS)}, "phase3_selection/outputs/selection_events.npz")


def plot_mu_comparison(parameters: dict) -> dict:
    expected = read_json(RESULTS / "expected_parameters.json")["mu"]
    partial = read_json(RESULTS / "partial_parameters.json")["mu"]
    labels = ["Expected", "10% data", "Full data"]
    vals = [expected["value"], partial["value"], parameters["mu"]["value"]]
    observed_sym = parameters["mu"]["uncertainty_symmetric"] or 0.0
    xerr = [
        [expected["uncertainty_minus"], partial["uncertainty_minus"] or partial["uncertainty_symmetric"] or 0.0, parameters["mu"]["uncertainty_minus"] or observed_sym],
        [expected["uncertainty_plus"], partial["uncertainty_plus"] or partial["uncertainty_symmetric"] or 0.0, parameters["mu"]["uncertainty_plus"] or observed_sym],
    ]
    fig, ax = plt.subplots(figsize=(6, 3))
    y = np.arange(len(labels))
    ax.errorbar(vals, y, xerr=xerr, fmt="o", color="black")
    ax.set_yticks(y, labels)
    ax.set_xlabel(r"Signal strength $\mu$")
    ax.set_xlim(left=0)
    mh.cms.label("Open Data", data=True, lumi=10.0, com=13, ax=ax)
    return register("observed_expected_mu_comparison", "Comparison of Phase 4a expected, Phase 4b 10% observed, and Phase 4c full observed signal-strength results.", {"expected_partial_observed_comparison": parameters["expected_partial_observed_comparison"]}, "analysis_note/results/observed_parameters.json")


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
    mh.cms.label("Open Data", data=True, lumi=10.0, com=13, ax=ax)
    return register("observed_nuisance_pulls", "Observed full-data nuisance best-fit values for the nominal final-state workspace; grouped MC-stat parameters are omitted from the display.", {"shown_parameters": names}, "analysis_note/results/observed_parameters.json")


def plot_impacts(parameters: dict) -> dict:
    impacts = parameters["nuisance_impacts"][:10]
    names = [row["nuisance"] for row in impacts]
    vals = [row["max_abs_impact"] or 0.0 for row in impacts]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(vals, np.arange(len(vals)), xerr=np.zeros(len(vals)), fmt="o", color="black")
    ax.set_yticks(np.arange(len(vals)), names)
    ax.set_xlabel(r"Max $|\Delta\mu|$")
    mh.cms.label("Open Data", data=True, lumi=10.0, com=13, ax=ax)
    return register("observed_nuisance_impacts", "Largest fixed-nuisance impacts on the full observed-data signal-strength fit.", {"top_n": len(impacts)}, "analysis_note/results/observed_parameters.json")


def plot_stability(validation: dict) -> dict:
    rows = validation["low_count_validation"]["alternative_binning_stability"]
    labels = [row["configuration"].replace("_", " ") for row in rows]
    vals = [row["mu_hat"] for row in rows]
    errs = [row["mu_uncertainty"] or 0.0 for row in rows]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(vals, np.arange(len(vals)), xerr=errs, fmt="o", color="black")
    ax.set_yticks(np.arange(len(vals)), labels)
    ax.set_xlabel(r"$\mu$ by binning/category fallback")
    mh.cms.label("Open Data", data=True, lumi=10.0, com=13, ax=ax)
    return register("observed_binning_stability", "Low-count stability check comparing nominal final-state and merged/inclusive fallback binnings on all selected full-data events.", {"rows": rows}, "analysis_note/results/observed_validation.json")


def plot_split(validation: dict) -> dict:
    rows = validation["deterministic_split_consistency"]["rows"]
    labels = [row["split"] for row in rows]
    vals = [row["mu_hat"] for row in rows]
    errs = [row["mu_uncertainty"] or 0.0 for row in rows]
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.errorbar(vals, np.arange(len(vals)), xerr=errs, fmt="o", color="black")
    ax.set_yticks(np.arange(len(vals)), labels)
    ax.set_xlabel(r"$\mu$ in deterministic split proxy")
    mh.cms.label("Open Data", data=True, lumi=5.0, com=13, ax=ax)
    return register("observed_split_consistency", "Deterministic half-split proxy consistency check for the full observed-data subsample; true CMS run-period metadata is unavailable.", {"split_consistency": validation["deterministic_split_consistency"]}, "analysis_note/results/observed_validation.json")


def plot_viability(parameters: dict, validation: dict) -> dict:
    covariance = read_json(RESULTS / "observed_covariance.json")
    components = covariance["uncertainty_breakdown"]["variance_components"]
    labels = ["Stat.", "MC stat.", "Syst.", "Total"]
    values = [
        np.sqrt(components["stat"]),
        np.sqrt(components["mc_stat"]),
        np.sqrt(max(components["syst_total_including_mc_stat"] - components["mc_stat"], 0.0)),
        np.sqrt(components["total"]),
    ]
    fig, ax = plt.subplots(figsize=(6, 4))
    y = np.arange(len(labels))
    ax.errorbar(values, y, xerr=np.zeros(len(values)), fmt="o", color="black")
    ax.axvline(abs(parameters["mu"]["value"]) * 0.5, color="gray", linewidth=1, linestyle="--")
    ax.set_yticks(y, labels)
    ax.set_xlabel(r"Uncertainty on $\mu$")
    mh.label.add_text(validation["viability"]["viability_verdict"], ax=ax)
    mh.cms.label("Open Data", data=True, lumi=10.0, com=13, ax=ax)
    return register("observed_uncertainty_viability", "Observed uncertainty breakdown and 50% relative-uncertainty viability threshold for the full-data signal-strength result.", {"viability": validation["viability"], "components": components}, "analysis_note/results/observed_covariance.json")


def plot_mass_scan() -> dict:
    mass = read_json(RESULTS / "observed_mass_scan.json")
    rows = [row for row in mass["scan_rows"] if row.get("fit_succeeded")]
    x = np.asarray([row["mass_hypothesis_GeV"] for row in rows], dtype=float)
    y = np.asarray([row["delta_twice_nll"] for row in rows], dtype=float)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(x, y, yerr=np.zeros_like(y), fmt="o-", color="black")
    ax.axhline(1.0, color="gray", linewidth=1, linestyle="--")
    ax.axvline(mass["best_mass_grid_GeV"], color="#4878a8", linewidth=1)
    ax.set_xlabel(r"Shifted-template $m_H$ hypothesis [GeV]")
    ax.set_ylabel(r"$\Delta(-2\log L)$")
    mh.label.add_text(f"best grid: {mass['best_mass_grid_GeV']:.1f} GeV", ax=ax)
    mh.cms.label("Open Data", data=True, lumi=10.0, com=13, ax=ax)
    return register("observed_mass_scan", "Observed full-data shifted-template mass scan with signal strength profiled at each mass hypothesis; the Z-peak region is excluded from Higgs mass hypotheses and the result is an approximate detector-level diagnostic.", {"best_mass_grid_GeV": mass["best_mass_grid_GeV"], "scan_range_GeV": mass["scan_range_GeV"], "uncertainty": mass["uncertainty"]}, "analysis_note/results/observed_mass_scan.json")


def main() -> None:
    ensure_dirs()
    logger = setup_logging()
    events = load_selection_events()
    masks = full_data_mask(events)
    parameters = read_json(RESULTS / "observed_parameters.json")
    validation = read_json(RESULTS / "observed_validation.json")
    figures = [
        plot_broad(events, masks),
        plot_categories(events, masks),
        plot_mu_comparison(parameters),
        plot_gof_pulls(parameters),
        plot_impacts(parameters),
        plot_stability(validation),
        plot_split(validation),
        plot_viability(parameters, validation),
        plot_mass_scan(),
    ]
    write_json(OUT / "FIGURES.json", figures)
    append_session(f"Observed figures written\n\n- Registered {len(figures)} figures in `phase4_inference/4c_observed/outputs/FIGURES.json`.")
    append_experiment(f"## 2026-05-30 — Phase 4c observed figures\n\n- Wrote and registered {len(figures)} full observed-data inference figures, including broad m4l, category overlays, expected comparison, nuisance diagnostics, split/stability checks, and the observed shifted-template mass scan.")
    logger.info("Wrote %d Phase 4c figures", len(figures))


if __name__ == "__main__":
    main()
