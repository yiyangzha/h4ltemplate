from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import boost_histogram as bh
import numpy as np
from rich.logging import RichHandler


HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
ROOT = PHASE.parent
OUT = PHASE / "outputs"
FIG = OUT / "figures"
DEBUG = OUT / "debug"
LOG_DIR = PHASE / "logs"
MODEL_DIR = OUT / "models"
SESSION = "magnus_d784"
SESSION_LOG = LOG_DIR / "executor_magnus_d784_20260529T204533Z.md"
LUMI_PB = 10_000.0
FIT_WINDOW = (105.0, 140.0)
BROAD_WINDOW = (70.0, 170.0)
LOW_SIDEBAND = (70.0, 105.0)
HIGH_SIDEBAND = (140.0, 170.0)
RANDOM_SEED = 42

M4L_BINS = np.array([105.0, 112.0, 118.0, 122.0, 126.0, 130.0, 140.0])
BROAD_M4L_BINS = np.array([70.0, 85.0, 100.0, 105.0, 112.0, 118.0, 122.0, 126.0, 130.0, 140.0, 155.0, 170.0])

SAMPLE_INFO: dict[str, dict[str, Any]] = {
    "GluGluToHToZZ.root": {
        "xsec_pb": 6.024e-03,
        "fullname": "GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_minloHJJ_JHUGenV7011_pythia8",
        "group": "signal_ggH",
        "stack": "Higgs signal",
        "is_signal": True,
    },
    "VBF_HToZZ.root": {
        "xsec_pb": 4.8794e-04,
        "fullname": "VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8",
        "group": "signal_VBF",
        "stack": "Higgs signal",
        "is_signal": True,
    },
    "ZHToZZ.root": {
        "xsec_pb": 9.8394e-05,
        "fullname": "ZH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8",
        "group": "signal_VH",
        "stack": "Higgs signal",
        "is_signal": True,
    },
    "WPHToZZ.root": {
        "xsec_pb": 1.072352e-04,
        "fullname": "WplusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8",
        "group": "signal_VH",
        "stack": "Higgs signal",
        "is_signal": True,
    },
    "WMHToZZ.root": {
        "xsec_pb": 6.706e-05,
        "fullname": "WminusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8/NANOAODSIM/106X_mc2017_realistic_v9-v2",
        "group": "signal_VH",
        "stack": "Higgs signal",
        "is_signal": True,
    },
    "ZZTo4L.root": {
        "xsec_pb": 1.325e00,
        "fullname": "ZZTo4L_TuneCP5_13TeV_powheg_pythia8",
        "group": "background_ZZ",
        "stack": "qqZZ",
        "is_signal": False,
    },
    "GGZZ2E2Mu.root": {
        "xsec_pb": 3.185e-03,
        "fullname": "GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8",
        "group": "background_ggZZ",
        "stack": "ggZZ",
        "is_signal": False,
    },
    "GGZZ4Mu.root": {
        "xsec_pb": 1.575e-03,
        "fullname": "GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8",
        "group": "background_ggZZ",
        "stack": "ggZZ",
        "is_signal": False,
    },
    "GGZZ4E.root": {
        "xsec_pb": 1.619e-03,
        "fullname": "GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8",
        "group": "background_ggZZ",
        "stack": "ggZZ",
        "is_signal": False,
    },
    "DYJetsToLL.root": {
        "xsec_pb": 5.396e03,
        "fullname": "DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
        "group": "background_reducible",
        "stack": "DY+jets fake proxy",
        "is_signal": False,
    },
    "TTBar.root": {
        "xsec_pb": 5.270e01,
        "fullname": "TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8",
        "group": "background_top",
        "stack": "TTBar diagnostic",
        "is_signal": False,
    },
}

FINAL_STATE_LABELS = ("4mu", "4e", "2e2mu")
STACK_ORDER = ["DY+jets fake proxy", "TTBar diagnostic", "ggZZ", "qqZZ", "Higgs signal"]
STACK_COLORS = {
    "DY+jets fake proxy": "#d95f02",
    "TTBar diagnostic": "#8c564b",
    "ggZZ": "#1b9e77",
    "qqZZ": "#377eb8",
    "Higgs signal": "#e41a1c",
}
VARIABLE_LABELS = {
    "m4l": r"$m_{4\ell}$ [GeV]",
    "mZ1": r"$m_{Z1}$ [GeV]",
    "mZ2": r"$m_{Z2}$ [GeV]",
    "pt4l": r"$p_T^{4\ell}$ [GeV]",
    "eta4l": r"$\eta_{4\ell}$",
    "y4l": r"$y_{4\ell}$",
    "lead_lepton_pt": r"Leading lepton $p_T$ [GeV]",
    "sublead_lepton_pt": r"Subleading lepton $p_T$ [GeV]",
    "lead_abs_eta": r"Leading lepton $|\eta|$",
    "sublead_abs_eta": r"Subleading lepton $|\eta|$",
    "cos_theta_star": r"$\cos\theta^*$",
    "cos_theta1": r"$\cos\theta_1$",
    "cos_theta2": r"$\cos\theta_2$",
    "phi": r"$\Phi$ [rad]",
    "phi1": r"$\Phi_1$ [rad]",
    "classifier_score": "Classifier score",
}

MODEL_DISPLAY_NAMES = {
    "bdt": "BDT",
    "logistic": "logistic",
    "small_nn": "small NN",
}


def model_display_name(model_key: object) -> str:
    return MODEL_DISPLAY_NAMES.get(str(model_key), str(model_key).replace("_", " "))


def setup_logging(name: str = "phase3") -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    return logging.getLogger(name)


def ensure_dirs() -> None:
    for path in (OUT, FIG, DEBUG, LOG_DIR, MODEL_DIR):
        path.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_jsonable(payload), indent=2, sort_keys=True) + "\n")


def to_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    return value


def append_session(entry: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with SESSION_LOG.open("a") as handle:
        handle.write(f"\n## {entry}\n")


def append_experiment(entry: str) -> None:
    with (ROOT / "experiment_log.md").open("a") as handle:
        handle.write(f"\n{entry}\n")


def paths() -> dict[str, Any]:
    return read_json(ROOT / "paths.json")


def primary_files() -> list[dict[str, Any]]:
    cfg = paths()
    files = [{"role": "primary_data", "kind": "data", "path": Path(cfg["data_dir"]) / "cms_10fb_13TeV.root", "name": "cms_10fb_13TeV.root"}]
    mc_dir = Path(cfg["mc_dir"])
    for name in sorted(SAMPLE_INFO):
        files.append({"role": "primary_mc", "kind": "mc", "path": mc_dir / name, "name": name})
    return [with_file_stat(item) for item in files if item["path"].exists()]


def all_known_files() -> list[dict[str, Any]]:
    cfg = paths()
    roles = [
        ("primary_data", "data", Path(cfg["data_dir"])),
        ("primary_mc", "mc", Path(cfg["mc_dir"])),
        ("local_data", "data", Path(cfg["local_data_dir"])),
        ("local_mc", "mc", Path(cfg["local_mc_dir"])),
    ]
    files: list[dict[str, Any]] = []
    for role, kind, directory in roles:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.root")):
            files.append(with_file_stat({"role": role, "kind": kind, "path": path, "name": path.name}))
    return files


def with_file_stat(item: dict[str, Any]) -> dict[str, Any]:
    path = Path(item["path"])
    return {**item, "path": str(path), "size_bytes": path.stat().st_size}


def sample_group(name: str) -> str:
    if name == "cms_10fb_13TeV.root":
        return "data"
    return SAMPLE_INFO[name]["group"]


def sample_stack(name: str) -> str:
    if name == "cms_10fb_13TeV.root":
        return "Data"
    return SAMPLE_INFO[name]["stack"]


def sample_weight(name: str, generated_events: float | None) -> float:
    if name == "cms_10fb_13TeV.root":
        return 1.0
    if not generated_events or generated_events <= 0:
        raise ValueError(f"Missing generated-event denominator for {name}")
    return float(SAMPLE_INFO[name]["xsec_pb"]) * LUMI_PB / float(generated_events)


def final_state_from_pdgs(arrays: dict[str, np.ndarray]) -> np.ndarray:
    pdgs = np.vstack([np.abs(arrays[f"l{i}pdgId"]).astype(int) for i in range(1, 5)]).T
    n_mu = np.sum(pdgs == 13, axis=1)
    n_el = np.sum(pdgs == 11, axis=1)
    labels = np.full(len(pdgs), "other", dtype="<U6")
    labels[(n_mu == 4) & (n_el == 0)] = "4mu"
    labels[(n_el == 4) & (n_mu == 0)] = "4e"
    labels[(n_mu == 2) & (n_el == 2)] = "2e2mu"
    return labels


def finite_all(arrays: dict[str, np.ndarray], names: list[str]) -> np.ndarray:
    if not names:
        any_array = next(iter(arrays.values()))
        return np.ones(len(any_array), dtype=bool)
    mask = np.ones(len(arrays[names[0]]), dtype=bool)
    for name in names:
        mask &= np.isfinite(arrays[name])
    return mask


def lepton_pt_arrays(arrays: dict[str, np.ndarray]) -> np.ndarray:
    return np.vstack([arrays[f"l{i}pt"].astype(float) for i in range(1, 5)]).T


def lepton_abs_eta_arrays(arrays: dict[str, np.ndarray]) -> np.ndarray:
    return np.vstack([np.abs(arrays[f"l{i}eta"].astype(float)) for i in range(1, 5)]).T


def leading(values: np.ndarray, rank: int) -> np.ndarray:
    sorted_values = np.sort(values, axis=1)[:, ::-1]
    return sorted_values[:, rank]


def in_range(values: np.ndarray, lo: float, hi: float, *, right_inclusive: bool = False) -> np.ndarray:
    if right_inclusive:
        return (values >= lo) & (values <= hi)
    return (values > lo) & (values < hi)


def poisson_sumw2(weights: np.ndarray) -> float:
    return float(np.sum(np.square(weights)))


def hist_counts(values: np.ndarray, weights: np.ndarray, edges: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    finite = np.isfinite(values) & np.isfinite(weights)
    axis = bh.axis.Variable(edges)
    hist = bh.Histogram(axis, storage=bh.storage.Weight())
    hist.fill(values[finite], weight=weights[finite])
    view = hist.view()
    counts = np.asarray(view.value, dtype=float)
    sumw2 = np.asarray(view.variance, dtype=float)
    return counts.astype(float), sumw2.astype(float)


def safe_divide(num: np.ndarray, den: np.ndarray) -> np.ndarray:
    out = np.full_like(num, np.nan, dtype=float)
    np.divide(num, den, out=out, where=den != 0)
    return out


def channel_order_key(label: str) -> int:
    order = {"4mu": 0, "4e": 1, "2e2mu": 2}
    return order.get(label, 99)
