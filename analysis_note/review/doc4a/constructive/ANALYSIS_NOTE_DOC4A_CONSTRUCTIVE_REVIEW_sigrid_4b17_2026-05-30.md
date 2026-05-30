Verdict: ITERATE

No Category A findings. The note is honest about the expected-only stage and the major downscopes, but a few presentation choices still risk overstating what Phase 4a has established to a referee.

## Category B

1. Abstract/conclusion still read too cleanly relative to the actual low-count limitation.
   Evidence: [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:33), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:571), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:581), [REGRESSION_CHECK_phase4a.md](/sandbox/work/jfc/analyses/higgs_4lep_mass/REGRESSION_CHECK_phase4a.md:11)
   The body is honest, but the abstract and conclusion do not foreground that the nominal final-state workspace is extremely sparse and that the `-20%` corruption test remained non-rejecting after three attempts. A referee can otherwise take the opening summary as a routine expected measurement writeup rather than an expected result with a one-sided sensitivity caveat.
   Requested fix: put one sentence in the abstract and one in the conclusion stating that Phase 4a is retained despite `17/18` bins with expected `S+B<5`, with the `-20%` corruption test documented as low-count infeasible rather than passed.

2. The CMS central-value "pull" comparison is more misleading than helpful for an Asimov result.
   Evidence: [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:537), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:549), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:571)
   Since `mu=1` is fixed by Asimov construction, the only quantitative comparison with CMS that carries real content here is precision, not central value. Reporting a `-0.083 sigma` pull invites the reader to interpret agreement where no observed-data comparison has actually been performed.
   Requested fix: remove the central-value pull language from the prose/table/conclusion, and keep the comparison explicitly on uncertainty ratio and scope differences.

3. The mass-profile discussion still gives external numeric differences that look closer to a measurement comparison than to closure.
   Evidence: [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:539), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:551), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:573)
   The note repeatedly says the mass-profile attempt is not an official measurement, which is good. But quoting `0.26 GeV` and `0.20 GeV` differences to CMS/PDG still nudges the narrative toward performance comparison, even though the exercise is detector-level shifted-template closure on injected signal.
   Requested fix: recast this section as internal closure only. If external references remain, state them qualitatively and avoid numeric deltas that resemble measurement residuals.

## Category C

1. The expected-only scope would be easier for a referee to parse with one compact "what Phase 4a establishes" paragraph at the start of Expected Results.
   Evidence: [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:462)
   Suggested content: one sentence each on what is established now (expected precision, validation status, documented downscopes) and what is explicitly deferred to Doc 4b/4c (observed `mu`, observed GoF, any data-constraining nuisance behavior).

2. Main-text numerics are too high-precision for note prose.
   Evidence: [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:33), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:259), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:571)
   Suggested fix: round prose/table values to sensible precision and leave full machine precision to the JSON payloads and auxiliary tables.

3. The note is strongest when it states downscopes in plain referee language; keep doing that consistently in comparison-facing lines.
   Evidence: [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:463), [analysis_note/ANALYSIS_NOTE_doc4a_v1.tex](/sandbox/work/jfc/analyses/higgs_4lep_mass/analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:577)
   Suggested fix: prefer phrases like "expected precision only" and "closure exercise only" over compact comparison shorthand anywhere a referee could mistake a staging artifact for a measured agreement.
