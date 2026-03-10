"""
Simple Harmonic Oscillator (SHO) physics module.

Models a mass-spring system governed by Hooke's law: F = -k * x,
which yields the equation of motion x''(t) = -(k/m) * x(t).

The general solution is x(t) = A * cos(omega_0 * t + phi), where:
  - A       is the amplitude of oscillation (metres)
  - omega_0 = sqrt(k / m) is the natural angular frequency (rad/s)
  - phi     is the initial phase (radians)

All physical quantities use SI units (kg, N/m, m, s).
"""

import numpy as np

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------
MASS = 1.0  # kg
SPRING_K = 10.0  # N/m
AMPLITUDE = 0.15  # m
PHASE = 0.0  # rad

OMEGA_0 = np.sqrt(SPRING_K / MASS)  # rad/s
PERIOD = 2 * np.pi / OMEGA_0  # s


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------


def position(t: float) -> float:
    """Return the displacement x(t) = AMPLITUDE * cos(OMEGA_0 * t + PHASE)."""
    return AMPLITUDE * np.cos(OMEGA_0 * t + PHASE)


def velocity(t: float) -> float:
    """Return the velocity v(t) = -AMPLITUDE * OMEGA_0 * sin(OMEGA_0 * t + PHASE)."""
    return -AMPLITUDE * OMEGA_0 * np.sin(OMEGA_0 * t + PHASE)


def acceleration(t: float) -> float:
    """Return the acceleration a(t) = -OMEGA_0**2 * position(t)."""
    return -(OMEGA_0**2) * position(t)


def time_series(t_arr: np.ndarray) -> np.ndarray:
    """Return position values for an array of times; vectorised position()."""
    return AMPLITUDE * np.cos(OMEGA_0 * t_arr + PHASE)
