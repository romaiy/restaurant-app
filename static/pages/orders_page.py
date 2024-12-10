from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class OrdersPage(QWidget):
    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.models = models
        self.setup_ui()

    def setup_ui(self):
        """Создает интерфейс страницы."""
        layout = QVBoxLayout(self)

        layout.setContentsMargins(24, 40, 24, 40)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignTop)

        label = QLabel("Заказы", self)
        label.setStyleSheet("font-size: 32px; font-weight: bold; color: #000000")

        layout.addWidget(label)
        self.setLayout(layout)
