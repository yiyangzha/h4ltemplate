#!/usr/bin/env python3

"""
Build a fake "unlabelled data" sample from labelled H->4l ntuples.

Input:
  - ROOT files produced by h4l_ntuplize.py
  - each file should contain a flat TTree named h4lTree

Behavior:
  - groups files by the sample names / aliases from prompt.md
  - computes expected event yields from xsec * lumi
  - samples events from each process proportional to its expected yield
  - shuffles the final merged sample
  - writes a ROOT or Parquet file with no process label column

Examples:
  python make_fake_data.py \
      --input /path/to/ntuples \
      --output fake_data.root \
      --lumi 20

  python make_fake_data.py \
      --input /path/to/ntuples/*.root \
      --output fake_data.parquet \
      --lumi 20 \
      --seed 7
"""

from __future__ import annotations

import argparse
import glob
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np
import uproot


SAMPLES = [
    {
        "label": "GluGluToHToZZ",
        "xsec_pb": 2.887e01,
        "aliases": [
            "GluGluToHToZZ.root",
            "GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_minloHJJ_JHUGenV7011_pythia8",
        ],
    },
    {
        "label": "VBF_HToZZ",
        "xsec_pb": 3.935e00,
        "aliases": [
            "VBF_HToZZ.root",
            "VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8",
        ],
    },
    {
        "label": "ZHToZZ",
        "xsec_pb": 7.935e-01,
        "aliases": [
            "ZHToZZ.root",
            "ZH_HToZZ_4LFilter_M125_TuneCP5_13TeV_powheg2-minlo-HZJ_JHUGenV7011_pythia8",
        ],
    },
    {
        "label": "WPHToZZ",
        "xsec_pb": 8.648e-01,
        "aliases": [
            "WPHToZZ.root",
            "WplusH_HToZZTo4L_M125_TuneCP5_13TeV_powheg2-minlo-HWJ_JHUGenV7011_pythia8",
        ],
    },
    {
        "label": "WMHToZZ",
        "xsec_pb": 5.409e-01,
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
        "xsec_pb": 5.270e01,
        "aliases": [
            "TTBar.root",
            "TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8",
        ],
    },
    {
        "label": "GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8",
        "xsec_pb": 3.185e+00,
        "aliases": [
            "GGZZ2E2Mu.root",
            "GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8",
        ],
    },
    {
        "label": "GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8",
        "xsec_pb": 1.575,
        "aliases": [
            "GGZZ4Mu.root",
            "GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8",
        ],
    },
    {
        "label": "GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8",
        "xsec_pb": 1.619,
        "aliases": [
            "GGZZ4E.root",
            "GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8",
        ],
    },
]


def expand_inputs(items: Sequence[str]) -> List[Path]:
    """Expand files, directories, and glob patterns into a flat file list."""
    out: List[Path] = []
    for item in items:
        p = Path(item)
        if any(ch in item for ch in ["*", "?", "["]):
            out.extend(Path(x) for x in sorted(glob.glob(item)))
        elif p.is_dir():
            out.extend(sorted(p.rglob("*.root")))
        else:
            out.append(p)

    files = [p for p in out if p.exists() and p.is_file()]
    if not files:
        raise FileNotFoundError("No input ROOT files found.")
    return files


def resolve_sample(path: Path) -> dict | None:
    """Return the sample spec matching a file path, or None if unknown."""
    haystack = f"{path.name} {path.as_posix()}"
    matches = []
    for spec in SAMPLES:
        pats = [spec["label"], *spec["aliases"]]
        if any(pat in haystack for pat in pats):
            matches.append(spec)
    if not matches:
        return None
    # Prefer the most specific match.
    return sorted(matches, key=lambda s: max(len(x) for x in [s["label"], *s["aliases"]]), reverse=True)[0]


def get_tree_info(fname: Path, tree_name: str) -> Tuple[int, List[str]]:
    with uproot.open(fname) as f:
        if tree_name not in f:
            raise KeyError(f"{fname} does not contain tree '{tree_name}'")
        tree = f[tree_name]
        keys = [k.decode() if isinstance(k, bytes) else k for k in tree.keys()]
        return int(tree.num_entries), keys


def load_arrays(fname: Path, tree_name: str, branches: Sequence[str]) -> Dict[str, np.ndarray]:
    with uproot.open(fname) as f:
        tree = f[tree_name]
        return tree.arrays(list(branches), library="np")


def proportional_targets(counts: List[int], total_target: int) -> List[int]:
    """Split total_target across files proportional to counts, preserving the sum."""
    if total_target <= 0:
        return [0] * len(counts)

    total = float(sum(counts))
    if total <= 0:
        return [0] * len(counts)

    raw = [total_target * c / total for c in counts]
    base = [int(np.floor(x)) for x in raw]
    remainder = total_target - sum(base)

    frac_order = np.argsort([x - np.floor(x) for x in raw])[::-1]
    for i in frac_order[:remainder]:
        base[int(i)] += 1
    return base


def scale_targets(targets: Dict[str, int], max_events: int) -> Dict[str, int]:
    """Scale down all targets so the total does not exceed max_events."""
    if max_events <= 0:
        return targets

    total = sum(targets.values())
    if total <= max_events:
        return targets

    scale = max_events / float(total)
    raw = {k: v * scale for k, v in targets.items()}
    out = {k: int(np.floor(v)) for k, v in raw.items()}
    remainder = max_events - sum(out.values())

    # Add leftover events to the biggest fractional parts.
    order = sorted(raw.keys(), key=lambda k: raw[k] - np.floor(raw[k]), reverse=True)
    for k in order[:remainder]:
        if targets[k] > 0:
            out[k] += 1
    return out


def sample_one_file(arrays: Dict[str, np.ndarray], n_take: int, rng: np.random.Generator) -> Dict[str, np.ndarray]:
    if n_take <= 0:
        return {}

    n_avail = len(next(iter(arrays.values())))
    replace = n_take > n_avail
    idx = rng.choice(n_avail, size=n_take, replace=replace)
    return {k: v[idx] for k, v in arrays.items()}


def concat_dicts(chunks: List[Dict[str, np.ndarray]]) -> Dict[str, np.ndarray]:
    if not chunks:
        return {}

    out: Dict[str, List[np.ndarray]] = {}
    for chunk in chunks:
        for k, v in chunk.items():
            out.setdefault(k, []).append(v)
    return {k: np.concatenate(vs, axis=0) for k, vs in out.items()}


def shuffle_dict(arrays: Dict[str, np.ndarray], rng: np.random.Generator) -> Dict[str, np.ndarray]:
    if not arrays:
        return {}
    n = len(next(iter(arrays.values())))
    order = rng.permutation(n)
    return {k: v[order] for k, v in arrays.items()}


def build_fake_data(
    files: Sequence[Path],
    tree_name: str,
    lumi_fb: float,
    seed: int,
    max_events: int,
) -> Tuple[Dict[str, np.ndarray], int, int]:
    """
    Returns:
      output_arrays, total_input_events, total_output_events
    """
    rng = np.random.default_rng(seed)

    grouped: Dict[str, List[Path]] = {}
    for f in files:
        spec = resolve_sample(f)
        if spec is None:
            print(f"WARNING: skipping unknown sample file: {f}")
            continue
        grouped.setdefault(spec["label"], []).append(f)

    if not grouped:
        raise RuntimeError("No files matched any known sample label.")

    per_sample_targets: Dict[str, int] = {}
    per_sample_counts: Dict[str, int] = {}
    total_input = 0

    for spec in SAMPLES:
        label = spec["label"]
        if label not in grouped:
            continue

        files_for_sample = grouped[label]
        print("files",files_for_sample)
        counts = []
        branches_common = None

        for f in files_for_sample:
            n, keys = get_tree_info(f, tree_name)
            counts.append(n)
            total_input += n
            keyset = set(keys)
            branches_common = keyset if branches_common is None else (branches_common & keyset)

        if not branches_common:
            raise RuntimeError(f"No common branches found for sample {label}")

        #target = int(round(spec["xsec_pb"] * lumi_fb * 1000.0))
        expected = spec["xsec_pb"] * lumi_fb * 1000.0
        target = int(rng.poisson(expected))
        per_sample_targets[label] = target
        per_sample_counts[label] = sum(counts)

    per_sample_targets = scale_targets(per_sample_targets, max_events)

    sampled_chunks: List[Dict[str, np.ndarray]] = []

    for spec in SAMPLES:
        label = spec["label"]
        if label not in grouped:
            continue

        files_for_sample = grouped[label]
        target_total = per_sample_targets.get(label, 0)
        if target_total <= 0:
            continue

        # Determine the common branches across the files in this sample.
        branches_common = None
        file_meta = []
        for f in files_for_sample:
            n, keys = get_tree_info(f, tree_name)
            branches_common = set(keys) if branches_common is None else (branches_common & set(keys))
            file_meta.append((f, n))

        branches = sorted(branches_common)
        counts = [n for _, n in file_meta]
        target_per_file = proportional_targets(counts, target_total)

        sample_chunks: List[Dict[str, np.ndarray]] = []
        for (f, n_avail), n_take in zip(file_meta, target_per_file):
            if n_take <= 0:
                continue
            arrays = load_arrays(f, tree_name, branches)
            sample_chunks.append(sample_one_file(arrays, n_take, rng))

        if sample_chunks:
            sampled_chunks.append(concat_dicts(sample_chunks))

    out = concat_dicts(sampled_chunks)
    out = shuffle_dict(out, rng)

    total_output = len(next(iter(out.values()))) if out else 0
    return out, total_input, total_output


def write_root(outfile: Path, arrays: Dict[str, np.ndarray], lumi_fb: float, n_input: int) -> None:
    branch_types = {k: v.dtype for k, v in arrays.items()}

    with uproot.recreate(outfile.as_posix()) as f:
        tree = f.mktree("h4lTree", branch_types)
        tree.extend(arrays)

        meta = f.mktree(
            "Metadata",
            {
                "nInputEvents": np.dtype("int64"),
                "nOutputEvents": np.dtype("int64"),
                "lumi_fb": np.dtype("float64"),
            },
        )
        meta.extend(
            {
                "nInputEvents": np.array([n_input], dtype=np.int64),
                "nOutputEvents": np.array([len(next(iter(arrays.values()))) if arrays else 0], dtype=np.int64),
                "lumi_fb": np.array([lumi_fb], dtype=np.float64),
            }
        )


def write_parquet(outfile: Path, arrays: Dict[str, np.ndarray], lumi_fb: float, n_input: int) -> None:
    import pyarrow as pa
    import pyarrow.parquet as pq

    pa_cols = {k: pa.array(v) for k, v in arrays.items()}
    table = pa.table(pa_cols).replace_schema_metadata(
        {
            b"nInputEvents": str(n_input).encode(),
            b"nOutputEvents": str(len(next(iter(arrays.values()))) if arrays else 0).encode(),
            b"lumi_fb": str(lumi_fb).encode(),
        }
    )
    pq.write_table(table, outfile.as_posix(), compression="snappy")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", nargs="+", required=True, help="ROOT file(s), directories, or glob patterns")
    p.add_argument("--output", required=True, help="Output .root or .parquet file")
    p.add_argument("--tree", default="h4lTree", help="Input tree name (default: h4lTree)")
    p.add_argument("--lumi", type=float, default=20.0, help="Target luminosity in fb^-1 (default: 20)")
    p.add_argument("--seed", type=int, default=12345, help="RNG seed (default: 12345)")
    p.add_argument(
        "--max-events",
        type=int,
        default=-1,
        help="Optional cap on the total output size; targets are scaled down proportionally",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    files = expand_inputs(args.input)
    outfile = Path(args.output)
    suffix = outfile.suffix.lower()

    if suffix not in {".root", ".parquet"}:
        raise SystemExit(f"Output must end in .root or .parquet, got {outfile.suffix}")

    arrays, n_input, n_output = build_fake_data(
        files=files,
        tree_name=args.tree,
        lumi_fb=args.lumi,
        seed=args.seed,
        max_events=args.max_events,
    )

    if not arrays:
        raise SystemExit("No events were selected; nothing to write.")

    if suffix == ".root":
        write_root(outfile, arrays, args.lumi, n_input)
    else:
        write_parquet(outfile, arrays, args.lumi, n_input)

    print(f"Wrote {n_output} events to {outfile}")
    print(f"Input events scanned: {n_input}")
    print(f"Lumi target: {args.lumi} fb^-1")


if __name__ == "__main__":
    main()
