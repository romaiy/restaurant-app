from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal


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

        layout.setContentsMargins(32, 20, 32, 20)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignLeft)
        layout.setObjectName("root")

        # Создаем кнопки навигации
        self.tables_button = QPushButton("Столики", self)
        self.orders_button = QPushButton("Заказы", self)
        self.dishes_button = QPushButton("Блюда", self)

        self.tables_button.setFixedSize(107, 51)
        self.orders_button.setFixedSize(97, 51)
        self.dishes_button.setFixedSize(93, 51)

        self.set_default_styles()

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

    def set_default_styles(self):
        """Устанавливает стиль по умолчанию для всех кнопок."""
        self.setStyleSheet("""
            QPushButton {
                background-color: none;
                color: #2E2E2E;
                border-radius: 20px;
                padding: 16px;
                font-size: 14px;
            }  
        """)

    def set_active_button(self, active_button):
        """Устанавливает стиль для активной кнопки."""
        for button in [self.tables_button, self.orders_button, self.dishes_button]:
            if button == active_button:
                button.setStyleSheet("background-color: rgba(228, 241, 255, 1); color: #007AFF")
            else:
                button.setStyleSheet("background-color: none; color: #2E2E2E")
