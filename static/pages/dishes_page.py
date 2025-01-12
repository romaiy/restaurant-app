from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QCursor, QIcon


class DishesPage(QWidget):
    addButtonClicked = pyqtSignal(str)  # Сигнал для передачи имени страницы

    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.models = models

        self.add_button = None

        self.parent = parent

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

        self.add_button.clicked.connect(lambda:
            [self.parent.pages['add_dish'].set_edit_data(None, {
            "name": '',
            "price": 0,
            "gram": 0,
            "description": '',
            }), self.addButtonClicked.emit("Добавление блюда")]
        )

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
        main_layout.setAlignment(Qt.AlignTop)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("border: none;")

        for idx, dish in enumerate(dishes):
            card = QFrame()
            card.setFixedHeight(180)
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

            btn_row = QHBoxLayout()
            btn_row.setSpacing(10)
            btn_row.setContentsMargins(0, 0, 0, 0)

            edit_button = QPushButton()
            edit_button.setCursor(QCursor(Qt.PointingHandCursor))
            edit_button.setStyleSheet("""
                padding: 0;
                margin: 0;
                background-color: #EFEFEF;
                border-radius: 6px
            """)
            edit_button.setFixedSize(32, 32)
            edit_icon = QIcon("static/assets/edit.svg")
            edit_button.setIcon(edit_icon)
            edit_button.setIconSize(QSize(24, 24))

            edit_button.clicked.connect(lambda _, dish_id=dish.id, dish_name=dish.name, dish_price=dish.price,
                dish_gram=dish.gram, dish_desc=dish.description:
                self.edit_dish(dish_id, {'name': dish_name, 'price': dish_price, 'gram': dish_gram, 'description': dish_desc}))

            delete_button = QPushButton()
            delete_button.setCursor(QCursor(Qt.PointingHandCursor))
            delete_button.setStyleSheet("""
                padding: 0;
                margin: 0;
                background-color: #FEE4E0;
                border-radius: 6px
            """)
            delete_button.setFixedSize(32, 32)
            delete_icon= QIcon("static/assets/delete.svg")
            delete_button.setIcon(delete_icon)
            delete_button.setIconSize(QSize(24, 24))

            delete_button.clicked.connect(lambda _, dish_id=dish.id: self.delete_dish(dish_id))

            btn_row.addWidget(edit_button)
            btn_row.addWidget(delete_button)

            btn_widget = QWidget()
            btn_widget.setStyleSheet("padding: 0; margin: 0")
            btn_widget.setFixedSize(74, 32)
            btn_widget.setLayout(btn_row)

            main_column.addWidget(name, alignment=Qt.AlignLeft)
            main_column.addWidget(row_widget, alignment=Qt.AlignLeft)
            main_column.addWidget(btn_widget, alignment=Qt.AlignLeft)

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
        scroll.setWidget(container_widget)

        return scroll

    def delete_dish(self, dish_id):
        self.models.dishes.delete(dish_id)
        self.setup_ui()

    def edit_dish(self, dish_id, fields):
        self.parent.pages['add_dish'].set_edit_data(dish_id, fields)
        self.parent.pages["add_dish"].setup_ui()
        self.addButtonClicked.emit("Добавление блюда")