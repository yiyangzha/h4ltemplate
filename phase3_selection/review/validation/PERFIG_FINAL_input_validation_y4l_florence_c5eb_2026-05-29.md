# Per-Figure Validation: `input_validation_y4l`

Result: **PASS**

Reviewed against `TOGGLES.md`, `agents/plot_validator.md`, `methodology/appendix-plotting.md`, `phase3_selection/outputs/FIGURES.json`, and `phase3_selection/outputs/figures/input_validation_y4l.png`.

Checks:
- The figure is registered in `FIGURES.json` with matching `id`, `png`, and caption metadata.
- The rendered panel is legible at publication size.
- Axis labels, tick labels, legend text, and annotations are readable.
- The experiment branding and ratio panel placement are consistent with the project plotting rules.
- No legend overlap, text collision, clipped content, or spurious artifacts are visible.
- The main panel and pull panel are coherent with the metadata values: `chi2 = 4983.397328708181`, `ndf = 5`, `p = 0.0`, `passes_d7_gate = false`.

No fixes required.
