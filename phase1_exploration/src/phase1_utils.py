from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from rich.logging import RichHandler


HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
ROOT = PHASE.parent
OUT = PHASE / "outputs"
FIG = OUT / "figures"
DEBUG = OUT / "debug"
LOG_DIR = PHASE / "logs"
SESSION_LOG = LOG_DIR / "executor_albert_0f97_20260529T181833Z.md"
RETRIEVAL_LOG = PHASE / "retrieval_log.md"
SESSION = "albert_0f97"
LUMI_PB = 10_000.0

SAMPLE_INFO = {
    "GluGluToHToZZ.root": {
        "xsec_pb": 6.024e-03,
        "fullname": "GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_minloHJJ_JHUGenV7011_pythia8",
        "group": "signal_ggH",
    },
    "VBF_HToZZ.root": {
        "xsec_pb": 4.8794e-04,
        "fullname": "VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8",
        "group": "signal_VBF",
    },
    "ZHToZZ.root": {
        "xsec_pb": 9.8394e-05,
        "fullname": "ZH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8",
        "group": "signal_VH",
    },
    "WPHToZZ.root": {
        "xsec_pb": 1.072352e-04,
        "fullname": "WplusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8",
        "group": "signal_VH",
    },
    "WMHToZZ.root": {
        "xsec_pb": 6.706e-05,
        "fullname": "WminusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8",
        "group": "signal_VH",
    },
    "ZZTo4L.root": {
        "xsec_pb": 1.325e00,
        "fullname": "ZZTo4L_TuneCP5_13TeV_powheg_pythia8",
        "group": "background_ZZ",
    },
    "DYJetsToLL.root": {
        "xsec_pb": 5.396e03,
        "fullname": "DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
        "group": "background_reducible",
    },
    "TTBar.root": {
        "xsec_pb": 5.270e01,
        "fullname": "TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8",
        "group": "background_top",
    },
    "GGZZ2E2Mu.root": {
        "xsec_pb": 3.185e-03,
        "fullname": "GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8",
        "group": "background_ggZZ",
    },
    "GGZZ4Mu.root": {
        "xsec_pb": 1.575e-03,
        "fullname": "GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8",
        "group": "background_ggZZ",
    },
    "GGZZ4E.root": {
        "xsec_pb": 1.619e-03,
        "fullname": "GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8",
        "group": "background_ggZZ",
    },
}


def setup_logging() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    return logging.getLogger("phase1")


def ensure_dirs() -> None:
    for path in (OUT, FIG, DEBUG, LOG_DIR):
        path.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def append_session(entry: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with SESSION_LOG.open("a") as handle:
        handle.write(f"\n## {entry}\n")


def append_experiment(entry: str) -> None:
    with (ROOT / "experiment_log.md").open("a") as handle:
        handle.write(f"\n{entry}\n")


def paths() -> dict[str, Any]:
    return read_json(ROOT / "paths.json")


def root_files() -> list[dict[str, Any]]:
    cfg = paths()
    roots = [
        ("primary_data", Path(cfg["data_dir"]), "data"),
        ("primary_mc", Path(cfg["mc_dir"]), "mc"),
        ("local_data", Path(cfg["local_data_dir"]), "data"),
        ("local_mc", Path(cfg["local_mc_dir"]), "mc"),
    ]
    files: list[dict[str, Any]] = []
    seen: set[tuple[str, Path]] = set()
    for role, directory, kind in roots:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.root")):
            key = (role, path.resolve())
            if key in seen:
                continue
            seen.add(key)
            info = SAMPLE_INFO.get(path.name, {})
            files.append(
                {
                    "role": role,
                    "kind": kind,
                    "path": str(path),
                    "name": path.name,
                    "size_bytes": path.stat().st_size,
                    "is_primary": role.startswith("primary"),
                    "sample_info": info,
                }
            )
    return files


def primary_files() -> list[dict[str, Any]]:
    return [item for item in root_files() if item["is_primary"]]


def source_note() -> str:
    return (
        "Numeric MC cross sections are user-provided effective sample cross "
        "sections from prompt.md; Phase 2/3 should validate generator records "
        "where public campaign metadata is available."
    )

