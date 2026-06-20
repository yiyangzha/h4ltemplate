# Agent Notes

- Record major work and validation results in `log.md`.
- Keep generated ROOT files, figures, temporary configs, caches, and local environment files out of git unless they are already tracked.
- Use the CMS/LCG environment for compiling or running `modify_nanoaod`:
  `source /cvmfs/cms.cern.ch/cmsset_default.sh`
  `source /cvmfs/sft.cern.ch/lcg/views/LCG_108/x86_64-el9-gcc14-opt/setup.sh`
- If CVMFS is unavailable and the user approves the fallback, use `scripts/run_modify_all_pixi.sh` to build and run `modify_nanoaod` with the pixi ROOT toolchain.
- Use the pixi environment for `plot.py` and Python plotting diagnostics.
- Use `scripts/build_an_pixi.sh` to compile the AN draft with pixi/tectonic.
- Do not mix the pixi environment with `modify_nanoaod` compilation or execution.
- Before full production reruns, use one small ROOT file for fast validation of code changes.
- For TnP fits, keep the broad mass fit range for sidebands and inspect rejected fit PDFs before changing fit models or thresholds.
