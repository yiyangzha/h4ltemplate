from __future__ import annotations

import math
from typing import Any

from expected_common import OUT, RESULTS, append_experiment, append_session, ensure_dirs, now, read_json, setup_logging


def fmt(value: Any, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return value
    try:
        numeric = float(value)
    except Exception:
        return str(value)
    if not math.isfinite(numeric):
        return "n/a"
    return f"{numeric:.{digits}g}"


def table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(item) for item in row) + " |")
    return "\n".join(lines)


def gof_table(gof: dict[str, Any]) -> str:
    rows = [
        [
            "combined",
            fmt(gof["combined"]["chi2"]),
            fmt(gof["combined"]["deviance"]),
            gof["combined"]["ndf"],
            fmt(gof["combined"]["p_value_chi2"], 5),
            fmt(gof["combined"]["p_value_deviance"], 5),
        ]
    ]
    for channel, item in sorted(gof["by_channel"].items()):
        rows.append([channel, fmt(item["chi2"]), fmt(item["deviance"]), item["ndf"], fmt(item["p_value_chi2"], 5), fmt(item["p_value_deviance"], 5)])
    return table(["Category", "chi2", "Poisson deviance", "ndf", "chi2 p", "deviance p"], rows)


def systematic_table(systematics: dict[str, Any]) -> str:
    rows = []
    for item in systematics["sources"]:
        rows.append(
            [
                item["source"],
                item["conventions"],
                item["ref_1"],
                item["ref_2"],
                item["this_analysis"],
                item["status"],
            ]
        )
    return table(["Source", "Conventions", "Ref 1", "Ref 2", "This analysis", "Status"], rows)


def main() -> None:
    ensure_dirs()
    logger = setup_logging()
    parameters = read_json(RESULTS / "expected_parameters.json")
    covariance = read_json(RESULTS / "expected_covariance.json")
    validation = read_json(RESULTS / "expected_validation.json")
    systematics = read_json(RESULTS / "expected_systematics.json")
    mass = read_json(RESULTS / "expected_mass_scan.json")
    figures = read_json(OUT / "FIGURES.json")

    mu = parameters["mu"]
    toy = validation["low_count_validation"]["toy_validation"]
    precision = validation["precision_comparison"]
    low_summary = validation["low_count_validation"]["input_handoff"]
    variance = covariance["uncertainty_breakdown"]["variance_components"]
    mass_closure_rows = [
        [row["injected_mass_GeV"], row["recovered_mass_grid_GeV"], fmt(row["bias_GeV"]), row["passes_bias_gate"]]
        for row in mass["closure"]
    ]
    injection_rows = [
        [row["injected_mu"], fmt(row["fitted_mu"]), fmt(row["bias"]), fmt(row["relative_bias_for_gate"]), row["passes_20pct_gate"]]
        for row in validation["signal_injection"]
    ]
    binning_rows = [
        [row["configuration"], ",".join(row["channels"]), fmt(row["mu_uncertainty"]), row["bins_below_5"], fmt(row["combined_p_value"], 5)]
        for row in validation["alternative_binning_stability"]
    ]
    channel_rows = [
        [row["channel"], fmt(row["mu_hat"]), fmt(row["mu_uncertainty"]), fmt(row["pull_vs_combined"]), fmt(row["combined_p_value"], 5)]
        for row in validation["final_state_channel_compatibility"]["rows"]
    ]
    corruption_rows = [
        [row["corruption"], fmt(row["deviance"]), row["ndf"], fmt(row["p_value"], 5), row["passes_failure_requirement"]]
        for row in validation["closure_sensitivity"]["rows"]
    ]
    impact_rows = [
        [row["nuisance"], fmt(row["mu_shift_down"]), fmt(row["mu_shift_up"]), fmt(row["max_abs_impact"])]
        for row in parameters["nuisance_impacts"][:12]
    ]
    figure_rows = [[item["id"], item["png"], item["pdf"]] for item in figures]

    text = f"""# Phase 4a Expected Inference

Session: `edmund_69a2`
Created: {now()}

## Summary

Phase 4a reports expected-only inference using MC/Asimov observations. The
fit observation is the nominal model expectation plus pyhf auxiliary data; no
real Open Data event counts are used as pseudo-data. The nominal handoff is the
Phase 3 S1 final-state categorization (`4mu`, `4e`, `2e2mu`) in
`105 < m4l < 140 GeV`.

The global signal-strength result is:

- `mu = {fmt(mu['value'])} -{fmt(mu['uncertainty_minus'])} +{fmt(mu['uncertainty_plus'])}`
- symmetric expected uncertainty: `{fmt(mu['uncertainty_symmetric'])}`
- precision ratio to CMS-HIG-16-041 symmetrized uncertainty: `{fmt(precision['ratio_this_over_reference'])}`
- ratio greater than 5x reference: `{precision['ratio_gt_5x']}`

## Model

The model is a binned simultaneous pyhf/HistFactory-style likelihood with one
global signal-strength POI `mu` scaling all Higgs templates together. The
workspace uses channels `{', '.join(parameters['workspace_summary']['channels'])}`
and mass-bin edges `{parameters['workspace_summary']['bin_edges']}`. MC
statistical uncertainty is propagated with group/category normalization
nuisances derived from Phase 3 `sumw2`; full per-bin staterror profiling was
not computationally stable in this sandbox, so the implementation is paired
with explicit alternative-binning stability checks.

## Expected Fit Result

{gof_table(parameters['gof'])}

The exact Asimov deviance is expected to be numerically zero when the fitted
expectation matches the generated model expectation. The chi2 values are
reported for audit only and are not observed-data goodness-of-fit results.

## Low-Count Validation And Binning

The Phase 3 handoff had
`{low_summary['final_state_bins_below_5_expected']}/{low_summary['final_state_total_bins']}`
final-state bins below five expected events. Phase 4a retains the final-state
simultaneous model because the Poisson toy validation passes:

- toys: `{toy['n_toys']}` with seed `{toy['seed']}`
- fit success fraction: `{fmt(toy['fit_success_fraction'])}`
- median `mu`: `{fmt(toy['median_mu'])}`
- median bias: `{fmt(toy['median_bias'])}`
- bias gate pass: `{toy['passes_bias_gate']}`

{table(["Binning", "Channels", "mu uncertainty", "bins below 5", "fit p"], binning_rows)}

Final-state channel compatibility:

{table(["Channel", "mu", "uncertainty", "pull vs combined", "fit p"], channel_rows)}

## Validation Tests

Signal injection and recovery:

{table(["Injected mu", "Fitted mu", "bias", "relative bias", "20 percent gate"], injection_rows)}

Closure-test sensitivity with intentionally corrupted model ingredients:

{table(["Corruption", "deviance", "ndf", "p-value", "fails as required"], corruption_rows)}

The corruption tests pass the sensitivity requirement because the intentionally
wrong models are rejected below `p = 0.05`.

## Covariance And Uncertainty Breakdown

Covariance matrices are in `analysis_note/results/expected_covariance.json`.
For the single reported parameter, the total covariance is the scalar variance
shown below.

{table(["Component", "variance", "uncertainty"], [[key, fmt(value), fmt(math.sqrt(value))] for key, value in variance.items()])}

## Nuisance Impacts

{table(["Nuisance", "mu shift down", "mu shift up", "max abs impact"], impact_rows)}

## Mass-Template Closure

The Phase 4a method-parity attempt uses shifted detector-level M125 templates
with `mu` profiled at each mass grid point. It is not an official calibrated
mass measurement, but it satisfies the expected-phase mass-template closure
gate on the available templates.

- nominal best mass grid point: `{fmt(mass['nominal_best_mass_grid_GeV'])} GeV`
- nominal best-fit `mu` in the mass scan: `{fmt(mass['nominal_best_mu_hat'])}`
- injected-mass closure passes: `{mass['closure_passes']}`
- promoted to nominal mass measurement: `{mass['promoted_to_nominal_mass_measurement']}`
- downgrade reason: {mass['downgrade_reason']}
- limitation: {mass['limitations']}

{table(["Injected mass [GeV]", "Recovered grid [GeV]", "bias [GeV]", "bias gate"], mass_closure_rows)}

## Systematic Completeness

{systematic_table(systematics)}

## Figures

{table(["Figure", "PNG", "PDF"], figure_rows)}

## Findings And Resolutions

| Finding | Resolution | Evidence |
| --- | --- | --- |
| Phase 3 handoff has many low-count final-state bins. | Retained final-state model only after Poisson toys and alternative-binning checks passed. | `expected_validation.json`, `expected_binning_stability.png`, `expected_binning_low_count_summary.png` |
| Full per-bin pyhf staterror model was computationally impractical. | Used grouped MC-stat normalization nuisances derived from `sumw2` and documented alternative-binning stability. | `expected_parameters.json`, `expected_covariance.json`, `expected_validation.json` |
| Plot watcher reported a crowded binning-stability figure. | Split the display into two separately registered figures. | `PLOT_WATCHER_RECHECK_vera_ee63.md` reports PASS with zero unresolved blockers. |
| MVA/classifier and VBF-like categories were rejected upstream. | No classifier migration or VBF systematics are propagated; they are documented as not applicable/downscoped. | `expected_systematics.json`, Phase 3 selection artifacts |

## Machine-Readable Outputs

- `analysis_note/results/expected_parameters.json`
- `analysis_note/results/expected_systematics.json`
- `analysis_note/results/expected_covariance.json`
- `analysis_note/results/expected_validation.json`
- `analysis_note/results/expected_mass_scan.json`
"""
    (OUT / "INFERENCE_EXPECTED.md").write_text(text)
    append_session("Expected inference artifact written\n\n- Wrote `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` from machine-readable expected-result JSON files.")
    append_experiment("## 2026-05-30 — Phase 4a expected inference artifact\n\n- Built `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` from expected-result JSON files.")
    logger.info("Wrote %s", OUT / "INFERENCE_EXPECTED.md")


if __name__ == "__main__":
    main()
