# Work Log

## 2026-06-20

- Inspected the repository, current ignored outputs, available raw ROOT inputs, and existing plotting code.
- Increased the configured lepton pT scale shifts in `config.json`; energy changes follow the pT scaling for available energy branches.
- Updated `plot.py` to organize output figures under `distributions/`, `efficiency/`, and `correlation/{input,output,delta}/`.
- Added per-pair correlation delta heatmaps using `Modified - raw` bin counts.
- Started improving TnP fits:
  - added fit-quality checks based on RooFit status, covariance quality, and pass/fail chi2/ndf;
  - wrote chi2/ndf and fit status directly on fit PDFs;
  - added rejected-fit diagnostic PDFs;
  - raised the minimum statistics for fitted TnP points and fall back to counting for low-stat or rejected fits;
  - decoupled pass/fail signal width parameters to improve fit stability.
- Inspected rejected fit PDFs. The low-mass structure below 90 GeV can mimic a second peak after other selections; per user instruction, removed the attempted two-peak model and changed the TnP fit mass range to start at 90 GeV.
- Quick plot validation on the smallest ROOT sample with `plot.py` in pixi:
  - no `two_gaussian` fit PDFs were produced;
  - 232 accepted fit PDFs and 59 rejected diagnostic fit PDFs were produced for the reduced quick config;
  - only 6 TnP bins fell back to counting after chi2/ndf rejection;
  - correlation input/output/delta directories were produced, with 10 delta heatmaps in the quick config.
- Checked the requested `modify_nanoaod` runtime environment. `/cvmfs/cms.cern.ch/cmsset_default.sh` is not present in this workspace environment, so final compile/run of `modify_nanoaod` with the required CVMFS sources cannot be performed here until CVMFS is available.
- Verified the pixi environment provides ROOT 6.40.02 and the required Python plotting packages.
