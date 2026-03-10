# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a demo/talk example showing Claude Code's multi-agent orchestration capabilities. The primary artifact is `harmonic_oscillator_animation/` — a PyQt6 desktop app that animates an undamped simple harmonic oscillator, built by 1 supervisory agent coordinating 7 specialist subagents.

The prompt used to generate it is in `harmonic_oscillator_animation_prompt.txt`. The run summary (timing, token usage, test results) is in `harmonic_oscillator_animation_run_summary.md`.

## Environment

Conda environment: `harmonic_oscillator_animation` (Python 3.11, numpy, scipy, matplotlib, PyQt6 via pip)

```bash
bash setup_env.sh   # creates env and installs package
```

## Running the App

```bash
./run.sh   # uses conda run; no manual env activation needed
```

## Development Commands

All commands run from within `harmonic_oscillator_animation/` with the conda env active.

```bash
# Lint
ruff check src/ tests/
ruff format --check src/ tests/
ruff format src/ tests/   # auto-fix formatting

# Tests (requires display; use xvfb-run on headless systems)
pytest --tb=short
xvfb-run --auto-servernum pytest   # headless

# Single test file
pytest tests/unit/test_physics.py
pytest tests/integration/test_widgets.py
pytest tests/e2e/test_app.py
```

Coverage threshold is 80% (enforced via `--cov-fail-under=80` in pyproject.toml).

## Architecture

`src/harmonic_oscillator_animation/` contains:

- **`physics.py`** — module-level constants (MASS, SPRING_K, AMPLITUDE, OMEGA_0, PERIOD) and pure functions (`position`, `velocity`, `acceleration`, `time_series`). No classes, numpy only.
- **`spring_renderer.py`** — `SpringRenderer(ax)` draws the animated coil spring + mass block on a matplotlib Axes. `update(x)` repositions artists for the current displacement.
- **`plot_widget.py`** — `PlotWidget(ax)` maintains a `deque` of (t, x) pairs. `append(t, x)` adds a point; `refresh()` redraws the line.
- **`app.py`** — `MainWindow(QMainWindow)` wires the two canvases into a `QVBoxLayout`, drives the loop via a `QTimer` (FRAME_MS=33 ms, ~30 fps), resets after 10×PERIOD.
- **`main.py`** — entry point: `QApplication` → `MainWindow.show()` → `exec()`.

Tests are organized as `tests/unit/`, `tests/integration/`, and `tests/e2e/`. The `conftest.py` provides an `app_window` fixture (MainWindow via qtbot, not shown).

CI runs lint then test (with xvfb) on ubuntu-latest via `.github/workflows/ci.yml`.
