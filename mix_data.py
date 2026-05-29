#!/usr/bin/env python3

"""
Build a fake 10 fb^-1 CMS data sample from the H->4l MC ntuples.

The input files are selected MC ntuples.  Each entry in h4lTree is one event
that passed the ntuplizer selection, while Metadata/nEvents entry 0 stores the
number of originally generated events for that MC file.

For every known process, this script computes the expected selected yield as

    xsec(pb) * lumi(fb^-1) * 1000 * n_selected / n_generated

then randomly takes that many h4lTree entries without replacement, unless a
process needs more fake-data entries than it has selected MC entries.  In that
case only that process is sampled with replacement.  The chosen entries from
all processes are shuffled into a fake data file, and all entries not used in
fake data are written as the new MC samples.
"""

from __future__ import annotations

import argparse
import glob
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence

import numpy as np
import uproot


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parents[2]
DEFAULT_INPUT = SCRIPT_DIR / "ntuple"
DEFAULT_DATA_DIR = SCRIPT_DIR / "data"
DEFAULT_MC_DIR = SCRIPT_DIR / "mc"
DEFAULT_DATA_NAME = "cms_10fb_13TeV.root"
DEFAULT_LUMI_FB = 10.0

TREE_NAME = "h4lTree"
METADATA_NAME = "Metadata"
METADATA_N_EVENTS = "nEvents"
DROP_FAKE_DATA_BRANCHES = {"run", "lumi", "event"}


SAMPLES = [
    {
        "label": "GluGluToHToZZ",
        "xsec_pb": 1.333521e-02,
        "aliases": [
            "GluGluToHToZZ.root",
            "GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_minloHJJ_JHUGenV7011_pythia8",
        ],
    },
    {
        "label": "VBF_HToZZ",
        "xsec_pb": 1.038159e-03,
        "aliases": [
            "VBF_HToZZ.root",
            "VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8",
        ],
    },
    {
        "label": "ZHToZZ",
        "xsec_pb": 2.458e-04,
        "aliases": [
            "ZHToZZ.root",
            "ZH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8",
        ],
    },
    {
        "label": "WPHToZZ",
        "xsec_pb": 2.305562e-04,
        "aliases": [
            "WPHToZZ.root",
            "WplusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8",
        ],
    },
    {
        "label": "WMHToZZ",
        "xsec_pb": 1.469e-04,
        "aliases": [
            "WMHToZZ.root",
            "WminusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8",
        ],
    },
    {
        "label": "ZZTo4L",
        "xsec_pb": 1.325e00,
        "aliases": [
            "ZZTo4L.root",
            "ZZTo4L_TuneCP5_13TeV_powheg_pythia8",
        ],
    },
    {
        "label": "DYJetsToLL",
        "xsec_pb": 5.396e03,
        "aliases": [
            "DYJetsToLL.root",
            "DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
        ],
    },
    {
        "label": "TTBar",
        "xsec_pb": 8.731e01,
        "aliases": [
            "TTBar.root",
            "TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8",
        ],
    },
    {
        "label": "GGZZ2E2Mu",
        "xsec_pb": 3.185e-03,
        "aliases": [
            "GGZZ2E2Mu.root",
            "GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8",
        ],
    },
    {
        "label": "GGZZ4Mu",
        "xsec_pb": 1.575e-03,
        "aliases": [
            "GGZZ4Mu.root",
            "GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8",
        ],
    },
    {
        "label": "GGZZ4E",
        "xsec_pb": 1.619e-03,
        "aliases": [
            "GGZZ4E.root",
            "GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8",
        ],
    },
]


@dataclass(frozen=True)
class FileInfo:
    path: Path
    sample_label: str
    xsec_pb: float
    selected_entries: int
    generated_events: int
    branches: List[str]


@dataclass(frozen=True)
class SamplePlan:
    label: str
    xsec_pb: float
    files: List[FileInfo]
    selected_entries: int
    generated_events: int
    expected_selected: float
    target_entries: int
    remaining_entries: int


def expand_inputs(items: Sequence[str]) -> List[Path]:
    """Expand files, directories, and glob patterns into a sorted ROOT file list."""
    out: List[Path] = []
    for item in items:
        p = Path(item).expanduser()
        if any(ch in item for ch in ["*", "?", "["]):
            out.extend(Path(x) for x in glob.glob(item))
        elif p.is_dir():
            out.extend(p.rglob("*.root"))
        else:
            out.append(p)

    files = sorted({p.resolve() for p in out if p.exists() and p.is_file() and p.suffix == ".root"})
    if not files:
        raise FileNotFoundError("No input ROOT files found.")
    return files


def resolve_sample(path: Path) -> Mapping[str, object] | None:
    """Return the sample spec matching a file path, or None if unknown."""
    haystack = f"{path.name} {path.as_posix()}"
    matches = []
    for spec in SAMPLES:
        patterns = [str(spec["label"]), *[str(x) for x in spec["aliases"]]]
        if any(pattern in haystack for pattern in patterns):
            matches.append(spec)

    if not matches:
        return None

    return sorted(
        matches,
        key=lambda spec: max(len(str(x)) for x in [spec["label"], *spec["aliases"]]),
        reverse=True,
    )[0]


def read_metadata_n_events(root_file: uproot.ReadOnlyDirectory, path: Path) -> int:
    if METADATA_NAME not in root_file:
        raise KeyError(f"{path} is missing the '{METADATA_NAME}' tree")

    metadata = root_file[METADATA_NAME]
    if METADATA_N_EVENTS not in metadata.keys():
        raise KeyError(f"{path} is missing '{METADATA_NAME}/{METADATA_N_EVENTS}'")

    n_events = metadata[METADATA_N_EVENTS].array(library="np")
    if len(n_events) == 0:
        raise ValueError(f"{path} has no entries in '{METADATA_NAME}/{METADATA_N_EVENTS}'")

    value = int(np.sum(n_events))
    if value <= 0:
        raise ValueError(f"{path} has non-positive generated event count: {value}")
    return value


def read_file_info(path: Path, tree_name: str) -> FileInfo:
    spec = resolve_sample(path)
    if spec is None:
        raise ValueError(f"Unknown MC sample; no cross section configured for {path}")

    with uproot.open(path, object_cache=None, array_cache=None) as root_file:
        if tree_name not in root_file:
            raise KeyError(f"{path} does not contain tree '{tree_name}'")

        tree = root_file[tree_name]
        branches = [k.decode() if isinstance(k, bytes) else str(k) for k in tree.keys()]
        selected_entries = int(tree.num_entries)
        generated_events = read_metadata_n_events(root_file, path)

    return FileInfo(
        path=path,
        sample_label=str(spec["label"]),
        xsec_pb=float(spec["xsec_pb"]),
        selected_entries=selected_entries,
        generated_events=generated_events,
        branches=branches,
    )


def build_sample_plans(files: Sequence[Path], tree_name: str, lumi_fb: float) -> List[SamplePlan]:
    grouped: Dict[str, List[FileInfo]] = {}
    for path in files:
        info = read_file_info(path, tree_name)
        grouped.setdefault(info.sample_label, []).append(info)

    plans: List[SamplePlan] = []
    for spec in SAMPLES:
        label = str(spec["label"])
        if label not in grouped:
            continue

        sample_files = grouped[label]
        selected_entries = sum(info.selected_entries for info in sample_files)
        generated_events = sum(info.generated_events for info in sample_files)
        expected_selected = float(spec["xsec_pb"]) * lumi_fb * 1000.0
        expected_selected *= selected_entries / float(generated_events)
        target_entries = int(math.floor(expected_selected + 0.5))
        remaining_entries = selected_entries - target_entries

        plans.append(
            SamplePlan(
                label=label,
                xsec_pb=float(spec["xsec_pb"]),
                files=sample_files,
                selected_entries=selected_entries,
                generated_events=generated_events,
                expected_selected=expected_selected,
                target_entries=target_entries,
                remaining_entries=remaining_entries,
            )
        )

    return plans


def print_sample_plan(plans: Sequence[SamplePlan], lumi_fb: float) -> None:
    print(f"Lumi target: {lumi_fb:g} fb^-1")
    print("Per-sample plan before writing:")
    print(
        f"{'sample':<18} {'xsec[pb]':>12} {'generated':>12} "
        f"{'selected':>10} {'data@lumi':>12} {'take':>8} {'mc left':>8}"
    )
    print("-" * 88)
    for plan in plans:
        print(
            f"{plan.label:<18} {plan.xsec_pb:>12.6g} {plan.generated_events:>12d} "
            f"{plan.selected_entries:>10d} {plan.expected_selected:>12.3f} "
            f"{plan.target_entries:>8d} {plan.remaining_entries:>8d}"
        )


def validate_plans(plans: Sequence[SamplePlan]) -> None:
    bad = [plan for plan in plans if plan.target_entries > 0 and plan.selected_entries <= 0]
    if not bad:
        return

    print("\nERROR: at least one sample needs fake-data entries but has no selected MC entries.")
    for plan in bad:
        print(
            f"  {plan.label}: need {plan.target_entries}, "
            f"available {plan.selected_entries}"
        )
    raise SystemExit(1)


def validate_output_names(file_infos: Iterable[FileInfo], output_dir: Path) -> None:
    names: Dict[str, Path] = {}
    for info in file_infos:
        name = info.path.name
        if name in names:
            raise ValueError(
                "Multiple input files would write the same MC output name "
                f"'{output_dir / name}': {names[name]} and {info.path}"
            )
        names[name] = info.path


def choose_entries(
    plans: Sequence[SamplePlan],
    rng: np.random.Generator,
) -> Dict[Path, np.ndarray]:
    """Choose fake-data entry indices for each input file."""
    chosen_by_file: Dict[Path, np.ndarray] = {}

    for plan in plans:
        replace = plan.target_entries > plan.selected_entries
        mode = "with replacement" if replace else "without replacement"
        print(f"Selecting {plan.target_entries} events for {plan.label} ({mode})")
        counts = [info.selected_entries for info in plan.files]
        offsets = np.cumsum([0, *counts])

        if plan.target_entries > 0:
            chosen_global = rng.choice(
                plan.selected_entries,
                size=plan.target_entries,
                replace=replace,
            )
        else:
            chosen_global = np.array([], dtype=np.int64)

        for index, info in enumerate(plan.files):
            start = offsets[index]
            stop = offsets[index + 1]
            in_file = chosen_global[(chosen_global >= start) & (chosen_global < stop)]
            chosen_by_file[info.path] = (in_file - start).astype(np.int64, copy=False)
            used_for_mc = np.unique(chosen_by_file[info.path])
            print(f"  {info.path.name}: fake data {len(chosen_by_file[info.path])}, "
                  f"new MC {info.selected_entries - len(used_for_mc)}")

    return chosen_by_file


def data_branch_order(file_infos: Sequence[FileInfo]) -> List[str]:
    """Use only branches common to all input MC files, dropping event identity branches."""
    if not file_infos:
        raise ValueError("No input files were planned.")

    common = set(file_infos[0].branches)
    for info in file_infos[1:]:
        common &= set(info.branches)

    branches = [
        branch
        for branch in file_infos[0].branches
        if branch in common and branch not in DROP_FAKE_DATA_BRANCHES
    ]
    if not branches:
        raise ValueError("No common h4lTree branches remain after dropping run/lumi/event.")
    return branches


def load_arrays(path: Path, tree_name: str, branches: Sequence[str]) -> Dict[str, np.ndarray]:
    with uproot.open(path) as root_file:
        tree = root_file[tree_name]
        return tree.arrays(list(branches), library="np")


def subset_arrays(arrays: Mapping[str, np.ndarray], indices: np.ndarray) -> Dict[str, np.ndarray]:
    return {key: value[indices] for key, value in arrays.items()}


def concat_chunks(chunks: Sequence[Mapping[str, np.ndarray]]) -> Dict[str, np.ndarray]:
    if not chunks:
        return {}

    keys = list(chunks[0].keys())
    keyset = set(keys)
    for chunk in chunks[1:]:
        if set(chunk.keys()) != keyset:
            raise ValueError("Cannot concatenate chunks with different branch sets.")

    return {
        key: np.concatenate([chunk[key] for chunk in chunks], axis=0)
        for key in keys
    }


def shuffle_arrays(
    arrays: Mapping[str, np.ndarray],
    rng: np.random.Generator,
) -> Dict[str, np.ndarray]:
    if not arrays:
        return {}

    n_entries = len(next(iter(arrays.values())))
    order = rng.permutation(n_entries)
    return {key: value[order] for key, value in arrays.items()}


def write_tree(
    outfile: Path,
    tree_name: str,
    arrays: Mapping[str, np.ndarray],
    metadata: Mapping[str, np.ndarray],
) -> None:
    if not arrays:
        raise ValueError(f"Refusing to write {outfile}: no h4lTree branches.")

    outfile.parent.mkdir(parents=True, exist_ok=True)
    branch_types = {key: value.dtype for key, value in arrays.items()}
    metadata_types = {key: value.dtype for key, value in metadata.items()}

    with uproot.recreate(outfile.as_posix()) as root_file:
        tree = root_file.mktree(tree_name, branch_types)
        tree.extend(dict(arrays))

        meta_tree = root_file.mktree(METADATA_NAME, metadata_types)
        meta_tree.extend(dict(metadata))


def write_outputs(
    plans: Sequence[SamplePlan],
    chosen_by_file: Mapping[Path, np.ndarray],
    tree_name: str,
    data_outfile: Path,
    mc_dir: Path,
    lumi_fb: float,
    rng: np.random.Generator,
) -> None:
    all_files = [info for plan in plans for info in plan.files]
    validate_output_names(all_files, mc_dir)
    fake_data_branches = data_branch_order(all_files)

    print(f"Fake data branches: {len(fake_data_branches)} kept, "
          f"{sorted(DROP_FAKE_DATA_BRANCHES)} dropped when present")

    fake_data_chunks: List[Dict[str, np.ndarray]] = []

    for plan in plans:
        print(f"Processing sample {plan.label}")
        for info in plan.files:
            selected = np.sort(chosen_by_file.get(info.path, np.array([], dtype=np.int64)))
            all_indices = np.arange(info.selected_entries, dtype=np.int64)
            used_for_mc = np.unique(selected)
            remaining = np.setdiff1d(all_indices, used_for_mc, assume_unique=True)

            arrays = load_arrays(info.path, tree_name, info.branches)

            if len(selected) > 0:
                fake_source = {branch: arrays[branch] for branch in fake_data_branches}
                fake_data_chunks.append(subset_arrays(fake_source, selected))

            mc_arrays = subset_arrays(arrays, remaining)
            mc_outfile = mc_dir / info.path.name
            write_tree(
                mc_outfile,
                tree_name,
                mc_arrays,
                {METADATA_N_EVENTS: np.array([info.generated_events], dtype=np.int64)},
            )
            print(f"  wrote MC {len(remaining)} entries -> {mc_outfile}")

    fake_data = shuffle_arrays(concat_chunks(fake_data_chunks), rng)
    if not fake_data:
        raise SystemExit("No fake data events were selected; nothing to write.")

    n_fake_data = len(next(iter(fake_data.values())))
    write_tree(
        data_outfile,
        tree_name,
        fake_data,
        {
            METADATA_N_EVENTS: np.array([n_fake_data], dtype=np.int64),
            "lumi_fb": np.array([lumi_fb], dtype=np.float64),
        },
    )
    print(f"Wrote fake data {n_fake_data} entries -> {data_outfile}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        nargs="+",
        default=[str(DEFAULT_INPUT)],
        help=f"Input ROOT file(s), directories, or glob patterns (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--data-dir",
        default=str(DEFAULT_DATA_DIR),
        help=f"Directory for fake data output (default: {DEFAULT_DATA_DIR})",
    )
    parser.add_argument(
        "--mc-dir",
        default=str(DEFAULT_MC_DIR),
        help=f"Directory for remaining MC outputs (default: {DEFAULT_MC_DIR})",
    )
    parser.add_argument(
        "--data-name",
        default=DEFAULT_DATA_NAME,
        help=f"Fake data ROOT filename (default: {DEFAULT_DATA_NAME})",
    )
    parser.add_argument(
        "--tree",
        default=TREE_NAME,
        help=f"Input/output tree name (default: {TREE_NAME})",
    )
    parser.add_argument(
        "--lumi",
        type=float,
        default=DEFAULT_LUMI_FB,
        help=f"Target luminosity in fb^-1 (default: {DEFAULT_LUMI_FB:g})",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=12345,
        help="Random seed for event choice and fake-data mixing (default: 12345)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the per-sample plan and validation only; do not write outputs",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.lumi <= 0:
        raise SystemExit("--lumi must be positive")

    input_files = expand_inputs(args.input)
    data_outfile = Path(args.data_dir).expanduser().resolve() / args.data_name
    mc_dir = Path(args.mc_dir).expanduser().resolve()

    print(f"Input ROOT files: {len(input_files)}")
    print(f"Data output: {data_outfile}")
    print(f"MC output directory: {mc_dir}")

    plans = build_sample_plans(input_files, args.tree, args.lumi)
    print_sample_plan(plans, args.lumi)
    validate_plans(plans)

    if args.dry_run:
        print("Dry run requested; outputs were not written.")
        return

    rng = np.random.default_rng(args.seed)
    chosen_by_file = choose_entries(plans, rng)
    write_outputs(
        plans=plans,
        chosen_by_file=chosen_by_file,
        tree_name=args.tree,
        data_outfile=data_outfile,
        mc_dir=mc_dir,
        lumi_fb=args.lumi,
        rng=rng,
    )


if __name__ == "__main__":
    main()
