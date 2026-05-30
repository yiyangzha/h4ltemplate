from __future__ import annotations

import json
import logging
import math
import ast
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from rich.logging import RichHandler


HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
ANALYSIS_ROOT = PHASE.parents[1]
PHASE3_OUT = ANALYSIS_ROOT / "phase3_selection" / "outputs"
OUT = PHASE / "outputs"
FIG = OUT / "figures"
RESULTS = ANALYSIS_ROOT / "analysis_note" / "results"
LOG_DIR = PHASE / "logs"
SESSION = "yuki_9d50"
SESSION_LOG = LOG_DIR / "executor_yuki_9d50_2026-05-30.md"

CHANNELS = ("4mu", "4e", "2e2mu")
CHANNEL_CODE = {"4mu": 0, "4e": 1, "2e2mu": 2}
FIT_BINS = np.array([70.0, 80.0, 90.0, 100.0, 105.0, 112.0, 118.0, 122.0, 126.0, 130.0, 140.0, 150.0, 160.0, 170.0])
ALT_BINS = {
    "final_state_nominal": FIT_BINS,
    "inclusive_nominal": FIT_BINS,
    "inclusive_coarse": np.array([70.0, 90.0, 105.0, 122.0, 126.0, 140.0, 170.0]),
    "inclusive_peak_side": np.array([70.0, 105.0, 122.0, 126.0, 140.0, 170.0]),
}
RANDOM_SEED = 4269
PARTIAL_DATA_SEED = 9417
PARTIAL_FRACTION = 0.10
FULL_LUMINOSITY_FB = 10.0
PARTIAL_LUMINOSITY_FB = FULL_LUMINOSITY_FB * PARTIAL_FRACTION
BROAD_BINS = np.array([70.0, 80.0, 90.0, 100.0, 105.0, 112.0, 118.0, 122.0, 126.0, 130.0, 140.0, 150.0, 160.0, 170.0])

SIGNAL_GROUPS = {"signal_ggH", "signal_VBF", "signal_VH"}
BACKGROUND_GROUPS = {"background_ZZ", "background_ggZZ", "background_reducible"}
NOMINAL_SAMPLE_GROUPS = SIGNAL_GROUPS | BACKGROUND_GROUPS


def setup_logging(name: str = "phase4b") -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    return logging.getLogger(name)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ensure_dirs() -> None:
    for path in (OUT, FIG, RESULTS, LOG_DIR):
        path.mkdir(parents=True, exist_ok=True)


def to_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    if isinstance(value, np.ndarray):
        return to_jsonable(value.tolist())
    if isinstance(value, np.generic):
        return to_jsonable(value.item())
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, Path):
        return str(value)
    return value


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_jsonable(payload), indent=2, sort_keys=True, allow_nan=False) + "\n")


def append_session(entry: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with SESSION_LOG.open("a") as handle:
        handle.write(f"\n## {now()} — {entry}\n")


def append_experiment(entry: str) -> None:
    with (ANALYSIS_ROOT / "experiment_log.md").open("a") as handle:
        handle.write(f"\n{entry}\n")


def load_fit_inputs() -> dict[str, Any]:
    return read_json(PHASE3_OUT / "fit_inputs_s1.json")


def load_selection_events() -> dict[str, Any]:
    payload = np.load(PHASE3_OUT / "selection_events.npz", allow_pickle=True)
    return {key: payload[key] for key in payload.files}


def sample_meta(events: dict[str, Any]) -> list[dict[str, Any]]:
    raw = events["sample_meta_json"][0]
    if isinstance(raw, str):
        return list(ast.literal_eval(raw))
    return list(raw)


def stack_label(group: str) -> str:
    if group == "signal_ggH":
        return "ggH signal"
    if group == "signal_VBF":
        return "VBF signal"
    if group == "signal_VH":
        return "VH signal"
    if group == "background_ZZ":
        return "qqZZ"
    if group == "background_ggZZ":
        return "ggZZ"
    if group == "background_reducible":
        return "DY+jets fake proxy"
    if group == "background_top":
        return "TTBar diagnostic"
    return group


def group_templates_from_fit_inputs(fit_inputs: dict[str, Any], channels: tuple[str, ...]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for group in NOMINAL_SAMPLE_GROUPS:
        grouped[group] = {
            "name": group,
            "stack": stack_label(group),
            "is_signal": group in SIGNAL_GROUPS,
            "channels": {channel: np.zeros(len(FIT_BINS) - 1, dtype=float) for channel in channels},
            "sumw2": {channel: np.zeros(len(FIT_BINS) - 1, dtype=float) for channel in channels},
        }
    for sample_payload in fit_inputs["samples"].values():
        group = sample_payload["group"]
        if group not in grouped:
            continue
        for channel in channels:
            item = sample_payload["fit_window"][channel]
            grouped[group]["channels"][channel] += np.asarray(item["counts"], dtype=float)
            grouped[group]["sumw2"][channel] += np.asarray(item["sumw2"], dtype=float)
    return grouped


def event_group_templates(
    events: dict[str, Any],
    edges: np.ndarray,
    *,
    channels: tuple[str, ...] = CHANNELS,
    mass_shift_factor: float = 1.0,
    include_groups: set[str] | None = None,
) -> dict[str, dict[str, Any]]:
    include = include_groups or NOMINAL_SAMPLE_GROUPS
    meta = sample_meta(events)
    groups = sorted({row["group"] for row in meta if row["group"] in include})
    out: dict[str, dict[str, Any]] = {}
    m4l = np.asarray(events["m4l"], dtype=float) * mass_shift_factor
    weights = np.asarray(events["weight"], dtype=float)
    sample_index = np.asarray(events["sample_index"], dtype=int)
    channel_code = np.asarray(events["channel_code"], dtype=int)
    is_data = np.asarray(events["is_data"], dtype=bool)
    for group in groups:
        out[group] = {
            "name": group,
            "stack": stack_label(group),
            "is_signal": group in SIGNAL_GROUPS,
            "channels": {channel: np.zeros(len(edges) - 1, dtype=float) for channel in channels},
            "sumw2": {channel: np.zeros(len(edges) - 1, dtype=float) for channel in channels},
        }
    for idx, row in enumerate(meta):
        group = row["group"]
        if group not in out:
            continue
        base = (sample_index == idx) & (~is_data) & (m4l > edges[0]) & (m4l < edges[-1])
        for channel in channels:
            mask = base & (channel_code == CHANNEL_CODE[channel])
            counts, _ = np.histogram(m4l[mask], bins=edges, weights=weights[mask])
            sumw2, _ = np.histogram(m4l[mask], bins=edges, weights=np.square(weights[mask]))
            out[group]["channels"][channel] += counts.astype(float)
            out[group]["sumw2"][channel] += sumw2.astype(float)
    return out


def inclusive_from_channels(grouped: dict[str, dict[str, Any]], channels: tuple[str, ...]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for group, payload in grouped.items():
        counts = np.zeros_like(next(iter(payload["channels"].values())), dtype=float)
        sumw2 = np.zeros_like(counts)
        for channel in channels:
            counts += payload["channels"][channel]
            sumw2 += payload["sumw2"][channel]
        out[group] = {
            **payload,
            "channels": {"inclusive": counts},
            "sumw2": {"inclusive": sumw2},
        }
    return out


def total_expectation(grouped: dict[str, dict[str, Any]], channel: str, include_signal: bool = True) -> np.ndarray:
    total = None
    for payload in grouped.values():
        if payload["is_signal"] and not include_signal:
            continue
        values = np.asarray(payload["channels"][channel], dtype=float)
        total = values.copy() if total is None else total + values
    return total if total is not None else np.zeros(len(FIT_BINS) - 1, dtype=float)


def clip_template(values: np.ndarray) -> list[float]:
    arr = np.asarray(values, dtype=float)
    arr = np.where(arr < 0.0, 0.0, arr)
    return arr.tolist()
