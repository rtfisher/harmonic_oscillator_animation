"""Spring renderer for the harmonic oscillator animation."""

from __future__ import annotations

import matplotlib.patches as mpatches
import numpy as np
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------
N_COILS = 12
COIL_RADIUS = 0.07
EQUILIBRIUM_Y = 0.0  # y-position of mass center at rest
MASS_HEIGHT = 0.07  # height of the mass rectangle
MASS_WIDTH = 0.12  # width of the mass rectangle
Y_CEILING = 0.32  # y of the ceiling line
LEAD_LENGTH = 0.03  # length of straight attachment segments


class SpringRenderer:
    """Draws a vertical coil spring connecting a fixed ceiling to a moving mass."""

    def __init__(self, ax: Axes) -> None:
        self._ax = ax

        # Background and limits
        ax.set_facecolor("#FAFAFA")
        ax.set_xlim(-0.3, 0.3)
        ax.set_ylim(-0.35, 0.35)
        ax.set_axis_off()

        # ------------------------------------------------------------------
        # Static ceiling bar
        # ------------------------------------------------------------------
        ceiling_line = Line2D(
            [-0.28, 0.28], [Y_CEILING, Y_CEILING], color="#333333", linewidth=2
        )
        ax.add_line(ceiling_line)

        # Hatch marks above ceiling
        n_hatches = 7
        x_positions = np.linspace(-0.24, 0.24, n_hatches)
        for x_h in x_positions:
            hatch = Line2D(
                [x_h, x_h - 0.03],
                [Y_CEILING, Y_CEILING + 0.04],
                color="#333333",
                linewidth=1,
            )
            ax.add_line(hatch)

        # ------------------------------------------------------------------
        # Initial spring geometry (at equilibrium)
        # ------------------------------------------------------------------
        y_top = Y_CEILING - LEAD_LENGTH
        mass_top_eq = EQUILIBRIUM_Y + MASS_HEIGHT / 2
        y_bottom = mass_top_eq + LEAD_LENGTH

        theta = np.linspace(0, 2 * np.pi * N_COILS, 600)
        x_coil = COIL_RADIUS * np.sin(theta)
        y_coil = np.linspace(y_top, y_bottom, len(theta))

        self._spring_line = Line2D(x_coil, y_coil, color="#555555", linewidth=1.5)
        ax.add_line(self._spring_line)

        # Top lead: ceiling attachment point → spring top
        self._top_lead = Line2D(
            [0, 0], [Y_CEILING, y_top], color="#555555", linewidth=1.5
        )
        ax.add_line(self._top_lead)

        # Bottom lead: spring bottom → mass top
        self._bottom_lead = Line2D(
            [0, 0], [y_bottom, mass_top_eq], color="#555555", linewidth=1.5
        )
        ax.add_line(self._bottom_lead)

        # ------------------------------------------------------------------
        # Mass block (FancyBboxPatch)
        # ------------------------------------------------------------------
        self._mass_patch = mpatches.FancyBboxPatch(
            xy=(-MASS_WIDTH / 2, EQUILIBRIUM_Y - MASS_HEIGHT / 2),
            width=MASS_WIDTH,
            height=MASS_HEIGHT,
            boxstyle="round,pad=0.005",
            facecolor="#4C72B0",
            edgecolor="#2c4a7c",
            linewidth=1.5,
        )
        ax.add_patch(self._mass_patch)

        # Mass label
        self._mass_label = ax.text(
            0,
            EQUILIBRIUM_Y,
            "m",
            ha="center",
            va="center",
            color="white",
            fontsize=12,
            fontweight="bold",
        )

    # ------------------------------------------------------------------
    # Animation update
    # ------------------------------------------------------------------
    def update(self, x: float) -> list:
        """Update the spring/mass geometry for displacement x from equilibrium.

        Parameters
        ----------
        x:
            Current displacement from equilibrium in data units (positive = down).

        Returns
        -------
        list
            Matplotlib artists that were modified (for blitting).
        """
        mass_y = EQUILIBRIUM_Y + x

        # Update mass patch (xy is bottom-left corner)
        self._mass_patch.set_y(mass_y - MASS_HEIGHT / 2)

        # Update mass label
        self._mass_label.set_position((0, mass_y))

        # Recompute spring coil
        y_top_fixed = Y_CEILING - LEAD_LENGTH
        spring_bottom = mass_y + MASS_HEIGHT / 2 + LEAD_LENGTH
        mass_top = mass_y + MASS_HEIGHT / 2

        y_coil_new = np.linspace(y_top_fixed, spring_bottom, 600)
        x_coil_new = COIL_RADIUS * np.sin(np.linspace(0, 2 * np.pi * N_COILS, 600))
        self._spring_line.set_data(x_coil_new, y_coil_new)

        # Update bottom lead: spring bottom → mass top
        self._bottom_lead.set_data([0, 0], [spring_bottom, mass_top])

        return [
            self._spring_line,
            self._bottom_lead,
            self._mass_patch,
            self._mass_label,
        ]
