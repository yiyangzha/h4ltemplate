#!/usr/bin/env bash
set -euo pipefail

pixi run make

rm -rf modified
mkdir -p modified

pixi run ./modify_nanoaod --config config.json "$@"
