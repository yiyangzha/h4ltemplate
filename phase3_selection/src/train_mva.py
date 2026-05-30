from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.stats import chi2
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from selection_common import (
    BROAD_M4L_BINS,
    BROAD_WINDOW,
    FINAL_STATE_LABELS,
    MODEL_DIR,
    OUT,
    RANDOM_SEED,
    TRAINING_WINDOW,
    VARIABLE_LABELS,
    append_experiment,
    append_session,
    hist_counts,
    now,
    read_json,
    setup_logging,
    write_json,
)


MASS_SAFE_FEATURES = [
    "pt4l",
    "eta4l",
    "lead_lepton_pt",
    "sublead_lepton_pt",
    "lead_abs_eta",
    "sublead_abs_eta",
    "cos_theta_star",
    "cos_theta1",
    "cos_theta2",
    "phi",
    "phi1",
    "channel_code",
]

JHEP_LIKE_DIAGNOSTIC_FEATURES = [
    "mZ1",
    "mZ2",
    "pt4l",
    "eta4l",
    "lead_lepton_pt",
    "sublead_lepton_pt",
    "lead_abs_eta",
    "sublead_abs_eta",
    "cos_theta_star",
    "cos_theta1",
    "cos_theta2",
    "phi",
    "phi1",
    "channel_code",
]

MODEL_CONFIGS = {
    "logistic_mass_safe": {
        "kind": "logistic",
        "description": "Weighted logistic regression on the repaired broad-window mass-safe feature set.",
        "feature_names": MASS_SAFE_FEATURES,
    },
    "bdt_mass_safe": {
        "kind": "bdt",
        "description": "Weighted histogram gradient-boosted classifier on the repaired broad-window mass-safe feature set.",
        "feature_names": MASS_SAFE_FEATURES,
    },
    "logistic_jhep_like_diagnostic": {
        "kind": "logistic",
        "description": "Weighted logistic regression on a broader JHEP-like diagnostic feature set including mZ1 and mZ2; kept diagnostic-only because of mass-sculpting risk checks.",
        "feature_names": JHEP_LIKE_DIAGNOSTIC_FEATURES,
    },
    "bdt_jhep_like_diagnostic": {
        "kind": "bdt",
        "description": "Weighted histogram gradient-boosted classifier on a broader JHEP-like diagnostic feature set including mZ1 and mZ2; kept diagnostic-only because of mass-sculpting risk checks.",
        "feature_names": JHEP_LIKE_DIAGNOSTIC_FEATURES,
    },
}


def load_sources() -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    events = np.load(OUT / "selection_events.npz", allow_pickle=True)
    angles = np.load(OUT / "angular_variables.npz", allow_pickle=True)
    event_payload = {key: events[key] for key in events.files}
    angle_payload = {key: angles[key] for key in angles.files}
    return event_payload, angle_payload


def build_feature_table(
    events: dict[str, np.ndarray],
    angles: dict[str, np.ndarray],
    feature_names: list[str],
) -> tuple[np.ndarray, dict[str, np.ndarray], list[int], list[int]]:
    feature_map = {}
    for name in feature_names:
        if name in events:
            values = events[name]
        elif name in angles:
            values = angles[name]
        else:
            raise KeyError(f"Feature '{name}' not found in selection_events.npz or angular_variables.npz")
        feature_map[name] = values.astype(int if name == "channel_code" else float)
    x = np.column_stack([feature_map[name] for name in feature_names])
    meta = {
        "is_data": events["is_data"].astype(bool),
        "is_signal": events["is_signal"].astype(bool),
        "weight": events["weight"].astype(float),
        "channel_code": events["channel_code"].astype(int),
        "m4l": events["m4l"].astype(float),
    }
    categorical_idx = [idx for idx, name in enumerate(feature_names) if name == "channel_code"]
    numeric_idx = [idx for idx, name in enumerate(feature_names) if name != "channel_code"]
    return x, meta, numeric_idx, categorical_idx


def build_logistic_model(numeric_idx: list[int], categorical_idx: list[int]) -> Pipeline:
    transformers = [("num", StandardScaler(), numeric_idx)]
    if categorical_idx:
        transformers.append(("cat", OneHotEncoder(handle_unknown="ignore"), categorical_idx))
    preprocessor = ColumnTransformer(transformers)
    return Pipeline(
        [
            ("pre", preprocessor),
            ("clf", LogisticRegression(max_iter=2000, random_state=RANDOM_SEED)),
        ]
    )


def build_bdt_model() -> HistGradientBoostingClassifier:
    return HistGradientBoostingClassifier(
        random_state=RANDOM_SEED,
        max_depth=3,
        max_iter=120,
        learning_rate=0.06,
        min_samples_leaf=100,
    )


def model_score(model, x: np.ndarray) -> np.ndarray:
    return model.predict_proba(x)[:, 1]


def weighted_yields(meta: dict[str, np.ndarray], mask: np.ndarray) -> dict[str, float]:
    weights = meta["weight"].astype(float)
    signal = mask & meta["is_signal"].astype(bool) & (~meta["is_data"].astype(bool))
    background = mask & (~meta["is_signal"].astype(bool)) & (~meta["is_data"].astype(bool))
    data = mask & meta["is_data"].astype(bool)
    signal_sum = float(np.sum(weights[signal]))
    background_sum = float(np.sum(weights[background]))
    return {
        "signal": signal_sum,
        "background": background_sum,
        "data": float(np.sum(weights[data])),
        "asimov_mu_uncertainty_proxy": (float(np.sqrt(signal_sum + background_sum) / signal_sum) if signal_sum > 0.0 else None),
    }


def score_shape_gate(score: np.ndarray, meta: dict[str, np.ndarray], mask: np.ndarray) -> dict[str, object]:
    is_data = meta["is_data"].astype(bool)
    weights = meta["weight"].astype(float)
    edges = np.linspace(0.0, 1.0, 11)
    data_counts, _ = hist_counts(score[mask & is_data], np.ones(np.sum(mask & is_data), dtype=float), edges)
    mc_counts, mc_sumw2 = hist_counts(score[mask & (~is_data)], weights[mask & (~is_data)], edges)
    scale = np.sum(data_counts) / np.sum(mc_counts) if np.sum(mc_counts) > 0.0 else np.nan
    mc_shape = mc_counts * scale if np.isfinite(scale) else mc_counts
    variance = data_counts + mc_sumw2 * scale * scale if np.isfinite(scale) else data_counts + mc_sumw2
    valid = variance > 0.0
    ndf = int(np.sum(valid) - 1)
    stat = None
    p_value = None
    if np.sum(mc_counts) > 0.0 and ndf > 0:
        candidate = float(np.sum(np.square(data_counts[valid] - mc_shape[valid]) / variance[valid]))
        if np.isfinite(candidate):
            stat = candidate
            p_value = float(chi2.sf(candidate, ndf))
    return {
        "score_bin_edges": edges.tolist(),
        "data_counts": data_counts.tolist(),
        "mc_counts": mc_counts.tolist(),
        "chi2": stat,
        "ndf": ndf,
        "p_value": p_value,
        "passes": bool(stat is not None and ndf > 0 and stat / ndf <= 5.0),
    }


def category_counts(score: np.ndarray, meta: dict[str, np.ndarray], threshold: float) -> dict[str, object]:
    channels = meta["channel_code"].astype(int)
    weights = meta["weight"].astype(float)
    m4l = meta["m4l"].astype(float)
    categories = {"low_score": score < threshold, "high_score": score >= threshold}
    result: dict[str, object] = {}
    low_bins = 0
    total_bins = 0
    for cat_name, cat_mask in categories.items():
        result[cat_name] = {}
        for code, channel in enumerate(FINAL_STATE_LABELS):
            mask = cat_mask & (channels == code) & (m4l > BROAD_WINDOW[0]) & (m4l < BROAD_WINDOW[1])
            signal = mask & meta["is_signal"].astype(bool) & (~meta["is_data"].astype(bool))
            background = mask & (~meta["is_signal"].astype(bool)) & (~meta["is_data"].astype(bool))
            counts_sig, sumw2_sig = hist_counts(m4l[signal], weights[signal], BROAD_M4L_BINS)
            counts_bkg, sumw2_bkg = hist_counts(m4l[background], weights[background], BROAD_M4L_BINS)
            total = counts_sig + counts_bkg
            total_bins += len(total)
            low_bins += int(np.sum(total < 5.0))
            result[cat_name][channel] = {
                "signal_counts": counts_sig.tolist(),
                "background_counts": counts_bkg.tolist(),
                "signal_sumw2": sumw2_sig.tolist(),
                "background_sumw2": sumw2_bkg.tolist(),
                "signal_expected": float(np.sum(counts_sig)),
                "background_expected": float(np.sum(counts_bkg)),
                "total_expected": float(np.sum(total)),
                "bins_below_5_expected": int(np.sum(total < 5.0)),
            }
    result["viability"] = {
        "window": "70 < m4l < 170 GeV",
        "mass_bin_edges_GeV": BROAD_M4L_BINS.tolist(),
        "low_stat_bin_fraction": (low_bins / total_bins if total_bins else 1.0),
        "passes": bool(total_bins and (low_bins / total_bins) <= 0.25),
    }
    return result


def weighted_corr(x: np.ndarray, y: np.ndarray, w: np.ndarray) -> float | None:
    if len(x) == 0:
        return None
    x_mean = np.average(x, weights=w)
    y_mean = np.average(y, weights=w)
    x_var = np.average((x - x_mean) ** 2, weights=w)
    y_var = np.average((y - y_mean) ** 2, weights=w)
    if x_var <= 0.0 or y_var <= 0.0:
        return None
    cov = np.average((x - x_mean) * (y - y_mean), weights=w)
    return float(cov / np.sqrt(x_var * y_var))


def mass_sculpting(score: np.ndarray, meta: dict[str, np.ndarray], threshold: float) -> dict[str, object]:
    m4l = meta["m4l"].astype(float)
    weights = meta["weight"].astype(float)
    background = (
        (~meta["is_data"].astype(bool))
        & (~meta["is_signal"].astype(bool))
        & (m4l > TRAINING_WINDOW[0])
        & (m4l < TRAINING_WINDOW[1])
    )
    high = background & (score >= threshold)
    low = background & (score < threshold)
    corr = weighted_corr(score[background], m4l[background], weights[background])
    mean_low = float(np.average(m4l[low], weights=weights[low])) if np.any(low) else None
    mean_high = float(np.average(m4l[high], weights=weights[high])) if np.any(high) else None
    return {
        "window": "80 < m4l < 170 GeV background diagnostic",
        "background_score_m4l_corr": corr,
        "background_low_score_mean_m4l_GeV": mean_low,
        "background_high_score_mean_m4l_GeV": mean_high,
        "mean_shift_GeV": (None if mean_low is None or mean_high is None else float(mean_high - mean_low)),
        "passes": bool(corr is not None and abs(corr) <= 0.20),
    }


def save_model_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> None:
    log = setup_logging()
    validation = read_json(OUT / "input_validation.json")
    events, angles = load_sources()
    meta = {
        "is_data": events["is_data"].astype(bool),
        "is_signal": events["is_signal"].astype(bool),
        "weight": events["weight"].astype(float),
        "channel_code": events["channel_code"].astype(int),
        "m4l": events["m4l"].astype(float),
    }
    evaluation_mask = (~meta["is_data"]) & (meta["m4l"] > TRAINING_WINDOW[0]) & (meta["m4l"] < TRAINING_WINDOW[1])

    payload: dict[str, object] = {
        "created_utc": now(),
        "random_seed": RANDOM_SEED,
        "training_window": {"name": "broad_training_window", "m4l_min_GeV": TRAINING_WINDOW[0], "m4l_max_GeV": TRAINING_WINDOW[1]},
        "evaluation_window": {"name": "broad_training_matched_window", "m4l_min_GeV": TRAINING_WINDOW[0], "m4l_max_GeV": TRAINING_WINDOW[1]},
        "mass_shape_policy": {
            "m4l_used_as_classifier_input": False,
            "reason": "m4l is excluded from all classifier inputs to avoid sculpting the fitted mass observable.",
        },
        "feature_selection_policy": {
            "mode": "curated_mass_safe_override",
            "reason": "The audit found that using D7 as a hard whitelist left only two weak inputs. The repaired training keeps D7 as a modeling diagnostic but uses a curated broad-window mass-safe feature set with proper weighted training.",
            "d7_passing_inputs": [name for name, item in validation["variables"].items() if item.get("passes_d7_gate")],
            "d7_failing_inputs": [name for name, item in validation["variables"].items() if not item.get("passes_d7_gate")],
            "nominal_mass_safe_features": MASS_SAFE_FEATURES,
            "diagnostic_jhep_like_features": JHEP_LIKE_DIAGNOSTIC_FEATURES,
        },
        "models": {},
        "promotion_decision": {},
    }

    scores_all: dict[str, np.ndarray] = {}
    best_name = None
    best_auc = -np.inf
    for model_name, cfg in MODEL_CONFIGS.items():
        feature_names = list(cfg["feature_names"])
        x_all, _, numeric_idx, categorical_idx = build_feature_table(events, angles, feature_names)
        y = meta["is_signal"][evaluation_mask].astype(int)
        w = meta["weight"][evaluation_mask].astype(float)
        x_window = x_all[evaluation_mask]
        x_train, x_test, y_train, y_test, w_train, w_test = train_test_split(
            x_window,
            y,
            w,
            test_size=0.30,
            random_state=RANDOM_SEED,
            stratify=y,
        )
        log.info("Training %s", model_name)
        if cfg["kind"] == "logistic":
            model = build_logistic_model(numeric_idx, categorical_idx)
            model.fit(x_train, y_train, clf__sample_weight=w_train)
        else:
            model = build_bdt_model()
            model.fit(x_train, y_train, sample_weight=w_train)
        train_score = model_score(model, x_train)
        test_score = model_score(model, x_test)
        auc_train = float(roc_auc_score(y_train, train_score, sample_weight=w_train))
        auc_test = float(roc_auc_score(y_test, test_score, sample_weight=w_test))
        score_all = model_score(model, x_all)
        scores_all[model_name] = score_all
        signal_window = evaluation_mask & meta["is_signal"]
        threshold = float(np.quantile(score_all[signal_window], 0.5))
        fpr, tpr, _ = roc_curve(y_test, test_score, sample_weight=w_test)
        overtraining_signal_mean_gap = float(abs(np.average(train_score[y_train == 1], weights=w_train[y_train == 1]) - np.average(test_score[y_test == 1], weights=w_test[y_test == 1])))
        overtraining_background_mean_gap = float(abs(np.average(train_score[y_train == 0], weights=w_train[y_train == 0]) - np.average(test_score[y_test == 0], weights=w_test[y_test == 0])))
        payload["models"][model_name] = {
            "description": cfg["description"],
            "feature_names": feature_names,
            "feature_labels": {name: VARIABLE_LABELS.get(name, name) for name in feature_names},
            "auc": auc_test,
            "weighted_auc_train": auc_train,
            "weighted_auc_test": auc_test,
            "weighted_auc_gap": float(abs(auc_train - auc_test)),
            "overtraining_signal_mean_gap": overtraining_signal_mean_gap,
            "overtraining_background_mean_gap": overtraining_background_mean_gap,
            "roc": {"fpr": fpr.tolist(), "tpr": tpr.tolist()},
            "score_data_mc_gate": score_shape_gate(score_all, meta, evaluation_mask | meta["is_data"]),
            "threshold": threshold,
            "category_counts": category_counts(score_all, meta, threshold),
            "mass_sculpting": mass_sculpting(score_all, meta, threshold),
            "diagnostic_only": "diagnostic" in model_name,
            "passes": False,
        }
        payload["models"][model_name]["passes"] = bool(
            payload["models"][model_name]["score_data_mc_gate"]["passes"]
            and payload["models"][model_name]["category_counts"]["viability"]["passes"]
            and payload["models"][model_name]["mass_sculpting"]["passes"]
            and payload["models"][model_name]["weighted_auc_gap"] < 0.05
            and overtraining_signal_mean_gap < 0.10
        )
        if (not payload["models"][model_name]["diagnostic_only"]) and auc_test > best_auc:
            best_auc = auc_test
            best_name = model_name
        save_model_json(MODEL_DIR / f"{model_name}.json", {"model": model_name, "features": feature_names, "description": cfg["description"]})

    best_score = scores_all[best_name]
    best_threshold = payload["models"][best_name]["threshold"]
    s1_yields = weighted_yields(meta, (meta["m4l"] > TRAINING_WINDOW[0]) & (meta["m4l"] < TRAINING_WINDOW[1]))
    high_score_yields = weighted_yields(meta, (best_score >= best_threshold) & (meta["m4l"] > TRAINING_WINDOW[0]) & (meta["m4l"] < TRAINING_WINDOW[1]))
    improvement = None
    if s1_yields["asimov_mu_uncertainty_proxy"] and high_score_yields["asimov_mu_uncertainty_proxy"]:
        improvement = 1.0 - (high_score_yields["asimov_mu_uncertainty_proxy"] / s1_yields["asimov_mu_uncertainty_proxy"])

    best_model = payload["models"][best_name]
    promote = bool(best_model["passes"] and improvement is not None and improvement > 0.10)
    payload["promotion_decision"] = {
        "best_model": best_name,
        "s1_mu_uncertainty_proxy": s1_yields["asimov_mu_uncertainty_proxy"],
        "best_high_score_mu_uncertainty_proxy": high_score_yields["asimov_mu_uncertainty_proxy"],
        "relative_improvement": improvement,
        "promote_s2": promote,
        "reason": "S2 is promoted only if the repaired mass-safe classifier passes score-shape, broad-window low-stat, mass-sculpting, and overtraining gates while improving the 80 < m4l < 170 GeV precision proxy by more than 10%.",
    }

    np.savez_compressed(
        OUT / "mva_scores.npz",
        **{f"score_{name}": values for name, values in scores_all.items()},
        best_score=best_score,
        best_model=np.array([best_name]),
        feature_names=np.array(best_model["feature_names"]),
    )
    write_json(OUT / "mva_training_metadata.json", payload)
    write_json(OUT / "mva_metrics.json", payload)
    write_json(OUT / "prefit_category_counts.json", payload["models"][best_name]["category_counts"])
    append_session(
        "2026-05-30 repaired MVA training\n\n"
        f"- Restored `train_mva.py` with weighted `80 < m4l < 170 GeV` training.\n"
        f"- Best nominal model: `{best_name}` on features {', '.join(best_model['feature_names'])} with weighted test AUC {best_model['weighted_auc_test']:.4f}.\n"
        f"- Promote S2: {promote}."
    )
    append_experiment(
        "## 2026-05-30 — Phase 3 MVA regression repair\n\n"
        f"- Restored `phase3_selection/src/train_mva.py` with weighted `80 < m4l < 170 GeV` training and evaluation.\n"
        f"- Best nominal repaired model `{best_name}` used: {', '.join(best_model['feature_names'])}.\n"
        f"- Weighted AUC = {best_model['weighted_auc_test']:.4f}; S2 promotion = {promote}."
    )


if __name__ == "__main__":
    main()
