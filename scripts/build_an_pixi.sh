#!/usr/bin/env bash
set -euo pipefail

pixi run tectonic notes/an.tex --outdir notes "$@"
