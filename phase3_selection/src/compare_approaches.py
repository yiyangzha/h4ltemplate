from __future__ import annotations

import ast

import numpy as np

from selection_common import (
    BROAD_M4L_BINS,
    FINAL_STATE_LABELS,
    OUT,
    TRAINING_WINDOW,
    append_experiment,
    append_session,
    hist_counts,
    now,
    read_json,
    setup_logging,
    write_json,
)


LOW_COUNT_THRESHOLD = 5.0


def s1_bin_viability() -> dict:
    events = np.load(OUT / "selection_events.npz", allow_pickle=True)
    edges = BROAD_M4L_BINS.tolist()
    m4l = events["m4l"].astype(float)
    channels = events["channel_code"].astype(int)
    weights = events["weight"].astype(float)
    is_data = events["is_data"].astype(bool)
    is_signal = events["is_signal"].astype(bool)
    sample_index = events["sample_index"].astype(int)
    meta = ast.literal_eval(str(events["sample_meta_json"][0]))
    nominal_background_indices = np.asarray(
        [row["group"] not in {"data", "background_top"} and not row["group"].startswith("signal") for row in meta],
        dtype=bool,
    )
    nominal_background = nominal_background_indices[sample_index]

    def category_totals(category: str) -> dict:
        if category == "inclusive":
            category_mask = np.ones(len(m4l), dtype=bool)
        else:
            category_mask = channels == FINAL_STATE_LABELS.index(category)
        window = (m4l > TRAINING_WINDOW[0]) & (m4l < TRAINING_WINDOW[1]) & category_mask
        signal, _ = hist_counts(m4l[window & is_signal & (~is_data)], weights[window & is_signal & (~is_data)], np.asarray(edges, dtype=float))
        background, _ = hist_counts(m4l[window & nominal_background & (~is_data)], weights[window & nominal_background & (~is_data)], np.asarray(edges, dtype=float))
        data, _ = hist_counts(m4l[window & is_data], np.ones(np.sum(window & is_data), dtype=float), np.asarray(edges, dtype=float))
        total = signal + background
        return {
            "bin_edges": edges,
            "signal_expected_by_bin": signal.tolist(),
            "background_expected_by_bin": background.tolist(),
            "total_expected_by_bin": total.tolist(),
            "data_observed_by_bin": data.tolist(),
            "bins_below_5_expected": int(np.sum(total < LOW_COUNT_THRESHOLD)),
            "total_bins": int(len(total)),
            "passes_min_expected_5_gate": bool(np.all(total >= LOW_COUNT_THRESHOLD)),
        }

    by_category = {category: category_totals(category) for category in FINAL_STATE_LABELS}
    inclusive = category_totals("inclusive")
    total_bins = sum(item["total_bins"] for item in by_category.values())
    low_bins = sum(item["bins_below_5_expected"] for item in by_category.values())
    return {
        "threshold_expected_events": LOW_COUNT_THRESHOLD,
        "summary": {
            "final_state_bins_below_5_expected": low_bins,
            "final_state_total_bins": total_bins,
            "final_state_fraction_below_5_expected": low_bins / total_bins if total_bins else None,
            "inclusive_bins_below_5_expected": inclusive["bins_below_5_expected"],
            "inclusive_total_bins": inclusive["total_bins"],
        },
        "by_category": by_category,
        "inclusive_diagnostic": inclusive,
        "handoff_status": "conditional_low_count_final_state_binning",
        "phase4_required_validation": [
            "low-count Poisson/toy validation",
            "MC-stat stability with sumw2 or per-bin statistical modifiers",
            "alternative rebinning or category merge if the low-count validation fails",
        ],
    }


def s1_metrics() -> dict:
    events = np.load(OUT / "selection_events.npz", allow_pickle=True)
    fit = (events["m4l"] > TRAINING_WINDOW[0]) & (events["m4l"] < TRAINING_WINDOW[1])
    is_signal = events["is_signal"].astype(bool)
    is_data = events["is_data"].astype(bool)
    weights = events["weight"].astype(float)
    signal = float(np.sum(weights[fit & is_signal]))
    background = float(np.sum(weights[fit & (~is_signal) & (~is_data)]))
    data = float(np.sum(weights[fit & is_data]))
    viability = s1_bin_viability()
    low = viability["summary"]["final_state_bins_below_5_expected"]
    total = viability["summary"]["final_state_total_bins"]
    return {
        "expected_signal": signal,
        "expected_background": background,
        "observed_data": data,
        "asimov_mu_uncertainty_proxy": float(np.sqrt(signal + background) / signal) if signal > 0 else None,
        "category_viability": (
            f"conditional low-count handoff: {low}/{total} final-state fit bins have S+B < "
            f"{LOW_COUNT_THRESHOLD:g}; Phase 4 must run low-count Poisson/toy validation and MC-stat stability before reporting results"
        ),
        "final_state_bin_viability": viability,
    }


def main() -> None:
    setup_logging()
    s1 = s1_metrics()
    mva = read_json(OUT / "mva_metrics.json") if (OUT / "mva_metrics.json").exists() else {"promotion_decision": {"promote_s2": False, "reason": "MVA metrics missing"}}
    s2 = mva.get("promotion_decision", {})
    selected = "S2_classifier_categories" if s2.get("promote_s2") else "S1_reference_like_final_state_categories"
    payload = {
        "created_utc": now(),
        "common_metric": "Asimov counting precision proxy sqrt(S+B)/S in 80 < m4l < 170 GeV, plus broad-window 70 < m4l < 170 GeV MVA score-shape/category/mass-sculpting gates",
        "approaches": {
            "S1_reference_like_cut_and_channel_fit": s1,
            "S2_angular_kinematic_classifier_categories": s2,
        },
        "selected_configuration": selected,
        "selection_reason": (
            "S2 passed all gates and improved the expected proxy by >10%."
            if selected.startswith("S2")
            else "S1 retained because S2 did not pass all input, score-shape, low-stat, overtraining, or >10% improvement gates; final-state binning is a conditional low-count Phase 4 handoff."
        ),
    }
    write_json(OUT / "approach_comparison.json", payload)
    write_json(
        OUT / "selected_configuration.json",
        {
            "created_utc": now(),
            "nominal_configuration": selected,
            "fit_inputs": "fit_inputs_s1.json" if selected.startswith("S1") else "fit_inputs_s2.json",
            "handoff_status": (
                "conditional_low_count_final_state_binning" if selected.startswith("S1") else "classifier_categories_promoted"
            ),
            "phase4_required_validation": s1.get("final_state_bin_viability", {}).get("phase4_required_validation", []),
            "low_count_bin_summary": s1.get("final_state_bin_viability", {}).get("summary", {}),
            "low_count_evidence_source": "approach_comparison.json:approaches.S1_reference_like_cut_and_channel_fit.final_state_bin_viability",
            "vbf_label_used": False,
        },
    )
    append_session(f"2026-05-29 approach comparison\n\n- Selected `{selected}` for nominal Phase 4 handoff.")
    append_experiment(
        "## 2026-05-29 — Phase 3 approach comparison\n\n"
        f"- Compared S1 and S2 on common expected precision and validation gates; selected `{selected}`."
    )


if __name__ == "__main__":
    main()
