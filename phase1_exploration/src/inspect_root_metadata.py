from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import uproot

from phase1_utils import (
    OUT,
    append_experiment,
    append_session,
    ensure_dirs,
    root_files,
    setup_logging,
    source_note,
    write_json,
)


def describe_file(file_info: dict) -> dict:
    path = Path(file_info["path"])
    result = dict(file_info)
    result["keys"] = []
    result["trees"] = {}
    with uproot.open(path) as root_file:
        for key in root_file.keys():
            obj = root_file[key]
            clean_key = key.split(";")[0]
            classname = getattr(obj, "classname", type(obj).__name__)
            result["keys"].append({"key": key, "name": clean_key, "class": classname})
            if not hasattr(obj, "num_entries") or not hasattr(obj, "keys"):
                continue
            branches = {}
            for branch_name in obj.keys():
                branch = obj[branch_name]
                branches[branch_name] = {
                    "typename": getattr(branch, "typename", ""),
                    "interpretation": str(branch.interpretation),
                    "num_entries": int(branch.num_entries),
                }
            result["trees"][clean_key] = {
                "key": key,
                "num_entries": int(obj.num_entries),
                "branches": branches,
            }
    return result


def main() -> None:
    ensure_dirs()
    log = setup_logging()
    files = root_files()
    log.info("Inspecting %d ROOT files structurally", len(files))
    records = []
    for file_info in files:
        log.info("Inspecting %s", file_info["path"])
        records.append(describe_file(file_info))
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_note": source_note(),
        "files": records,
    }
    write_json(OUT / "root_metadata.json", payload)
    append_session(
        "2026-05-29 metadata inventory\n\n"
        f"- Wrote `phase1_exploration/outputs/root_metadata.json` with "
        f"{len(records)} ROOT files structurally inspected."
    )
    append_experiment(
        "## 2026-05-29 — Phase 1 metadata inventory\n\n"
        f"- Inspected {len(records)} ROOT files structurally with uproot and "
        "wrote `phase1_exploration/outputs/root_metadata.json`."
    )


if __name__ == "__main__":
    main()

