from collections import deque

import matplotlib.axes  # for type hint only
import numpy as np

from harmonic_oscillator_animation.physics import AMPLITUDE, PERIOD


class PlotWidget:
    def __init__(self, ax: matplotlib.axes.Axes) -> None:
        self._ax = ax
        self._t_buf = deque()
        self._x_buf = deque()

        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Position (m)")
        ax.set_ylim(-1.2 * AMPLITUDE, 1.2 * AMPLITUDE)
        ax.grid(True, color="#cccccc", linewidth=0.5)
        ax.set_facecolor("#FAFAFA")

        (self._line,) = ax.plot([], [], color="#1f77b4", linewidth=1.5)
        ax.set_xlim(0, 0.1 * PERIOD)

    def append(self, t: float, x: float) -> None:
        self._t_buf.append(t)
        self._x_buf.append(x)

    def refresh(self) -> None:
        if not self._t_buf:
            self._line.set_data([], [])
            return

        t_arr = np.array(self._t_buf)
        x_arr = np.array(self._x_buf)

        self._line.set_data(t_arr, x_arr)
        self._ax.set_xlim(0, t_arr[-1] + 0.1 * PERIOD)

    def clear(self) -> None:
        self._t_buf.clear()
        self._x_buf.clear()
