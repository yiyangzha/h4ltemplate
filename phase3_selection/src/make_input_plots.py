from __future__ import annotations

import numpy as np

from plot_utils import data_mc_comparison, save_and_register
from selection_common import OUT, VARIABLE_LABELS, append_experiment, append_session, read_json, setup_logging


def main() -> None:
    log = setup_logging()
    validation = read_json(OUT / "input_validation.json")
    made = 0
    for name, item in validation["variables"].items():
        log.info("Plotting input validation %s", name)
        edges = np.asarray(item["bin_edges"], dtype=float)
        data = np.asarray(item["data_counts"], dtype=float)
        scale = item["shape_normalization_scale_data_over_mc"]
        mc = np.asarray(item["mc_weighted_counts"], dtype=float)
        if scale is not None and np.isfinite(scale):
            mc = mc * float(scale)
        fig = data_mc_comparison(
            edges,
            data,
            {"MC prediction": mc},
            VARIABLE_LABELS.get(name, name),
            "Events",
            r"$13$ TeV, broad window",
        )
        verdict = "passes" if item["passes_d7_gate"] else "fails"
        caption = (
            f"{VARIABLE_LABELS.get(name, name)} input-validation distribution in the broad `70 <= m4l <= 170 GeV` window. "
            f"The D7 shape gate {verdict} with chi2/ndf = {item['chi2_per_ndf']} and p = {item['p_value']}; "
            "this comparison is used only to decide classifier-input eligibility, not to normalize fit templates."
        )
        save_and_register(
            fig,
            f"input_validation_{name}",
            caption,
            "phase3_selection/outputs/input_validation.json",
            {
                "variable": name,
                "passes_d7_gate": item["passes_d7_gate"],
                "shape_normalization_scale_data_over_mc": scale,
                "chi2": item["chi2"],
                "ndf": item["ndf"],
                "p_value": item["p_value"],
            },
        )
        made += 1
    append_session(f"2026-05-29 input plots\n\n- Wrote {made} input validation figures.")
    append_experiment(f"## 2026-05-29 — Phase 3 input-validation figures\n\n- Produced {made} D7 input-validation figures and updated `FIGURES.json`.")


if __name__ == "__main__":
    main()
