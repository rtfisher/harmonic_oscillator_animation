#!/bin/bash
PYTHONPATH="$(dirname "$0")/harmonic_oscillator_animation/src" \
conda run -n harmonic_oscillator_animation python -m harmonic_oscillator_animation.main
