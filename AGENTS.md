# Agent Notes

- Record major work and validation results in `log.md`.
- Keep generated ROOT files, figures, temporary configs, caches, and local environment files out of git unless they are already tracked.
- Use the CMS/LCG environment for compiling or running `modify_nanoaod`:
  `source /cvmfs/cms.cern.ch/cmsset_default.sh`
  `source /cvmfs/sft.cern.ch/lcg/views/LCG_108/x86_64-el9-gcc14-opt/setup.sh`
- Use the pixi environment for `plot.py` and Python plotting diagnostics.
- Do not mix the pixi environment with `modify_nanoaod` compilation or execution.
- Before full production reruns, use one small ROOT file for fast validation of code changes.
- For TnP fits, use the configured mass range starting at 90 GeV and inspect rejected fit PDFs before changing fit models or thresholds.
