from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from harmonic_oscillator_animation import physics
from harmonic_oscillator_animation.plot_widget import PlotWidget
from harmonic_oscillator_animation.spring_renderer import SpringRenderer

FRAME_MS = 33  # ~30 fps


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Simple Harmonic Oscillator")
        self.setFixedSize(700, 800)

        # Apply light palette
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#FFFFFF"))
        self.setPalette(palette)

        # Create spring figure and canvas
        self._spring_fig = Figure(figsize=(7, 4), facecolor="#FAFAFA")
        self._spring_ax = self._spring_fig.add_subplot(111)
        self._spring_canvas = FigureCanvas(self._spring_fig)

        # Create plot figure and canvas
        self._plot_fig = Figure(figsize=(7, 4), facecolor="#FAFAFA")
        self._plot_ax = self._plot_fig.add_subplot(111)
        self._plot_canvas = FigureCanvas(self._plot_fig)

        # Instantiate renderers
        self._spring_renderer = SpringRenderer(self._spring_ax)
        self._plot_widget = PlotWidget(self._plot_ax)

        # Build layout
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._spring_canvas)
        layout.addWidget(self._plot_canvas)
        self.setCentralWidget(central)

        # Init simulation state
        self._t = 0.0

        # Start animation timer (AFTER layout is complete)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(FRAME_MS)

    def _tick(self):
        # Increment time
        self._t += FRAME_MS / 1000.0
        # Check for loop reset (after 10 periods)
        if self._t >= 10 * physics.PERIOD:
            self._t = 0.0
            self._plot_widget.clear()
        # Compute position
        x = physics.position(self._t)
        # Update spring
        self._spring_renderer.update(x)
        # Update plot
        self._plot_widget.append(self._t, x)
        self._plot_widget.refresh()
        # Redraw both canvases
        self._spring_canvas.draw_idle()
        self._plot_canvas.draw_idle()
