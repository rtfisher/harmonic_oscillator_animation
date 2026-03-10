#!/Users/rfisher/miniconda3/envs/harmonic_oscillator_animation/bin/python
import sys

from PyQt6.QtWidgets import QApplication

from harmonic_oscillator_animation.app import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
