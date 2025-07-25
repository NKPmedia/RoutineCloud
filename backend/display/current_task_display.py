from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

from entity import Task


class CurrentTaskDisplay(QWidget):
    def __init__(self, task: Task = None):
        super().__init__()
        self.main_layout = QVBoxLayout()  # Start with a single column layout
        self.setLayout(self.main_layout)
        self.update_display(task)

    def update_display(self, task: Task):
        # Clear existing layout
        self.clear_layout(self.main_layout)

        if task is None:
            # Fallback display
            fallback_label = QLabel("No current task")
            fallback_label.setStyleSheet("font-size: 32px; color: white;")
            fallback_label.setAlignment(Qt.AlignCenter)
            self.main_layout.addWidget(fallback_label)
        else:
            # Normal display with task info
            main_layout = QHBoxLayout()

            # Left column: icon and name
            left_col = QVBoxLayout()
            icon_label = QLabel(task.icon)
            icon_label.setStyleSheet("font-size: 64px; color: white;")
            left_col.addWidget(icon_label)

            name_label = QLabel(task.name)
            name_label.setStyleSheet("font-size: 32px; color: white;")
            left_col.addWidget(name_label)
            left_col.addStretch()
            main_layout.addLayout(left_col)

            # Right column: time
            right_col = QVBoxLayout()
            time_label = QLabel(task.remaining_time)
            time_label.setStyleSheet("font-size: 32px; color: white;")
            time_label.setAlignment(Qt.AlignCenter)
            right_col.addStretch()
            right_col.addWidget(time_label)
            right_col.addStretch()
            main_layout.addLayout(right_col)

            main_layout.setStretch(0, 3)
            main_layout.setStretch(1, 2)

            self.main_layout.addLayout(main_layout)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())

