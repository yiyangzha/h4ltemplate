# Per-Figure Validation: `cutflow_summary`

Result: **FAIL**

Source checked:
- `phase3_selection/outputs/FIGURES.json` entry for `cutflow_summary`
- `phase3_selection/outputs/figures/cutflow_summary.png`

Assessment:
- The caption and metadata are coherent: the figure is a cumulative Phase 3 cutflow, and the visible endpoint is consistent with the metadata/caption values of **69 data events** and **56.6098 expected MC events**.
- The figure is **not publication-ready as rendered** because the x-axis labels are too dense and the long cut names are hard to read at normal AN size. The multiline tick labels crowd the bottom margin, especially for the `broad validation window` and `fit window` steps, and the final numeric range labels are visually awkward.

Failures:
1. **Readability / long x tick labels**
   - The cut names are too long for the current horizontal layout.
   - Several labels wrap into multiple lines and crowd the bottom of the panel.
   - The bottom axis text is near the threshold where a reviewer would need to zoom to read it cleanly.
   - Fix: shorten the displayed tick labels to concise publication names, e.g. `all`, `finite core`, `trigger > 0`, `valid FS`, `flavor-matched ID`, `Z-pair sanity`, `70-170`, `105-140`, and move the full cut definitions into the caption or a note below the figure.

2. **Label clarity**
   - The long window labels are rendered as stacked text blocks with embedded numeric ranges, which makes the sequence harder to scan.
   - Fix: render the window steps as compact labels and, if necessary, add a small legend or footnote for the exact mass windows rather than encoding them in the tick labels.

PASS criteria not met:
- Readability at AN scale
- Clean publication-style tick labeling

