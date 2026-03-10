"""Integration tests for SpringRenderer and PlotWidget."""

import matplotlib
import pytest

matplotlib.use("Agg")  # headless backend for CI
import matplotlib.pyplot as plt

from harmonic_oscillator_animation.plot_widget import PlotWidget
from harmonic_oscillator_animation.spring_renderer import (
    EQUILIBRIUM_Y,
    MASS_HEIGHT,
    SpringRenderer,
)


@pytest.fixture
def spring_ax():
    fig, ax = plt.subplots()
    yield ax
    plt.close(fig)


@pytest.fixture
def plot_ax():
    fig, ax = plt.subplots()
    yield ax
    plt.close(fig)


def test_spring_renderer_update_returns_artists(spring_ax):
    renderer = SpringRenderer(spring_ax)
    artists = renderer.update(0.1)
    assert isinstance(artists, list)
    assert len(artists) > 0


def test_spring_renderer_mass_position(spring_ax):
    renderer = SpringRenderer(spring_ax)
    x_offset = 0.05
    renderer.update(x_offset)
    # FancyBboxPatch .get_y() returns bottom-left y; center = get_y() + MASS_HEIGHT/2
    patch_center_y = renderer._mass_patch.get_y() + MASS_HEIGHT / 2
    expected_y = EQUILIBRIUM_Y + x_offset
    assert patch_center_y == pytest.approx(expected_y, abs=1e-6)


def test_plot_widget_append_and_refresh(plot_ax):
    widget = PlotWidget(plot_ax)
    for i in range(5):
        widget.append(float(i) * 0.1, float(i) * 0.01)
    widget.refresh()
    xdata, ydata = widget._line.get_data()
    assert len(xdata) == 5
    assert len(ydata) == 5


def test_plot_widget_clear(plot_ax):
    widget = PlotWidget(plot_ax)
    for i in range(5):
        widget.append(float(i) * 0.1, float(i) * 0.01)
    widget.clear()
    widget.refresh()
    xdata, ydata = widget._line.get_data()
    assert len(xdata) == 0
    assert len(ydata) == 0
