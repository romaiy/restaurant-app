from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor, QIcon


class AddOrderPage(QWidget):
    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.models = models

        self.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 16px;
                margin: 0;
                padding: 0;
            }
        """)

        self.parent = parent

        self.add_button = None
        self.return_button = None

        self.added_dishes = []

        self.setup_ui()

    def return_to_orders(self):
        self.added_dishes = []
        self.parent.switch_page("Заказы")
        self.setup_ui()

    def create_order(self):
        if len(self.added_dishes):
            self.models.orders.add(self.added_dishes, 1, 1)
        else:
            print("Не выбраны блюда")

    def setup_ui(self):
        """Создает интерфейс страницы."""
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

        layout = QVBoxLayout(self)

        layout.setContentsMargins(24, 40, 24, 40)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignTop)

        order_number = len(self.models.orders.get_list())

        label = QLabel("Заказ №" + str(order_number + 1), self)
        label.setStyleSheet("font-size: 32px; font-weight: bold; color: #000000")

        layout.addWidget(label)
        layout.addWidget(self.create_buttons())
        layout.addWidget(self.create_dish_cards())

        self.setLayout(layout)

    def create_buttons(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setAlignment(Qt.AlignLeft)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.add_button = QPushButton("Сохранить заказ", self)
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_button.setStyleSheet("""
            background-color: #007AFF;
            color: #FFFFFF;
            font-size: 16px;
            border-radius: 8px
        """)
        self.add_button.setFixedSize(194, 54)

        self.add_button.clicked.connect(self.create_order)

        self.return_button = QPushButton("Вернуться без сохранения заказа", self)
        self.return_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.return_button.setStyleSheet("""
            background-color: none;
            color:  #007AFF;
            font-size: 16px;
            border-radius: 8px
        """)
        self.return_button.setFixedSize(330, 54)

        self.return_button.clicked.connect(self.return_to_orders)

        main_layout.addWidget(self.add_button)
        main_layout.addWidget(self.return_button)

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

            row_widget = QWidget()
            row_widget.setStyleSheet("padding: 0; margin: 0")
            row_widget.setFixedSize(115, 52)
            row_widget.setLayout(info_row)

            main_column.addWidget(name, alignment=Qt.AlignLeft)
            main_column.addWidget(row_widget, alignment=Qt.AlignLeft)

            # Описание
            description_layout = QVBoxLayout()
            description_layout.setAlignment(Qt.AlignLeft)
            description_layout.setSpacing(6)
            description_layout.setContentsMargins(0, 0, 0, 0)

            description_title = QLabel("Описание:")
            description_title.setStyleSheet("""
                color: #2E2E2E;
            """)

            description = QLabel(dish.description)
            description.setStyleSheet("""
                color: #2E2E2E;
                font-size: 14px;
            """)

            description_layout.addWidget(description_title, alignment=Qt.AlignLeft)
            description_layout.addWidget(description, alignment=Qt.AlignLeft)

            description_widget = QWidget()
            description_widget.setStyleSheet("padding: 0; margin: 0")
            description_widget.setFixedSize(132, 52)
            description_widget.setLayout(description_layout)

            plus_btn = QPushButton()
            plus_btn.setCursor(QCursor(Qt.PointingHandCursor))
            plus_btn.setStyleSheet("""
                padding: 0;
                margin: 0;
                background-color: #EFEFEF;
                border-radius: 6px
            """)
            plus_btn.setFixedSize(32, 32)
            plus_icon= QIcon("static/assets/plus.svg")
            plus_btn.setIcon(plus_icon)
            plus_btn.setIconSize(QSize(24, 24))

            card_layout.addLayout(main_column)
            card_layout.addWidget(description_widget, alignment=Qt.AlignTop)
            card_layout.addWidget(plus_btn, alignment=Qt.AlignTop)

            card.setLayout(card_layout)

            main_layout.addWidget(card)

        container_widget = QWidget()
        container_widget.setLayout(main_layout)

        return container_widget