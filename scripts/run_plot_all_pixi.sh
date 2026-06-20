#!/usr/bin/env bash
set -euo pipefail

rm -rf figures
mkdir -p figures

pixi run python plot.py --config-plot config_plot.json "$@"
