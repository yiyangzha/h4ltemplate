# Per-figure validation: cutflow_summary

Result: PASS

Checks performed:
- `TOGGLES.md` reviewed: `REVIEW_MODEL_DIVERSITY=true`.
- `agents/plot_validator.md` reviewed for visual validation criteria.
- `methodology/appendix-plotting.md` reviewed for plotting standards.
- `phase3_selection/outputs/FIGURES.json` entry for `cutflow_summary` reviewed.
- Rendered PNG inspected: `phase3_selection/outputs/figures/cutflow_summary.png`.

Assessment:
- The redesigned cutflow is readable at AN size. The abbreviated step labels are legible and no longer form dense multi-line blocks.
- The endpoint values are coherent with the metadata: data raw events end at 69 and MC weighted yield ends at 56.6098, matching the figure description and JSON metadata.
- No title-like text is present on the plot itself. The CMS/Open Data/Open Simulation branding and the `13 TeV, 10 fb^-1` text are part of the experiment label style, not a figure title.
- No visible overlap, clipping, or label collision is present. The legend sits in an open region and does not obscure data.

Verdict: PASS
