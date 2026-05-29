from __future__ import annotations

from datetime import datetime, timezone

import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np
from mplhep.utils import mpl_magic

from phase1_utils import FIG, OUT, append_experiment, append_session, ensure_dirs, read_json, setup_logging, write_json

mh.style.use("CMS")

PLOT_OBSERVABLES = [
    "m4l",
    "z1_mass",
    "z2_mass",
    "pt4l",
    "eta4l",
    "leading_lepton_pt",
    "njets",
    "lead_jet_pt",
    "d_bkg_kin",
]


def pretty_label(label: str) -> str:
    return label.replace("_", " ")


def grouped_samples(samples: list[dict]) -> dict[str, dict]:
    groups: dict[str, dict] = {}
    for sample in samples:
        label = sample["group"]
        edges = np.asarray(sample["edges"], dtype=float)
        counts = np.asarray(sample["counts"], dtype=float)
        if label not in groups:
            groups[label] = {"edges": edges, "counts": np.zeros_like(counts), "files": []}
        groups[label]["counts"] += counts
        groups[label]["files"].append(sample["file"])
    return groups


def plot_observable(name: str, payload: dict) -> dict | None:
    samples = payload.get("samples", [])
    if not samples:
        return None
    cfg = payload["config"]
    groups = grouped_samples(samples)
    fig, ax = plt.subplots(figsize=(10, 10))
    colors = {
        "data": "black",
        "signal_ggH": "#d62728",
        "signal_VBF": "#9467bd",
        "signal_VH": "#e377c2",
        "background_ZZ": "#1f77b4",
        "background_ggZZ": "#17becf",
        "background_reducible": "#ff7f0e",
        "background_top": "#8c564b",
    }
    for label, group in sorted(groups.items()):
        edges = group["edges"]
        counts = group["counts"]
        total = counts.sum()
        if total <= 0:
            continue
        widths = np.diff(edges)
        centers = 0.5 * (edges[:-1] + edges[1:])
        density = counts / (total * widths)
        yerr = np.sqrt(counts) / (total * widths)
        ax.errorbar(
            centers,
            density,
            yerr=yerr,
            xerr=0.5 * widths,
            marker="o",
            linestyle="None",
            color=colors.get(label, None),
            label=pretty_label(label),
        )
    ax.set_xlabel(cfg["xlabel"])
    ax.set_ylabel("Normalized entries")
    ax.legend(loc="upper right", fontsize="x-small")
    mpl_magic(ax)
    mh.label.exp_label(
        exp="CMS",
        text="",
        loc=0,
        data=True,
        llabel="Open Data+Sim",
        rlabel=r"$13$ TeV, small slices",
        ax=ax,
    )
    png = FIG / f"{name}_small_slice_shapes.png"
    pdf = FIG / f"{name}_small_slice_shapes.pdf"
    fig.savefig(str(pdf.with_suffix(".pdf")), bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(str(png.with_suffix(".png")), bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    caption = (
        f"{cfg['xlabel']} small-slice shape comparison. The distributions use at most "
        "1000 entries per primary ROOT file and are area-normalized only for Phase 1 "
        "shape reconnaissance, not for yield validation. Large differences here flag "
        "candidate variables for Phase 2/3 data-MC quality checks rather than final "
        "selection conclusions."
    )
    return {
        "id": f"phase1_{name}_small_slice_shapes",
        "observable": name,
        "png": str(png.relative_to(OUT)),
        "pdf": str(pdf.relative_to(OUT)),
        "caption": caption,
        "description": caption,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source": "phase1_exploration/outputs/exploration_histograms.json",
        "samples": sorted(groups.keys()),
    }


def main() -> None:
    ensure_dirs()
    log = setup_logging()
    data = read_json(OUT / "exploration_histograms.json")
    figures = []
    for observable in PLOT_OBSERVABLES:
        figure = plot_observable(observable, data["observables"].get(observable, {}))
        if figure is None:
            log.info("No samples available for %s; skipping plot", observable)
            continue
        figures.append(figure)
        append_session(f"FIGURE_READY: phase1_exploration/outputs/{figure['png']}")
    write_json(OUT / "FIGURES.json", figures)
    append_session(
        "2026-05-29 exploration plots\n\n"
        f"- Wrote `phase1_exploration/outputs/FIGURES.json` with {len(figures)} registered figures."
    )
    append_experiment(
        "## 2026-05-29 — Phase 1 exploration figures\n\n"
        f"- Produced {len(figures)} small-slice exploration figures and updated "
        "`phase1_exploration/outputs/FIGURES.json`."
    )


if __name__ == "__main__":
    main()
