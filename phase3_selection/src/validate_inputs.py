from __future__ import annotations

import numpy as np
from scipy.stats import chi2

from selection_common import (
    OUT,
    VARIABLE_LABELS,
    append_experiment,
    append_session,
    now,
    read_json,
    safe_divide,
    setup_logging,
    write_json,
)


VARIABLE_BINS = {
    "mZ1": np.array([40, 60, 70, 80, 90, 100, 110, 120], dtype=float),
    "mZ2": np.array([4, 12, 20, 30, 45, 60, 80, 120], dtype=float),
    "pt4l": np.array([0, 10, 20, 35, 60, 100, 200], dtype=float),
    "eta4l": np.array([-3, -2, -1, 0, 1, 2, 3], dtype=float),
    "y4l": np.array([-3, -2, -1, 0, 1, 2, 3], dtype=float),
    "lead_lepton_pt": np.array([0, 20, 30, 45, 70, 110, 200], dtype=float),
    "sublead_lepton_pt": np.array([0, 10, 15, 25, 40, 70, 150], dtype=float),
    "lead_abs_eta": np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5], dtype=float),
    "sublead_abs_eta": np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5], dtype=float),
    "cos_theta_star": np.linspace(-1, 1, 7),
    "cos_theta1": np.linspace(-1, 1, 7),
    "cos_theta2": np.linspace(-1, 1, 7),
    "phi": np.linspace(-np.pi, np.pi, 7),
    "phi1": np.linspace(-np.pi, np.pi, 7),
}


def hist_pair(values: np.ndarray, is_data: np.ndarray, weights: np.ndarray, edges: np.ndarray) -> dict:
    data_counts, _ = np.histogram(values[is_data], bins=edges)
    mc_counts, _ = np.histogram(values[~is_data], bins=edges, weights=weights[~is_data])
    mc_sumw2, _ = np.histogram(values[~is_data], bins=edges, weights=np.square(weights[~is_data]))
    finite = np.isfinite(data_counts) & np.isfinite(mc_counts)
    data_total = float(np.sum(data_counts))
    mc_total = float(np.sum(mc_counts))
    scale = data_total / mc_total if mc_total > 0 else np.nan
    mc_shape = mc_counts * scale if np.isfinite(scale) else mc_counts
    mc_shape_var = mc_sumw2 * scale * scale if np.isfinite(scale) else mc_sumw2
    variance = data_counts + mc_shape_var
    valid = finite & (variance > 0) & ((data_counts + mc_shape) > 0)
    ndf = int(np.sum(valid) - 1)
    stat = float(np.sum(np.square(data_counts[valid] - mc_shape[valid]) / variance[valid])) if ndf > 0 else np.nan
    p_value = float(chi2.sf(stat, ndf)) if ndf > 0 and np.isfinite(stat) else np.nan
    ratio = safe_divide(data_counts.astype(float), mc_shape)
    populated = (data_counts + mc_shape) > 0
    finite_ratio = ratio[np.isfinite(ratio) & populated]
    trend = float(np.nanmax(np.abs(finite_ratio - 1.0))) if len(finite_ratio) else np.nan
    coherent_fail = bool(np.isfinite(trend) and trend > 0.20)
    pass_gate = bool(ndf > 0 and np.isfinite(stat) and (stat / ndf) <= 5.0 and not coherent_fail)
    return {
        "bin_edges": edges.tolist(),
        "data_counts": data_counts.tolist(),
        "mc_weighted_counts": mc_counts.tolist(),
        "mc_sumw2": mc_sumw2.tolist(),
        "shape_normalization_scale_data_over_mc": scale,
        "chi2": stat,
        "ndf": ndf,
        "chi2_per_ndf": None if ndf <= 0 or not np.isfinite(stat) else stat / ndf,
        "p_value": p_value,
        "max_abs_shape_ratio_deviation": trend,
        "coherent_ratio_trend_above_20pct": coherent_fail,
        "passes_d7_gate": pass_gate,
        "normalization_note": "D7 shape gate uses MC scaled to data integral for shape comparison only; nominal yields remain prompt-luminosity normalized.",
    }


def main() -> None:
    log = setup_logging()
    events = np.load(OUT / "selection_events.npz", allow_pickle=True)
    angles = np.load(OUT / "angular_variables.npz", allow_pickle=True)
    is_data = events["is_data"].astype(bool)
    weights = events["weight"].astype(float)
    payload = {"created_utc": now(), "variables": {}, "discarded_without_gate": {}}
    for name, edges in VARIABLE_BINS.items():
        log.info("Validating %s", name)
        source = angles if name in angles.files else events
        values = source[name].astype(float)
        result = hist_pair(values, is_data, weights, edges)
        result["label"] = VARIABLE_LABELS.get(name, name)
        result["source"] = "angular_variables.npz" if source is angles else "selection_events.npz"
        payload["variables"][name] = result
    payload["discarded_without_gate"] = {
        "m4l": "Excluded from classifier inputs to avoid mass sculpting in the mass-shape fit.",
        "max_pf_rel_iso03": "Not a Phase 2 default classifier input; miniRelIso tails were flagged in Phase 1 and isolation is kept out of S2.",
        "max_sip3d": "Not used in S2 after baseline object selection; retained only as diagnostic if Phase 4 needs lepton efficiency envelopes.",
        "pvNdof": "Excluded by Phase 2 [A6] unless calibrated; not promoted to classifier input.",
    }
    write_json(OUT / "input_validation.json", payload)
    passed = [name for name, item in payload["variables"].items() if item["passes_d7_gate"]]
    append_session(
        "2026-05-29 input validation\n\n"
        f"- Wrote `input_validation.json`; {len(passed)} variables passed the D7 shape gate: {', '.join(passed)}."
    )
    append_experiment(
        "## 2026-05-29 — Phase 3 input-variable modeling gate\n\n"
        f"- Computed D7 data/MC shape gates for {len(payload['variables'])} candidate S2 variables; "
        f"{len(passed)} passed before classifier training."
    )


if __name__ == "__main__":
    main()
