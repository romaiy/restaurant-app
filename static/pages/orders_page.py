from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor


class OrdersPage(QWidget):
    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.models = models

        self.add_button = None
        self.clear_button = None

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
        layout.addWidget(self.create_buttons())
        layout.addWidget(self.create_order_cards())

        self.setLayout(layout)

    def create_buttons(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setAlignment(Qt.AlignLeft)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.add_button = QPushButton("Добавить", self)
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_button.setStyleSheet("""
            background-color: #007AFF;
            color: #FFFFFF;
            font-size: 16px;
            border-radius: 8px
        """)
        self.add_button.setFixedSize(139, 54)

        self.clear_button = QPushButton("Очистить историю", self)
        self.clear_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.clear_button.setStyleSheet("""
            background-color: rgba(243, 36, 0, 0.15);
            color:  #FF3B30;
            font-size: 16px;
            border-radius: 8px
        """)
        self.clear_button.setFixedSize(211, 54)

        main_layout.addWidget(self.add_button)
        main_layout.addWidget(self.clear_button)

        container_widget = QWidget()
        container_widget.setLayout(main_layout)

        return container_widget

    def create_order_cards(self):
        orders = self.models.orders.get_list()

        if len(orders) == 0:
            label = QLabel("Пока нет заказов", self)
            label.setStyleSheet("""
                color: #000000;
                font-size: 16px
            """)

            return label


        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(0, 0, 0, 0)

        container_widget = QWidget()
        container_widget.setLayout(main_layout)

        return container_widget