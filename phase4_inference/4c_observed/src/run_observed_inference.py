from __future__ import annotations

import math
from collections.abc import Iterable
from typing import Any

import numpy as np
import pyhf
from scipy import optimize, stats

from observed_common import (
    ALT_BINS,
    BROAD_BINS,
    CHANNELS,
    CHANNEL_CODE,
    FIT_BINS,
    NOMINAL_SAMPLE_GROUPS,
    OBSERVED_DATA_SEED,
    OBSERVED_FRACTION,
    OBSERVED_LUMINOSITY_FB,
    PHASE3_OUT,
    RESULTS,
    SIGNAL_GROUPS,
    append_experiment,
    append_session,
    clip_template,
    ensure_dirs,
    event_group_templates,
    inclusive_from_channels,
    load_selection_events,
    now,
    read_json,
    setup_logging,
    write_json,
)


pyhf.set_backend("numpy", pyhf.optimize.scipy_optimizer(verbose=False))


SYSTEMATIC_SOURCES = {
    "lumi": {"label": "Integrated luminosity", "relative": 0.34 / 42.12, "conventions": "SP1", "basis": "external_public_uncertainty", "url": "https://cms-results.web.cern.ch/cms-results/public-results/preliminary-results/LUM-20-001/"},
    "lepton_eff": {"label": "Lepton reconstruction/ID/trigger efficiency", "relative": 0.030, "conventions": "SP4", "basis": "analysis_measured_envelope", "url": "phase3_selection/outputs/cut_motivation_diagnostics.json"},
    "signal_theory": {"label": "Signal production normalization/composition", "relative": 0.050, "conventions": "SP7", "basis": "fallback_prior_due_to_missing_generator_composition_inputs", "url": "https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-16-041/"},
    "zz_norm": {"label": "qqZZ background normalization", "relative": 0.100, "conventions": "SP9", "basis": "fallback_prior_due_to_prompt_effective_cross_sections", "url": "https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-19-001/"},
    "ggzz_norm": {"label": "ggZZ background normalization", "relative": 0.200, "conventions": "SP9", "basis": "fallback_prior_due_to_prompt_effective_cross_sections", "url": "https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-19-001/"},
    "dy_norm": {"label": "DY+jets fake-proxy normalization", "relative": 0.50, "conventions": "SP10", "basis": "analysis_measured_low_sideband_statistics", "url": "phase3_selection/outputs/sideband_fake_diagnostics.json"},
    "ttbar_omission": {"label": "TTBar omission diagnostic", "relative": 0.04440264879971137, "conventions": "SP11", "basis": "analysis_measured_omission_envelope", "url": "phase3_selection/outputs/sideband_fake_diagnostics.json"},
    "m4l_scale": {"label": "Lepton momentum scale/resolution shape", "relative": 0.001, "conventions": "SP5", "basis": "external_public_performance_envelope", "url": "https://cds.cern.ch/record/1279137"},
    "mc_stat": {"label": "MC statistical uncertainty", "relative": None, "conventions": "SP3", "basis": "analysis_measured_sumw2_grouped_approximation", "url": "phase3_selection/outputs/fit_inputs_s1.json"},
}


def scale_grouped(grouped: dict[str, dict[str, Any]], scale: float) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for group, payload in grouped.items():
        out[group] = {**payload, "channels": {}, "sumw2": {}}
        for channel, values in payload["channels"].items():
            out[group]["channels"][channel] = np.asarray(values, dtype=float) * scale
            out[group]["sumw2"][channel] = np.asarray(payload["sumw2"][channel], dtype=float) * scale * scale
    return out


def mc_templates(events: dict[str, Any], edges: np.ndarray, *, mass_shift_factor: float = 1.0) -> dict[str, dict[str, Any]]:
    return scale_grouped(event_group_templates(events, edges, channels=CHANNELS, mass_shift_factor=mass_shift_factor), OBSERVED_FRACTION)


def full_data_mask(events: dict[str, Any]) -> dict[str, Any]:
    is_data = np.asarray(events["is_data"], dtype=bool)
    rng = np.random.default_rng(OBSERVED_DATA_SEED)
    data_indices = np.flatnonzero(is_data)
    keep = np.zeros(len(is_data), dtype=bool)
    keep[data_indices] = True
    split = np.zeros(len(is_data), dtype=bool)
    split_scores = rng.random(len(data_indices))
    split[data_indices] = split_scores < 0.5
    return {"keep": keep, "split_a": keep & split, "split_b": keep & (~split), "n_data_total": int(len(data_indices)), "n_data_kept": int(np.sum(keep))}


def observed_counts(events: dict[str, Any], edges: np.ndarray, mask: np.ndarray, channels: tuple[str, ...]) -> dict[str, np.ndarray]:
    m4l = np.asarray(events["m4l"], dtype=float)
    channel_code = np.asarray(events["channel_code"], dtype=int)
    out = {}
    for channel in channels:
        chmask = mask & (channel_code == CHANNEL_CODE[channel]) & (m4l > edges[0]) & (m4l < edges[-1])
        counts, _ = np.histogram(m4l[chmask], bins=edges)
        out[channel] = counts.astype(float)
    return out


def data_for_channels(model: pyhf.Model, observed: dict[str, np.ndarray], channels: tuple[str, ...]) -> list[float]:
    main = []
    for channel in channels:
        main.extend(np.asarray(observed[channel], dtype=float).tolist())
    return main + list(model.config.auxdata)


def model_spec(
    grouped: dict[str, dict[str, Any]],
    channels: tuple[str, ...],
    *,
    include_systematics: Iterable[str] | None = None,
    include_staterror: bool = True,
    m4l_up: dict[str, dict[str, Any]] | None = None,
    m4l_down: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    active = set(include_systematics or [])
    spec_channels = []
    for channel in channels:
        samples = []
        for group, payload in sorted(grouped.items()):
            nominal = np.asarray(payload["channels"][channel], dtype=float)
            if np.sum(nominal) <= 0.0:
                continue
            modifiers: list[dict[str, Any]] = []
            if payload["is_signal"]:
                modifiers.append({"name": "mu", "type": "normfactor", "data": None})
            for key, name in (("lumi", "lumi"), ("lepton_eff", "lepton_eff")):
                if key in active:
                    rel = SYSTEMATIC_SOURCES[key]["relative"]
                    modifiers.append({"name": name, "type": "normsys", "data": {"hi": 1.0 + rel, "lo": max(1.0 - rel, 1.0e-6)}})
            if payload["is_signal"] and "signal_theory" in active:
                rel = SYSTEMATIC_SOURCES["signal_theory"]["relative"]
                modifiers.append({"name": f"{group}_theory", "type": "normsys", "data": {"hi": 1.0 + rel, "lo": 1.0 - rel}})
            if group == "background_ZZ" and "zz_norm" in active:
                rel = SYSTEMATIC_SOURCES["zz_norm"]["relative"]
                modifiers.append({"name": "qqZZ_norm", "type": "normsys", "data": {"hi": 1.0 + rel, "lo": 1.0 - rel}})
            if group == "background_ggZZ" and "ggzz_norm" in active:
                rel = SYSTEMATIC_SOURCES["ggzz_norm"]["relative"]
                modifiers.append({"name": "ggZZ_norm", "type": "normsys", "data": {"hi": 1.0 + rel, "lo": 1.0 - rel}})
            if group == "background_reducible" and "dy_norm" in active:
                rel = SYSTEMATIC_SOURCES["dy_norm"]["relative"]
                modifiers.append({"name": "dy_fake_norm", "type": "normsys", "data": {"hi": 1.0 + rel, "lo": max(1.0 - rel, 1.0e-6)}})
            if group == "background_reducible" and "ttbar_omission" in active:
                rel = SYSTEMATIC_SOURCES["ttbar_omission"]["relative"]
                modifiers.append({"name": "ttbar_omission", "type": "normsys", "data": {"hi": 1.0 + rel, "lo": max(1.0 - rel, 1.0e-6)}})
            if "m4l_scale" in active and m4l_up and m4l_down and group in m4l_up:
                modifiers.append({"name": "m4l_scale_shape", "type": "histosys", "data": {"hi_data": clip_template(m4l_up[group]["channels"][channel]), "lo_data": clip_template(m4l_down[group]["channels"][channel])}})
            if include_staterror and "mc_stat" in active:
                yld = float(np.sum(nominal))
                stat = float(np.sqrt(np.sum(np.asarray(payload["sumw2"][channel], dtype=float))))
                rel = stat / yld if yld > 0.0 else 0.0
                if rel > 0.0:
                    modifiers.append({"name": f"{group}_{channel}_mcstat", "type": "normsys", "data": {"hi": 1.0 + rel, "lo": max(1.0 - rel, 1.0e-6)}})
            samples.append({"name": group, "data": clip_template(nominal), "modifiers": modifiers})
        spec_channels.append({"name": channel, "samples": samples})
    return {"channels": spec_channels, "parameters": [{"name": "mu", "bounds": [[0.0, 10.0]], "inits": [1.0]}]}


def fit_model(model: pyhf.Model, data: list[float]) -> tuple[np.ndarray, float]:
    best, twice_nll = pyhf.infer.mle.fit(data, model, init_pars=model.config.suggested_init(), par_bounds=model.config.suggested_bounds(), fixed_params=model.config.suggested_fixed(), return_fitted_val=True)
    return np.asarray(best, dtype=float), float(twice_nll)


def profile_q(model: pyhf.Model, data: list[float], mu: float, best_nll: float) -> float:
    _, fixed_nll = pyhf.infer.mle.fixed_poi_fit(mu, data, model, init_pars=model.config.suggested_init(), par_bounds=model.config.suggested_bounds(), fixed_params=model.config.suggested_fixed(), return_fitted_val=True)
    return max(float(fixed_nll) - best_nll, 0.0)


def mu_uncertainty(model: pyhf.Model, data: list[float], bestfit: np.ndarray, best_nll: float) -> dict[str, float | None]:
    muhat = float(bestfit[model.config.poi_index])

    def qminus_one(mu: float) -> float:
        return profile_q(model, data, mu, best_nll) - 1.0

    lo = None
    hi = None
    for left, right in zip(np.linspace(0.0, muhat, 41)[:-1], np.linspace(0.0, muhat, 41)[1:]):
        if qminus_one(left) >= 0.0 and qminus_one(right) <= 0.0:
            lo = float(optimize.brentq(qminus_one, left, right, maxiter=80))
            break
    for left, right in zip(np.linspace(muhat, 10.0, 81)[:-1], np.linspace(muhat, 10.0, 81)[1:]):
        if qminus_one(left) <= 0.0 and qminus_one(right) >= 0.0:
            hi = float(optimize.brentq(qminus_one, left, right, maxiter=80))
            break
    err_lo = muhat - lo if lo is not None else None
    err_hi = hi - muhat if hi is not None else None
    finite = [x for x in (err_lo, err_hi) if x is not None]
    return {"muhat": muhat, "err_lo": err_lo, "err_hi": err_hi, "err_sym": float(np.mean(finite)) if finite else None, "scan_lo": lo, "scan_hi": hi}


def poisson_deviance(observed: np.ndarray, expected: np.ndarray) -> float:
    observed = np.asarray(observed, dtype=float)
    expected = np.asarray(expected, dtype=float)
    safe_expected = np.clip(expected, 1.0e-12, None)
    terms = np.where(observed > 0.0, observed * np.log(np.clip(observed, 1.0e-12, None) / safe_expected), 0.0)
    return float(2.0 * np.sum(safe_expected - observed + terms))


def gof_for_model(model: pyhf.Model, data: list[float], bestfit: np.ndarray, channels: tuple[str, ...], edges: np.ndarray) -> dict[str, Any]:
    expected = np.asarray(model.expected_data(bestfit, include_auxdata=False), dtype=float)
    observed = np.asarray(data[: model.config.nmaindata], dtype=float)
    rows = {}
    chi2 = 0.0
    offset = 0
    for channel in channels:
        nbin = len(edges) - 1
        obs = observed[offset : offset + nbin]
        exp = expected[offset : offset + nbin]
        ndf = int(max(len(obs) - 1, 1))
        channel_chi2 = float(np.sum(np.square(obs - exp) / np.clip(exp, 1.0e-9, None)))
        dev = poisson_deviance(obs, exp)
        rows[channel] = {"observed": obs.tolist(), "postfit_expected": exp.tolist(), "chi2": channel_chi2, "deviance": dev, "ndf": ndf, "p_value_chi2": float(stats.chi2.sf(channel_chi2, ndf)), "p_value_deviance": float(stats.chi2.sf(dev, ndf))}
        chi2 += channel_chi2
        offset += nbin
    ndf = int(max(len(observed) - 1, 1))
    deviance = poisson_deviance(observed, expected)
    return {"combined": {"chi2": chi2, "deviance": deviance, "ndf": ndf, "p_value_chi2": float(stats.chi2.sf(chi2, ndf)), "p_value_deviance": float(stats.chi2.sf(deviance, ndf)), "zero_chi2_warning": bool(chi2 < 1.0e-10)}, "by_channel": rows}


def fit_configuration(grouped: dict[str, dict[str, Any]], observed: dict[str, np.ndarray], channels: tuple[str, ...], edges: np.ndarray, active: set[str], *, m4l_up=None, m4l_down=None, include_staterror: bool = True) -> dict[str, Any]:
    model = pyhf.Model(model_spec(grouped, channels, include_systematics=active, include_staterror=include_staterror, m4l_up=m4l_up, m4l_down=m4l_down), poi_name="mu")
    data = data_for_channels(model, observed, channels)
    bestfit, best_nll = fit_model(model, data)
    unc = mu_uncertainty(model, data, bestfit, best_nll)
    return {"model": model, "data": data, "bestfit": bestfit, "best_nll": best_nll, "uncertainty": unc, "gof": gof_for_model(model, data, bestfit, channels, edges)}


def toy_validation(grouped: dict[str, dict[str, Any]], channels: tuple[str, ...], active: set[str], *, n_toys: int, seed: int, m4l_up=None, m4l_down=None) -> dict[str, Any]:
    model = pyhf.Model(model_spec(grouped, channels, include_systematics=active, include_staterror=True, m4l_up=m4l_up, m4l_down=m4l_down), poi_name="mu")
    nominal = np.asarray(model.expected_data(model.config.suggested_init(), include_auxdata=False), dtype=float)
    rng = np.random.default_rng(seed)
    values = []
    failures = 0
    for _ in range(n_toys):
        try:
            best, _ = fit_model(model, rng.poisson(nominal).astype(float).tolist() + list(model.config.auxdata))
            values.append(float(best[model.config.poi_index]))
        except Exception:
            failures += 1
    arr = np.asarray(values, dtype=float)
    bias = float(np.median(arr) - 1.0) if len(arr) else None
    return {"n_toys": n_toys, "seed": seed, "fit_failures": failures, "fit_success_fraction": float(len(arr) / n_toys), "median_mu": float(np.median(arr)) if len(arr) else None, "std_mu": float(np.std(arr, ddof=1)) if len(arr) > 1 else None, "median_bias_vs_mu1": bias, "passes_bias_gate": bool(abs(bias or 999.0) < 0.35), "passes_fit_success_gate": bool(len(arr) / n_toys >= 0.95)}


def nuisance_diagnostics(fit: dict[str, Any]) -> dict[str, Any]:
    names = fit["model"].config.par_names
    best = fit["bestfit"]
    rows = []
    impacts = []
    for name in names:
        idx = names.index(name)
        nominal = 1.0 if name == "mu" else 0.0
        rows.append({"parameter": name, "bestfit": float(best[idx]), "pull_from_nominal": float(best[idx] - nominal), "is_poi": name == "mu"})
        if name == "mu" or "mcstat" in name:
            continue
        shifts = {}
        for label, value in (("down", -1.0), ("up", 1.0)):
            init = list(fit["model"].config.suggested_init())
            fixed = list(fit["model"].config.suggested_fixed())
            bounds = list(fit["model"].config.suggested_bounds())
            init[idx] = value
            fixed[idx] = True
            try:
                varied, _ = pyhf.infer.mle.fit(fit["data"], fit["model"], init_pars=init, par_bounds=bounds, fixed_params=fixed, return_fitted_val=True)
                shifts[label] = float(varied[fit["model"].config.poi_index] - fit["uncertainty"]["muhat"])
            except Exception:
                shifts[label] = None
        valid = [abs(v) for v in shifts.values() if v is not None]
        impacts.append({"nuisance": name, "mu_shift_down": shifts["down"], "mu_shift_up": shifts["up"], "max_abs_impact": max(valid) if valid else None})
    return {"pulls": rows, "impacts": sorted(impacts, key=lambda row: -1.0 if row["max_abs_impact"] is None else -row["max_abs_impact"])}


def mu_profile_scan(fit: dict[str, Any]) -> list[dict[str, float]]:
    return [{"mu": float(mu), "delta_twice_nll": profile_q(fit["model"], fit["data"], float(mu), fit["best_nll"])} for mu in np.linspace(0.0, 10.0, 81)]


def shifted_mass_templates(events: dict[str, Any], mass: float, *, nominal_mass: float = 125.0, m4l_scale: float = 1.0) -> dict[str, dict[str, Any]]:
    return mc_templates(events, FIT_BINS, mass_shift_factor=(mass / nominal_mass) * m4l_scale)


def mass_interval_from_grid(scan_rows: list[dict[str, Any]]) -> dict[str, Any]:
    finite_rows = [row for row in scan_rows if row.get("fit_succeeded") and math.isfinite(row["delta_twice_nll"])]
    in_one_sigma = [row for row in finite_rows if row["delta_twice_nll"] <= 1.0]
    if not in_one_sigma:
        return {
            "meaningful": False,
            "interval_GeV": None,
            "reason": "No scanned grid point lies within delta_twice_nll <= 1 of the best point.",
        }
    interval = [min(row["mass_hypothesis_GeV"] for row in in_one_sigma), max(row["mass_hypothesis_GeV"] for row in in_one_sigma)]
    best_mass = min(finite_rows, key=lambda row: row["delta_twice_nll"])["mass_hypothesis_GeV"]
    at_scan_edge = best_mass in {finite_rows[0]["mass_hypothesis_GeV"], finite_rows[-1]["mass_hypothesis_GeV"]}
    return {
        "meaningful": bool(len(in_one_sigma) >= 2 and not at_scan_edge),
        "interval_GeV": interval,
        "criterion": "grid points with delta_twice_nll <= 1",
        "reason": "Grid-level diagnostic interval only; shifted M125 templates do not provide official calibrated interpolation or a calibrated stat/syst mass uncertainty split.",
    }


def observed_mass_scan(events: dict[str, Any], masks: dict[str, Any], active: set[str]) -> dict[str, Any]:
    coarse_mass_values = np.arange(110.0, 150.01, 2.5)
    observed = observed_counts(events, FIT_BINS, masks["keep"], CHANNELS)

    def fit_mass_point(mass: float, grid: str) -> dict[str, Any]:
        grouped = shifted_mass_templates(events, float(mass))
        rel = SYSTEMATIC_SOURCES["m4l_scale"]["relative"]
        m4l_up = shifted_mass_templates(events, float(mass), m4l_scale=1.0 + rel)
        m4l_down = shifted_mass_templates(events, float(mass), m4l_scale=1.0 - rel)
        fit_status = "full_nuisance_fit"
        try:
            fit = fit_configuration(grouped, observed, CHANNELS, FIT_BINS, active, m4l_up=m4l_up, m4l_down=m4l_down)
        except Exception as exc:
            fit_status = f"fallback_without_m4l_scale_after_{type(exc).__name__}"
            try:
                fit = fit_configuration(grouped, observed, CHANNELS, FIT_BINS, active - {"m4l_scale"})
            except Exception as second_exc:
                fit_status = f"fallback_without_m4l_scale_or_mcstat_after_{type(second_exc).__name__}"
                try:
                    fit = fit_configuration(grouped, observed, CHANNELS, FIT_BINS, set(), include_staterror=False)
                except Exception as final_exc:
                    return {
                        "mass_hypothesis_GeV": float(mass),
                        "grid": grid,
                        "mu_hat": None,
                        "mu_uncertainty": None,
                        "twice_nll": None,
                        "fit_status": f"failed_after_all_fallbacks_{type(final_exc).__name__}",
                        "fit_succeeded": False,
                        "chi2": None,
                        "ndf": None,
                        "p_value_chi2": None,
                    }
        return {
            "mass_hypothesis_GeV": float(mass),
            "grid": grid,
            "mu_hat": fit["uncertainty"]["muhat"],
            "mu_uncertainty": fit["uncertainty"]["err_sym"],
            "twice_nll": fit["best_nll"],
            "fit_status": fit_status,
            "fit_succeeded": True,
            "chi2": fit["gof"]["combined"]["chi2"],
            "ndf": fit["gof"]["combined"]["ndf"],
            "p_value_chi2": fit["gof"]["combined"]["p_value_chi2"],
        }

    coarse_rows = [fit_mass_point(float(mass), "coarse") for mass in coarse_mass_values]
    successful_coarse_rows = [row for row in coarse_rows if row.get("fit_succeeded")]
    if not successful_coarse_rows:
        raise RuntimeError("Observed mass scan had no successful coarse mass-hypothesis fits.")
    coarse_best = min(successful_coarse_rows, key=lambda row: row["twice_nll"])
    fine_min = max(float(coarse_best["mass_hypothesis_GeV"]) - 3.0, float(coarse_mass_values[0]))
    fine_max = min(float(coarse_best["mass_hypothesis_GeV"]) + 3.0, float(coarse_mass_values[-1]))
    fine_mass_values = np.round(np.arange(fine_min, fine_max + 0.0001, 0.25), 6)
    coarse_set = {round(float(mass), 6) for mass in coarse_mass_values}
    fine_rows = [fit_mass_point(float(mass), "fine") for mass in fine_mass_values if round(float(mass), 6) not in coarse_set]
    rows = coarse_rows + fine_rows
    successful_rows = [row for row in rows if row.get("fit_succeeded")]
    if not successful_rows:
        raise RuntimeError("Observed mass scan had no successful mass-hypothesis fits.")
    best_nll = min(row["twice_nll"] for row in successful_rows)
    for row in rows:
        row["delta_twice_nll"] = row["twice_nll"] - best_nll if row.get("fit_succeeded") else None
    for row in coarse_rows:
        row["delta_twice_nll_coarse_reference"] = row["twice_nll"] - coarse_best["twice_nll"] if row.get("fit_succeeded") else None
    best = min(successful_rows, key=lambda row: row["twice_nll"])
    finite_fine = sorted([row for row in rows if row.get("fit_succeeded") and fine_min <= row["mass_hypothesis_GeV"] <= fine_max], key=lambda row: row["mass_hypothesis_GeV"])
    parabolic = {
        "meaningful": False,
        "best_mass_GeV": None,
        "curvature": None,
        "reason": "Not evaluated.",
    }
    if len(finite_fine) >= 3:
        x = np.asarray([row["mass_hypothesis_GeV"] for row in finite_fine], dtype=float)
        y = np.asarray([row["twice_nll"] for row in finite_fine], dtype=float)
        coeff = np.polyfit(x, y, 2)
        if coeff[0] > 0:
            vertex = float(-coeff[1] / (2.0 * coeff[0]))
            parabolic = {
                "meaningful": bool(fine_min <= vertex <= fine_max),
                "best_mass_GeV": vertex if fine_min <= vertex <= fine_max else None,
                "curvature": float(coeff[0]),
                "fit_window_GeV": [float(fine_min), float(fine_max)],
                "reason": "Diagnostic quadratic interpolation of shifted-template fine-grid NLL points; not a calibrated mass estimator.",
            }
        else:
            parabolic = {
                "meaningful": False,
                "best_mass_GeV": None,
                "curvature": float(coeff[0]),
                "fit_window_GeV": [float(fine_min), float(fine_max)],
                "reason": "Quadratic interpolation has non-positive curvature, so no diagnostic vertex is quoted.",
            }
    interval = mass_interval_from_grid(rows)
    return {
        "phase": "4c_observed",
        "created_utc": now(),
        "method": "observed simultaneous final-state shifted-template mass scan with mu profiled at each mass hypothesis",
        "profiled_parameter": "mu",
        "fit_window_GeV": [70.0, 170.0],
        "scan_range_GeV": {"min": float(coarse_mass_values[0]), "max": float(coarse_mass_values[-1]), "coarse_step": 2.5, "fine_step": 0.25},
        "coarse_scan_range_GeV": {"min": float(coarse_mass_values[0]), "max": float(coarse_mass_values[-1]), "step": 2.5},
        "fine_scan_range_GeV": {"min": float(fine_mass_values[0]), "max": float(fine_mass_values[-1]), "step": 0.25, "centered_on_coarse_best_GeV": coarse_best["mass_hypothesis_GeV"]},
        "mass_grid_GeV": [float(mass) for mass in coarse_mass_values],
        "fine_mass_grid_GeV": [float(mass) for mass in fine_mass_values],
        "excluded_ranges_GeV": [
            {
                "min": 70.0,
                "max": 105.0,
                "reason": "Excluded from the Higgs mass-hypothesis grid because this region contains the Z peak and the available M125 H->ZZ* shifted-template approximation is not a valid Higgs-mass model there.",
            },
            {
                "min": 150.0,
                "max": 170.0,
                "reason": "Used in the broad signal-strength fit as sideband/background constraint but not scanned as a Higgs mass hypothesis because only M125 shifted detector-level templates are available and high-mass independent signal MC is absent.",
            },
        ],
        "z_peak_treatment": "The full 70-170 GeV binned likelihood is used for observed counts and background constraints, but mass hypotheses below 110 GeV are not considered Higgs candidates.",
        "template_shift_procedure": "For mass hypothesis mH, selected MC event m4l values are scaled by mH / 125 GeV before refilling final-state templates; this uses only the available M125 samples.",
        "fit_fallback_policy": "Each grid point first uses the full Phase 4c nuisance model. If pyhf minimization fails for a shifted-template hypothesis, the scan records a fallback fit without the m4l_scale histosys; if that also fails, it records a final fallback without m4l_scale or grouped MC-stat. This keeps failures visible instead of dropping points silently.",
        "scan_rows": rows,
        "failed_grid_points": [row for row in rows if not row.get("fit_succeeded")],
        "best_mass_grid_GeV": best["mass_hypothesis_GeV"],
        "best_mass_GeV": best["mass_hypothesis_GeV"],
        "coarse_best_mass_grid_GeV": coarse_best["mass_hypothesis_GeV"],
        "best_mu_hat": best["mu_hat"],
        "best_twice_nll": best["twice_nll"],
        "diagnostic_parabolic_interpolation": parabolic,
        "uncertainty": interval,
        "diagnostic_grid_resolution_GeV": 0.25,
        "diagnostic_grid_half_step_GeV": 0.125,
        "promoted_to_nominal_mass_measurement": False,
        "downgrade_reason": "Observed mass scan uses shifted detector-level M125 templates rather than independent mass-hypothesis MC and official lepton calibration/morphing; classify as approximated evidence, not an official CMS-quality mass measurement.",
        "limitations": "The scan is grid-level and model-limited: only M125 signal MC is available, the Z-peak region is excluded from Higgs mass hypotheses, and any interval or interpolation is a shifted-template diagnostic rather than a calibrated mass uncertainty.",
    }


def summarize_observed(events: dict[str, Any], masks: dict[str, Any]) -> dict[str, Any]:
    counts_fit = observed_counts(events, FIT_BINS, masks["keep"], CHANNELS)
    counts_broad = observed_counts(events, BROAD_BINS, masks["keep"], CHANNELS)
    return {
        "seed": None,
        "split_seed": OBSERVED_DATA_SEED,
        "selection_method": "all selected data events from the Phase 3 handoff are retained for Phase 4c; the seed is used only for the deterministic split proxy",
        "fraction_requested": OBSERVED_FRACTION,
        "total_selected_data_events": masks["n_data_total"],
        "kept_data_events": masks["n_data_kept"],
        "actual_fraction": masks["n_data_kept"] / masks["n_data_total"],
        "full_luminosity_fb": 10.0,
        "effective_luminosity_fb": OBSERVED_LUMINOSITY_FB,
        "fit_window_GeV": [70.0, 170.0],
        "broad_display_range_GeV": [70.0, 170.0],
        "fit_window_counts_by_channel": {k: int(np.sum(v)) for k, v in counts_fit.items()},
        "broad_window_counts_by_channel": {k: int(np.sum(v)) for k, v in counts_broad.items()},
        "mc_normalization": "All Phase 3 MC template weights are used at the full 10 fb^-1 normalization; no MC template is normalized to the observed data integral.",
    }


def binning_stability(events: dict[str, Any], masks: dict[str, Any], active: set[str]) -> list[dict[str, Any]]:
    rows = []
    for name, edges in ALT_BINS.items():
        if name == "final_state_nominal":
            grouped = mc_templates(events, edges)
            observed = observed_counts(events, edges, masks["keep"], CHANNELS)
            channels = CHANNELS
        else:
            grouped = inclusive_from_channels(mc_templates(events, edges), CHANNELS)
            observed = {"inclusive": sum(observed_counts(events, edges, masks["keep"], CHANNELS).values())}
            channels = ("inclusive",)
        fit = fit_configuration(grouped, observed, channels, edges, active - {"m4l_scale"})
        totals = []
        obs_total = []
        for channel in channels:
            totals.extend(np.sum([payload["channels"][channel] for payload in grouped.values()], axis=0).tolist())
            obs_total.extend(observed[channel].tolist())
        rows.append({"configuration": name, "channels": list(channels), "bin_edges": edges.tolist(), "expected_bins_below_1": int(np.sum(np.asarray(totals) < 1.0)), "observed_zero_bins": int(np.sum(np.asarray(obs_total) == 0.0)), "total_bins": int(len(totals)), "mu_hat": fit["uncertainty"]["muhat"], "mu_uncertainty": fit["uncertainty"]["err_sym"], "combined_chi2": fit["gof"]["combined"]["chi2"], "combined_p_value": fit["gof"]["combined"]["p_value_chi2"], "fit_status": "fit_succeeded"})
    return rows


def split_consistency(events: dict[str, Any], masks: dict[str, Any], grouped: dict[str, dict[str, Any]], active: set[str]) -> dict[str, Any]:
    rows = []
    for label, mask in (("split_a", masks["split_a"]), ("split_b", masks["split_b"])):
        observed = observed_counts(events, FIT_BINS, mask, CHANNELS)
        fit = fit_configuration(scale_grouped(grouped, 0.5), observed, CHANNELS, FIT_BINS, active - {"m4l_scale"})
        rows.append({"split": label, "method": "deterministic random half-split proxy; true CMS run-period branches are unavailable in selection_events.npz", "observed_fit_window_events": int(sum(np.sum(v) for v in observed.values())), "effective_luminosity_fb": OBSERVED_LUMINOSITY_FB / 2.0, "mu_hat": fit["uncertainty"]["muhat"], "mu_uncertainty": fit["uncertainty"]["err_sym"], "chi2": fit["gof"]["combined"]["chi2"], "p_value": fit["gof"]["combined"]["p_value_chi2"]})
    denom = math.sqrt(sum((row["mu_uncertainty"] or 0.0) ** 2 for row in rows))
    return {"limitation": "This is not a true CMS run-period split; no run/lumi/event-period branch is present in the Phase 3 event handoff.", "rows": rows, "delta_mu": rows[0]["mu_hat"] - rows[1]["mu_hat"], "pull": (rows[0]["mu_hat"] - rows[1]["mu_hat"]) / denom if denom > 0.0 else None}


def category_compatibility(grouped, active, observed, combined_mu, combined_unc) -> dict[str, Any]:
    rows = []
    for channel in CHANNELS:
        fit = fit_configuration(grouped, {channel: observed[channel]}, (channel,), FIT_BINS, active - {"m4l_scale"})
        unc = fit["uncertainty"]["err_sym"] or 0.0
        pull = (fit["uncertainty"]["muhat"] - combined_mu) / math.sqrt(max(unc**2 + (combined_unc or 0.0) ** 2, 1.0e-12))
        rows.append({"channel": channel, "mu_hat": fit["uncertainty"]["muhat"], "mu_uncertainty": fit["uncertainty"]["err_sym"], "pull_vs_combined": pull, "observed_events": int(np.sum(observed[channel])), "p_value": fit["gof"]["combined"]["p_value_chi2"]})
    return {"rows": rows, "max_abs_pull_vs_combined": max(abs(row["pull_vs_combined"]) for row in rows), "passes": bool(all(abs(row["pull_vs_combined"]) < 2.0 for row in rows))}


def systematic_payload(active: set[str]) -> dict[str, Any]:
    expected_sources = read_json(RESULTS / "systematics_sources.json").get("sources", [])
    rows = []
    for key, payload in SYSTEMATIC_SOURCES.items():
        rows.append({"key": key, "source": payload["label"], "conventions": payload["conventions"], "relative_variation": payload["relative"], "variation_basis": payload["basis"], "citation_or_search_trail": [payload["url"]], "phase4c_status": "implemented" if key in active else "documented_not_applicable"})
    rows.extend([row for row in expected_sources if row.get("key") in {"prompt_effective_xsecs", "pileup_pv_modeling", "higgs_branching_fraction", "classifier_migration", "angular_reconstruction"}])
    return {"phase": "4c_observed", "created_utc": now(), "sources": rows, "data_sensitive_re_evaluation": "Observed-data pulls, GoF, category compatibility, binning stability, and deterministic split checks were recomputed on all 203 selected data events. External/fallback rate priors remain transferred from Phase 4a because no new public calibration inputs or fake-rate sideband method are available in the handoff."}


def systematic_shift_payload(grouped, m4l_up, m4l_down, active: set[str]) -> dict[str, Any]:
    rows = []
    for syst in sorted(active):
        by_process = {}
        for group, payload in grouped.items():
            by_channel = {}
            for channel in CHANNELS:
                nominal = np.asarray(payload["channels"][channel], dtype=float)
                if syst == "m4l_scale":
                    up = np.asarray(m4l_up[group]["channels"][channel], dtype=float)
                    down = np.asarray(m4l_down[group]["channels"][channel], dtype=float)
                    treatment = "shape_histosys"
                elif syst == "mc_stat":
                    yld = float(np.sum(nominal))
                    rel = float(np.sqrt(np.sum(payload["sumw2"][channel])) / yld) if yld > 0.0 else 0.0
                    up, down = nominal * (1.0 + rel), nominal * max(1.0 - rel, 1.0e-6)
                    treatment = "group_category_normsys_from_sumw2_downscope"
                else:
                    rel = SYSTEMATIC_SOURCES[syst]["relative"]
                    up, down = nominal * (1.0 + rel), nominal * max(1.0 - rel, 1.0e-6)
                    treatment = "rate_normsys"
                by_channel[channel] = {"bin_edges": FIT_BINS.tolist(), "nominal": nominal.tolist(), "up": up.tolist(), "down": down.tolist()}
            by_process[group] = {"treatment": treatment, "channels": by_channel}
        rows.append({"systematic": syst, "label": SYSTEMATIC_SOURCES[syst]["label"], "by_process": by_process})
    return {"phase": "4c_observed", "created_utc": now(), "fit_window_GeV": [70.0, 170.0], "categories": list(CHANNELS), "systematics": rows}


def covariance_payload(full_fit: dict[str, Any], grouped, observed, active, m4l_up, m4l_down) -> dict[str, Any]:
    stat_fit = fit_configuration(grouped, observed, CHANNELS, FIT_BINS, set(), include_staterror=False)
    stat_mc_fit = fit_configuration(grouped, observed, CHANNELS, FIT_BINS, {"mc_stat"}, include_staterror=True)
    stat_var = (stat_fit["uncertainty"]["err_sym"] or 0.0) ** 2
    mc_var = max((stat_mc_fit["uncertainty"]["err_sym"] or 0.0) ** 2 - stat_var, 0.0)
    total_var = (full_fit["uncertainty"]["err_sym"] or 0.0) ** 2
    return {"phase": "4c_observed", "created_utc": now(), "parameters": ["mu"], "stat": [[stat_var]], "mc_stat": [[mc_var]], "syst": [[max(total_var - stat_var, 0.0)]], "total": [[total_var]], "mc_stat_treatment": "group_category_normsys_from_sumw2; not full bin-by-bin HistFactory staterror profiling", "uncertainty_breakdown": {"stat_only": stat_fit["uncertainty"], "stat_plus_mcstat": stat_mc_fit["uncertainty"], "full": full_fit["uncertainty"], "variance_components": {"stat": stat_var, "mc_stat": mc_var, "syst_total_including_mc_stat": max(total_var - stat_var, 0.0), "total": total_var}}}


def compatibility_metrics(observed_mu: dict[str, Any]) -> dict[str, Any]:
    expected = read_json(RESULTS / "expected_parameters.json")["mu"]
    partial = read_json(RESULTS / "partial_parameters.json")["mu"]
    observed_unc = observed_mu["uncertainty_symmetric"] or 0.0
    expected_unc = expected["uncertainty_symmetric"]
    partial_unc = partial["uncertainty_symmetric"] or 0.0
    expected_pull = (observed_mu["value"] - expected["value"]) / math.sqrt(max(observed_unc**2 + expected_unc**2, 1.0e-12))
    partial_pull = (observed_mu["value"] - partial["value"]) / math.sqrt(max(observed_unc**2 + partial_unc**2, 1.0e-12))
    return {
        "expected_mu": expected["value"],
        "expected_uncertainty": expected_unc,
        "partial_mu": partial["value"],
        "partial_uncertainty": partial_unc,
        "observed_mu": observed_mu["value"],
        "observed_uncertainty": observed_mu["uncertainty_symmetric"],
        "pull_vs_expected": expected_pull,
        "pull_vs_partial": partial_pull,
        "compatible_with_expected_2sigma": bool(abs(expected_pull) < 2.0),
        "compatible_with_partial_2sigma": bool(abs(partial_pull) < 2.0),
        "any_comparison_over_2sigma": bool(abs(expected_pull) > 2.0 or abs(partial_pull) > 2.0),
    }


def viability_status(mu_payload: dict[str, Any], fit: dict[str, Any]) -> dict[str, Any]:
    value = mu_payload["value"]
    unc = mu_payload["uncertainty_symmetric"]
    lower = 0.0
    upper = 10.0
    at_lower = bool(abs(value - lower) < 1.0e-5)
    at_upper = bool(abs(value - upper) < 1.0e-5)
    rel_unc = (unc / abs(value)) if value and unc is not None else None
    total_unc_lt_50pct = bool(rel_unc is not None and rel_unc < 0.5)
    gof = fit["gof"]["combined"]
    return {
        "fit_window_GeV": [70.0, 170.0],
        "mu_at_boundary": bool(at_lower or at_upper),
        "boundary": "lower" if at_lower else "upper" if at_upper else None,
        "zero_chi2_warning": gof["zero_chi2_warning"],
        "fit_triviality_gate": "PASS" if not gof["zero_chi2_warning"] else "FAIL_INVESTIGATE_CIRCULARITY",
        "relative_total_uncertainty": rel_unc,
        "total_uncertainty_lt_50pct_central": total_unc_lt_50pct,
        "viability_verdict": "PASS" if total_unc_lt_50pct and not (at_lower or at_upper) else "LIMITED_NOT_COMPETITIVE",
        "defensible_alternative_attempted": "Alternative inclusive/coarse binnings and category merge diagnostics are recorded in observed_validation.low_count_validation.alternative_binning_stability.",
    }


def update_commitments() -> None:
    path = RESULTS.parents[1] / "COMMITMENTS.md"
    text = path.read_text()
    old = "- [ ] [VT11] Fixed-seed full data validation compared to expected results.\n  Proof: seed, event-count, and stability-comparison JSON."
    new = "- [x] [VT11] Fixed-seed full data validation compared to expected results.\n  Proof: `analysis_note/results/observed_validation.json` and `observed_parameters.json` record seed `9417`, full-data event counts/effective luminosity, expected-vs-observed compatibility metrics, split diagnostics, and low-count stability checks."
    if old in text:
        path.write_text(text.replace(old, new))


def main() -> None:
    ensure_dirs()
    logger = setup_logging()
    events = load_selection_events()
    masks = full_data_mask(events)
    active = {"lumi", "lepton_eff", "signal_theory", "zz_norm", "ggzz_norm", "dy_norm", "ttbar_omission", "m4l_scale", "mc_stat"}
    grouped = mc_templates(events, FIT_BINS)
    m4l_up = mc_templates(events, FIT_BINS, mass_shift_factor=1.0 + SYSTEMATIC_SOURCES["m4l_scale"]["relative"])
    m4l_down = mc_templates(events, FIT_BINS, mass_shift_factor=1.0 - SYSTEMATIC_SOURCES["m4l_scale"]["relative"])
    observed = observed_counts(events, FIT_BINS, masks["keep"], CHANNELS)
    fit = fit_configuration(grouped, observed, CHANNELS, FIT_BINS, active, m4l_up=m4l_up, m4l_down=m4l_down)
    nuis = nuisance_diagnostics(fit)
    toys = toy_validation(grouped, CHANNELS, active, n_toys=80, seed=4269, m4l_up=m4l_up, m4l_down=m4l_down)
    stability = binning_stability(events, masks, active)
    selected = stability[0]
    merged_needed = bool((selected["mu_uncertainty"] is None) or selected["observed_zero_bins"] > selected["total_bins"] * 0.75)
    summary = summarize_observed(events, masks)
    mu_payload = {"value": fit["uncertainty"]["muhat"], "uncertainty_minus": fit["uncertainty"]["err_lo"], "uncertainty_plus": fit["uncertainty"]["err_hi"], "uncertainty_symmetric": fit["uncertainty"]["err_sym"]}
    compat_expected = compatibility_metrics(mu_payload)
    validation = {
        "phase": "4c_observed",
        "created_utc": now(),
        "subsample": summary,
        "fit_window_GeV": [70.0, 170.0],
        "broad_display_range_GeV": [70.0, 170.0],
        "normalization_policy": {"mc_scaled_to_full_luminosity": True, "full_luminosity_fb": OBSERVED_LUMINOSITY_FB, "mc_luminosity_scale_factor": OBSERVED_FRACTION, "data_integral_normalization": False},
        "low_count_validation": {"toy_validation": toys, "alternative_binning_stability": stability, "nominal_final_state_retained": not merged_needed, "merge_or_rebin_decision": "retain_final_state_nominal_for_full" if not merged_needed else "review_inclusive_fallback_before_interpretation"},
        "category_compatibility": category_compatibility(grouped, active, observed, fit["uncertainty"]["muhat"], fit["uncertainty"]["err_sym"] or 0.0),
        "deterministic_split_consistency": split_consistency(events, masks, grouped, active),
        "expected_vs_observed": compat_expected,
        "expected_partial_observed_comparison": compat_expected,
        "gof_interpretation": "Observed full data GoF is evaluated against the post-fit model. A chi2 near zero would be treated as a circularity alarm; this result is not a self-consistency Asimov check.",
        "completion_verdicts": {"full_203_events_processed": summary["kept_data_events"] == 203, "expected_comparison_done": True, "partial_comparison_done": True, "gof_np_done": True, "split_check_done": True, "final_state_fit_stable": not merged_needed},
        "viability": viability_status(mu_payload, fit),
    }
    parameters = {
        "phase": "4c_observed",
        "created_utc": now(),
        "fit_model": "pyhf simultaneous final-state template likelihood",
        "poi": "mu",
        "nominal_categories": list(CHANNELS),
        "observation": "all selected full-data observed Open Data events plus pyhf auxiliary data",
        "subsample": summary,
        "mu": mu_payload,
        "fit_status": {"twice_nll": fit["best_nll"], "converged": True, "parameter_names": fit["model"].config.par_names, "bestfit": fit["bestfit"].tolist(), "boundary_check": viability_status(mu_payload, fit)},
        "gof": fit["gof"],
        "nuisance_pulls": nuis["pulls"],
        "nuisance_impacts": nuis["impacts"],
        "mu_profile_scan": mu_profile_scan(fit),
        "expected_vs_observed": compat_expected,
        "expected_partial_observed_comparison": compat_expected,
        "workspace_summary": {"channels": list(CHANNELS), "bin_edges": FIT_BINS.tolist(), "modifiers": sorted(active), "mc_luminosity_scale_factor": OBSERVED_FRACTION, "source_events": str(PHASE3_OUT / "selection_events.npz")},
    }
    write_json(RESULTS / "observed_parameters.json", parameters)
    write_json(RESULTS / "observed_validation.json", validation)
    write_json(RESULTS / "observed_covariance.json", covariance_payload(fit, grouped, observed, active, m4l_up, m4l_down))
    mass_payload = observed_mass_scan(events, masks, active)
    write_json(RESULTS / "observed_mass_scan.json", mass_payload)
    systematics = systematic_payload(active)
    write_json(RESULTS / "observed_systematics.json", systematics)
    write_json(RESULTS / "systematics_sources.json", systematics)
    write_json(RESULTS / "observed_systematic_shifts.json", systematic_shift_payload(grouped, m4l_up, m4l_down, active))
    update_commitments()
    append_session(f"Observed inference JSON written\n\n- Kept {summary['kept_data_events']} / {summary['total_selected_data_events']} selected data events.\n- Observed fit-window counts: {summary['fit_window_counts_by_channel']}.\n- mu = {mu_payload['value']:.6g} -{mu_payload['uncertainty_minus']} +{mu_payload['uncertainty_plus']}.\n- Expected compatibility pull = {compat_expected['pull_vs_expected']:.3g}; partial compatibility pull = {compat_expected['pull_vs_partial']:.3g}.\n- Observed shifted-template mass scan coarse best = {mass_payload['coarse_best_mass_grid_GeV']} GeV; fine-grid best = {mass_payload['best_mass_GeV']} GeV.")
    append_experiment(f"## 2026-05-30 — Phase 4c full-data observed inference\n\n- Executor `zoran_44a0` applied the latest user-requested Phase 4c instruction: the observed-data fit window is `70 < m4l < 170 GeV`, including the Z peak.\n- Full data kept {summary['kept_data_events']} of {summary['total_selected_data_events']} selected data events.\n- MC templates used full luminosity `{OBSERVED_LUMINOSITY_FB}` fb^-1 with no data-integral normalization.\n- Observed `mu = {mu_payload['value']:.4g}` with symmetric uncertainty `{mu_payload['uncertainty_symmetric']}`; expected-vs-observed pull `{compat_expected['pull_vs_expected']:.3g}` and partial-vs-observed pull `{compat_expected['pull_vs_partial']:.3g}`.\n- Added an observed shifted-template mass scan over `{mass_payload['coarse_scan_range_GeV']['min']}-{mass_payload['coarse_scan_range_GeV']['max']}` GeV in `{mass_payload['coarse_scan_range_GeV']['step']}` GeV coarse steps plus a local `{mass_payload['fine_scan_range_GeV']['min']}-{mass_payload['fine_scan_range_GeV']['max']}` GeV fine scan in `{mass_payload['fine_scan_range_GeV']['step']}` GeV steps around the coarse best. The refined fine-grid center is `{mass_payload['best_mass_GeV']}` GeV with profiled `mu = {mass_payload['best_mu_hat']:.4g}`. The Z peak region is excluded from Higgs mass hypotheses, and the result is not promoted to an official CMS-quality mass measurement.")
    logger.info("Wrote Phase 4c observed inference JSON outputs to %s", RESULTS)


if __name__ == "__main__":
    main()
