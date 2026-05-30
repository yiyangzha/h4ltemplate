from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np
from mplhep.utils import mpl_magic

import expected_common
from expected_common import (
    CHANNELS,
    FIG,
    FIT_BINS,
    OUT,
    PHASE,
    RESULTS,
    append_experiment,
    append_session,
    ensure_dirs,
    load_fit_inputs,
    now,
    read_json,
    setup_logging,
    write_json,
)


mh.style.use("CMS")

COLORS = {
    "Higgs signal": "#d62728",
    "qqZZ": "#1f77b4",
    "ggZZ": "#2ca02c",
    "DY+jets fake proxy": "#ff7f0e",
    "Expected total": "black",
}


def safe_mpl_magic(ax) -> None:
    try:
        mpl_magic(ax, soft_fail=True)
    except Exception:
        return


def figure_registry() -> list[dict[str, Any]]:
    path = OUT / "FIGURES.json"
    if not path.exists():
        return []
    payload = read_json(path)
    return payload if isinstance(payload, list) else []


def check_watcher_feedback() -> None:
    validation_dir = PHASE / "review" / "validation"
    if not validation_dir.exists():
        return
    superseding_rechecks = sorted(validation_dir.glob("PLOT_WATCHER_RECHECK_*.md"))
    if any("PASS" in path.read_text() and "Unresolved blockers: `0`" in path.read_text() for path in superseding_rechecks):
        return
    for path in sorted(validation_dir.glob("PLOT_WATCHER_FEEDBACK_*.md")):
        text = path.read_text()
        if "FAIL" in text and "Unresolved blockers: `0`" not in text:
            append_session(f"Watcher feedback check\n\n- Checked `{path}` after figure save; file contains `FAIL` or unresolved blocker text and requires manual inspection.")


def save_and_register(fig, stem: str, caption: str, source: str, metadata: dict[str, Any] | None = None) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    path = FIG / stem
    fig.savefig(str(path.with_suffix(".pdf")), bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(str(path.with_suffix(".png")), bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    entry = {
        "id": stem,
        "png": str(path.with_suffix(".png").relative_to(OUT)),
        "pdf": str(path.with_suffix(".pdf").relative_to(OUT)),
        "caption": caption,
        "description": caption,
        "source": source,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "metadata": metadata or {},
    }
    registry = figure_registry()
    for idx, item in enumerate(registry):
        if item.get("id") == stem:
            registry[idx] = entry
            break
    else:
        registry.append(entry)
    write_json(OUT / "FIGURES.json", registry)
    append_session(f"FIGURE_READY: phase4_inference/4a_expected/outputs/{entry['png']}")
    check_watcher_feedback()


def centers(edges: np.ndarray) -> np.ndarray:
    return 0.5 * (edges[:-1] + edges[1:])


def stack_from_fit_inputs(fit_inputs: dict[str, Any], channel: str) -> dict[str, np.ndarray]:
    stacks = {"Higgs signal": np.zeros(len(FIT_BINS) - 1), "qqZZ": np.zeros(len(FIT_BINS) - 1), "ggZZ": np.zeros(len(FIT_BINS) - 1), "DY+jets fake proxy": np.zeros(len(FIT_BINS) - 1)}
    for sample_payload in fit_inputs["samples"].values():
        item = sample_payload["fit_window"][channel]
        stack = item["stack"]
        if stack in stacks:
            stacks[stack] += np.asarray(item["counts"], dtype=float)
    return stacks


def stack_from_window(fit_inputs: dict[str, Any], window: str, channel: str) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    key = "bin_edges" if window == "fit_window" else "broad_window_edges"
    edges = np.asarray(fit_inputs[key], dtype=float)
    stacks = {
        "Higgs signal": np.zeros(len(edges) - 1),
        "qqZZ": np.zeros(len(edges) - 1),
        "ggZZ": np.zeros(len(edges) - 1),
        "DY+jets fake proxy": np.zeros(len(edges) - 1),
    }
    for sample_payload in fit_inputs["samples"].values():
        item = sample_payload[window][channel]
        stack = item["stack"]
        if stack in stacks:
            stacks[stack] += np.asarray(item["counts"], dtype=float)
    return edges, stacks


def plot_expected_m4l_broad() -> int:
    fit_inputs = load_fit_inputs()
    edges, stacks = stack_from_window(fit_inputs, "broad_window", "inclusive")
    x = centers(edges)
    xerr = 0.5 * np.diff(edges)
    signal = stacks["Higgs signal"]
    background = stacks["DY+jets fake proxy"] + stacks["ggZZ"] + stacks["qqZZ"]
    total = signal + background
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.errorbar(x, background, xerr=xerr, marker="o", linestyle="None", color="#1f77b4", label="Background")
    ax.errorbar(x, signal, xerr=xerr, marker="^", linestyle="None", color="#d62728", label="Higgs signal")
    ax.errorbar(x, total, xerr=xerr, marker="s", linestyle="None", color="black", label="Expected total")
    ax.set_xlabel(r"$m_{4\ell}$ [GeV]")
    ax.set_ylabel("Expected events")
    ax.legend(loc="upper right", fontsize="x-small")
    safe_mpl_magic(ax)
    mh.label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV, 10 fb$^{-1}$", ax=ax)
    caption = (
        "Expected inclusive four-lepton mass distribution in the broad validation range 70 < m4l < 170 GeV. "
        "The broad display is used for validation/sideband context; the signal-strength fit window remains 105 < m4l < 140 GeV."
    )
    save_and_register(
        fig,
        "expected_m4l_broad_inclusive",
        caption,
        "phase3_selection/outputs/fit_inputs_s1.json",
        {"window": "broad_window", "display_range_GeV": [70.0, 170.0], "fit_window_GeV": [105.0, 140.0]},
    )
    return 1


def plot_expected_m4l() -> int:
    fit_inputs = load_fit_inputs()
    x = centers(FIT_BINS)
    xerr = 0.5 * np.diff(FIT_BINS)
    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex="all")
    fig.subplots_adjust(hspace=0)
    for ax, channel in zip(axes, CHANNELS):
        stacks = stack_from_fit_inputs(fit_inputs, channel)
        signal = stacks["Higgs signal"]
        background = stacks["DY+jets fake proxy"] + stacks["ggZZ"] + stacks["qqZZ"]
        total = signal + background
        show_label = channel == CHANNELS[0]
        ax.errorbar(x, background, xerr=xerr, marker="o", linestyle="None", color="#1f77b4", label="Background" if show_label else None)
        ax.errorbar(x, signal, xerr=xerr, marker="^", linestyle="None", color="#d62728", label="Higgs signal" if show_label else None)
        ax.errorbar(x, total, xerr=xerr, marker="s", linestyle="None", color="black", label="Expected total" if show_label else None)
        ax.set_ylabel(f"{channel} events")
        mh.label.exp_label(
            exp="CMS",
            text="",
            loc=2,
            data=True,
            llabel=f"Open Simulation ({channel})",
            rlabel=r"$13$ TeV, 10 fb$^{-1}$" if show_label else "",
            ax=ax,
        )
        if show_label:
            ax.legend(loc="upper right", fontsize="x-small")
        safe_mpl_magic(ax)
    axes[-1].set_xlabel(r"$m_{4\ell}$ [GeV]")
    caption = (
        "Expected Asimov four-lepton mass templates in the final-state categories used by the Phase 4a simultaneous fit. "
        "Points show the background expectation, Higgs signal expectation, and their total; no observed Open Data counts are used as pseudo-data."
    )
    save_and_register(fig, "expected_m4l_final_state_templates", caption, "phase3_selection/outputs/fit_inputs_s1.json", {"channels": list(CHANNELS)})
    return 1


def plot_mu_scan(parameters: dict[str, Any]) -> int:
    rows = parameters["mu_profile_scan"]
    x = np.asarray([row["mu"] for row in rows], dtype=float)
    y = np.asarray([row["delta_twice_nll"] for row in rows], dtype=float)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(x, y, color="black", label=r"$-2\Delta\log L$")
    ax.axhline(1.0, color="#d62728", linestyle="--", label=r"$1\sigma$")
    ax.axhline(4.0, color="#1f77b4", linestyle=":", label=r"$2\sigma$")
    ax.set_xlabel(r"Signal strength $\mu$")
    ax.set_ylabel(r"$-2\Delta\log L$")
    ax.set_ylim(bottom=0.0)
    ax.legend(loc="upper center", fontsize="x-small")
    safe_mpl_magic(ax)
    mh.label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV, 10 fb$^{-1}$", ax=ax)
    caption = (
        "Expected profile-likelihood scan for the global Higgs signal-strength parameter. "
        f"The Asimov best fit is mu = {parameters['mu']['value']:.3g} with symmetric expected uncertainty {parameters['mu']['uncertainty_symmetric']:.3g}."
    )
    save_and_register(fig, "expected_mu_profile_scan", caption, "analysis_note/results/expected_parameters.json", parameters["mu"])
    return 1


def plot_impacts(parameters: dict[str, Any]) -> int:
    rows = [row for row in parameters["nuisance_impacts"] if row["max_abs_impact"] is not None][:12]
    labels = [row["nuisance"].replace("_", " ") for row in rows]
    y = np.arange(len(rows), dtype=float)[::-1]
    impacts = np.asarray([row["max_abs_impact"] for row in rows], dtype=float)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.errorbar(impacts, y, marker="o", linestyle="None", color="#9467bd")
    ax.set_yticks(y, labels)
    ax.set_xlabel(r"Maximum absolute shift in $\mu$")
    ax.set_ylabel("Nuisance parameter")
    mh.label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV", ax=ax)
    caption = "Expected nuisance impact ranking on the global signal strength, evaluated by fixing each nuisance at plus or minus one standard deviation and refitting the Asimov model."
    save_and_register(fig, "expected_nuisance_impacts", caption, "analysis_note/results/expected_parameters.json", {"shown": labels})
    return 1


def plot_uncertainty(covariance: dict[str, Any]) -> int:
    comps = covariance["uncertainty_breakdown"]["variance_components"]
    labels = ["Stat", "MC stat", "Syst total", "Total"]
    values = np.sqrt([comps["stat"], comps["mc_stat"], comps["syst_total_including_mc_stat"], comps["total"]])
    y = np.arange(len(labels), dtype=float)[::-1]
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.errorbar(values, y, marker="o", linestyle="None", color="#2ca02c")
    ax.set_yticks(y, labels)
    ax.set_xlabel(r"Expected uncertainty on $\mu$")
    ax.set_ylabel("Component")
    mh.label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV", ax=ax)
    caption = "Expected uncertainty breakdown for the Phase 4a Asimov signal-strength fit, derived from the stat-only, MC-stat, and full nuisance fits."
    save_and_register(fig, "expected_uncertainty_breakdown", caption, "analysis_note/results/expected_covariance.json", comps)
    return 1


def plot_systematic_shift_summary() -> int:
    shifts = read_json(RESULTS / "expected_systematic_shifts.json")
    systematics = shifts["systematics"]
    shape_rows = [row for row in systematics if row["is_shape"]]
    rate_rows = [row for row in systematics if row["is_rate_only"]]
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))
    fig.subplots_adjust(left=0.28, right=0.95, hspace=0.08)

    ax = axes[0]
    if shape_rows:
        shape = shape_rows[0]
        proc = shape["by_process"]["background_ZZ"]["channels"]["2e2mu"]
        edges = np.asarray(proc["bin_edges"], dtype=float)
        x = centers(edges)
        y_up = np.asarray(proc["delta_up"], dtype=float)
        y_down = np.asarray(proc["delta_down"], dtype=float)
        ax.errorbar(x, y_up, xerr=0.5 * np.diff(edges), marker="o", linestyle="None", color="#d62728", label="m4l scale up")
        ax.errorbar(x, y_down, xerr=0.5 * np.diff(edges), marker="s", linestyle="None", color="#1f77b4", label="m4l scale down")
    ax.axhline(0.0, color="gray", linestyle="--")
    ax.set_ylabel("Bin yield shift")
    ax.tick_params(labelbottom=False)
    ax.legend(loc="upper right", fontsize="x-small")
    mh.label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV", ax=ax)

    ax = axes[1]
    labels = []
    values = []
    for row in rate_rows:
        max_shift = 0.0
        for process in row["by_process"].values():
            for channel in process["channels"].values():
                max_shift = max(max_shift, abs(channel["relative_up_integral"] or 0.0), abs(channel["relative_down_integral"] or 0.0))
        labels.append(row["systematic"].replace("_", " "))
        values.append(max_shift)
    y = np.arange(len(labels), dtype=float)[::-1]
    ax.errorbar(values, y, marker="o", linestyle="None", color="black")
    ax.set_yticks(y, labels)
    if values:
        ax.set_xlim(0.0, max(values) * 1.12)
    ax.set_xlabel("Maximum absolute rate shift")
    ax.set_ylabel("Rate-only source")
    safe_mpl_magic(axes[0])
    safe_mpl_magic(axes[1])
    caption = (
        "Per-systematic shifted-bin summary. The upper panel shows the actual m4l-scale shape-source bin shifts for one representative process/channel; "
        "the lower panel shows maximum integral effects for rate-only sources without inventing fake shape dependence."
    )
    save_and_register(
        fig,
        "expected_systematic_shift_summary",
        caption,
        "analysis_note/results/expected_systematic_shifts.json",
        {"shape_example": "background_ZZ:2e2mu:m4l_scale", "rate_sources": labels},
    )
    return 1


def plot_injection(validation: dict[str, Any]) -> int:
    rows = validation["signal_injection"]
    x = np.asarray([row["injected_mu"] for row in rows], dtype=float)
    y = np.asarray([row["fitted_mu"] for row in rows], dtype=float)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot([0, 5], [0, 5], color="gray", linestyle="--", label="Exact recovery")
    ax.errorbar(x, y, marker="o", linestyle="None", color="black", label="Fit result")
    ax.set_xlabel(r"Injected $\mu$")
    ax.set_ylabel(r"Fitted $\mu$")
    ax.legend(loc="upper center", fontsize="x-small")
    safe_mpl_magic(ax)
    mh.label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV", ax=ax)
    caption = "Signal injection and recovery test at mu = 0, 1, 2, and 5. All injected Asimov configurations are refit with the same nuisance model and checked against the 20 percent bias gate."
    save_and_register(fig, "expected_signal_injection_recovery", caption, "analysis_note/results/expected_validation.json", {"rows": rows})
    return 1


def plot_validation(validation: dict[str, Any]) -> int:
    toy = validation["low_count_validation"]["toy_validation"]
    corruption = validation["closure_sensitivity"]["rows"]
    labels = ["Toy success", "Toy median bias", "Corrupt low p", "Corrupt high p"]
    values = [toy["fit_success_fraction"], abs(toy["median_bias"]), corruption[0]["p_value"], corruption[1]["p_value"]]
    y = np.arange(len(labels), dtype=float)[::-1]
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.errorbar(values, y, marker="o", linestyle="None", color="#17becf")
    ax.axvline(0.05, color="#d62728", linestyle="--", label="p = 0.05")
    ax.set_xscale("log")
    ax.set_yticks(y, labels)
    ax.set_xlabel("Validation metric value")
    ax.set_ylabel("Low-count and closure test")
    ax.legend(loc="lower right", fontsize="x-small")
    safe_mpl_magic(ax)
    mh.label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV", ax=ax)
    caption = (
        "Low-count toy and closure-sensitivity validation summary. "
        "The final-state simultaneous corruption test rejects the +20 percent mass-response case; the -20 percent case is retained as a documented low-count sensitivity limitation in the JSON."
    )
    save_and_register(fig, "expected_low_count_validation", caption, "analysis_note/results/expected_validation.json", {"toy": toy, "corruption": corruption})
    return 1


def binning_rows(validation: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str], np.ndarray]:
    rows = validation["alternative_binning_stability"]
    labels = [row["configuration"].replace("_", " ") for row in rows]
    y = np.arange(len(rows), dtype=float)[::-1]
    return rows, labels, y


def plot_binning_stability(validation: dict[str, Any]) -> int:
    rows, labels, y = binning_rows(validation)
    unc = np.asarray([row["mu_uncertainty"] for row in rows], dtype=float)
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.subplots_adjust(left=0.32, right=0.9)
    x_pad = max(0.001, 0.15 * float(np.max(unc) - np.min(unc)))
    ax.errorbar(unc, y, marker="o", linestyle="None", color="black")
    ax.set_xlim(float(np.min(unc)) - x_pad, float(np.max(unc)) + x_pad)
    ax.set_yticks(y, labels)
    ax.set_xlabel(r"Expected $\mu$ uncertainty")
    mh.label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV", ax=ax)
    caption = "Alternative-binning stability comparison for the expected signal-strength fit. The final-state nominal configuration is retained for the Asimov result after low-count toy validation, while inclusive/coarse variants provide stability cross-checks."
    save_and_register(fig, "expected_binning_stability", caption, "analysis_note/results/expected_validation.json", {"rows": rows})
    return 1


def plot_binning_low_count(validation: dict[str, Any]) -> int:
    rows, labels, y = binning_rows(validation)
    below = np.asarray([row["bins_below_5"] for row in rows], dtype=float)
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.subplots_adjust(left=0.32, right=0.97)
    ax.errorbar(below, y, marker="s", linestyle="None", color="#ff7f0e")
    ax.set_xlim(-0.8, float(np.max(below)) + 0.8)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Bins below five expected events")
    mh.label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV", ax=ax)
    caption = (
        "Low-count bin summary for the alternative-binning stability comparison. "
        "The nominal final-state model retains low expected-count bins only after the dedicated Poisson toy validation passes."
    )
    save_and_register(fig, "expected_binning_low_count_summary", caption, "analysis_note/results/expected_validation.json", {"rows": rows})
    return 1


def plot_binning(validation: dict[str, Any]) -> int:
    made = 0
    made += plot_binning_stability(validation)
    made += plot_binning_low_count(validation)
    return made


def plot_mass_scan(mass_scan: dict[str, Any]) -> int:
    rows = mass_scan["scan_rows"]
    x = np.asarray([row["mass_hypothesis_GeV"] for row in rows], dtype=float)
    y = np.asarray([row["twice_nll"] for row in rows], dtype=float)
    y = y - np.nanmin(y)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(x, y, color="black", label="Profile")
    ax.set_xlabel(r"Shifted signal-template mass hypothesis [GeV]")
    ax.set_ylabel(r"$-2\Delta\log L$")
    ax.legend(loc="upper right", fontsize="x-small")
    safe_mpl_magic(ax)
    mh.label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation", rlabel=r"$13$ TeV", ax=ax)
    caption = (
        "Detector-level shifted-template mass-profile attempt with mu profiled. "
        "This is retained as method-parity evidence; it is not promoted to an official-quality mass measurement because independent mass-hypothesis MC and official calibration inputs are unavailable."
    )
    save_and_register(fig, "expected_mass_profile_attempt", caption, "analysis_note/results/expected_mass_scan.json", {"promoted": mass_scan["promoted_to_nominal_mass_measurement"]})
    return 1


def plot_reference(validation: dict[str, Any], parameters: dict[str, Any]) -> int:
    labels = ["This analysis (expected)", "CMS-HIG-16-041", "CMS-HIG-19-001"]
    central = np.asarray([parameters["mu"]["value"], 1.05, 0.94], dtype=float)
    err = np.asarray([parameters["mu"]["uncertainty_symmetric"], 0.18, (0.07**2 + 0.085**2) ** 0.5], dtype=float)
    y = np.arange(len(labels), dtype=float)[::-1]
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.errorbar(central, y, xerr=err, marker="o", linestyle="None", color="black")
    ax.axvline(1.0, color="gray", linestyle="--", label="SM expectation")
    ax.set_yticks(y, labels)
    ax.set_xlabel(r"Signal strength $\mu$")
    ax.set_ylabel("Reference")
    ax.legend(loc="lower right", fontsize="x-small")
    safe_mpl_magic(ax)
    mh.label.exp_label(exp="CMS", text="", loc=2, data=True, llabel="Open Simulation and public references", rlabel=r"$13$ TeV", ax=ax)
    caption = (
        "Expected Phase 4a signal-strength precision compared with public CMS H to ZZ to four-lepton references. "
        f"The expected uncertainty/reference ratio {validation['precision_comparison']['ratio_this_over_reference']:.3g} is computed relative to CMS-HIG-16-041 only; "
        "CMS-HIG-19-001 is shown as an additional public comparison."
    )
    save_and_register(fig, "expected_reference_comparison", caption, "analysis_note/results/expected_validation.json", validation["precision_comparison"])
    return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Produce Phase 4a expected-inference plots.")
    parser.add_argument("--only", choices=["expected_binning_stability", "expected_reference_comparison"], help="Regenerate one plot without touching unrelated figure timestamps.")
    args = parser.parse_args()
    ensure_dirs()
    setup_logging()
    parameters = read_json(RESULTS / "expected_parameters.json")
    covariance = read_json(RESULTS / "expected_covariance.json")
    validation = read_json(RESULTS / "expected_validation.json")
    mass = read_json(RESULTS / "expected_mass_scan.json")
    made = 0
    if args.only == "expected_binning_stability":
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        expected_common.SESSION_LOG = expected_common.LOG_DIR / f"fixer_petra_3e4d_{stamp}.md"
        made += plot_binning_stability(validation)
        append_session(f"Expected plot fix written\n\n- Regenerated `{args.only}` PNG/PDF pair and updated its `outputs/FIGURES.json` entry.")
        append_experiment(f"## 2026-05-30 — Phase 4a expected binning-stability layout fix\n\n- Regenerated `expected_binning_stability` with a shorter x-axis label and wider right margin to resolve right-edge clipping.")
        return
    if args.only == "expected_reference_comparison":
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        expected_common.SESSION_LOG = expected_common.LOG_DIR / f"fixer_fiona_24f0_{stamp}.md"
        made += plot_reference(validation, parameters)
        append_session(f"Expected plot fix written\n\n- Regenerated `{args.only}` PNG/PDF pair and updated its `outputs/FIGURES.json` entry.")
        append_experiment(
            "## 2026-05-30 — Phase 4a expected reference-comparison label fix\n\n"
            "- Regenerated `expected_reference_comparison` with publication-standard reference labels and caption metadata clarifying that the 3.19 precision ratio is relative to CMS-HIG-16-041 only."
        )
        return
    made += plot_expected_m4l_broad()
    made += plot_expected_m4l()
    made += plot_mu_scan(parameters)
    made += plot_impacts(parameters)
    made += plot_uncertainty(covariance)
    made += plot_systematic_shift_summary()
    made += plot_injection(validation)
    made += plot_validation(validation)
    made += plot_binning(validation)
    made += plot_mass_scan(mass)
    made += plot_reference(validation, parameters)
    append_session(f"Expected plots written\n\n- Wrote {made} Phase 4a expected-inference PNG/PDF figure pairs and updated `outputs/FIGURES.json`.")
    append_experiment(f"## 2026-05-30 — Phase 4a expected plots\n\n- Produced {made} expected-inference figures and registered them in `phase4_inference/4a_expected/outputs/FIGURES.json`.")


if __name__ == "__main__":
    main()
