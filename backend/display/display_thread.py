import pyrootutils

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=["pyproject.toml", ".git"],
    pythonpath=True,
    cwd=True
)

import sys
import threading
import time
import os

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt, QTimer

from backend import routine_state
from display.current_task_display import CurrentTaskDisplay
from display.next_tasks_display import NextTasksDisplay
from display.time_widget import TimeDisplay




from colors import BACKGROUND, TEXT_LIGHT_BEIGE


def qcolor_from_tuple(rgb_tuple):
    return QColor(*rgb_tuple)

class DisplayWindow(QWidget):
    def __init__(self, screen_size=(1024, 600)):
        super().__init__()
        self.setWindowTitle("Bedtime Routine")
        self.resize(*screen_size)

        # Set background color
        pal = self.palette()
        pal.setColor(QPalette.Window, qcolor_from_tuple(BACKGROUND))
        self.setPalette(pal)
        self.setAutoFillBackground(True)

        layout = QVBoxLayout()
        layout.addWidget(TimeDisplay(["🛏️", "🦷", "🛁"]))
        layout.addWidget(CurrentTaskDisplay())
        layout.addWidget(NextTasksDisplay(["👕 Pajamas", "📖 Story", "💡 Lights Out"]))

        self.setLayout(layout)

        # Set Background Color
        self.setStyleSheet("background-color: #0A0A32;")

        self.is_fullscreen = False

    def get_current_time(self):
        return time.strftime("%H:%M")

    def update_display(self):
        # Get state as needed
        is_active = routine_state.is_routine_active
        current_task = routine_state.current_task

        if is_active and current_task:
            self.task_label.setText(f"Current Task: {current_task['name']}")
        else:
            self.task_label.setText("No Active Routine")

    def keyPressEvent(self, event):
        # Toggle fullscreen on F10
        if event.key() == Qt.Key_F10:
            if self.is_fullscreen:
                self.showNormal()
            else:
                self.showFullScreen()
            self.is_fullscreen = not self.is_fullscreen
        super().keyPressEvent(event)


class DisplayThread(threading.Thread):
    def __init__(self, screen_size=(1024, 600)):
        super().__init__(daemon=True)
        self.screen_size = screen_size
        self.running = False

    def run(self):
        self.running = True
        self.app = QApplication(sys.argv)
        self.window = DisplayWindow(screen_size=self.screen_size)
        self.window.show()
        self.app.exec()
        self.running = False

    def stop(self):
        self.running = False
        # Graceful exit if needed. This may require more handling in real deployments.

def start_display_thread(screen_size=(1024, 600)):
    thread = DisplayThread(screen_size=screen_size)
    thread.start()
    return thread

if __name__ == "__main__":
    thread = start_display_thread()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        thread.stop()