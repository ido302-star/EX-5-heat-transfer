import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

# The project's GitHub page
GITHUB_URL = "https://github.com/ido302-star/EX-5-heat-transfer"

# The image path is built from this file's folder, so it works from any working directory
IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "my_image.png")

HELP_TEXT = """
<p>This app simulates heat flowing between two bodies that are connected by a bar.</p>
<ul>
  <li><b>Sliders</b> &ndash; set the starting temperature of each body.</li>
  <li><b>Mass</b> and <b>H. Cap.</b> &ndash; set the mass and heat capacity of each body.</li>
  <li><b>Conductivity</b> &ndash; sets how fast heat moves through the bar.</li>
  <li><b>Start / Stop</b> &ndash; runs or pauses the simulation.</li>
  <li><b>Graphs</b> &ndash; opens the graph window to see the temperatures over time.</li>
</ul>
"""


class AboutWindow(QWidget):
    """A window that explains how to use the app."""

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("About")
        self.setFixedWidth(420)

        # Title
        self.title_label = QLabel("Heat Transfer")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("about_title")  # styled in style.qss

        # Image (scaled down to fit the window)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(IMAGE_PATH)
        if pixmap.isNull():
            self.image_label.setText("(image not found)")
        else:
            self.image_label.setPixmap(pixmap.scaledToWidth(360, Qt.TransformationMode.SmoothTransformation))

        # How-to-use text
        self.help_label = QLabel(HELP_TEXT)
        self.help_label.setWordWrap(True)
        self.help_label.setObjectName("about_text")

        # Clickable link that opens in the web browser
        self.link_label = QLabel(f'The project is on GitHub at:<br><a href="{GITHUB_URL}">{GITHUB_URL}</a>')
        self.link_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setObjectName("about_link")

        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(self.close_button)

        # Main layout with margins and spacing
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        layout.addWidget(self.title_label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.help_label)
        layout.addWidget(self.link_label)
        layout.addLayout(button_row)
        self.setLayout(layout)
