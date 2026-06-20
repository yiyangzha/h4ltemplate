# modify_nanoaod

Compiled ROOT/C++17 tool for modifying NanoAOD lepton pT and configured ID/Iso/Trig branches in place.

## 1. How to Run

Build:

```bash
make
```

Equivalent direct build command:

```bash
c++ -O3 -DNDEBUG -Wall -Wextra -Wpedantic $(root-config --cflags) \
  -o modify_nanoaod modify_nanoaod.cpp $(root-config --libs)
```

If CVMFS is available, set up the CMS/LCG toolchain first:

```bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
source /cvmfs/sft.cern.ch/lcg/views/LCG_108/x86_64-el9-gcc14-opt/setup.sh
```

If CVMFS is not available but the local pixi environment has ROOT, use:

```bash
pixi run make
```

Run:

```bash
./modify_nanoaod --config config.json
```

Useful options:

```bash
./modify_nanoaod --config config.json --dry-run
./modify_nanoaod --config config.json --threads 8
```

`--dry-run` checks input discovery and output names without writing files. `--threads` overrides `global.threads` from the config.

Run the plotting step in the pixi environment:

```bash
pixi run python plot.py --config-plot config_plot.json
```

The plotting code writes TnP fit status and pass/fail `chi2/ndf` values onto fit PDFs. Fits with bad status, covariance quality, or `chi2/ndf` above the configured threshold fall back to counting efficiencies.

## 2. Modification invariants

- Lepton pT scale and resolution are deterministic functions of the configured flavor/eta/pT/charge rules and a stable event-object RNG key. They are not derived from the input sample distribution.
- Efficiency maps are pre-scanned once across all configured input ROOT files, then the merged target/current maps are used for every output file. The branch updates use minimal flips to reach the common target curve.
- Efficiency distortions are limited to an overall vertical factor plus the configured turn-on horizontal shift and width change.
- For truth-matched H/Z opposite-sign same-flavor lepton pairs, non-random center-value pT/energy scale changes preserve the reconstructed dilepton invariant mass. Random resolution smearing is still allowed to change the mass.

## 3. Config: input

```json
"input": {
  "path": "/path/to/*.root",
  "recursive": true
}
```

- `path`: input ROOT file, directory, or wildcard pattern.
- `paths`: optional array form for multiple inputs.
- `recursive`: when `path` is a directory, recursively find `.root` files if true.

The program writes one output ROOT file per input ROOT file.

## 4. Config: output

```json
"output": {
  "directory": "modified",
  "suffix": "_modified",
  "copy_metadata_trees": true,
  "overwrite": false
}
```

- `directory`: output directory.
- `suffix`: suffix added to each input file stem.
- `copy_metadata_trees`: copy non-`Events` trees and metadata objects when practical.
- `overwrite`: if false, stop when an output file already exists.

## 5. Config: scale

```json
"scale": {
  "enabled": true,
  "pt_reference": 45.0,
  "muon": {
    "barrel": {
      "abs_eta_min": 0.0,
      "abs_eta_max": 1.2,
      "constant": 0.0010,
      "pt_slope_log": 0.0,
      "charge_asymmetry": 0.0
    }
  }
}
```

For each lepton:

```text
pt_new = pt_old * (1 + scale_shift)
scale_shift = constant + pt_slope_log * log(pt / pt_reference) + charge_asymmetry * charge
```

- `enabled`: turn pT scale modification on or off.
- `pt_reference`: reference pT used in the logarithmic slope term.
- `muon` / `electron`: flavor-specific eta regions.
- `abs_eta_min`, `abs_eta_max`: region boundaries in `abs(eta)`.
- `constant`: constant fractional pT shift.
- `pt_slope_log`: logarithmic pT-dependent fractional shift.
- `charge_asymmetry`: optional charge-dependent fractional shift.

Eta, phi, mass, and lepton counts are unchanged unless separately configured in code.
