# modify_nanoaod

Compiled ROOT/C++17 tool for modifying NanoAOD lepton pT and configured ID/Iso/Trig branches in place.

## 1. How to Run

Build:

```bash
make
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

## 2. Config: input

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

## 3. Config: output

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

## 4. Config: scale

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
