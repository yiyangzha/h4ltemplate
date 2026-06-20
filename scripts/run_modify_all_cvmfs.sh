#!/usr/bin/env bash
set -euo pipefail

source /cvmfs/cms.cern.ch/cmsset_default.sh
source /cvmfs/sft.cern.ch/lcg/views/LCG_108/x86_64-el9-gcc14-opt/setup.sh

make

rm -rf modified
mkdir -p modified

./modify_nanoaod --config config.json "$@"
