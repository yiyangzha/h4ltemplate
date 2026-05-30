from __future__ import annotations

import math

from partial_common import OUT, RESULTS, append_experiment, append_session, ensure_dirs, now, read_json, setup_logging


def fmt(value, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        if not math.isfinite(value):
            return "n/a"
        return f"{value:.{digits}g}"
    return str(value)


def table(headers: list[str], rows: list[list[object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(fmt(x) for x in row) + " |")
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    logger = setup_logging()
    params = read_json(RESULTS / "partial_parameters.json")
    validation = read_json(RESULTS / "partial_validation.json")
    covariance = read_json(RESULTS / "partial_covariance.json")
    figures = read_json(OUT / "FIGURES.json")
    summary = params["subsample"]
    mu = params["mu"]
    gof = params["gof"]["combined"]
    expected = params["expected_vs_partial"]
    stability_rows = [
        [row["configuration"], ", ".join(row["channels"]), row["mu_hat"], row["mu_uncertainty"], row["observed_zero_bins"], row["combined_p_value"]]
        for row in validation["low_count_validation"]["alternative_binning_stability"]
    ]
    channel_rows = [
        [row["channel"], row["observed_events"], row["mu_hat"], row["mu_uncertainty"], row["pull_vs_combined"], row["p_value"]]
        for row in validation["category_compatibility"]["rows"]
    ]
    split_rows = [
        [row["split"], row["observed_fit_window_events"], row["effective_luminosity_fb"], row["mu_hat"], row["mu_uncertainty"], row["p_value"]]
        for row in validation["deterministic_split_consistency"]["rows"]
    ]
    impact_rows = [
        [row["nuisance"], row["mu_shift_down"], row["mu_shift_up"], row["max_abs_impact"]]
        for row in params["nuisance_impacts"][:10]
    ]
    fig_rows = [[fig["id"], fig["png"], fig["pdf"]] for fig in figures]
    text = f"""# Phase 4b Partial-Data Inference

Session: `yuki_9d50`
Created: {now()}

## Summary

Phase 4b runs the reviewed Phase 4a final-state template likelihood on a
fixed-seed 10% observed-data subsample. Per the latest user-requested Phase 4b
override, the partial-data fit window is `70 < m4l < 170 GeV`, including the Z
peak. This replaces the earlier CMS-like `105 < m4l < 140 GeV` Phase 4b
instruction for this quick rerun only. MC templates are scaled by `0.10` to an effective
luminosity of `{fmt(summary['effective_luminosity_fb'])} fb^-1`; no template
is normalized to the observed data integral.

The 10% observed result is:

- `mu = {fmt(mu['value'])} -{fmt(mu['uncertainty_minus'])} +{fmt(mu['uncertainty_plus'])}`
- symmetric uncertainty: `{fmt(mu['uncertainty_symmetric'])}`
- expected-vs-partial pull: `{fmt(expected['pull_vs_expected'])}`
- compatibility with Phase 4a expected within 2 sigma: `{expected['compatible_with_expected_2sigma']}`

## Fixed-Seed Subsample

- seed: `{summary['seed']}`
- selection method: {summary['selection_method']}
- selected data events kept: `{summary['kept_data_events']}` of `{summary['total_selected_data_events']}` (`{fmt(summary['actual_fraction'])}`)
- fit-window event counts by channel: `{summary['fit_window_counts_by_channel']}`
- broad-window event counts by channel: `{summary['broad_window_counts_by_channel']}`
- normalization policy: {summary['mc_normalization']}

## Observed Fit And GoF

{table(['quantity', 'value'], [
    ['mu', mu['value']],
    ['uncertainty minus', mu['uncertainty_minus']],
    ['uncertainty plus', mu['uncertainty_plus']],
    ['chi2', gof['chi2']],
    ['ndf', gof['ndf']],
    ['chi2 p-value', gof['p_value_chi2']],
    ['Poisson deviance', gof['deviance']],
    ['deviance p-value', gof['p_value_deviance']],
])}

This is an observed-data GoF against the post-fit model, not an Asimov
self-consistency check. The `zero_chi2_warning` flag is
`{gof['zero_chi2_warning']}`.

## Expected-Vs-Partial Compatibility

{table(['quantity', 'value'], [
    ['Phase 4a expected mu', expected['expected_mu']],
    ['Phase 4a expected uncertainty', expected['expected_uncertainty']],
    ['Phase 4b partial mu', expected['partial_mu']],
    ['Phase 4b partial uncertainty', expected['partial_uncertainty']],
    ['pull', expected['pull_vs_expected']],
])}

## Low-Count And Binning Stability

{table(['configuration', 'channels', 'mu', 'uncertainty', 'observed zero bins', 'GoF p'], stability_rows)}

Nominal final-state model retained:
`{validation['low_count_validation']['nominal_final_state_retained']}`.
Decision: `{validation['low_count_validation']['merge_or_rebin_decision']}`.

Toy validation repeats the Phase 4a low-count stability check on the 10%
luminosity model:

{table(['quantity', 'value'], [
    ['toys', validation['low_count_validation']['toy_validation']['n_toys']],
    ['seed', validation['low_count_validation']['toy_validation']['seed']],
    ['fit success fraction', validation['low_count_validation']['toy_validation']['fit_success_fraction']],
    ['median mu', validation['low_count_validation']['toy_validation']['median_mu']],
    ['median bias vs mu=1', validation['low_count_validation']['toy_validation']['median_bias_vs_mu1']],
])}

## Per-Category Compatibility

{table(['channel', 'observed events', 'mu', 'uncertainty', 'pull vs combined', 'GoF p'], channel_rows)}

## Deterministic Split Proxy

True CMS run-period metadata is unavailable in the Phase 3 event handoff, so
Phase 4b uses a documented deterministic random half-split proxy.

{table(['split', 'events', 'effective lumi fb^-1', 'mu', 'uncertainty', 'GoF p'], split_rows)}

Split pull: `{fmt(validation['deterministic_split_consistency']['pull'])}`.

## Nuisance Pulls And Impacts

Top nuisance impacts:

{table(['nuisance', 'mu shift down', 'mu shift up', 'max abs impact'], impact_rows)}

Full pull and impact payloads are in
`analysis_note/results/partial_parameters.json`.

## Uncertainty Breakdown

{table(['component', 'variance', 'uncertainty'], [
    ['stat', covariance['uncertainty_breakdown']['variance_components']['stat'], math.sqrt(covariance['uncertainty_breakdown']['variance_components']['stat'])],
    ['mc_stat', covariance['uncertainty_breakdown']['variance_components']['mc_stat'], math.sqrt(covariance['uncertainty_breakdown']['variance_components']['mc_stat'])],
    ['syst incl mc_stat', covariance['uncertainty_breakdown']['variance_components']['syst_total_including_mc_stat'], math.sqrt(covariance['uncertainty_breakdown']['variance_components']['syst_total_including_mc_stat'])],
    ['total', covariance['uncertainty_breakdown']['variance_components']['total'], math.sqrt(covariance['uncertainty_breakdown']['variance_components']['total'])],
])}

The grouped MC-stat treatment remains the reviewed Phase 4a approximation, not
a full bin-by-bin HistFactory staterror profile.

## Figures

{table(['figure', 'PNG', 'PDF'], fig_rows)}

## Findings And Resolutions

| Finding | Resolution | Evidence |
| --- | --- | --- |
| Phase 4a final-state workspace was sparse and required repeated observed-data stability checks. | Repeated toy validation, alternative inclusive/coarse binnings, category compatibility, and deterministic split checks on the fixed-seed 10% data. | `partial_validation.json`, `partial_binning_stability.png`, `partial_split_consistency.png` |
| True CMS run-period information is unavailable in the Phase 3 handoff. | Used a deterministic random half-split proxy and labelled it as a limitation, not a run-period validation. | `partial_validation.json` deterministic split section |
| Reducible background remains a DY+jets MC fake proxy rather than a full data-driven fake-rate estimate. | Preserved the Phase 2/3 scope and propagated the broad DY fake-proxy nuisance; no hand scaling to observed data integral was applied. | `partial_systematics.json`, `partial_m4l_broad_inclusive.png` |
| VBF and MVA/NN categories are not nominal categories. | Retained S1 final-state categories only; no VBF or classifier labels are used in the fit. | Phase 3 `selected_configuration.json`, `partial_parameters.json` |
| Phase 4b must update VT11. | Marked VT11 resolved with seed, event counts, effective luminosity, expected comparison, and stability evidence. | `COMMITMENTS.md`, `partial_validation.json` |

## Machine-Readable Outputs

- `analysis_note/results/partial_parameters.json`
- `analysis_note/results/partial_validation.json`
- `analysis_note/results/partial_covariance.json`
- `analysis_note/results/partial_systematics.json`
- `analysis_note/results/partial_systematic_shifts.json`
- `analysis_note/results/systematics_sources.json`
"""
    (OUT / "INFERENCE_PARTIAL.md").write_text(text)
    append_session("Partial inference artifact written\n\n- Wrote `phase4_inference/4b_partial/outputs/INFERENCE_PARTIAL.md`.")
    append_experiment("## 2026-05-30 — Phase 4b partial artifact\n\n- Built `phase4_inference/4b_partial/outputs/INFERENCE_PARTIAL.md` from 10% observed-data result JSONs.")
    logger.info("Wrote %s", OUT / "INFERENCE_PARTIAL.md")


if __name__ == "__main__":
    main()
