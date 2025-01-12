from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QComboBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor, QIcon

from utils.types import ORDER_STATUS

status_by_text = {
    'Создан': ORDER_STATUS["CREATED"],
    'Ждут заказ': ORDER_STATUS["WAITING"],
    'Готов': ORDER_STATUS["READY"]
}

status_list = list(status_by_text.values())

text_by_status = {value: key for key, value in status_by_text.items()}

class AddOrderPage(QWidget):
    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.models = models

        self.fields = {
            "table_id": 1,
            "status": ORDER_STATUS["CREATED"],
        }

        self.free_tables = self.models.tables.get_free_tables()

        self.table_combobox = None
        self.status_combobox = None

        self.parent = parent

        self.add_button = None
        self.return_button = None

        self.added_dishes = []
        self.order_id = None
        self.edited_order_idx = None

        self.buttons = {}

        self.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 16px;
                margin: 0;
                padding: 0;
            }

            QComboBox {
                color: #2E2E2E;
                margin: 0px;
                background-color: white;
                padding-left: 16px;
                border: 1px solid #E2E2E2;
                border-radius: 8px;
                font-size: 16px;
                max-width: 584px
            }

            QComboBox::down-arrow {
                image: url(static/assets/selector.png);
            }

            QComboBox QAbstractItemView {
                border: none;
                selection-background-color: lightgray;
                background-color: white;
                padding: 16px 0;
            }


            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 24px;
                padding-right: 16px;
                border-top-right-radius: 3px; /* same radius as the QComboBox */
                border-bottom-right-radius: 3px;
            }
        """)
        self.setup_ui()

    def set_edit_data(self, order_id, edited_order_idx, fields, added_dishes):
        self.order_id = order_id
        self.edited_order_idx = edited_order_idx
        self.fields = fields if order_id else {'table_id': [str(table.table_number) for table in self.free_tables][0], "status": ORDER_STATUS["CREATED"]}
        self.added_dishes = added_dishes

    def update_field(self, f, text):
        if f == 'table_id':
            self.fields['table_id'] = int(text)
        else:
            self.fields['status'] = status_by_text[text]

    def return_to_orders(self):
        self.added_dishes = []
        self.edited_order_idx = None
        self.order_id = None
        self.parent.switch_page("Заказы")
        self.setup_ui()

    def create_order(self):
        if len(self.added_dishes):
            if self.order_id:
                self.models.orders.update(self.order_id, self.fields['status'], self.fields['table_id'], self.added_dishes)
            else:
                self.models.orders.add(self.added_dishes, 1, self.fields['table_id'], self.fields['status'])

            self.parent.pages["orders"].setup_ui()
            self.parent.pages["tables"].setup_ui()
            self.return_to_orders()
        else:
            print("Не выбраны блюда")

    def add_or_delete_dish(self, dish_id):
        if dish_id in self.added_dishes:
            self.added_dishes.remove(dish_id)
        else:
            self.added_dishes.append(dish_id)

    def setup_ui(self):
        """Создает интерфейс страницы."""
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

        if not self.order_id:
            self.free_tables = self.models.tables.get_free_tables()
            self.fields = {'table_id': [str(table.table_number) for table in self.free_tables][0],
                            "status": ORDER_STATUS["CREATED"]}

        layout = QVBoxLayout(self)

        layout.setContentsMargins(24, 40, 24, 40)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignTop)

        order_number = len(self.models.orders.get_list())

        label = QLabel("Заказ №" + str(self.edited_order_idx if self.edited_order_idx else order_number + 1), self)
        label.setStyleSheet("font-size: 32px; font-weight: bold; color: #000000")

        layout.addWidget(label)
        layout.addWidget(self.create_inputs())
        layout.addWidget(self.create_buttons())
        layout.addWidget(self.create_dish_cards())

        self.setLayout(layout)

    def create_inputs(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setAlignment(Qt.AlignLeft)
        main_layout.setContentsMargins(0, 0, 0, 0)

        table_layout = QVBoxLayout()
        table_layout.setSpacing(0)
        table_layout.setAlignment(Qt.AlignLeft)
        table_layout.setContentsMargins(0, 0, 0, 0)

        table_label = QLabel('Номер столика')
        table_label.setStyleSheet("font-size: 16px; font-weight: medium; color: #2E2E2E; margin-bottom: 8px")

        self.table_combobox = QComboBox()

        if self.order_id:
            self.table_combobox.addItem(str(self.fields['table_id']))
        self.table_combobox.addItems([str(table.table_number) for table in self.free_tables])

        self.table_combobox.setFixedSize(350, 54)
        self.table_combobox.setCurrentText(str(self.fields['table_id']))
        self.table_combobox.currentTextChanged.connect(lambda text, f='table_id': self.update_field(f, text))

        table_layout.addWidget(table_label)
        table_layout.addWidget(self.table_combobox)

        status_layout = QVBoxLayout()
        status_layout.setSpacing(0)
        status_layout.setAlignment(Qt.AlignLeft)
        status_layout.setContentsMargins(0, 0, 0, 0)

        status_label = QLabel('Статус заказа')
        status_label.setStyleSheet("font-size: 16px; font-weight: medium; color: #2E2E2E; margin-bottom: 8px")

        self.status_combobox = QComboBox()
        self.status_combobox.addItems(['Создан', 'Ждут заказ', 'Готов'])
        self.status_combobox.setFixedSize(350, 54)
        self.status_combobox.setCurrentText(text_by_status[self.fields['status']])
        self.status_combobox.currentTextChanged.connect(lambda text, f='status': self.update_field(f, text))

        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_combobox)

        main_layout.addLayout(table_layout)
        main_layout.addLayout(status_layout)

        container_widget = QWidget()
        container_widget.setLayout(main_layout)

        return container_widget

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

        for dish in dishes:
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

            plus_icon = QIcon("static/assets/plus.svg")
            minus_icon = QIcon("static/assets/minus.svg")

            plus_btn.setIcon(plus_icon)
            plus_btn.setIconSize(QSize(24, 24))

            self.buttons[dish.id] = plus_btn  # Сохранение кнопки по dish.id

            def update_button_style(dish_id):
                if dish_id in self.added_dishes:
                    self.buttons[dish_id].setStyleSheet("""
                        padding: 0;
                        margin: 0;
                        background-color: rgba(228, 241, 255, 1);
                        border-radius: 6px;
                    """)
                    self.buttons[dish_id].setIcon(minus_icon)
                else:
                    self.buttons[dish_id].setStyleSheet("""
                        padding: 0;
                        margin: 0;
                        background-color: #EFEFEF; 
                        border-radius: 6px;
                    """)
                    self.buttons[dish_id].setIcon(plus_icon)

            update_button_style(dish.id)

            plus_btn.clicked.connect(lambda checked=False, dish_id=dish.id: [
                self.add_or_delete_dish(dish_id),
                update_button_style(dish_id)
            ])

            card_layout.addLayout(main_column)
            card_layout.addWidget(description_widget, alignment=Qt.AlignTop)
            card_layout.addWidget(plus_btn, alignment=Qt.AlignTop)

            card.setLayout(card_layout)

            main_layout.addWidget(card)

        container_widget = QWidget()
        container_widget.setLayout(main_layout)

        return container_widget
