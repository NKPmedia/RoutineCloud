from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class NextTasksDisplay(QWidget):
    def __init__(self, tasks=None):
        super().__init__()

        if tasks is None:
            tasks = ["👕 Pajamas", "📖 Story", "💡 Lights Out"]

        layout = QVBoxLayout()
        self.setLayout(layout)

        for task in tasks:
            task_label = QLabel(task)
            task_label.setStyleSheet("font-size: 24px; color: white;")
            layout.addWidget(task_label)
