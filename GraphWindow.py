import csv
import os

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QWidget, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox,
    QFileDialog,
)

# Line color for each body
BODY_COLORS = {"Body 1": "red", "Body 2": "blue"}


class GraphWindow(QWidget):
    """A separate window that shows temperature graphs."""

    def __init__(self, time_history, body1_temp_history, body2_temp_history):
        super().__init__()
        # References to the main window's history lists (the same list objects)
        self.time_history = time_history
        self.body1_temp_history = body1_temp_history
        self.body2_temp_history = body2_temp_history
        self.lines = {}  # the lines already drawn, e.g. {"Body 1": line}
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Graph Window")

        # ---------- Left side: the matplotlib plot ----------
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot()
        self.setup_axes()

        # ---------- Right side: body selection and buttons ----------
        self.body_combo = QComboBox()
        self.body_combo.addItems(["Body 1", "Body 2"])
        self.draw_button = QPushButton("Draw")
        self.draw_button.clicked.connect(self.draw_graph)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_graph)
        self.export_button = QPushButton("Export to CSV")
        self.export_button.clicked.connect(self.export_csv)

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

    def setup_axes(self):
        # Title, axis labels and grid (used at the start and after Clear)
        self.ax.set_title("Temperature vs. Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True, alpha=0.3)
        self.figure.tight_layout()

    def draw_graph(self):
        # No simulation was run yet: nothing to draw
        if len(self.time_history) == 0:
            QMessageBox.information(self, "No data", "Please run the simulation first.")
            return

        body = self.body_combo.currentText()
        if body == "Body 1":
            temperatures = self.body1_temp_history
        else:
            temperatures = self.body2_temp_history

        # Copy the lists, so the line keeps this data even if the simulation goes on
        times = list(self.time_history)
        temperatures = list(temperatures)

        if body in self.lines:
            # Already drawn: update it with the latest data (no duplicate line)
            self.lines[body].set_data(times, temperatures)
        else:
            # New line on top of what is already drawn
            line, = self.ax.plot(times, temperatures, color=BODY_COLORS[body], label=body)
            self.lines[body] = line

        self.ax.relim()            # fit the axes to the data
        self.ax.autoscale_view()
        self.ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()

    def export_csv(self):
        # No simulation was run yet: nothing to save
        if len(self.time_history) == 0:
            QMessageBox.information(self, "No data", "Please run the simulation first.")
            return

        # Let the user choose where to save the file
        path, _ = QFileDialog.getSaveFileName(
            self, "Export to CSV", "heat_transfer_results.csv", "CSV files (*.csv)")
        if path == "":
            return  # the user pressed Cancel

        # Write a header row and one row per time step.
        # "utf-8-sig" lets Excel show the ° sign correctly.
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(["Time (s)", "Body 1 Temperature (°C)", "Body 2 Temperature (°C)"])
                for time, temperature1, temperature2 in zip(self.time_history,
                                                            self.body1_temp_history,
                                                            self.body2_temp_history):
                    writer.writerow([round(time, 2), temperature1, temperature2])
        except OSError as error:
            # For example: the file is open in Excel and locked
            QMessageBox.warning(self, "Export failed",
                                f"Could not save the file:\n{path}\n\n"
                                f"If it is open in Excel, close it and try again.\n\n({error})")
            return

        # Open the saved file (in Excel on Windows)
        os.startfile(path)

    def clear_graph(self):
        # Remove all lines, then put back the title, labels and grid
        self.ax.clear()
        self.lines.clear()
        self.setup_axes()
        self.canvas.draw()
