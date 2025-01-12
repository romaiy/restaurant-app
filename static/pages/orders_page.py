from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QCursor, QIcon

from utils.types import ORDER_STATUS


class OrdersPage(QWidget):
    addButtonClicked = pyqtSignal(str)  # Сигнал для передачи имени страницы

    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.models = models

        self.parent = parent

        self.add_button = None
        self.clear_button = None

        self.setup_ui()

    def setup_ui(self):
        """Создает интерфейс страницы."""
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

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

    def delete_order(self, order_id):
        self.models.orders.delete(order_id)
        self.parent.pages["add_order"].setup_ui()
        self.setup_ui()

    def edit_order(self, order_id, order_idx, fields, dish_ids):
        self.parent.pages['add_order'].set_edit_data(order_id, order_idx, fields, dish_ids)
        self.parent.pages["add_order"].setup_ui()
        self.addButtonClicked.emit("Добавление заказа")

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
        self.add_button.clicked.connect(lambda: [
            self.parent.pages['add_order'].set_edit_data(None, None, { "table_id": 1, "status": ORDER_STATUS["CREATED"]}, []),
            self.parent.pages["add_order"].setup_ui(),
            self.addButtonClicked.emit("Добавление заказа")
        ])

        self.clear_button = QPushButton("Очистить историю", self)
        self.clear_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.clear_button.setStyleSheet("""
            background-color: rgba(243, 36, 0, 0.15);
            color:  #FF3B30;
            font-size: 16px;
            border-radius: 8px
        """)
        self.clear_button.setFixedSize(211, 54)
        self.clear_button.clicked.connect(lambda: [self.models.orders.delete_all_orders(), self.setup_ui(), self.parent.pages["add_order"].setup_ui()])

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

        row_layout = QHBoxLayout()
        row_layout.setAlignment(Qt.AlignLeft)
        row_layout.setSpacing(16)
        row_layout.setContentsMargins(0, 0, 0, 0)

        for idx, order in enumerate(orders):
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setFrameShadow(QFrame.Raised)
            card.setStyleSheet("background-color: #FFFFFF; padding: 14px; margin: 0px; border-radius: 12px;")

            card.setFixedSize(450, 175)

            card_layout = QVBoxLayout()
            card_layout.setAlignment(Qt.AlignLeft)
            card_layout.setSpacing(12)

            title_layout = QVBoxLayout()
            title_layout.setAlignment(Qt.AlignLeft)
            title_layout.setSpacing(2)

            order_number = QLabel(
                f"№ {idx + 1}")
            order_number.setAlignment(Qt.AlignTop)
            order_number.setStyleSheet("font-size: 28px; font-weight: bold; color: #000000; padding: 0; margin: 0")

            order_sheff = QLabel(f"Повар - Соколов Р.М., столик N{order.table_id}")
            order_sheff.setAlignment(Qt.AlignTop)
            order_sheff.setStyleSheet("font-size: 14px; font-weight: medium; color: #888888; padding: 0; margin: 0")

            title_layout.addWidget(order_number)
            title_layout.addWidget(order_sheff)

            order_desc = QLabel(order.items)
            order_desc.setAlignment(Qt.AlignTop)
            order_desc.setStyleSheet("font-size: 14px; font-weight: medium; color: #2E2E2E; padding: 0; margin: 0")

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

            edit_button.clicked.connect(lambda _, order_id=order.id, table_id=order.table_id, status=order.status, dish_ids=order.item_ids:
                self.edit_order(order_id, idx + 1, {'table_id': table_id, 'status': status}, list(map(int, dish_ids.split(',')))))

            delete_button = QPushButton()
            delete_button.setCursor(QCursor(Qt.PointingHandCursor))
            delete_button.setStyleSheet("""
                padding: 0;
                margin: 0;
                background-color: #FEE4E0;
                border-radius: 6px
            """)
            delete_button.setFixedSize(32, 32)
            delete_icon = QIcon("static/assets/delete.svg")
            delete_button.setIcon(delete_icon)
            delete_button.setIconSize(QSize(24, 24))

            delete_button.clicked.connect(lambda _, order_id=order.id: self.delete_order(order_id))

            btn_row.addWidget(edit_button)
            btn_row.addWidget(delete_button)

            btn_widget = QWidget()
            btn_widget.setStyleSheet("padding: 0; margin: 0")
            btn_widget.setFixedSize(74, 32)
            btn_widget.setLayout(btn_row)

            card_layout.addLayout(title_layout)
            card_layout.addWidget(order_desc)
            card_layout.addWidget(btn_widget)

            card.setLayout(card_layout)

            row_layout.addWidget(card)

            if (idx + 1) % 3 == 0:
                main_layout.addLayout(row_layout)
                row_layout = QHBoxLayout()
                row_layout.setSpacing(16)
                row_layout.setAlignment(Qt.AlignLeft)
                row_layout.setContentsMargins(0, 0, 0, 0)

        if row_layout.count() > 0:
            main_layout.addLayout(row_layout)

        container_widget = QWidget()
        container_widget.setLayout(main_layout)

        return container_widget