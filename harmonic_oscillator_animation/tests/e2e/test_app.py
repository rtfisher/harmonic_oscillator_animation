"""End-to-end tests for MainWindow."""

from harmonic_oscillator_animation.app import FRAME_MS
from harmonic_oscillator_animation.physics import PERIOD


def test_window_title(app_window):
    assert app_window.windowTitle() == "Simple Harmonic Oscillator"


def test_window_size(app_window):
    assert app_window.width() == 700
    assert app_window.height() == 800


def test_timer_fires(app_window, qtbot):
    initial_t = app_window._t
    # Wait enough time for at least one timer tick
    qtbot.wait(FRAME_MS * 3)
    assert app_window._t > initial_t


def test_loop_reset(app_window, qtbot):
    # Place time just before reset threshold
    app_window._t = 10 * PERIOD - (FRAME_MS / 1000.0) * 0.5
    # Seed some plot data so we can verify it gets cleared
    app_window._plot_widget.append(0.1, 0.01)
    # Trigger one tick manually
    app_window._tick()
    # After reset, _t should be small (restarted from 0 + one step)
    assert app_window._t < FRAME_MS / 1000.0 + 1e-9
    # Buffer should contain exactly one point (appended at t=0 after reset)
    assert len(app_window._plot_widget._t_buf) == 1
    assert list(app_window._plot_widget._t_buf)[0] == 0.0
