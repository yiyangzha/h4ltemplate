# Doc 4a Fix Summary

Session: wanda_5bec
Date: 2026-05-30

## Findings Resolved

### Category A: raw dictionary in sideband caption

Resolved. Rewrote the caption for `fig:sideband-dy-ttbar-diagnostics` as prose and rounded the TTBar/DY ratios to 0.16, 0.10, and 0.044.

### Category B: sparse-workspace and corruption limitation understated

Resolved. Added concise abstract and conclusion language stating that the final-state workspace is sparse, with 17 of 18 expected bins having `S+B<5`, and that the `-20%` corruption sensitivity is documented low-count infeasible after three attempts, not passed.

### Category B: Asimov central-value pull comparison

Resolved. Removed the CMS-HIG-16-041 central-value pull calculation and table wording. The comparison now discusses only uncertainty ratio and analysis scope for the Asimov expected result.

### Category B: mass-profile external comparison

Resolved. Recast the mass-profile discussion as internal shifted-template closure only and removed CMS/PDG mass-delta wording from the mass-profile comparison.

### Category C: appendix caption polish

Resolved. Replaced literal inequality wording in appendix captions with math range notation and rounded excessive caption precision where straightforward.

### Category C: truncated corruption-test row

Resolved. Expanded the truncated table entries to full phrases, including "profiled Pearson chi2 on the final-state simultaneous workspace".

## Verification

- Recompiled with `pixi run tectonic --keep-logs analysis_note/ANALYSIS_NOTE_doc4a_v1.tex`.
- Checked for raw dictionary caption, central-value pull phrase, CMS/PDG mass deltas, literal inequality wording, and truncated `simulta` table text.
- Checked included figure files exist under `analysis_note/figures/`.
- Checked `analysis_note/ANALYSIS_NOTE_doc4a_v1.log` for `Overfull`, `undefined`, and `Citation`; no matches.
- Ran `git diff --check`; no whitespace errors.

## Remaining Issues

The TeX compile reported existing Underfull hbox warnings only. No requested blocking issue remains.
