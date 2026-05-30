# Plot Watcher Fallback

Session: `vera_3fd2`  
Executor: `yuki_9d50`  
Date: `2026-05-30`  
Verdict: `FAIL`

Standard used: `agents/plot_validator.md` (fallback base; `agents/plot_watcher.md` absent).

Registry check:
- `phase4_inference/4b_partial/outputs/FIGURES.json` exists but contains `[]` while two PNGs exist in `outputs/figures/`. This is a blocker for figure tracking and caption/metadata review.

Figures:

1. `partial_m4l_broad_inclusive.png` — `FAIL`
- Legend overlaps active plot content, including the tall data error bar near the qqZZ peak. Move the legend to genuinely empty space or reduce/restructure it.
- Broad `70-170 GeV` view does not make the `105-140 GeV` fit window visually clear. Add a shaded band, bracket, inset, or explicit annotation so the relation between the broad spectrum and fit region is obvious.
- Data/MC normalization convention is not stated on the figure. Make the normalization treatment explicit in the caption and ensure the plot presentation is consistent with that statement.
- Ratio panel readability is weak: the `Data/MC` y-label is oversized relative to the panel and dominates the lower subplot. Reduce label size or adjust layout.

2. `partial_m4l_fit_window_categories.png` — `FAIL`
- Top labels are severely overlapped/clipped: `CMS`, `Open Data`, and luminosity text collide across the first two panels. Rebuild the layout so the experiment label appears once, cleanly, and within bounds.
- The legend intrudes into the `2e2mu` panel and obscures the plotted region. Move it outside the axes or into unused whitespace above/below the panel grid.
- Panel composition is too cramped for three category plots at this size. Increase canvas height/spacing or redesign the arrangement so labels, panel names, and legend no longer collide.
- Fit-window presentation is implicit but acceptable from the x-range; the blocking issue is readability, not physics content.

Required fixes before PASS:
- Populate `FIGURES.json` with the produced figures.
- Regenerate both PNGs after layout fixes.
- Recheck that labels, legend placement, and fit-window communication remain readable at analysis-note scale.
