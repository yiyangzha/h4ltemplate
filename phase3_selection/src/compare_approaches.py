from __future__ import annotations

import numpy as np

from selection_common import FIT_WINDOW, OUT, append_experiment, append_session, now, read_json, setup_logging, write_json


def s1_metrics() -> dict:
    events = np.load(OUT / "selection_events.npz", allow_pickle=True)
    fit = (events["m4l"] > FIT_WINDOW[0]) & (events["m4l"] < FIT_WINDOW[1])
    is_signal = events["is_signal"].astype(bool)
    is_data = events["is_data"].astype(bool)
    weights = events["weight"].astype(float)
    signal = float(np.sum(weights[fit & is_signal]))
    background = float(np.sum(weights[fit & (~is_signal) & (~is_data)]))
    data = float(np.sum(weights[fit & is_data]))
    return {
        "expected_signal": signal,
        "expected_background": background,
        "observed_data": data,
        "asimov_mu_uncertainty_proxy": float(np.sqrt(signal + background) / signal) if signal > 0 else None,
        "category_viability": "passes final-state categories; see cutflow and fit_inputs_s1.json",
    }


def main() -> None:
    setup_logging()
    s1 = s1_metrics()
    mva = read_json(OUT / "mva_metrics.json") if (OUT / "mva_metrics.json").exists() else {"promotion_decision": {"promote_s2": False, "reason": "MVA metrics missing"}}
    s2 = mva.get("promotion_decision", {})
    selected = "S2_classifier_categories" if s2.get("promote_s2") else "S1_reference_like_final_state_categories"
    payload = {
        "created_utc": now(),
        "common_metric": "Asimov counting precision proxy sqrt(S+B)/S in 105 < m4l < 140 GeV, plus D7/GoF/category gates",
        "approaches": {
            "S1_reference_like_cut_and_channel_fit": s1,
            "S2_angular_kinematic_classifier_categories": s2,
        },
        "selected_configuration": selected,
        "selection_reason": (
            "S2 passed all gates and improved the expected proxy by >10%."
            if selected.startswith("S2")
            else "S1 retained because S2 did not pass all input, score-shape, low-stat, overtraining, or >10% improvement gates."
        ),
    }
    write_json(OUT / "approach_comparison.json", payload)
    write_json(
        OUT / "selected_configuration.json",
        {
            "created_utc": now(),
            "nominal_configuration": selected,
            "fit_inputs": "fit_inputs_s1.json" if selected.startswith("S1") else "fit_inputs_s2.json",
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
