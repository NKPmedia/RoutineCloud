from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
import time

class TimeDisplay(QWidget):
    def __init__(self, completed_icons=None):
        super().__init__()

        if completed_icons is None:
            completed_icons = []

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Time label
        self.time_label = QLabel(self.get_current_time())
        self.time_label.setStyleSheet("font-size: 40px;"
                                      "padding: 16px;"
                                      " color: white;")
        self.layout.addWidget(self.time_label)
        self.layout.addStretch()
        # Completed task icons
        complete_icon_box = QHBoxLayout()
        for icon in completed_icons:
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 30px; color: white;")
            complete_icon_box.addWidget(icon_label)
        self.layout.addLayout(complete_icon_box)
        complete_icon_box.setAlignment(Qt.AlignLeft)


        self.layout.setStretch(0, 1)
        self.layout.setStretch(1, 1)
        self.layout.setStretch(2, 4)

        # Update every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def get_current_time(self):
        return time.strftime("%H:%M")

    def update_time(self):
        self.time_label.setText(self.get_current_time())