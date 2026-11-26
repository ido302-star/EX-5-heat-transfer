from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QWidget, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout,
)


class GraphWindow(QWidget):
    """A separate window that shows temperature graphs."""

    def __init__(self, time_history, body1_temp_history, body2_temp_history):
        super().__init__()
        # References to the main window's history lists (the same list objects)
        self.time_history = time_history
        self.body1_temp_history = body1_temp_history
        self.body2_temp_history = body2_temp_history
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Graph Window")

        # ---------- Left side: an empty matplotlib plot ----------
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot()
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.figure.tight_layout()

        # ---------- Right side: body selection and buttons ----------
        self.body_combo = QComboBox()
        self.body_combo.addItems(["Body 1", "Body 2"])
        self.draw_button = QPushButton("Draw")
        self.clear_button = QPushButton("Clear")
        self.export_button = QPushButton("Export to CSV")

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.body_combo)
        right_layout.addWidget(self.draw_button)
        right_layout.addWidget(self.clear_button)
        right_layout.addWidget(self.export_button)
        right_layout.addStretch()  # push the controls to the top

        # ---------- Main layout ----------
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.canvas)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)
