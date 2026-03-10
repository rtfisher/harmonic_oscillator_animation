"""Pytest configuration and shared fixtures."""

import pytest

from harmonic_oscillator_animation.app import MainWindow

# pytest-qt provides the qtbot fixture automatically.


@pytest.fixture
def app_window(qtbot):
    """Create a MainWindow instance without showing it."""
    window = MainWindow()
    qtbot.addWidget(window)
    return window
