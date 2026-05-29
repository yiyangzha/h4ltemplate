from __future__ import annotations

from datetime import datetime, timezone

import numpy as np
import uproot

from phase1_utils import LUMI_PB, OUT, SAMPLE_INFO, append_experiment, append_session, ensure_dirs, primary_files, setup_logging, write_json


def metadata_sum(root_file: uproot.ReadOnlyDirectory) -> tuple[float | None, list[str]]:
    messages: list[str] = []
    for key in root_file.keys():
        name = key.split(";")[0]
        if name.lower() != "metadata":
            continue
        tree = root_file[key]
        if not hasattr(tree, "arrays"):
            continue
        branches = list(tree.keys())
        for candidate in ("nEvents", "genEventCount", "n_events", "nevents"):
            if candidate in branches:
                values = tree[candidate].array(library="np")
                return float(np.sum(values)), [f"Metadata branch `{candidate}` summed over {len(values)} rows"]
        messages.append(f"Metadata tree found but no known generated-event-count branch in {branches}")
    return None, messages or ["No Metadata tree found"]


def infer_coverage(name: str, fullname: str) -> dict[str, object]:
    text = f"{name} {fullname}"
    generators = [token for token in ("powheg", "powheg2", "JHUGen", "pythia8", "madgraph", "mcfm") if token.lower() in text.lower()]
    return {
        "sqrt_s_TeV": 13 if "13TeV" in text or "13 TeV" in text else None,
        "tune": "CP5" if "TuneCP5" in text else None,
        "generators": sorted(set(generators)),
        "process_text": fullname,
    }


def main() -> None:
    ensure_dirs()
    log = setup_logging()
    records = []
    for file_info in primary_files():
        log.info("Checking coverage for %s", file_info["name"])
        with uproot.open(file_info["path"]) as root_file:
            events_entries = None
            physics_tree_names = []
            tree_entries = {}
            for key in root_file.keys():
                tree = root_file[key]
                if hasattr(tree, "num_entries"):
                    clean = key.split(";")[0]
                    tree_entries[clean] = int(tree.num_entries)
                    if clean.lower() != "metadata":
                        physics_tree_names.append(clean)
                        events_entries = int(tree.num_entries)
            generated, metadata_messages = metadata_sum(root_file)
        sample = SAMPLE_INFO.get(file_info["name"], {})
        xsec = sample.get("xsec_pb")
        expected_yield = float(xsec) * LUMI_PB if xsec is not None else None
        nominal_weight = expected_yield / generated if expected_yield is not None and generated else None
        records.append(
            {
                **file_info,
                "tree_entries": tree_entries,
                "physics_tree_names": physics_tree_names,
                "events_entries": events_entries,
                "metadata_generated_events": generated,
                "metadata_messages": metadata_messages,
                "xsec_pb_user_prompt": xsec,
                "target_lumi_pb_user_prompt": LUMI_PB,
                "expected_yield_before_detector_acceptance": expected_yield,
                "nominal_mc_weight_if_generated_count_used": nominal_weight,
                "coverage": infer_coverage(file_info["name"], sample.get("fullname", file_info["name"])),
                "preselection_note": (
                    "For MC, Events entries are analysis ntuple rows after ntuplizer-level requirements; "
                    "the Metadata generated count is the denominator for luminosity normalization."
                    if file_info["kind"] == "mc"
                    else "For data, no inclusive public H->4l expectation is used to infer preselection in Phase 1; "
                    "the event count is treated as the ntuple content of the user-provided 10 fb^-1 subset."
                ),
            }
        )
    write_json(
        OUT / "preselection_coverage.json",
        {"created_utc": datetime.now(timezone.utc).isoformat(), "records": records},
    )
    append_session(
        "2026-05-29 preselection and coverage check\n\n"
        "- Wrote `phase1_exploration/outputs/preselection_coverage.json` with "
        "Metadata generated-event sums, nominal MC weights, and coverage tags."
    )
    append_experiment(
        "## 2026-05-29 — Phase 1 coverage check\n\n"
        "- Summed MC Metadata generated-event counts where available and computed "
        "prompt-luminosity nominal MC weights for downstream validation."
    )


if __name__ == "__main__":
    main()
