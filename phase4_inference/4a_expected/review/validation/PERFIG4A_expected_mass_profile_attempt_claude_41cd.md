# Per-figure validation: `expected_mass_profile_attempt`

Session: `claude_41cd`

Verdict: **PASS**

Checks performed:

- Registry/coherence: `FIGURES.json` matches the rendered artifact name and explicitly marks this plot as **not promoted** to a nominal mass measurement.
- Visual quality: the curve, axes, legend, and experiment label are legible; no overlap or clipping is visible in the rendered PNG.
- Label quality: the figure is labeled `CMS Open Simulation`, which is consistent with a method-parity / closure-style artifact rather than an official measurement.
- Metadata/number consistency: the scan shown in the plot is consistent with the registry/source summary, and the minimum is visually located near the nominal 125 GeV point as expected for the closure attempt.
- Physics sanity: the plot behaves like a smooth profile-likelihood scan with a well-defined minimum; nothing suggests a malformed scan or an accidental publication-style mass result.

No fixes required.
