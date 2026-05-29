from __future__ import annotations

from datetime import datetime, timezone
from numbers import Number

import awkward as ak
import numpy as np
import uproot

from phase1_utils import OUT, append_experiment, append_session, ensure_dirs, primary_files, setup_logging, write_json

SLICE = 1000
FLAG_TOKENS = ("flag", "id", "type", "cat", "channel", "charge", "n", "num", "pass", "sel", "process")


def numeric_flat(array: ak.Array) -> np.ndarray:
    flat = ak.flatten(array, axis=None)
    if len(flat) == 0:
        return np.asarray([])
    try:
        return np.asarray(ak.to_numpy(flat))
    except (TypeError, ValueError):
        return np.asarray([])


def branch_summary(name: str, array: ak.Array) -> dict:
    values = numeric_flat(array)
    summary: dict[str, object] = {
        "entries_loaded": int(len(array)),
        "awkward_type": str(ak.type(array)),
        "total_values": int(len(values)),
    }
    if len(values) == 0 or not np.issubdtype(values.dtype, np.number):
        summary["numeric"] = False
        return summary
    finite = np.isfinite(values)
    summary.update(
        {
            "numeric": True,
            "dtype": str(values.dtype),
            "nan_count": int(np.isnan(values).sum()) if np.issubdtype(values.dtype, np.floating) else 0,
            "inf_count": int(np.isinf(values).sum()) if np.issubdtype(values.dtype, np.floating) else 0,
            "finite_count": int(finite.sum()),
        }
    )
    if finite.any():
        finite_values = values[finite]
        summary.update(
            {
                "min": float(np.min(finite_values)),
                "max": float(np.max(finite_values)),
                "mean": float(np.mean(finite_values)),
            }
        )
    lower = name.lower()
    looks_flag = (
        np.issubdtype(values.dtype, np.integer)
        or np.issubdtype(values.dtype, np.bool_)
        or any(token in lower for token in FLAG_TOKENS)
    )
    if looks_flag:
        unique, counts = np.unique(values[finite] if finite.any() else values, return_counts=True)
        max_items = min(len(unique), 50)
        summary["unique_survey"] = {
            "n_unique": int(len(unique)),
            "values": [
                {"value": scalar_to_builtin(unique[i]), "count": int(counts[i])}
                for i in range(max_items)
            ],
            "truncated": bool(len(unique) > max_items),
        }
    return summary


def scalar_to_builtin(value: object) -> object:
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Number):
        return value
    return str(value)


def main() -> None:
    ensure_dirs()
    log = setup_logging()
    records = []
    for file_info in primary_files():
        with uproot.open(file_info["path"]) as root_file:
            file_record = {**file_info, "trees": {}}
            for key in root_file.keys():
                tree = root_file[key]
                if not hasattr(tree, "arrays"):
                    continue
                stop = min(SLICE, int(tree.num_entries))
                log.info("Loading %s:%s entries 0:%d", file_info["name"], key, stop)
                arrays = tree.arrays(entry_stop=stop, library="ak")
                file_record["trees"][key.split(";")[0]] = {
                    "entries_available": int(tree.num_entries),
                    "entries_loaded": int(stop),
                    "branches": {
                        branch: branch_summary(branch, arrays[branch])
                        for branch in arrays.fields
                    },
                }
            records.append(file_record)
    write_json(
        OUT / "slice_recon.json",
        {"created_utc": datetime.now(timezone.utc).isoformat(), "slice_entries": SLICE, "files": records},
    )
    append_session(
        "2026-05-29 small-slice reconnaissance\n\n"
        "- Wrote `phase1_exploration/outputs/slice_recon.json` using at most "
        "1000 entries per primary tree."
    )
    append_experiment(
        "## 2026-05-29 — Phase 1 small-slice reconnaissance\n\n"
        "- Surveyed branch ranges, NaN/inf counts, and integer/flag unique "
        "values on at most 1000 entries per primary tree."
    )


if __name__ == "__main__":
    main()

