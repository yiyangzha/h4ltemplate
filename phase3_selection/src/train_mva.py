from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.stats import chi2
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import auc, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from selection_common import (
    FINAL_STATE_LABELS,
    FIT_WINDOW,
    M4L_BINS,
    MODEL_DIR,
    OUT,
    RANDOM_SEED,
    VARIABLE_LABELS,
    append_experiment,
    append_session,
    hist_counts,
    now,
    read_json,
    setup_logging,
    write_json,
)


def load_feature_matrix(names: list[str]) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    events = np.load(OUT / "selection_events.npz", allow_pickle=True)
    angles = np.load(OUT / "angular_variables.npz", allow_pickle=True)
    sources = {key: angles[key].astype(float) if key in angles.files else events[key].astype(float) for key in names}
    x = np.column_stack([sources[key] for key in names])
    meta = {key: events[key] for key in ("is_data", "is_signal", "weight", "channel_code", "m4l")}
    return x, meta


def weighted_yields(meta: dict[str, np.ndarray], mask: np.ndarray) -> dict[str, float]:
    weights = meta["weight"].astype(float)
    signal = mask & meta["is_signal"].astype(bool)
    background = mask & (~meta["is_signal"].astype(bool)) & (~meta["is_data"].astype(bool))
    data = mask & meta["is_data"].astype(bool)
    return {
        "signal": float(np.sum(weights[signal])),
        "background": float(np.sum(weights[background])),
        "data": float(np.sum(weights[data])),
        "asimov_mu_uncertainty_proxy": float(np.sqrt(np.sum(weights[signal]) + np.sum(weights[background])) / np.sum(weights[signal]))
        if np.sum(weights[signal]) > 0
        else None,
    }


def score_shape_gate(score: np.ndarray, meta: dict[str, np.ndarray]) -> dict[str, float | bool | int]:
    is_data = meta["is_data"].astype(bool)
    weights = meta["weight"].astype(float)
    edges = np.linspace(0, 1, 7)
    data_counts, _ = np.histogram(score[is_data], bins=edges)
    mc_counts, _ = np.histogram(score[~is_data], bins=edges, weights=weights[~is_data])
    mc_sumw2, _ = np.histogram(score[~is_data], bins=edges, weights=np.square(weights[~is_data]))
    scale = np.sum(data_counts) / np.sum(mc_counts) if np.sum(mc_counts) > 0 else np.nan
    mc_shape = mc_counts * scale if np.isfinite(scale) else mc_counts
    variance = data_counts + mc_sumw2 * scale * scale if np.isfinite(scale) else data_counts + mc_sumw2
    valid = variance > 0
    ndf = int(np.sum(valid) - 1)
    stat = float(np.sum(np.square(data_counts[valid] - mc_shape[valid]) / variance[valid])) if ndf > 0 else np.nan
    p_value = float(chi2.sf(stat, ndf)) if ndf > 0 and np.isfinite(stat) else np.nan
    return {"chi2": stat, "ndf": ndf, "p_value": p_value, "passes": bool(ndf > 0 and stat / ndf <= 5.0)}


def category_counts(score: np.ndarray, meta: dict[str, np.ndarray], threshold: float) -> dict:
    channels = meta["channel_code"].astype(int)
    weights = meta["weight"].astype(float)
    m4l = meta["m4l"].astype(float)
    categories = {"low_score": score < threshold, "high_score": score >= threshold}
    result = {}
    low_bins = 0
    total_bins = 0
    zero_background_categories = []
    for cat_name, cat_mask in categories.items():
        result[cat_name] = {}
        for code, channel in enumerate(FINAL_STATE_LABELS):
            mask = cat_mask & (channels == code) & (m4l > FIT_WINDOW[0]) & (m4l < FIT_WINDOW[1])
            signal = mask & meta["is_signal"].astype(bool)
            background = mask & (~meta["is_signal"].astype(bool)) & (~meta["is_data"].astype(bool))
            counts_sig, sumw2_sig = hist_counts(m4l[signal], weights[signal], M4L_BINS)
            counts_bkg, sumw2_bkg = hist_counts(m4l[background], weights[background], M4L_BINS)
            total = counts_sig + counts_bkg
            total_bins += len(total)
            low_bins += int(np.sum(total < 5.0))
            if float(np.sum(counts_bkg)) <= 0:
                zero_background_categories.append(f"{cat_name}:{channel}")
            result[cat_name][channel] = {
                "signal_counts": counts_sig.tolist(),
                "background_counts": counts_bkg.tolist(),
                "signal_sumw2": sumw2_sig.tolist(),
                "background_sumw2": sumw2_bkg.tolist(),
                "total_expected": float(np.sum(total)),
                "signal_expected": float(np.sum(counts_sig)),
                "background_expected": float(np.sum(counts_bkg)),
                "bins_below_5_expected": int(np.sum(total < 5.0)),
            }
    result["viability"] = {
        "low_stat_bin_fraction": low_bins / total_bins if total_bins else 1.0,
        "zero_background_categories": zero_background_categories,
        "passes": bool(total_bins and (low_bins / total_bins) <= 0.25 and not zero_background_categories),
    }
    return result


def model_score(model, x: np.ndarray) -> np.ndarray:
    return model.predict_proba(x)[:, 1]


def main() -> None:
    log = setup_logging()
    validation = read_json(OUT / "input_validation.json")
    feature_names = [name for name, item in validation["variables"].items() if item["passes_d7_gate"] and name != "m4l"]
    payload = {
        "created_utc": now(),
        "random_seed": RANDOM_SEED,
        "feature_names": feature_names,
        "feature_labels": {name: VARIABLE_LABELS.get(name, name) for name in feature_names},
        "models": {},
        "promotion_decision": {},
    }
    if len(feature_names) < 2:
        payload["promotion_decision"] = {"promote_s2": False, "reason": "Fewer than two variables passed the D7 gate; classifier training not promoted."}
        write_json(OUT / "mva_training_metadata.json", payload)
        write_json(OUT / "mva_metrics.json", payload)
        append_session("2026-05-29 MVA gate\n\n- Fewer than two D7-passing inputs; S2 classifier not trained.")
        return
    x, meta = load_feature_matrix(feature_names)
    mc_mask = ~meta["is_data"].astype(bool)
    labels = meta["is_signal"].astype(bool)[mc_mask].astype(int)
    weights = meta["weight"].astype(float)[mc_mask]
    x_train, x_test, y_train, y_test, w_train, w_test = train_test_split(
        x[mc_mask], labels, weights, test_size=0.30, random_state=RANDOM_SEED, stratify=labels
    )
    models = {
        "logistic": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)),
        "bdt": GradientBoostingClassifier(random_state=RANDOM_SEED, max_depth=2, n_estimators=80, learning_rate=0.05),
        "small_nn": make_pipeline(
            StandardScaler(),
            MLPClassifier(hidden_layer_sizes=(12,), alpha=0.01, max_iter=300, random_state=RANDOM_SEED, early_stopping=True),
        ),
    }
    best_name = None
    best_auc = -np.inf
    scores_all = {}
    for name, model in models.items():
        log.info("Training %s", name)
        if name == "bdt":
            model.fit(x_train, y_train, sample_weight=w_train)
        else:
            model.fit(x_train, y_train)
        test_score = model_score(model, x_test)
        train_score = model_score(model, x_train)
        fpr, tpr, _ = roc_curve(y_test, test_score, sample_weight=w_test)
        score_bins = np.linspace(0, 1, 11)
        train_sig, _ = np.histogram(train_score[y_train == 1], bins=score_bins)
        train_bkg, _ = np.histogram(train_score[y_train == 0], bins=score_bins)
        test_sig, _ = np.histogram(test_score[y_test == 1], bins=score_bins)
        test_bkg, _ = np.histogram(test_score[y_test == 0], bins=score_bins)
        score_all = model_score(model, x)
        scores_all[name] = score_all
        overtraining_gap = float(abs(np.mean(train_score[y_train == 1]) - np.mean(test_score[y_test == 1])))
        gate = score_shape_gate(score_all, meta)
        threshold = float(np.median(score_all[meta["is_signal"].astype(bool) & (~meta["is_data"].astype(bool))]))
        counts = category_counts(score_all, meta, threshold)
        payload["models"][name] = {
            "auc": float(auc(fpr, tpr)),
            "overtraining_signal_mean_gap": overtraining_gap,
            "score_data_mc_gate": gate,
            "threshold": threshold,
            "category_counts": counts,
            "roc": {"fpr": fpr.tolist(), "tpr": tpr.tolist()},
            "score_bins": score_bins.tolist(),
            "train_test_score_histograms": {
                "train_signal": train_sig.tolist(),
                "train_background": train_bkg.tolist(),
                "test_signal": test_sig.tolist(),
                "test_background": test_bkg.tolist(),
            },
            "feature_importance": (
                {feature: float(importance) for feature, importance in zip(feature_names, model.feature_importances_, strict=True)}
                if hasattr(model, "feature_importances_")
                else {}
            ),
            "passes": bool(gate["passes"] and counts["viability"]["passes"] and overtraining_gap < 0.10),
        }
        if payload["models"][name]["auc"] > best_auc:
            best_auc = payload["models"][name]["auc"]
            best_name = name
    s1_yields = weighted_yields(meta, (meta["m4l"] > FIT_WINDOW[0]) & (meta["m4l"] < FIT_WINDOW[1]))
    best_score = scores_all[best_name]
    best_threshold = payload["models"][best_name]["threshold"]
    high_score_yields = weighted_yields(meta, (best_score >= best_threshold) & (meta["m4l"] > FIT_WINDOW[0]) & (meta["m4l"] < FIT_WINDOW[1]))
    improvement = None
    if s1_yields["asimov_mu_uncertainty_proxy"] and high_score_yields["asimov_mu_uncertainty_proxy"]:
        improvement = 1.0 - (high_score_yields["asimov_mu_uncertainty_proxy"] / s1_yields["asimov_mu_uncertainty_proxy"])
    promote = bool(best_name and payload["models"][best_name]["passes"] and improvement is not None and improvement > 0.10)
    payload["promotion_decision"] = {
        "best_model": best_name,
        "s1_mu_uncertainty_proxy": s1_yields["asimov_mu_uncertainty_proxy"],
        "best_high_score_mu_uncertainty_proxy": high_score_yields["asimov_mu_uncertainty_proxy"],
        "relative_improvement": improvement,
        "promote_s2": promote,
        "reason": "S2 promoted only if best model passes score/viability/overtraining gates and improves expected mu uncertainty proxy by >10%.",
    }
    np.savez_compressed(
        OUT / "mva_scores.npz",
        **{f"score_{name}": value for name, value in scores_all.items()},
        best_score=best_score,
        best_model=np.array([best_name]),
        feature_names=np.array(feature_names),
    )
    write_json(OUT / "mva_training_metadata.json", payload)
    write_json(OUT / "mva_metrics.json", payload)
    write_json(OUT / "prefit_category_counts.json", payload["models"][best_name]["category_counts"])
    append_session(
        "2026-05-29 MVA training\n\n"
        f"- Trained logistic, BDT, and small NN on {len(feature_names)} D7-passing variables. "
        f"Best model: {best_name}; promote S2: {promote}."
    )
    append_experiment(
        "## 2026-05-29 — Phase 3 S2 classifier attempt\n\n"
        f"- Trained logistic, BDT, and small NN alternatives with fixed seed; best model `{best_name}` "
        f"promotion decision: {promote}."
    )


if __name__ == "__main__":
    main()
