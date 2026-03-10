"""Unit tests for the physics module."""

import numpy as np
import pytest

from harmonic_oscillator_animation.physics import (
    AMPLITUDE,
    MASS,
    OMEGA_0,
    PERIOD,
    SPRING_K,
    acceleration,
    position,
    time_series,
    velocity,
)


def test_position_at_zero():
    assert position(0.0) == pytest.approx(AMPLITUDE)


def test_position_at_quarter_period():
    assert abs(position(PERIOD / 4)) < 1e-9


def test_position_at_half_period():
    assert position(PERIOD / 2) == pytest.approx(-AMPLITUDE, abs=1e-9)


def test_velocity_at_zero():
    assert velocity(0.0) == pytest.approx(0.0, abs=1e-9)


def test_velocity_at_quarter_period():
    assert abs(velocity(PERIOD / 4)) == pytest.approx(AMPLITUDE * OMEGA_0, rel=1e-6)


def test_acceleration_proportional():
    rng = np.random.default_rng(42)
    t_vals = rng.uniform(0, 10 * PERIOD, size=10)
    for t in t_vals:
        assert acceleration(t) == pytest.approx(-(OMEGA_0**2) * position(t), rel=1e-9)


def test_time_series_shape():
    t_arr = np.linspace(0, PERIOD, 100)
    result = time_series(t_arr)
    assert result.shape == (100,)


def test_energy_conservation():
    t_arr = np.linspace(0, PERIOD, 20)
    x_arr = time_series(t_arr)
    v_arr = np.array([velocity(t) for t in t_arr])
    ke = 0.5 * MASS * v_arr**2
    pe = 0.5 * SPRING_K * x_arr**2
    total = ke + pe
    expected = 0.5 * SPRING_K * AMPLITUDE**2
    np.testing.assert_allclose(total, expected, rtol=1e-6)
