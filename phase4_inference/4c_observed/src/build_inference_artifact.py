from __future__ import annotations

import math

from observed_common import OUT, RESULTS, append_experiment, append_session, ensure_dirs, now, read_json, setup_logging


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
    params = read_json(RESULTS / "observed_parameters.json")
    validation = read_json(RESULTS / "observed_validation.json")
    covariance = read_json(RESULTS / "observed_covariance.json")
    mass_scan = read_json(RESULTS / "observed_mass_scan.json")
    figures = read_json(OUT / "FIGURES.json")
    summary = params["subsample"]
    mu = params["mu"]
    gof = params["gof"]["combined"]
    expected = params["expected_vs_observed"]
    viability = validation["viability"]
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
    mass_rows = [
        [row["mass_hypothesis_GeV"], row.get("grid", "coarse"), row["mu_hat"], row["delta_twice_nll"], row["p_value_chi2"], row["fit_status"]]
        for row in mass_scan["scan_rows"]
    ]
    text = f"""# Phase 4c Observed-Data Inference

Session: `zoran_44a0`
Created: {now()}

## Summary

Phase 4c runs the reviewed Phase 4a final-state template likelihood on the full
observed dataset. Per the latest user instruction, the observed-data fit window
is `70 < m4l < 170 GeV`, including the Z peak. MC templates use the full
`{fmt(summary['effective_luminosity_fb'])} fb^-1` normalization; no template is
normalized to the observed data integral.

The full-data observed result is:

- `mu = {fmt(mu['value'])} -{fmt(mu['uncertainty_minus'])} +{fmt(mu['uncertainty_plus'])}`
- symmetric uncertainty: `{fmt(mu['uncertainty_symmetric'])}`
- expected-vs-observed pull: `{fmt(expected['pull_vs_expected'])}`
- partial-vs-observed pull: `{fmt(expected['pull_vs_partial'])}`
- compatibility with Phase 4a expected within 2 sigma: `{expected['compatible_with_expected_2sigma']}`
- compatibility with Phase 4b 10% result within 2 sigma: `{expected['compatible_with_partial_2sigma']}`
- viability verdict: `{viability['viability_verdict']}`
- observed shifted-template mass fine-grid best: `{fmt(mass_scan['best_mass_GeV'])} GeV`
- diagnostic grid half-step: `{fmt(mass_scan['diagnostic_grid_half_step_GeV'])} GeV`

## Full Dataset

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
    ['fit triviality gate', viability['fit_triviality_gate']],
    ['mu at boundary', viability['mu_at_boundary']],
    ['relative total uncertainty', viability['relative_total_uncertainty']],
    ['viability verdict', viability['viability_verdict']],
])}

This is an observed-data GoF against the post-fit model, not an Asimov
self-consistency check. The `zero_chi2_warning` flag is
`{gof['zero_chi2_warning']}`.

## Expected-Vs-Observed Compatibility

{table(['quantity', 'value'], [
    ['Phase 4a expected mu', expected['expected_mu']],
    ['Phase 4a expected uncertainty', expected['expected_uncertainty']],
    ['Phase 4b partial mu', expected['partial_mu']],
    ['Phase 4b partial uncertainty', expected['partial_uncertainty']],
    ['Phase 4c observed mu', expected['observed_mu']],
    ['Phase 4c observed uncertainty', expected['observed_uncertainty']],
    ['pull vs expected', expected['pull_vs_expected']],
    ['pull vs partial', expected['pull_vs_partial']],
    ['any comparison over 2 sigma', expected['any_comparison_over_2sigma']],
])}

## Low-Count And Binning Stability

{table(['configuration', 'channels', 'mu', 'uncertainty', 'observed zero bins', 'GoF p'], stability_rows)}

Nominal final-state model retained:
`{validation['low_count_validation']['nominal_final_state_retained']}`.
Decision: `{validation['low_count_validation']['merge_or_rebin_decision']}`.

Toy validation repeats the Phase 4a low-count stability check on the full-data
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
Phase 4c uses a documented deterministic random half-split proxy.

{table(['split', 'events', 'effective lumi fb^-1', 'mu', 'uncertainty', 'GoF p'], split_rows)}

Split pull: `{fmt(validation['deterministic_split_consistency']['pull'])}`.

## Nuisance Pulls And Impacts

Top nuisance impacts:

{table(['nuisance', 'mu shift down', 'mu shift up', 'max abs impact'], impact_rows)}

Full pull and impact payloads are in
`analysis_note/results/observed_parameters.json`.

## Uncertainty Breakdown

{table(['component', 'variance', 'uncertainty'], [
    ['stat', covariance['uncertainty_breakdown']['variance_components']['stat'], math.sqrt(covariance['uncertainty_breakdown']['variance_components']['stat'])],
    ['mc_stat', covariance['uncertainty_breakdown']['variance_components']['mc_stat'], math.sqrt(covariance['uncertainty_breakdown']['variance_components']['mc_stat'])],
    ['syst incl mc_stat', covariance['uncertainty_breakdown']['variance_components']['syst_total_including_mc_stat'], math.sqrt(covariance['uncertainty_breakdown']['variance_components']['syst_total_including_mc_stat'])],
    ['total', covariance['uncertainty_breakdown']['variance_components']['total'], math.sqrt(covariance['uncertainty_breakdown']['variance_components']['total'])],
])}

The grouped MC-stat treatment remains the reviewed Phase 4a approximation, not
a full bin-by-bin HistFactory staterror profile.

## Observed Mass Scan

The full-data follow-up does not assume the observed Higgs candidate peak is at
125 GeV. It scans shifted M125 detector-level templates with `mu` profiled at
each mass hypothesis. The likelihood still uses the broad `70 < m4l < 170 GeV`
fit bins, but the Z peak region is excluded from the Higgs mass-hypothesis grid.

{table(['quantity', 'value'], [
    ['scan min GeV', mass_scan['scan_range_GeV']['min']],
    ['scan max GeV', mass_scan['scan_range_GeV']['max']],
    ['coarse scan step GeV', mass_scan['coarse_scan_range_GeV']['step']],
    ['fine scan min GeV', mass_scan['fine_scan_range_GeV']['min']],
    ['fine scan max GeV', mass_scan['fine_scan_range_GeV']['max']],
    ['fine scan step GeV', mass_scan['fine_scan_range_GeV']['step']],
    ['coarse best mass grid GeV', mass_scan['coarse_best_mass_grid_GeV']],
    ['fine-grid best mass GeV', mass_scan['best_mass_GeV']],
    ['diagnostic grid half-step GeV', mass_scan['diagnostic_grid_half_step_GeV']],
    ['diagnostic parabolic best GeV', mass_scan['diagnostic_parabolic_interpolation']['best_mass_GeV']],
    ['best profiled mu', mass_scan['best_mu_hat']],
    ['uncertainty meaningful', mass_scan['uncertainty']['meaningful']],
    ['grid interval GeV', mass_scan['uncertainty']['interval_GeV']],
    ['promoted to nominal mass measurement', mass_scan['promoted_to_nominal_mass_measurement']],
])}

{table(['mH hypothesis GeV', 'grid', 'profiled mu', 'delta -2lnL', 'GoF p', 'fit status'], mass_rows)}

Limitations: {mass_scan['limitations']}

## Figures

{table(['figure', 'PNG', 'PDF'], fig_rows)}

## Findings And Resolutions

| Finding | Resolution | Evidence |
| --- | --- | --- |
| Phase 4a final-state workspace was sparse and required repeated observed-data stability checks. | Repeated toy validation, alternative inclusive/coarse binnings, category compatibility, and deterministic split checks on all selected full-data events. | `observed_validation.json`, `observed_binning_stability.png`, `observed_split_consistency.png` |
| True CMS run-period information is unavailable in the Phase 3 handoff. | Used a deterministic random half-split proxy and labelled it as a limitation, not a run-period validation. | `observed_validation.json` deterministic split section |
| Reducible background remains a DY+jets MC fake proxy rather than a full data-driven fake-rate estimate. | Preserved the Phase 2/3 scope and propagated the broad DY fake-proxy nuisance; no hand scaling to observed data integral was applied. | `observed_systematics.json`, `observed_m4l_broad_inclusive.png` |
| VBF and MVA/NN categories are not nominal categories. | Retained S1 final-state categories only; no VBF or classifier labels are used in the fit. | Phase 3 `selected_configuration.json`, `observed_parameters.json` |
| Full-data viability must be checked honestly. | Evaluated the boundary, fit-triviality, and total-uncertainty gates; if the result is not competitive the verdict remains `LIMITED_NOT_COMPETITIVE` rather than being tuned. | `observed_validation.json`, `observed_uncertainty_viability.png` |
| Data-sensitive systematics must be re-evaluated where possible. | Recomputed observed-data nuisance pulls, impacts, GoF, category compatibility, alternative binnings, and deterministic split diagnostics; external/fallback priors remain transferred because no new calibration or fake-rate inputs are available. | `observed_parameters.json`, `observed_systematics.json` |
| Full-data mass must not be assumed to be 125 GeV. | Added an observed shifted-template mass scan with `mu` profiled at each mass hypothesis; classified as approximate detector-level evidence rather than an official calibrated mass measurement. | `observed_mass_scan.json`, `observed_mass_scan.png` |

## Machine-Readable Outputs

- `analysis_note/results/observed_parameters.json`
- `analysis_note/results/observed_validation.json`
- `analysis_note/results/observed_covariance.json`
- `analysis_note/results/observed_mass_scan.json`
- `analysis_note/results/observed_systematics.json`
- `analysis_note/results/observed_systematic_shifts.json`
- `analysis_note/results/systematics_sources.json`
"""
    (OUT / "INFERENCE_OBSERVED.md").write_text(text)
    append_session("Observed inference artifact written\n\n- Wrote `phase4_inference/4c_observed/outputs/INFERENCE_OBSERVED.md`.")
    append_experiment("## 2026-05-30 — Phase 4c observed artifact\n\n- Built `phase4_inference/4c_observed/outputs/INFERENCE_OBSERVED.md` from full observed-data result JSONs.")
    logger.info("Wrote %s", OUT / "INFERENCE_OBSERVED.md")


if __name__ == "__main__":
    main()
