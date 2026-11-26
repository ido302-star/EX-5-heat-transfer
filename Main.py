import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QSlider, QDoubleSpinBox, QPushButton,
    QFrame, QHBoxLayout, QVBoxLayout, QGridLayout, QAbstractSpinBox,
)

MAX_TEMP = 1000  # highest temperature allowed in the UI (°C)


class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        # other windows and variables here
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Heat Transfer")

        # ---------- Top area: sliders, bodies and the connecting bar ----------
        self.slider1 = self.make_temp_slider(200)
        self.body1_rect = self.make_body_rect("red")

        self.conductivity_label = QLabel("Conductivity")
        self.conductivity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.conductivity_spin = QDoubleSpinBox()
        self.conductivity_spin.setRange(0.01, 100.0)
        self.conductivity_spin.setValue(1.00)
        self.conductivity_spin.setSuffix(" J/s°C")

        # Gray bar that connects the two bodies
        self.bar = QFrame()
        self.bar.setFixedHeight(20)
        self.bar.setStyleSheet("background-color: gray;")

        middle_top = QVBoxLayout()
        middle_top.addStretch()
        middle_top.addWidget(self.conductivity_label)
        middle_top.addWidget(self.conductivity_spin)
        middle_top.addWidget(self.bar)
        middle_top.addStretch()

        self.body2_rect = self.make_body_rect("black")
        self.slider2 = self.make_temp_slider(0)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(0)  # no gap, so the bar touches both bodies
        top_layout.addWidget(self.slider1)
        top_layout.addSpacing(10)
        top_layout.addWidget(self.body1_rect)
        top_layout.addLayout(middle_top)
        top_layout.addWidget(self.body2_rect)
        top_layout.addSpacing(10)
        top_layout.addWidget(self.slider2)

        # ---------- Bottom area: three columns ----------
        # Body 1 (labels on the left)
        self.temp1_spin = self.make_temp_display(200.0)
        self.mass1_spin = self.make_mass_spin()
        self.hcap1_spin = self.make_hcap_spin()
        left_grid = QGridLayout()
        self.add_fields(left_grid, [self.temp1_spin, self.mass1_spin, self.hcap1_spin],
                        labels_on_left=True)

        # Middle buttons
        self.start_button = QPushButton("Start")
        self.start_button.setCheckable(True)  # toggle: Start / Stop
        self.graphs_button = QPushButton("Graphs")
        self.about_button = QPushButton("About")
        middle_bottom = QVBoxLayout()
        middle_bottom.addWidget(self.start_button)
        middle_bottom.addWidget(self.graphs_button)
        middle_bottom.addWidget(self.about_button)

        # Body 2 (labels on the right)
        self.temp2_spin = self.make_temp_display(0.0)
        self.mass2_spin = self.make_mass_spin()
        self.hcap2_spin = self.make_hcap_spin()
        right_grid = QGridLayout()
        self.add_fields(right_grid, [self.temp2_spin, self.mass2_spin, self.hcap2_spin],
                        labels_on_left=False)

        bottom_layout = QHBoxLayout()
        bottom_layout.addLayout(left_grid)
        bottom_layout.addStretch()
        bottom_layout.addLayout(middle_bottom)
        bottom_layout.addStretch()
        bottom_layout.addLayout(right_grid)

        # ---------- Main layout ----------
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

    # ---------- Helper methods that build widgets ----------
    def make_temp_slider(self, value):
        slider = QSlider(Qt.Orientation.Vertical)
        slider.setRange(0, MAX_TEMP)
        slider.setValue(value)
        return slider

    def make_body_rect(self, color):
        rect = QFrame()
        rect.setFixedSize(80, 150)
        rect.setStyleSheet(f"background-color: {color};")
        return rect

    def make_temp_display(self, value):
        # Read-only: the temperature will be changed only through the slider
        spin = QDoubleSpinBox()
        spin.setRange(0.0, MAX_TEMP)
        spin.setDecimals(1)
        spin.setValue(value)
        spin.setSuffix(" °C")
        spin.setReadOnly(True)
        spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        return spin

    def make_mass_spin(self):
        spin = QDoubleSpinBox()
        spin.setRange(0.01, 1000.0)  # mass must be > 0
        spin.setValue(10.00)
        spin.setSuffix(" kg")
        return spin

    def make_hcap_spin(self):
        spin = QDoubleSpinBox()
        spin.setRange(0.01, 10000.0)  # heat capacity must be > 0
        spin.setValue(0.40)
        spin.setSuffix(" J/kg°C")
        return spin

    def add_fields(self, grid, fields, labels_on_left):
        # Put each field in a row with its label on the chosen side
        names = ["Temp.", "Mass", "H. Cap."]
        label_col, field_col = (0, 1) if labels_on_left else (1, 0)
        for row in range(len(fields)):
            grid.addWidget(QLabel(names[row]), row, label_col)
            grid.addWidget(fields[row], row, field_col)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeatTransfer()
    window.show()
    sys.exit(app.exec())
