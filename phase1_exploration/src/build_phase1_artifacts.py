from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from phase1_utils import (
    LUMI_PB,
    OUT,
    RETRIEVAL_LOG,
    SAMPLE_INFO,
    append_experiment,
    append_session,
    ensure_dirs,
    read_json,
    setup_logging,
)


SOURCES = {
    "CMS-HIG-16-041": "CMS-HIG-16-041 / JHEP 11 (2017) 047 public page, arXiv:1706.09936, DOI 10.1007/JHEP11(2017)047: https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-16-041/",
    "HEPData-80189": "HEPData record for CMS-HIG-16-041, DOI 10.17182/hepdata.80189: https://www.hepdata.net/record/ins1608166",
    "CMS-LUM-20-001": "CMS-PAS-LUM-20-001 public page for CMS 2017 luminosity: https://cms-results.web.cern.ch/cms-results/public-results/preliminary-results/LUM-20-001/",
    "PDG-2024": "PDG 2024 Gauge and Higgs Bosons Summary Table, Phys. Rev. D 110, 030001 (2024): https://pdg.lbl.gov/2024/tables/rpp2024-sum-gauge-higgs-bosons.pdf",
}


def md_table(headers: list[str], rows: list[list[object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(item) for item in row) + " |")
    return "\n".join(out)


def load_optional(path: Path) -> dict:
    return read_json(path) if path.exists() else {}


def branch_inventory(metadata: dict) -> str:
    lines = []
    for file_record in metadata.get("files", []):
        sample = file_record.get("sample_info", {})
        lines.append(f"### `{file_record['role']}/{file_record['name']}`")
        lines.append("")
        lines.append(f"- Path: `{file_record['path']}`")
        lines.append(f"- Size: {file_record['size_bytes']} bytes")
        if sample:
            lines.append(f"- Prompt cross section: {sample.get('xsec_pb')} pb")
            lines.append(f"- Full sample name: `{sample.get('fullname')}`")
        tree_rows = []
        for tree_name, tree in file_record.get("trees", {}).items():
            tree_rows.append([tree_name, tree["num_entries"], len(tree["branches"])])
        lines.append(md_table(["Tree", "Entries", "Branches"], tree_rows or [["none", 0, 0]]))
        lines.append("")
        for tree_name, tree in file_record.get("trees", {}).items():
            lines.append(f"#### Branches in `{tree_name}`")
            rows = [
                [branch, info.get("typename", ""), info.get("interpretation", ""), info.get("num_entries", "")]
                for branch, info in sorted(tree["branches"].items())
            ]
            lines.append(md_table(["Branch", "Type", "Interpretation", "Entries"], rows))
            lines.append("")
    return "\n".join(lines)


def unique_survey(slice_recon: dict) -> str:
    lines = []
    for file_record in slice_recon.get("files", []):
        for tree_name, tree in file_record.get("trees", {}).items():
            rows = []
            for branch, summary in sorted(tree.get("branches", {}).items()):
                survey = summary.get("unique_survey")
                if not survey:
                    continue
                values = ", ".join(f"{item['value']}({item['count']})" for item in survey["values"][:12])
                if survey.get("truncated"):
                    values += ", ..."
                rows.append([
                    file_record["name"],
                    tree_name,
                    branch,
                    survey["n_unique"],
                    summary.get("min", ""),
                    summary.get("max", ""),
                    summary.get("mean", ""),
                    values,
                ])
            if rows:
                lines.append(md_table(["File", "Tree", "Branch", "N unique", "Min", "Max", "Mean", "Values(counts)"], rows))
                lines.append("")
    return "\n".join(lines) if lines else "No integer/flag-like branches were found in the small-slice survey.\n"


def data_quality(slice_recon: dict) -> str:
    rows = []
    for file_record in slice_recon.get("files", []):
        for tree_name, tree in file_record.get("trees", {}).items():
            nan = 0
            inf = 0
            numeric = 0
            for summary in tree.get("branches", {}).values():
                if summary.get("numeric"):
                    numeric += 1
                    nan += int(summary.get("nan_count", 0))
                    inf += int(summary.get("inf_count", 0))
            rows.append([file_record["name"], tree_name, tree["entries_loaded"], numeric, nan, inf])
    return md_table(["File", "Tree", "Entries loaded", "Numeric branches", "NaN count", "Inf count"], rows)


def branch_availability(metadata: dict) -> str:
    primary_branches = set()
    for file_record in metadata.get("files", []):
        if not file_record.get("is_primary"):
            continue
        for tree in file_record.get("trees", {}).values():
            primary_branches.update(tree.get("branches", {}).keys())
    checks = [
        ("Four-lepton mass", ("m4l",)),
        ("Z candidate masses", ("mZ1", "mZ2")),
        ("Four-lepton kinematics", ("pt4l", "eta4l", "phi4l")),
        ("Per-lepton four-vector inputs", ("l1pt", "l1eta", "l1phi", "l1mass", "l4pt", "l4eta", "l4phi", "l4mass")),
        ("Jet/VBF observables", ("nJet", "nJets", "jetPt", "mjj", "detajj", "j1pt", "j2pt")),
        ("Angular primitives", ("phi4l", "l1phi", "l2phi", "l3phi", "l4phi")),
        ("Precomputed MELA/angular discriminants", ("D_bkg_kin", "Dsig", "KD", "costheta", "cosTheta", "mela")),
        ("Generator/truth branches", ("gen", "truth", "lhe", "mother", "status")),
    ]
    rows = []
    lower_map = {branch.lower(): branch for branch in primary_branches}
    for topic, tokens in checks:
        matches = sorted(
            branch
            for branch in primary_branches
            if any(token.lower() in branch.lower() for token in tokens)
        )
        rows.append([topic, "FOUND" if matches else "NOT FOUND", ", ".join(matches[:20]) if matches else "none in primary h4lTree/Metadata branches"])
    return md_table(["Capability", "Status", "Matching branches"], rows)


def primary_local_comparison(metadata: dict) -> str:
    by_name: dict[str, dict[str, dict]] = defaultdict(dict)
    for file_record in metadata.get("files", []):
        by_name[file_record["name"]][file_record["role"]] = file_record
    rows = []
    for name, roles in sorted(by_name.items()):
        primary = roles.get("primary_data") or roles.get("primary_mc")
        local = roles.get("local_data") or roles.get("local_mc")
        if not primary or not local:
            continue
        primary_entries = {tree: info["num_entries"] for tree, info in primary.get("trees", {}).items()}
        local_entries = {tree: info["num_entries"] for tree, info in local.get("trees", {}).items()}
        rows.append([
            name,
            primary["size_bytes"],
            local["size_bytes"],
            primary_entries,
            local_entries,
            "same" if primary["size_bytes"] == local["size_bytes"] and primary_entries == local_entries else "different",
        ])
    return md_table(["File", "Primary size", "Local size", "Primary tree entries", "Local tree entries", "Verdict"], rows)


def write_data_recon(metadata: dict, slice_recon: dict, coverage: dict, figures: list[dict]) -> None:
    coverage_rows = []
    for record in coverage.get("records", []):
        coverage_rows.append(
            [
                record["name"],
                record["kind"],
                record.get("events_entries"),
                record.get("metadata_generated_events"),
                record.get("xsec_pb_user_prompt", ""),
                record.get("expected_yield_before_detector_acceptance", ""),
                record.get("nominal_mc_weight_if_generated_count_used", ""),
                ", ".join(record.get("coverage", {}).get("generators", [])),
                record.get("coverage", {}).get("tune"),
                record.get("coverage", {}).get("sqrt_s_TeV"),
            ]
        )
    figure_rows = [[fig["id"], fig["png"], fig["caption"]] for fig in figures]
    text = f"""# Data Reconnaissance

Session: `albert_0f97`
Created: {datetime.now(timezone.utc).isoformat()}

## Summary

Phase 1 structurally inspected both the user-specified `/sandbox/work/jfc/analyses/h4ltemplate` ROOT files and the local `data/` and `mc/` copies. The primary event reconnaissance uses the user-specified paths because those are the prompt inputs; local copies are inventoried separately because their byte sizes differ and should not be assumed identical.

## Primary vs Local Copy Check

{primary_local_comparison(metadata)}

The primary source paths from `paths.json` are not byte-identical to the local copies for most MC samples, and some local files contain more `Metadata` rows and `h4lTree` entries. Downstream phases should use the user-specified primary paths unless the orchestrator formally changes the data source, because mixing primary and local copies would change yields and generated-event denominators.

## Sample Inventory and MC Coverage

{md_table(["File", "Kind", "Events entries", "Metadata generated events", "Prompt xsec [pb]", "Expected yield at 10 fb^-1", "Nominal weight", "Generators", "Tune", "sqrt(s) [TeV]"], coverage_rows)}

The MC cross sections above are prompt-provided effective sample cross sections. For downstream normalization the documented Phase 1 formula is `weight = sigma * L / sum(nEvents from Metadata)`, using the algebraic generated-event denominator recorded in each MC file's Metadata tree where available.

## Tree and Branch Inventory

{branch_inventory(metadata)}

## Physics Capability From Branch Names

{branch_availability(metadata)}

Phase 1 finds the core four-lepton variables (`m4l`, `mZ1`, `mZ2`, `pt4l`, `eta4l`, `phi4l`) and per-lepton kinematics/ID/isolation variables. It finds azimuthal-angle primitives but does not find jet/VBF branches, generator-level truth branches, or precomputed MELA/angular discriminants in the primary branch inventory. Phase 2/3 must therefore either compute VBF and angular inputs from available lower-level information if possible, or formally document the limitation before committing to those analysis features.

## Integer and Flag Unique-Value Survey

{unique_survey(slice_recon)}

## Data Quality Assessment

{data_quality(slice_recon)}

No full-event production processing was performed in Phase 1. The quality survey loaded at most 1000 entries per primary tree and counted NaN/inf values after flattening numeric branches.

## Truth-Level Information

Truth-level support is assessed from branch names and tree content in the metadata inventory. The only `pdgId`-like branches found in the primary files are reconstructed lepton flavor identifiers (`l1pdgId` through `l4pdgId`); no primary branches matching generator/truth tokens (`gen`, `truth`, `lhe`, `mother`, `status`) were found. Phase 2 must not assume truth matching or particle-level closure is available from these ntuples without adding an external method or source.

## Pre-Applied Selections

The ntuples are not raw CMS MiniAOD/NanoAOD; they are flat ntuples produced by `h4l_ntuplize.py`. Therefore the `Events` tree entries are already after ntuplizer-level object/event construction. MC files include `Metadata` generated-event counts for normalization denominators; the ratio of `Events` rows to generated metadata rows is a first diagnostic of preselection/skimming. Data do not include a public inclusive denominator in Phase 1, so no data preselection efficiency is inferred from the target observable.

## Exploration Figures

{md_table(["Figure ID", "PNG", "Caption"], figure_rows or [["none", "", "No candidate variables were plottable"]])}

## Code Reference

- `pixi run p1-metadata`
- `pixi run p1-recon-slice`
- `pixi run p1-preselection`
- `pixi run p1-hists`
- `pixi run p1-plots`
- `pixi run p1-artifacts`

## Open Issues for Phase 2

- Validate prompt-provided effective cross sections against public campaign metadata where possible; Phase 1 records them as user-provided, not independently verified.
- Decide whether downstream work should use the larger user-specified source files or the local copies; Phase 1 recommends the user-specified paths because they are the stated prompt inputs.
- If a required angular discriminator branch is absent, Phase 2/3 must compute angular observables from available four-lepton kinematics or document infeasibility.
"""
    (OUT / "DATA_RECONNAISSANCE.md").write_text(text)


def write_input_inventory(coverage: dict) -> None:
    rows = [
        ["Target data luminosity", "FOUND_USER_PROVIDED", "10 fb^-1", "`prompt.md`; compare CMS full 2017 high-quality luminosity 42.12 +/- 0.34 fb^-1 from CMS-PAS-LUM-20-001 summary", "prompt read; CMS luminosity public page"],
        ["CMS 2017 full-year luminosity", "FOUND_REFERENCE", "42.12 +/- 0.34 fb^-1", "CMS-PAS-LUM-20-001 summary, https://cms-results.web.cern.ch/cms-results/public-results/preliminary-results/LUM-20-001/", "web search: CMS luminosity 2017 13 TeV"],
        ["Reference fit mass window", "FOUND_REFERENCE", "105 < m4l < 140 GeV for mass/width scan; low-mass distribution often 70 < m4l < 170 GeV", "CMS-HIG-16-041 public figure/table descriptions, https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-16-041/", "web search: CMS-HIG-16-041 mass window"],
        ["Published HIG-16-041 signal strength", "FOUND_REFERENCE", "mu = 1.05 +0.19/-0.17 at mH=125.09 GeV", "CMS-HIG-16-041 abstract / HEPData record, https://www.hepdata.net/record/ins1608166", "web search: CMS-HIG-16-041 HEPData"],
        ["Published HIG-16-041 fiducial cross section", "FOUND_REFERENCE", "2.92 +0.48/-0.44 (stat) +0.28/-0.24 (syst) fb; SM 2.76 +/- 0.14 fb", "CMS-HIG-16-041 abstract / HEPData record, https://www.hepdata.net/record/ins1608166", "web search: HEPData CMS-HIG-16-041"],
        ["Published HIG-16-041 Higgs mass", "FOUND_REFERENCE", "125.26 +/- 0.21 GeV", "CMS-HIG-16-041 abstract / HEPData record, https://www.hepdata.net/record/ins1608166", "web search: CMS-HIG-16-041 Table 7"],
        ["Published HIG-16-041 width constraint", "FOUND_REFERENCE", "Gamma_H < 1.10 GeV at 95% CL", "CMS-HIG-16-041 abstract / HEPData record, https://www.hepdata.net/record/ins1608166", "web search: CMS-HIG-16-041 width"],
        ["PDG 2024 Z mass", "FOUND_REFERENCE", "91.1880 +/- 0.0020 GeV", "PDG 2024 Gauge and Higgs Bosons Summary Table, page 2, https://pdg.lbl.gov/2024/tables/rpp2024-sum-gauge-higgs-bosons.pdf", "web search/open: PDG 2024 summary tables"],
        ["PDG 2024 Z width", "FOUND_REFERENCE", "2.4955 +/- 0.0023 GeV", "PDG 2024 Gauge and Higgs Bosons Summary Table, page 2, https://pdg.lbl.gov/2024/tables/rpp2024-sum-gauge-higgs-bosons.pdf", "web search/open: PDG 2024 summary tables"],
        ["PDG 2024 Higgs mass", "FOUND_REFERENCE", "125.20 +/- 0.11 GeV", "PDG 2024 Gauge and Higgs Bosons Summary Table, page 4, https://pdg.lbl.gov/2024/tables/rpp2024-sum-gauge-higgs-bosons.pdf", "web search/open: PDG 2024 summary tables"],
        ["PDG 2024 Higgs width", "FOUND_REFERENCE", "3.7 +1.9/-1.4 MeV with on/off-shell coupling assumption", "PDG 2024 Gauge and Higgs Bosons Summary Table, page 4, https://pdg.lbl.gov/2024/tables/rpp2024-sum-gauge-higgs-bosons.pdf", "web search/open: PDG 2024 summary tables"],
        ["PDG 2024 H -> ZZ* fraction", "FOUND_REFERENCE", "2.80 +/- 0.30%", "PDG 2024 Gauge and Higgs Bosons Summary Table, page 5, https://pdg.lbl.gov/2024/tables/rpp2024-sum-gauge-higgs-bosons.pdf", "web search/open: PDG 2024 summary tables"],
    ]
    for name, sample in sorted(SAMPLE_INFO.items()):
        generated = next((r.get("metadata_generated_events") for r in coverage.get("records", []) if r["name"] == name and r["kind"] == "mc"), None)
        rows.append([
            f"{name} effective cross section",
            "FOUND_USER_PROVIDED",
            f"{sample['xsec_pb']} pb; Metadata nEvents sum={generated}",
            "`prompt.md` user-provided sample list and ROOT Metadata tree",
            "prompt read; `pixi run p1-preselection`",
        ])
    text = f"""# Input Inventory

Session: `albert_0f97`
Created: {datetime.now(timezone.utc).isoformat()}

{md_table(["Input", "Status", "Value", "Source", "Search trail"], rows)}

## Retrieval Notes

MCP_ALPHAXIV and MCP_LEP_CORPUS are both false in `TOGGLES.md`. No MCP retrieval tools were called. Public web searches and source pages were used instead; the retrieval trail is summarized in `phase1_exploration/retrieval_log.md`.
"""
    (OUT / "INPUT_INVENTORY.md").write_text(text)


def write_literature() -> None:
    text = f"""# Literature Survey

Session: `albert_0f97`
Created: {datetime.now(timezone.utc).isoformat()}

## Search Trail

- MCP status: `MCP_ALPHAXIV=false`, `MCP_LEP_CORPUS=false`; no MCP tools called.
- Public searches: `CMS-HIG-16-041 JHEP 11 2017 047`, `arXiv 1706.09936 mass window`, `HEPData CMS-HIG-16-041`, `CMS luminosity 2017 13 TeV`, and `PDG 2024 Gauge and Higgs Bosons Summary Table`.
- Primary public sources retained: CMS-HIG-16-041 public publication page, CMS-PAS-HIG-16-041 public preliminary page, HEPData record DOI 10.17182/hepdata.80189, CMS-PAS-LUM-20-001 luminosity page, and PDG 2024 summary table.

## Reference Analysis: CMS-HIG-16-041 / JHEP 11 (2017) 047

CMS-HIG-16-041 measured properties of the Higgs boson in H->ZZ->4l with 35.9 fb^-1 at 13 TeV. The public CMS page gives the signal-strength definition and reports mu = 1.05 +0.19/-0.17 at mH = 125.09 GeV, a fiducial cross section of 2.92 +0.48/-0.44 (stat) +0.28/-0.24 (syst) fb compatible with an SM prediction of 2.76 +/- 0.14 fb, mH = 125.26 +/- 0.21 GeV, and Gamma_H < 1.10 GeV at 95% CL. The same page documents seven production-sensitive categories, including VBF-1jet and VBF-2jet categories, and shows categorization discriminants in 118 < m4l < 130 GeV.

For this open-data analysis, the most directly comparable results are the m4l distribution shape, a simplified simultaneous category signal-strength fit, the inclusive signal strength, and broad production-category behavior. The full CMS mass measurement is only partially comparable because the official result uses calibrated lepton momenta, per-event mass uncertainties, a kinematic discriminant, data-driven Z+X estimation, and the full 35.9 fb^-1 2016 dataset, while this analysis uses 10 fb^-1 of 2017 open-data ntuples and a DY+jets MC approximation for reducible background.

## Mass Window and Methods

The public figure descriptions for CMS-HIG-16-041 state that the observed mass/width likelihood scans use the signal range 105 < m4l < 140 GeV. Phase 2 should therefore adopt that fit window for the mass/signal-strength extraction unless the ntuple content makes it infeasible. The broader 70 < m4l < 170 GeV distribution is useful for exploratory and sideband plots but is not the quoted mass-fit window.

## Modern/Public Comparable Results

The HEPData record for the same paper provides public numerical tables for integrated and differential fiducial cross sections and correlations. A later CMS H->4l production cross-section publication using 137 fb^-1 reports mu = 0.94 +/- 0.07 (stat) +0.09/-0.08 (syst) and an inclusive fiducial cross section of 2.84 +0.23/-0.22 (stat) +0.26/-0.21 (syst) fb at mH = 125.38 GeV. This is useful as context but less directly comparable because it uses the full Run 2 dataset and a later analysis configuration.

## PDG and World-Average Inputs

The PDG 2024 Gauge and Higgs Bosons Summary Table gives mZ = 91.1880 +/- 0.0020 GeV, Gamma_Z = 2.4955 +/- 0.0023 GeV, mH = 125.20 +/- 0.11 GeV, a Higgs width summary value of 3.7 +1.9/-1.4 MeV under the stated on/off-shell coupling assumption, and H->ZZ* fraction 2.80 +/- 0.30%. These are validation/reference inputs, not tunable analysis parameters.

## Implications for Downstream Strategy

- The official CMS reference uses a simultaneous fit with production-sensitive categories; this open-data analysis should keep at least inclusive, VBF-like, and other categories if statistics allow.
- The requested NN angular discriminator is methodologically aligned with matrix-element/angular information used in official H->4l analyses, but Phase 2/3 must verify that the ntuples include the kinematic inputs needed to compute rest-frame angles.
- DY+jets MC for reducible background is a deliberate simplification relative to official data-driven Z+X estimation; the final note must state this as a comparability limitation.
- Published values above should be used as validation targets and table entries, with explicit caveats for luminosity, year, selection, and background-method differences.

## Source Index

{md_table(["Source", "Use"], [[key, value] for key, value in SOURCES.items()])}
"""
    (OUT / "LITERATURE_SURVEY.md").write_text(text)
    RETRIEVAL_LOG.write_text(
        "# Phase 1 Retrieval Log\n\n"
        "- MCP_ALPHAXIV=false and MCP_LEP_CORPUS=false; no MCP calls made.\n"
        "- Queried public web for CMS-HIG-16-041/JHEP 11 (2017) 047, HEPData DOI 10.17182/hepdata.80189, CMS 2017 luminosity, and PDG 2024 summary tables.\n"
        "- Retained CMS public page: https://cms-results.web.cern.ch/cms-results/public-results/publications/HIG-16-041/\n"
        "- Retained HEPData record: https://www.hepdata.net/record/ins1608166\n"
        "- Retained CMS luminosity page: https://cms-results.web.cern.ch/cms-results/public-results/preliminary-results/LUM-20-001/\n"
        "- Retained PDG summary table: https://pdg.lbl.gov/2024/tables/rpp2024-sum-gauge-higgs-bosons.pdf\n"
    )


def main() -> None:
    ensure_dirs()
    setup_logging()
    metadata = load_optional(OUT / "root_metadata.json")
    slice_recon = load_optional(OUT / "slice_recon.json")
    coverage = load_optional(OUT / "preselection_coverage.json")
    figures = read_json(OUT / "FIGURES.json") if (OUT / "FIGURES.json").exists() else []
    write_data_recon(metadata, slice_recon, coverage, figures)
    write_input_inventory(coverage)
    write_literature()
    append_session(
        "2026-05-29 Phase 1 artifacts\n\n"
        "- Wrote `DATA_RECONNAISSANCE.md`, `INPUT_INVENTORY.md`, and "
        "`LITERATURE_SURVEY.md`."
    )
    append_experiment(
        "## 2026-05-29 — Phase 1 artifacts built\n\n"
        "- Built Phase 1 markdown artifacts from metadata, small-slice surveys, "
        "coverage checks, figure registry, and public literature source notes."
    )


if __name__ == "__main__":
    main()
