from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal


class Header(QWidget):
    buttonClicked = pyqtSignal(str)  # Сигнал для передачи имени страницы

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tables_button = None
        self.orders_button = None
        self.dishes_button = None
        self.setup_ui()

    def setup_ui(self):
        """Создает интерфейс хедера."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Создаем кнопки навигации
        self.tables_button = QPushButton("Столики", self)
        self.orders_button = QPushButton("Заказы", self)
        self.dishes_button = QPushButton("Блюда", self)

        # Добавляем кнопки в макет
        layout.addWidget(self.tables_button)
        layout.addWidget(self.orders_button)
        layout.addWidget(self.dishes_button)

        # Подключаем кнопки к слоту для отправки сигнала
        self.tables_button.clicked.connect(lambda: self.buttonClicked.emit("Столики"))
        self.orders_button.clicked.connect(lambda: self.buttonClicked.emit("Заказы"))
        self.dishes_button.clicked.connect(lambda: self.buttonClicked.emit("Блюда"))

        # Устанавливаем начальную активную кнопку
        self.set_active_button(self.tables_button)

    def set_active_button(self, active_button):
        """Устанавливает стиль для активной кнопки."""
        for button in [self.tables_button, self.orders_button, self.dishes_button]:
            if button == active_button:
                button.setStyleSheet("background-color: lightblue; color: blue; font-weight: bold;")
            else:
                button.setStyleSheet("background-color: none; color: black;")
