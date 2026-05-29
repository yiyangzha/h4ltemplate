from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import uproot

from selection_common import (
    BROAD_WINDOW,
    OUT,
    append_experiment,
    append_session,
    final_state_from_pdgs,
    in_range,
    now,
    primary_files,
    sample_group,
    sample_stack,
    sample_weight,
    setup_logging,
    write_json,
)
from build_selection_table import BRANCHES as SELECTION_BRANCHES
from build_selection_table import metadata_generated, masks


ANGLE_BRANCHES = ["m4l", "mZ1", "mZ2"] + [
    f"l{i}{suffix}" for i in range(1, 5) for suffix in ("pt", "eta", "phi", "mass", "pdgId", "charge", "zId", "elCutBased", "muPF", "muMedium")
]
BRANCHES = sorted(set(SELECTION_BRANCHES + ANGLE_BRANCHES))


def p4(pt: np.ndarray, eta: np.ndarray, phi: np.ndarray, mass: np.ndarray) -> np.ndarray:
    px = pt * np.cos(phi)
    py = pt * np.sin(phi)
    pz = pt * np.sinh(eta)
    energy = np.sqrt(np.maximum(px * px + py * py + pz * pz + mass * mass, 0.0))
    return np.stack([energy, px, py, pz], axis=1)


def mass(v: np.ndarray) -> np.ndarray:
    m2 = v[:, 0] ** 2 - np.sum(v[:, 1:] ** 2, axis=1)
    return np.sqrt(np.maximum(m2, 0.0))


def boost(v: np.ndarray, beta: np.ndarray) -> np.ndarray:
    beta2 = np.sum(beta * beta, axis=1)
    beta2 = np.clip(beta2, 0.0, 0.999999)
    gamma = 1.0 / np.sqrt(1.0 - beta2)
    bp = np.sum(beta * v[:, 1:], axis=1)
    factor = np.zeros_like(bp)
    valid = beta2 > 0
    factor[valid] = ((gamma[valid] - 1.0) * bp[valid] / beta2[valid]) - gamma[valid] * v[valid, 0]
    out_vec = v[:, 1:] + factor[:, None] * beta
    out_e = gamma * (v[:, 0] - bp)
    return np.column_stack([out_e, out_vec])


def unit(vec: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vec, axis=1)
    out = np.zeros_like(vec)
    np.divide(vec, norm[:, None], out=out, where=norm[:, None] > 0)
    return out


def angle_payload(arrays: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    leptons = [p4(arrays[f"l{i}pt"], arrays[f"l{i}eta"], arrays[f"l{i}phi"], arrays[f"l{i}mass"]) for i in range(1, 5)]
    z1 = leptons[0] + leptons[1]
    z2 = leptons[2] + leptons[3]
    h = z1 + z2
    beta_h = h[:, 1:] / h[:, 0:1]
    z1_h = boost(z1, beta_h)
    cos_theta_star = unit(z1_h[:, 1:])[:, 2]
    beam = np.tile(np.array([0.0, 0.0, 1.0]), (len(h), 1))
    boosted_leptons_h = [boost(lep, beta_h) for lep in leptons]
    z1_dir = unit(z1_h[:, 1:])
    z2_h = boost(z2, beta_h)
    z2_dir = unit(z2_h[:, 1:])
    l1_in_z1 = boost(leptons[0], z1[:, 1:] / z1[:, 0:1])[:, 1:]
    l3_in_z2 = boost(leptons[2], z2[:, 1:] / z2[:, 0:1])[:, 1:]
    cos_theta1 = np.sum(unit(l1_in_z1) * (-z2_dir), axis=1)
    cos_theta2 = np.sum(unit(l3_in_z2) * (-z1_dir), axis=1)
    n1 = unit(np.cross(boosted_leptons_h[0][:, 1:], boosted_leptons_h[1][:, 1:]))
    n2 = unit(np.cross(boosted_leptons_h[2][:, 1:], boosted_leptons_h[3][:, 1:]))
    phi = np.arctan2(np.sum(np.cross(n1, n2) * z1_dir, axis=1), np.sum(n1 * n2, axis=1))
    nsc = unit(np.cross(beam, z1_dir))
    phi1 = np.arctan2(np.sum(np.cross(nsc, n1) * z1_dir, axis=1), np.sum(nsc * n1, axis=1))
    return {
        "m4l_recomputed": mass(h),
        "mZ1_recomputed": mass(z1),
        "mZ2_recomputed": mass(z2),
        "cos_theta_star": np.clip(cos_theta_star, -1.0, 1.0),
        "cos_theta1": np.clip(cos_theta1, -1.0, 1.0),
        "cos_theta2": np.clip(cos_theta2, -1.0, 1.0),
        "phi": phi,
        "phi1": phi1,
    }


def main() -> None:
    log = setup_logging()
    rows = []
    compact: dict[str, list[np.ndarray]] = {key: [] for key in ("cos_theta_star", "cos_theta1", "cos_theta2", "phi", "phi1", "sample_index", "weight", "is_data", "is_signal", "channel_code", "m4l")}
    sample_meta = []
    for sample_idx, info in enumerate(primary_files()):
        path = Path(info["path"])
        log.info("Computing angular closure for %s", path.name)
        with uproot.open(path) as root_file:
            generated = metadata_generated(root_file)
            arrays = root_file["h4lTree"].arrays(BRANCHES, library="np")
        selected = masks(arrays)["broad_validation_window_70_170"]
        payload = angle_payload({key: value[selected] for key, value in arrays.items()})
        stored_m4l = arrays["m4l"][selected].astype(float)
        stored_mz1 = arrays["mZ1"][selected].astype(float)
        stored_mz2 = arrays["mZ2"][selected].astype(float)
        diffs = {
            "m4l": np.abs(payload["m4l_recomputed"] - stored_m4l),
            "mZ1": np.abs(payload["mZ1_recomputed"] - stored_mz1),
            "mZ2": np.abs(payload["mZ2_recomputed"] - stored_mz2),
        }
        range_counts = {
            key: int(np.sum((payload[key] < -1.000001) | (payload[key] > 1.000001)))
            for key in ("cos_theta_star", "cos_theta1", "cos_theta2")
        }
        range_counts.update({key: int(np.sum((payload[key] < -np.pi - 1e-6) | (payload[key] > np.pi + 1e-6))) for key in ("phi", "phi1")})
        rows.append(
            {
                "sample": path.name,
                "group": sample_group(path.name),
                "selected_broad_entries": int(np.sum(selected)),
                "median_abs_diff_GeV": {key: float(np.median(value)) if len(value) else None for key, value in diffs.items()},
                "p95_abs_diff_GeV": {key: float(np.percentile(value, 95)) if len(value) else None for key, value in diffs.items()},
                "passes_0p1_GeV_median_gate": bool(all(float(np.median(value)) < 0.1 for value in diffs.values() if len(value))),
                "out_of_range_counts": range_counts,
            }
        )
        channels = final_state_from_pdgs({key: value[selected] for key, value in arrays.items()})
        for key in ("cos_theta_star", "cos_theta1", "cos_theta2", "phi", "phi1"):
            compact[key].append(payload[key].astype(float))
        compact["m4l"].append(stored_m4l)
        compact["sample_index"].append(np.full(np.sum(selected), sample_idx, dtype=np.int16))
        compact["weight"].append(np.full(np.sum(selected), sample_weight(path.name, generated), dtype=float))
        compact["is_data"].append(np.full(np.sum(selected), path.name == "cms_10fb_13TeV.root", dtype=bool))
        compact["is_signal"].append(np.full(np.sum(selected), bool(__import__("selection_common").SAMPLE_INFO.get(path.name, {}).get("is_signal", False)), dtype=bool))
        compact["channel_code"].append(np.array([{"4mu": 0, "4e": 1, "2e2mu": 2}.get(v, -1) for v in channels], dtype=np.int16))
        sample_meta.append({"sample": path.name, "group": sample_group(path.name), "stack": sample_stack(path.name)})
    overall_pass = all(row["passes_0p1_GeV_median_gate"] and not any(row["out_of_range_counts"].values()) for row in rows)
    write_json(
        OUT / "angular_closure.json",
        {
            "created_utc": now(),
            "formula_note": "Angles are detector-level candidates reconstructed from retained lepton four-vectors; use requires data/MC input-validation gates.",
            "source_citation": "Phase 2 strategy cites CMS-HIG-16-041 angular/MELA references, Oreglia Appendix D, and Anderson et al. PRD 89 (2014) 035007.",
            "overall_pass": overall_pass,
            "samples": rows,
        },
    )
    np.savez_compressed(OUT / "angular_variables.npz", **{key: np.concatenate(value) for key, value in compact.items()}, sample_meta_json=np.array([str(sample_meta)], dtype=object))
    append_session("2026-05-29 angular closure\n\n- Wrote `angular_closure.json` and `angular_variables.npz`.")
    append_experiment(
        "## 2026-05-29 — Phase 3 angular reconstruction closure\n\n"
        "- Recomputed broad-window four-lepton and Z-candidate masses from retained lepton four-vectors, "
        "computed detector-level angular candidates, and wrote physical-range closure outputs."
    )


if __name__ == "__main__":
    main()
