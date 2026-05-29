from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import hist
import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np
from mplhep.utils import mpl_magic

from selection_common import FIG, OUT, STACK_COLORS, STACK_ORDER, append_session, read_json, write_json

mh.style.use("CMS")


def figure_registry() -> list[dict[str, Any]]:
    path = OUT / "FIGURES.json"
    if not path.exists():
        return []
    try:
        payload = read_json(path)
    except Exception:
        return []
    return payload if isinstance(payload, list) else []


def save_and_register(fig, stem: str, caption: str, source: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    FIG.mkdir(parents=True, exist_ok=True)
    path = FIG / stem
    fig.savefig(str(path.with_suffix(".pdf")), bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(str(path.with_suffix(".png")), bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    entry = {
        "id": stem,
        "png": str(path.with_suffix(".png").relative_to(OUT)),
        "pdf": str(path.with_suffix(".pdf").relative_to(OUT)),
        "caption": caption,
        "description": caption,
        "source": source,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "metadata": metadata or {},
    }
    registry = [item for item in figure_registry() if item.get("id") != stem]
    registry.append(entry)
    write_json(OUT / "FIGURES.json", registry)
    append_session(f"FIGURE_READY: phase3_selection/outputs/{entry['png']}")
    return entry


def make_hist(edges: np.ndarray, values: np.ndarray):
    h = hist.Hist(hist.axis.Variable(edges, name="x"), storage=hist.storage.Double())
    h.view(flow=False)[:] = values
    return h


def data_mc_comparison(
    edges: np.ndarray,
    data_counts: np.ndarray,
    mc_by_stack: dict[str, np.ndarray],
    xlabel: str,
    ylabel: str,
    rlabel: str,
    legend_loc: str = "upper right",
):
    fig, (ax, rax) = plt.subplots(2, 1, figsize=(10, 10), gridspec_kw={"height_ratios": [3, 1]}, sharex=True)
    fig.subplots_adjust(hspace=0)
    centers = 0.5 * (edges[:-1] + edges[1:])
    widths = np.diff(edges)
    stacks = [name for name in STACK_ORDER if name in mc_by_stack and np.sum(mc_by_stack[name]) > 0]
    stacks.extend(name for name in mc_by_stack if name not in stacks and np.sum(mc_by_stack[name]) > 0)
    hists = [make_hist(edges, mc_by_stack[name]) for name in stacks]
    colors = [STACK_COLORS.get(name) for name in stacks]
    if hists:
        mh.histplot(hists, ax=ax, stack=True, histtype="fill", label=stacks, color=colors, alpha=0.75)
    data_err = np.sqrt(data_counts)
    ax.errorbar(centers, data_counts, yerr=data_err, xerr=0.5 * widths, marker="o", linestyle="None", color="black", label="Data")
    mc_total = np.sum(np.vstack([mc_by_stack[name] for name in stacks]), axis=0) if stacks else np.zeros_like(data_counts, dtype=float)
    visible_top = max(float(np.max(data_counts + data_err)) if len(data_counts) else 0.0, float(np.max(mc_total)) if len(mc_total) else 0.0)
    if visible_top > 0.0:
        current_bottom, current_top = ax.get_ylim()
        ax.set_ylim(current_bottom, max(current_top, visible_top * 1.55))
    pull_den = np.sqrt(data_counts + np.maximum(mc_total, 0.0))
    pulls = np.zeros_like(data_counts, dtype=float)
    np.divide(data_counts - mc_total, pull_den, out=pulls, where=pull_den > 0)
    rax.axhline(0.0, color="black", linewidth=1)
    rax.errorbar(centers, pulls, yerr=np.ones_like(pulls), xerr=0.5 * widths, marker="o", linestyle="None", color="black")
    rax.set_ylim(-3.5, 3.5)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    rax.set_ylabel("Pull")
    rax.set_xlabel(xlabel)
    ax.tick_params(labelbottom=False)
    ax.legend(loc=legend_loc, fontsize="x-small")
    mpl_magic(ax)
    mh.label.exp_label(
        exp="CMS",
        text="",
        loc=2,
        data=True,
        llabel="Open Data and Open Simulation",
        rlabel=rlabel,
        ax=ax,
    )
    return fig
