from __future__ import annotations

from pathlib import Path
from typing import Any

import uproot

from selection_common import OUT, ROOT, all_known_files, append_experiment, append_session, ensure_dirs, paths, setup_logging, write_json


JET_TOKENS = ("jet", "njet", "mjj", "detajj", "j1", "j2", "vbf")


def branches(path: Path) -> list[str]:
    with uproot.open(path) as root_file:
        if "h4lTree" not in root_file:
            return []
        return list(root_file["h4lTree"].keys())


def ntuplizer_evidence() -> dict[str, Any]:
    ntuplizer = ROOT / "h4l_ntuplize.py"
    if not ntuplizer.exists():
        candidate = Path("/sandbox/work/jfc/analyses/h4ltemplate/h4l_ntuplize.py")
        ntuplizer = candidate if candidate.exists() else ntuplizer
    if not ntuplizer.exists():
        return {"path": None, "found": False, "jet_output_mentions": [], "branch_output_mentions": []}
    text = ntuplizer.read_text(errors="replace").splitlines()
    jet_mentions = []
    output_mentions = []
    for idx, line in enumerate(text, start=1):
        low = line.lower()
        if "jet" in low or "vbf" in low or "mjj" in low:
            jet_mentions.append({"line": idx, "text": line.strip()})
        if "mktree" in low or "h4ltree" in low or "trigbits" in low or "m4l" in low:
            output_mentions.append({"line": idx, "text": line.strip()})
    return {
        "path": str(ntuplizer),
        "found": True,
        "jet_output_mentions": jet_mentions,
        "branch_output_mentions": output_mentions[:40],
        "interpretation": "No jet/VBF output-field evidence found in ntuplizer source." if not jet_mentions else "Jet/VBF text exists; inspect whether it is written to h4lTree.",
    }


def main() -> None:
    ensure_dirs()
    log = setup_logging()
    cfg = paths()
    allow = [str(Path(item)) for item in cfg.get("allow", [])]
    evidence = {
        "created_utc": __import__("selection_common").now(),
        "allow_list": allow,
        "primary_and_local_branch_checks": [],
        "ntuplizer_evidence": ntuplizer_evidence(),
        "join_check": {
            "allowed_upstream_sources": [],
            "safe_event_key_join_possible": False,
            "reason": "paths.json allow-list permits only flat ntuple data and MC directories; no NanoAOD/source directory is allowed for a real jet join.",
        },
    }
    all_matches = []
    for info in all_known_files():
        path = Path(info["path"])
        log.info("Checking branch names for %s", path)
        names = branches(path)
        matches = [name for name in names if any(tok in name.lower() for tok in JET_TOKENS)]
        all_matches.extend(matches)
        evidence["primary_and_local_branch_checks"].append(
            {
                "role": info["role"],
                "kind": info["kind"],
                "name": info["name"],
                "path": str(path),
                "branch_count": len(names),
                "jet_or_vbf_like_branches": matches,
                "event_key_branches": [name for name in names if name in {"run", "lumi", "event"}],
            }
        )
    feasible = bool(all_matches)
    evidence["real_vbf_category_feasible"] = feasible
    evidence["decision"] = (
        "Real jet-based VBF recovery requires downstream purity/systematic checks."
        if feasible
        else "Formal downscope: no real jet or VBF discriminator branches are available in allowed flat ntuples."
    )
    evidence["no_lepton_only_vbf_label"] = True
    write_json(OUT / "vbf_recovery_downscope.json", evidence)
    append_session(
        "2026-05-29 VBF recovery/downscope gate\n\n"
        "- Checked primary/local branch names, current allow-list, event-key availability, and ntuplizer source evidence. "
        f"Decision: {'feasible' if feasible else 'formal VBF downscope'}."
    )
    append_experiment(
        "## 2026-05-29 — Phase 3 VBF recovery/downscope gate\n\n"
        "- Checked primary and local branch inventories plus ntuplizer provenance for jet/VBF content. "
        f"Decision: {'real jet recovery feasible' if feasible else 'formal VBF downscope; no lepton-only category will be labeled VBF'}."
    )


if __name__ == "__main__":
    main()
