#!/bin/bash
set -e

SCRIPT_DIR="$(dirname "$0")"

conda env create -f "$SCRIPT_DIR/harmonic_oscillator_animation/environment.yml"
conda run -n harmonic_oscillator_animation pip install -e "$SCRIPT_DIR/harmonic_oscillator_animation/"

echo "Done. Activate with: conda activate harmonic_oscillator_animation"
