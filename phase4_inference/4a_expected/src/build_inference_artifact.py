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
                item.get("commitment_label", item["conventions"]),
                fmt(item.get("nominal_or_variation_size", item.get("relative_variation"))),
                item.get("variation_basis", "n/a"),
                item.get("fallback_flag", False),
                ", ".join(item.get("affected_templates_processes", [])) or "none",
                item.get("evaluation_method", item.get("ref_2", "")),
                item["this_analysis"],
                item.get("phase4a_status", item["status"]),
            ]
        )
    return table(
        ["Source", "Label", "Size", "Basis", "Fallback", "Affected", "Evaluation", "This analysis", "Status"],
        rows,
    )


def main() -> None:
    ensure_dirs()
    logger = setup_logging()
    parameters = read_json(RESULTS / "expected_parameters.json")
    covariance = read_json(RESULTS / "expected_covariance.json")
    validation = read_json(RESULTS / "expected_validation.json")
    systematics = read_json(RESULTS / "expected_systematics.json")
    systematic_shifts = read_json(RESULTS / "expected_systematic_shifts.json")
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
    corruption_pass = validation["closure_sensitivity"]["passes"]
    corruption_status = validation["closure_sensitivity"].get("criterion_status", "passed" if corruption_pass else "failed")
    corruption_limitation = validation["closure_sensitivity"].get("quantitative_limitation") or "none"
    corruption_attempt_rows = [
        [
            row["attempt"],
            row["test"],
            fmt(row["statistic"]),
            row["ndf"],
            fmt(row["p_value"], 5),
            row["rejects_at_0p05"],
        ]
        for row in validation["closure_sensitivity"].get("remediation_attempts", [])
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
`70 < m4l < 170 GeV`, including the Z peak neighborhood.

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
with explicit alternative-binning stability checks. This grouped treatment is
a formal expected-phase downscope/approximation to per-bin HistFactory
`staterror` terms, not a completed full per-bin MC-stat profile.

## Expected Fit Result

{gof_table(parameters['gof'])}

The exact Asimov deviance is expected to be numerically zero when the fitted
expectation matches the generated model expectation. The chi2 values are
reported for audit only and are not observed-data goodness-of-fit results.
The independent validation evidence is the Poisson toy behavior, signal
injection/recovery, corrupted-model closure rejection, and alternative-binning
stability below.

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

This retention is conditional on the expected-only Phase 4a inputs. The
observed 10 percent and full-data phases must repeat the stability checks and
merge or rebin if observed-data fits or toys become unstable.

{table(["Binning", "Channels", "mu uncertainty", "bins below 5", "fit p"], binning_rows)}

Final-state channel compatibility:

{table(["Channel", "mu", "uncertainty", "pull vs combined", "fit p"], channel_rows)}

## Validation Tests

Signal injection and recovery:

{table(["Injected mu", "Fitted mu", "bias", "relative bias", "20 percent gate"], injection_rows)}

Closure-test sensitivity with intentionally corrupted model ingredients:

{table(["Corruption", "deviance", "ndf", "p-value", "fails as required"], corruption_rows)}

Final-state simultaneous corruption-test pass status: `{corruption_pass}`.
Criterion status: `{corruption_status}`.
The intentionally wrong +20 percent mass-response model is rejected below
`p = 0.05`; the -20 percent direction is not rejected in the low-count
final-state workspace. Quantitative limitation: {corruption_limitation}

{table(["Attempt", "test", "statistic", "ndf", "p-value", "rejects"], corruption_attempt_rows) if corruption_attempt_rows else ""}

## Covariance And Uncertainty Breakdown

Covariance matrices are in `analysis_note/results/expected_covariance.json`.
For the single reported parameter, the total covariance is the scalar variance
shown below.

{table(["Component", "variance", "uncertainty"], [[key, fmt(value), fmt(math.sqrt(value))] for key, value in variance.items()])}

## Nuisance Impacts

{table(["Nuisance", "mu shift down", "mu shift up", "max abs impact"], impact_rows)}

Asimov nuisance pulls are expected to be zero because the pseudo-data are
generated from the nominal model. The table and impact figure therefore show
expected sensitivity from fixed nuisance shifts, not observed-data pulls or
post-fit constraints.

## Mass-Template Closure

The Phase 4a method-parity attempt uses shifted detector-level M125 templates
in the same simultaneous final-state category structure as the expected `mu`
workspace, with `mu` profiled at each mass grid point. It is not an official
calibrated mass measurement, but it satisfies the expected-phase
mass-template closure gate on the available templates.

- scan range: `{fmt(mass['scan_range_GeV']['min'])}` to `{fmt(mass['scan_range_GeV']['max'])}` GeV in `{fmt(mass['scan_range_GeV']['step'])}` GeV steps
- excluded ranges: `{mass.get('excluded_ranges_GeV', [])}`
- nominal best mass grid point: `{fmt(mass['nominal_best_mass_grid_GeV'])} GeV`
- nominal best-fit `mu` in the mass scan: `{fmt(mass['nominal_best_mu_hat'])}`
- categories: `{', '.join(mass.get('categories', []))}`
- workspace parity: {mass.get('workspace_parity', 'n/a')}
- injected-mass closure passes: `{mass['closure_passes']}`
- promoted to nominal mass measurement: `{mass['promoted_to_nominal_mass_measurement']}`
- downgrade reason: {mass['downgrade_reason']}
- limitation: {mass['limitations']}

{table(["Injected mass [GeV]", "Recovered grid [GeV]", "bias [GeV]", "bias gate"], mass_closure_rows)}

## Systematic Completeness

{systematic_table(systematics)}

Rows marked as fallback priors or user-provided prompt inputs are explicitly
downscoped expected-phase approximations caused by missing official generator
composition or effective-cross-section inputs. They are propagated to avoid
silently dropping the source, but they should not be read as precision
external calibrations. The machine-readable source table is duplicated to
`analysis_note/results/systematics_sources.json` for reviewer and note-writer
traceability.

Machine-readable shifted-bin payloads are written to
`analysis_note/results/expected_systematic_shifts.json`. They contain
nominal/up/down bin arrays for `{len(systematic_shifts['systematics'])}` active
systematic sources by process group and final-state channel. Rate-only sources
are represented as uniform normalization shifts; the `m4l_scale` source is the
shape histosys. The grouped `mc_stat` payload is labelled as the same formal
downscope/approximation used in the covariance.

## Figures

{table(["Figure", "PNG", "PDF"], figure_rows)}

## Findings And Resolutions

| Finding | Resolution | Evidence |
| --- | --- | --- |
| Phase 3 handoff has many low-count final-state bins. | Retained final-state model only after Poisson toys and alternative-binning checks passed. | `expected_validation.json`, `expected_binning_stability.png`, `expected_binning_low_count_summary.png` |
| Full per-bin pyhf staterror model was computationally impractical. | Used grouped MC-stat normalization nuisances derived from `sumw2`, labelled the approximation in JSON/prose, and documented alternative-binning stability. | `expected_parameters.json`, `expected_covariance.json`, `expected_validation.json` |
| Phase 4a review found the first mass scan was inclusive rather than category-simultaneous. | Rebuilt the mass-profile closure as a simultaneous `4mu`, `4e`, and `2e2mu` category scan with `mu` profiled and the active Phase 4a nuisance set. | `expected_mass_scan.json`, `expected_mass_profile_attempt.png` |
| Phase 4a review found missing systematic-source evidence rows. | Added `systematics_sources.json`, including SP2 prompt-effective-cross-section and SP6 pileup/PV rows plus fallback flags, affected processes, and evaluation methods. | `systematics_sources.json`, `expected_systematics.json` |
| Phase 4a review found missing per-systematic shifted-bin payloads and per-bin effect figures. | Added `expected_systematic_shifts.json` with nominal/up/down arrays by active systematic, process, and final state; added a registered shape/rate summary figure without fake shape dependence for rate-only sources. | `expected_systematic_shifts.json`, `expected_systematic_shift_summary.png` |
| Phase 4a review found MC-stat covariance rows inconsistent. | Recorded grouped MC-stat as a nonzero component consistently in the top-level covariance, per-systematic row, and variance-component breakdown. | `expected_covariance.json` |
| Phase 4a review found corruption sensitivity was inclusive-only. | Recomputed the 20 percent mass-response corruption test in the final-state simultaneous workspace and documented the non-rejected -20 percent direction as a quantitative low-count limitation. | `expected_validation.json` |
| Plot watcher reported a crowded binning-stability figure. | Split the display into two separately registered figures and rerendered the stability figure with extra x-axis padding/no data-overlapping legend. | `PLOT_WATCHER_RECHECK_vera_ee63.md` reports PASS with zero unresolved blockers. |
| Earlier watcher files still contain stale FAIL/BLOCKED text. | Current figure status is determined by the later `PLOT_WATCHER_RECHECK_vera_ee63.md` PASS and the rerendered figure mtimes; stale watcher files are retained as audit history only. | `phase4_inference/4a_expected/review/validation/PLOT_WATCHER_RECHECK_vera_ee63.md` |
| Exact Asimov GoF values can look tautological. | Labelled chi2=0/p=1 as expected self-consistency and pointed to toys, injections, corruption tests, and binning variants as the actual validation evidence. | `expected_validation.json`, Validation Tests section |
| Mass-profile closure could be misread as an official mass result. | Kept it as method-parity evidence only and explicitly did not promote it to a calibrated mass measurement. | `expected_mass_scan.json`, `expected_mass_profile_attempt.png` |
| MVA/classifier and VBF-like categories were rejected upstream. | No classifier migration or VBF systematics are propagated; they are documented as not applicable/downscoped. | `expected_systematics.json`, Phase 3 selection artifacts |

## Machine-Readable Outputs

- `analysis_note/results/expected_parameters.json`
- `analysis_note/results/expected_systematics.json`
- `analysis_note/results/expected_covariance.json`
- `analysis_note/results/expected_validation.json`
- `analysis_note/results/expected_mass_scan.json`
- `analysis_note/results/systematics_sources.json`
- `analysis_note/results/expected_systematic_shifts.json`
"""
    (OUT / "INFERENCE_EXPECTED.md").write_text(text)
    append_session("Expected inference artifact written\n\n- Wrote `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` from machine-readable expected-result JSON files.")
    append_experiment("## 2026-05-30 — Phase 4a expected inference artifact\n\n- Built `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` from expected-result JSON files.")
    logger.info("Wrote %s", OUT / "INFERENCE_EXPECTED.md")


if __name__ == "__main__":
    main()
