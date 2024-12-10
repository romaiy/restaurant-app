from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor


class DishesPage(QWidget):
    addButtonClicked = pyqtSignal(str)  # Сигнал для передачи имени страницы

    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.models = models

        self.add_button = None

        self.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 16px;
                margin: 0;
                padding: 0;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        """Создает интерфейс страницы."""
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

        layout = QVBoxLayout(self)

        layout.setContentsMargins(24, 40, 24, 40)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignTop)

        label = QLabel("Меню", self)
        label.setStyleSheet("font-size: 32px; font-weight: bold; color: #000000")

        layout.addWidget(label)
        layout.addWidget(self.create_buttons())
        layout.addWidget(self.create_dish_cards())

        self.add_button.clicked.connect(lambda: self.addButtonClicked.emit("Добавление блюда"))

        self.setLayout(layout)

    def create_buttons(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setAlignment(Qt.AlignLeft)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.add_button = QPushButton("Добавить блюдо", self)
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_button.setStyleSheet("""
            background-color: #007AFF;
            color: #FFFFFF;
            font-size: 16px;
            border-radius: 8px
        """)
        self.add_button.setFixedSize(194, 54)

        main_layout.addWidget(self.add_button)

        container_widget = QWidget()
        container_widget.setLayout(main_layout)

        return container_widget

    def create_dish_cards(self):
        dishes = self.models.dishes.get_list()

        if len(dishes) == 0:
            label = QLabel("Нет добавленных блюд", self)
            label.setStyleSheet("""
                color: #000000;
                font-size: 16px
            """)

            return label

        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(0, 0, 0, 0)
        for idx, dish in enumerate(dishes):
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setFrameShadow(QFrame.Raised)
            card.setStyleSheet("background-color: #FFFFFF; padding: 20px; margin: 0px; border-radius: 12px;")

            card_layout = QHBoxLayout()
            card_layout.setSpacing(24)

            main_column = QVBoxLayout()
            main_column.setSpacing(10)
            main_column.setContentsMargins(0, 0, 0, 0)

            name = QLabel(dish.name)
            name.setStyleSheet("""
                color: black;
                font-weight: bold;
                font-size: 24px;
                padding: 0;
                margin: 0;
            """)

            info_row = QHBoxLayout()
            info_row.setSpacing(8)
            info_row.setContentsMargins(0, 0, 0, 0)

            price = QLabel(str(int(dish.price)) + " ₽")
            divider = QLabel("|")
            gram = QLabel(str(int(dish.gram)) + " гр")

            info_row.addWidget(price)
            info_row.addWidget(divider)
            info_row.addWidget(gram)

            main_column.addWidget(name)
            main_column.addLayout(info_row)

            card_layout.addLayout(main_column)

            card.setLayout(card_layout)

            main_layout.addWidget(card)

        container_widget = QWidget()
        container_widget.setLayout(main_layout)

        return container_widget