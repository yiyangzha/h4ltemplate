PASS

# Doc 4a Critical Review

Session: `renata_b98b`  
Date: 2026-05-30  
Artifact: `analysis_note/ANALYSIS_NOTE_doc4a_v1.{tex,pdf}`

## Scope

Reviewed the Doc 4a note source, compiled-PDF evidence from VERIFY, result JSON files, commitments, Phase 4a regression check, Phase 4a summary, and upstream Phase 4a/Phase 3 artifacts. MCP tools were false and were not called. Local PDF text/metadata extraction tools (`pdftotext`, `pdfinfo`) were unavailable, so PDF review relied on the compiled PDF file existence plus the VERIFY compile/page-count evidence and the LaTeX source that generated it.

## Findings

### C1. Appendix input-validation captions use awkward literal inequality wording

Category: C

Evidence: Fourteen appendix captions render the broad validation window as literal prose, e.g. `70  less than or equal to  m4l  less than or equal to  170 GeV`, rather than a mathematical range. Examples are in `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:633`, `:640`, `:647`, `:654`, `:661`, `:668`, `:675`, `:682`, `:689`, `:696`, `:703`, `:710`, `:717`, and `:724`.

Impact: This does not alter physics content or figure staging because the captions still clearly identify the broad 70-170 GeV classifier-input diagnostic window and state that these plots do not normalize fit templates. It is presentation polish for Doc 4b/4c.

### C2. One corruption-test table entry is visibly truncated in source

Category: C

Evidence: The third row of the low-count corruption-sensitivity table says `profiled Pearson chi2 on the final-state simulta` in `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:431`. The same test is correctly described in JSON as `profiled Pearson chi2 on the final-state simultaneous expected bins` with statistic 22.7243, ndf 17, and p=0.15844 in `analysis_note/results/expected_validation.json:126`.

Impact: Non-blocking, because the table still gives the correct statistic/ndf/p-value and the surrounding prose states that the -20% mass-response corruption is documented low-count infeasible. It should be expanded before a final public note.

## Checks Performed

Number consistency: PASS. The note quotes `mu = 1.0 +0.6327358408468291 -0.51674064615437` and symmetric uncertainty `0.5747382435005995` in the abstract and conclusions (`analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:33`, `:571`), matching `expected_parameters.json` (`value=1.0`, `uncertainty_minus=0.51674064615437`, `uncertainty_plus=0.6327358408468291`, `uncertainty_symmetric=0.5747382435005995`; `analysis_note/results/expected_parameters.json:107-110`). The variance decomposition in the note (`V_stat=0.3063689401723719`, `V_syst=0.023955108369782596`, `V_tot=0.33032404854215447`; `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:227`) matches `expected_covariance.json` (`analysis_note/results/expected_covariance.json:141-143`; MC stat component at `:140`).

Expected-only staging: PASS. The note states that no observed Open Data counts are used as pseudo-data (`analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:33`, `:198`, `:505`), and the JSON source says the Asimov observation is the nominal model expectation plus auxiliary data with no observed counts (`analysis_note/results/expected_parameters.json:2`). Asimov chi2/p=1 is correctly framed as bookkeeping rather than independent GoF (`analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:457`; JSON chi2/p at `analysis_note/results/expected_parameters.json:99-102`).

No tuning to references: PASS. The comparison section says CMS-HIG-16-041 and CMS-HIG-19-001 are context only and not fit inputs (`analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:537`). The precision ratio 3.193 agrees with the validation JSON ratio `3.192990241669998` (`analysis_note/results/expected_validation.json:271`).

Limitations carried honestly: PASS. The note carries the grouped MC-stat downscope (`analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:264-265`), non-official mass-profile status (`:511-512`, `:539`), VBF/NN downscopes (`:49`, `:103`, `:583`), and the non-rejected -20% mass-response corruption limitation (`:424-431`, `:581`). The JSON records `criterion_status=documented_low_count_infeasible` and `passes=false`, with three p-values 0.45954, 0.60486, and 0.15844 (`analysis_note/results/expected_validation.json:99-126`).

Completion vs Doc 4a requirements: PASS. VERIFY records 66-page PDF compilation, 49 figure references, 49 unique figures, zero missing figures, zero TBD placeholders, and no undefined citation/reference warnings (`analysis_note/review/doc4a/VERIFY_odette_354d_2026-05-30.md`). The TeX includes 49 `includegraphics` commands and `analysis_note/figures` contains 49 PDFs. The note includes the expected result, systematic inventory, validation/cross-checks, comparison matrix, limitations, reproduction contract, and machine-readable-result index.

Decision/commitment traceability: PASS with documented downscopes. Phase 3 selected S1 final-state categories and documented 17/18 low-count final-state bins (`phase3_selection/outputs/SELECTION.md:8-16`, `:101-120`). Phase 4a retained the final-state model only after toy and binning validation (`phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md:50-72`). `COMMITMENTS.md` records D1-D9 as resolved or formally downscoped, with SP3 full bin-by-bin MC stat still explicitly downscoped rather than silently declared complete (`COMMITMENTS.md:58-64`).

Figure/caption coherence: PASS for physics staging. Body captions distinguish broad validation plots from fit-window templates (`analysis_note/ANALYSIS_NOTE_doc4a_v1.tex:138-139`, `:738-739`) and expected Asimov templates from observed data (`:505`). The two Category C caption polish issues above do not change physics interpretation.

## Verdict

PASS. I found no Category A or B issue. The note is internally consistent with the JSON source of truth, preserves expected-only staging, does not tune to reference results, and carries the material limitations into the AN. The two Category C findings should be cleaned up in the next note revision but do not block Doc 4a review.
