from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class TablesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Создает интерфейс страницы."""
        layout = QVBoxLayout(self)
        label = QLabel("Страница: Столики", self)
        label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(label)
