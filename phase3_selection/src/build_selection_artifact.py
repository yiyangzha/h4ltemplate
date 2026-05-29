from __future__ import annotations

import math
from pathlib import Path

from selection_common import FINAL_STATE_LABELS, OUT, append_experiment, append_session, model_display_name, read_json, sample_display_name, setup_logging


def table(headers: list[str], rows: list[list[object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(item) for item in row) + " |")
    return "\n".join(lines)


def fmt(value: object, digits: int = 3) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (int, str)):
        return str(value)
    try:
        numeric = float(value)
        if not math.isfinite(numeric):
            return "n/a"
        return f"{numeric:.{digits}g}"
    except Exception:
        return str(value)


def cutflow_table(cutflow: dict) -> str:
    steps = cutflow["steps"]
    rows = []
    for step in steps:
        data_row = next(item for item in cutflow["samples"]["cms_10fb_13TeV.root"]["all_channels"] if item["step"] == step)
        mc_yield = 0.0
        mc_raw = 0
        for sample, payload in cutflow["samples"].items():
            if sample == "cms_10fb_13TeV.root":
                continue
            item = next(row for row in payload["all_channels"] if row["step"] == step)
            mc_yield += item["weighted_yield"]
            mc_raw += item["raw_entries"]
        rows.append([step, data_row["raw_entries"], mc_raw, fmt(mc_yield), data_row["monotonic"]])
    return table(["Step", "Data events", "MC raw entries", "MC weighted yield", "Monotonic"], rows)


def input_table(validation: dict) -> str:
    rows = []
    for name, item in sorted(validation["variables"].items()):
        rows.append([name, fmt(item["chi2_per_ndf"]), item["ndf"], fmt(item["p_value"], 4), fmt(item["max_abs_shape_ratio_deviation"]), item["passes_d7_gate"]])
    return table(["Variable", "chi2/ndf", "ndf", "p", "max shape ratio deviation", "D7 pass"], rows)


def angular_table(closure: dict) -> str:
    rows = []
    for item in closure["samples"]:
        rows.append(
            [
                item["sample"],
                item["selected_broad_entries"],
                fmt(item["median_abs_diff_GeV"]["m4l"], 4),
                fmt(item["median_abs_diff_GeV"]["mZ1"], 4),
                fmt(item["median_abs_diff_GeV"]["mZ2"], 4),
                item["passes_0p1_GeV_median_gate"],
                sum(item["out_of_range_counts"].values()),
            ]
        )
    return table(["Sample", "Broad entries", "median dm4l [GeV]", "median dmZ1 [GeV]", "median dmZ2 [GeV]", "0.1 GeV gate", "out-of-range angles"], rows)


def sideband_table(sidebands: dict) -> str:
    rows = []
    for sample in ("DYJetsToLL.root", "TTBar.root", "cms_10fb_13TeV.root", "ZZTo4L.root"):
        payload = sidebands["samples"][sample]
        rows.append(
            [
                sample_display_name(sample),
                fmt(payload["low_sideband_70_105"]["weighted_yield"]),
                fmt(payload["signal_window_105_140"]["weighted_yield"]),
                fmt(payload["high_sideband_140_170"]["weighted_yield"]),
            ]
        )
    return table(["Sample", "70 <= m4l < 105", "105 < m4l < 140", "140 < m4l <= 170"], rows)


def cut_motivation_table(diagnostics: dict) -> str:
    rows = []
    summary = diagnostics["data_mc_summary"]
    for cut in diagnostics["cuts"]:
        key = cut["key"]
        for channel in diagnostics["channels"]:
            data = summary.get("Open data", {}).get(channel, {}).get(key, {})
            mc = summary.get("Open simulation total", {}).get(channel, {}).get(key, {})
            rows.append(
                [
                    cut["label"],
                    channel,
                    fmt(data.get("efficiency"), 4),
                    fmt(mc.get("efficiency"), 4),
                    data.get("numerator_raw_entries", "n/a"),
                    data.get("denominator_raw_entries", "n/a"),
                    fmt(mc.get("numerator_weighted_yield")),
                    fmt(mc.get("denominator_weighted_yield")),
                ]
            )
    return table(
        ["Cut", "Final state", "Data eff.", "MC eff.", "Data pass", "Data denom.", "MC pass", "MC denom."],
        rows,
    )


def s1_low_stat_table(viability: dict) -> str:
    rows = []
    for category in FINAL_STATE_LABELS:
        item = viability["by_category"][category]
        edges = item["bin_edges"]
        for idx, total in enumerate(item["total_expected_by_bin"]):
            rows.append(
                [
                    category,
                    f"{edges[idx]:g}-{edges[idx + 1]:g}",
                    fmt(item["signal_expected_by_bin"][idx]),
                    fmt(item["background_expected_by_bin"][idx]),
                    fmt(total),
                    fmt(total < viability["threshold_expected_events"]),
                ]
            )
    return table(["Category", "m4l bin [GeV]", "Signal", "Background", "S+B", "S+B < 5"], rows)


def mva_gate_table(mva: dict) -> str:
    rows = []
    for name, item in sorted(mva.get("models", {}).items()):
        gate = item["score_data_mc_gate"]
        viability = item["category_counts"]["viability"]
        rows.append(
            [
                model_display_name(name),
                fmt(item["auc"], 4),
                fmt(item["overtraining_signal_mean_gap"], 4),
                fmt(gate["chi2"], 4),
                gate["ndf"],
                fmt(gate["p_value"], 4),
                gate["passes"],
                fmt(viability["low_stat_bin_fraction"], 4),
                viability["passes"],
                item["passes"],
            ]
        )
    return table(
        [
            "Model",
            "AUC",
            "overtrain gap",
            "score chi2",
            "score ndf",
            "score p",
            "score gate",
            "low-stat bin fraction",
            "category gate",
            "all S2 gates",
        ],
        rows,
    )


def figure_table(figures: list[dict]) -> str:
    rows = [[item["id"], item["png"], item["pdf"]] for item in figures]
    return table(["Figure id", "PNG", "PDF"], rows)


def main() -> None:
    setup_logging()
    provenance = read_json(OUT / "selection_provenance.json")
    normalization = read_json(OUT / "normalization.json")
    cutflow = read_json(OUT / "cutflow.json")
    cut_motivation = read_json(OUT / "cut_motivation_diagnostics.json")
    sidebands = read_json(OUT / "sideband_fake_diagnostics.json")
    vbf = read_json(OUT / "vbf_recovery_downscope.json")
    angular = read_json(OUT / "angular_closure.json")
    validation = read_json(OUT / "input_validation.json")
    mva = read_json(OUT / "mva_metrics.json")
    comparison = read_json(OUT / "approach_comparison.json")
    figures = read_json(OUT / "FIGURES.json")
    s2_result = comparison["approaches"]["S2_angular_kinematic_classifier_categories"]
    s1_result = comparison["approaches"]["S1_reference_like_cut_and_channel_fit"]
    s1_viability = s1_result["final_state_bin_viability"]
    s1_low_summary = s1_viability["summary"]
    best_model_label = model_display_name(mva["promotion_decision"].get("best_model"))
    s2_best_model_label = model_display_name(s2_result.get("best_model"))
    norm_rows = [
        [item["sample"], item["group"], fmt(item["metadata_generated_events"]), fmt(item["xsec_pb_user_prompt"], 6), fmt(item["nominal_weight"], 6)]
        for item in normalization["records"]
        if item["kind"] == "mc"
    ]
    selected = comparison["selected_configuration"]
    text = f"""# Phase 3 Selection And Processing

Session: `magnus_d784`
Created from machine-readable Phase 3 outputs.

## Summary

Phase 3 implements the reviewed Phase 2 strategy using the primary prompt
ROOT paths only. The nominal Phase 4 handoff is `{selected}` with final-state
categories `4mu`, `4e`, and `2e2mu`, but this binning is conditional:
{s1_low_summary['final_state_bins_below_5_expected']}/{s1_low_summary['final_state_total_bins']}
final-state fit bins have `S+B < 5` and require Phase 4 low-count Poisson/toy
validation plus MC-stat stability checks before a result is reported. No VBF
category is used because the recovery gate found no real jet/VBF information in
the allowed flat ntuples. The S2 angular/kinematic classifier was attempted and
rejected by the input, score-shape, low-stat, and expected-precision gates.

## Data Source Freeze And Provenance

Nominal processing used the primary prompt data and MC paths recorded in
`paths.json`, not local copies. `selection_provenance.json` records file size,
tree entries, metadata denominators, branch counts, and jet-like branch
matches for every nominal input. `primary_paths_only_for_nominal` is
`{provenance['primary_paths_only_for_nominal']}`.

## MC Normalization

The MC normalization is `weight = sigma_eff_pb * L_pb / sum_Metadata_nEvents`
with `L = 10000 pb^-1`, as specified in Phase 2. No MC component is hand-scaled
to the data integral for fit inputs or yield plots.

{table(["Sample", "Group", "Metadata nEvents", "xsec [pb]", "nominal weight"], norm_rows)}

## Object Definitions And Final Selection

The ntuples already contain the best four-lepton candidate selected by the
ntuplizer. Phase 3 applies only event-level checks that can be audited from
retained branches:

- finite core four-lepton, Z-mass, and lepton variables;
- trigger bitmask requirement `trigBits != 0`, not equality to one integer;
- final-state categories inferred from retained lepton PDG IDs;
- flavor-matched lepton ID checks, using electron cut-based IDs only for
  electrons and muon PF+medium IDs only for muons;
- Z-pair sanity using retained `zId`, charge, flavor, `mZ1`, and `mZ2`;
- broad validation window `70 <= m4l <= 170 GeV` for sidebands and diagnostics;
- fit window `105 < m4l < 140 GeV` for fit-ready templates.

## Cutflow

{cutflow_table(cutflow)}

## Cut Motivation Diagnostics

Trigger, flavor-matched lepton-ID, and Z-pair sanity efficiencies are recorded
as step-to-previous-step ratios by final state. Data uses raw event counts, and
MC uses prompt-normalized weighted yields. The dedicated machine-readable source
is `cut_motivation_diagnostics.json`.

{cut_motivation_table(cut_motivation)}

## Categories And VBF Recovery/Downscope

The nominal categories are the final states `4mu`, `4e`, and `2e2mu`, retained
because the S2 classifier split fails and no real VBF category is available.
This is not an unconditional category/bin viability pass: the selected
final-state binning is a conditional Phase 4 handoff. The per-bin expected
`S+B` evidence is:

{s1_low_stat_table(s1_viability)}

The VBF recovery gate checked primary and local branch inventories, the current
allow-list, event-key join feasibility, and `h4l_ntuplize.py` provenance.
It found {len(vbf['primary_and_local_branch_checks'])} checked flat ntuples,
zero files with jet/VBF-like branches, zero allowed upstream join sources, and
`safe_event_key_join_possible = {vbf['join_check']['safe_event_key_join_possible']}`.
Decision: {vbf['decision']} No lepton-only category is labeled VBF.

## Angular Reconstruction And NN Gate

Four-vector closure passed before angular variables were considered. The
computed angular candidates have physical ranges in every checked selected
event. The angle definitions are detector-level candidates derived from the
retained lepton four-vectors and the Phase 2-cited H->4l angular references.

{angular_table(angular)}

## Input-Variable Modeling Gate

D7 was applied before classifier training. Shape comparisons use a data-area
normalization only for input-modeling diagnostics; nominal yields remain
prompt-luminosity normalized. Only variables passing `chi2/ndf <= 5` and no
coherent shape-ratio trend above 20 percent were eligible for S2 training.

{input_table(validation)}

Variables explicitly not promoted: `m4l` is excluded to avoid mass sculpting;
`pvNdof` and isolation-tail variables remain excluded under Phase 2 [A6].

## S1 Versus S2 Approach Comparison

{table(["Approach", "Metric/result"], [
    ["S1 reference-like final-state fit", "mu uncertainty proxy = " + fmt(s1_result["asimov_mu_uncertainty_proxy"]) + "; conditional low-count handoff"],
    ["S2 classifier categories", "best model = " + s2_best_model_label + ", relative improvement = " + fmt(s2_result.get("relative_improvement"))],
    ["Nominal selection", selected],
])}

S2 was not promoted. The best classifier is
{best_model_label} with a relative proxy change of
{fmt(mva['promotion_decision'].get('relative_improvement'))}; this is worse
than S1, not a >10 percent improvement. The detailed S2 gate table is:

{mva_gate_table(mva)}

The BDT score-shape gate passes, but its category-viability gate fails; the
logistic and small NN score-shape and category-viability gates both fail. No
trained classifier variant satisfies all S2 promotion gates.

## Fake And Sideband Diagnostics

DY+jets remains the nominal reducible fake proxy. The signal region is excluded
from sideband constraints. The TTBar diagnostic is not promoted to a nominal
component because the TTBar diagnostic / DY+jets fake-proxy ratios are below
the Phase 2 thresholds:
{sidebands['ttbar_decision']['ratios_ttbar_over_dy']}.

{sideband_table(sidebands)}

## Fit-Ready Handoff

The fit-ready handoff for Phase 4 is `fit_inputs_s1.json`. It contains
prompt-normalized `m4l` templates in `105 < m4l < 140 GeV`, bin edges
`[105, 112, 118, 122, 126, 130, 140]`, sumw2 arrays for MC-stat terms, and
final-state categories plus an inclusive diagnostic category. Phase 4 may use
the `4mu`, `4e`, and `2e2mu` categories for the simultaneous fit only after
low-count Poisson/toy validation and MC-stat stability checks. If those checks
fail, Phase 4 must rebin or merge categories before reporting a result. The
inclusive category is a diagnostic cross-check only and must not be fitted
simultaneously with the mutually exclusive final-state categories. The
broad-window templates are explicitly validation-only.

## Figures

{figure_table(figures)}

## Method Health And Open Issues

- Cutflow monotonicity: all sample/channel cumulative cutflows are monotonic.
- Cut motivation: trigger, lepton-ID, and Z-pair sanity efficiency diagnostics
  are recorded in `cut_motivation_diagnostics.json` and the registered
  `cut_motivation_efficiencies` figure.
- S1 binning: conditional handoff; low-count final-state bins must be validated
  in Phase 4 with toys/Poisson treatment and MC-stat stability.
- Angular closure: passed with median mass differences far below `0.1 GeV`.
- Classifier/NN: attempted and rejected; S2 diagnostics are preserved for the
  analysis note appendix as a serious rejected approach.
- VBF: formally downscoped for current flat ntuples; production-sensitive VBF
  comparisons are non-comparable unless future allowed inputs expose real jets.
- Reducible background: DY+jets MC is retained as the nominal fake proxy per
  user request and Phase 2 [D6]; this remains a comparability limitation versus
  CMS data-driven Z+X.
- Phase 4 must build the actual `pyhf`/HistFactory workspace, nuisance model,
  injection tests, GoF, pulls/impacts, and simultaneous mass-extraction attempt
  from these fit-ready inputs.

## Code Reference

Run the Phase 3 chain with `pixi run p3-all`. The full analysis chain through
Phase 3 is `pixi run all`.
"""
    (OUT / "SELECTION.md").write_text(text)
    append_session("2026-05-29 selection artifact\n\n- Wrote `phase3_selection/outputs/SELECTION.md`.")
    append_experiment("## 2026-05-29 — Phase 3 selection artifact\n\n- Built `phase3_selection/outputs/SELECTION.md` from Phase 3 JSON/NPZ outputs.")


if __name__ == "__main__":
    main()
