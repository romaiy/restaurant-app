from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt

from utils.types import ORDER_STATUS

text_by_status = {
    ORDER_STATUS["CREATED"]: 'Создан',
    ORDER_STATUS["WAITING"]: 'Ждут заказ',
    ORDER_STATUS["READY"]:'Готов'
}

style_by_status = {
    ORDER_STATUS["CREATED"]: {'color': 'rgba(255, 149, 0, 1)', 'background': 'rgba(255, 149, 0, 0.25)', 'width': '50px'},
    ORDER_STATUS["WAITING"]: {'color': 'rgba(255, 59, 48, 1)', 'background': 'rgba(255, 59, 48, 0.25)', 'width': '75px'},
    ORDER_STATUS["READY"]: {'color': 'rgba(52, 199, 89, 1)', 'background': 'rgba(52, 199, 89, 0.25)', 'width': '40px'}
}

class TablesPage(QWidget):
    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.models = models

        self.setup_ui()

    def setup_ui(self):
        """Создает интерфейс страницы."""
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

        layout = QVBoxLayout(self)

        layout.setContentsMargins(24, 40, 24, 40)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignTop)

        label = QLabel("Столики", self)
        label.setStyleSheet("font-size: 32px; font-weight: bold; color: #000000")

        layout.addWidget(label)
        layout.addWidget(self.create_table_cards())
        self.setLayout(layout)

    def create_table_cards(self):
        """Функция для создания лейаута с карточками, содержащими номера столов."""
        tables = self.models.tables.get_list()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(0, 0, 0, 0)

        row_layout = QHBoxLayout()
        row_layout.setAlignment(Qt.AlignLeft)
        row_layout.setSpacing(16)
        row_layout.setContentsMargins(0, 0, 0, 0)

        for idx, table in enumerate(tables):
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setFrameShadow(QFrame.Raised)
            card.setStyleSheet("background-color: #FFFFFF; padding: 14px; margin: 0px; border-radius: 12px;")

            card.setFixedSize(450, 172)

            card_layout = QVBoxLayout()
            card_layout.setAlignment(Qt.AlignLeft)
            card_layout.setSpacing(12)

            table_status = QLabel(text_by_status[table.status] if table.status else "Пустой")
            table_status.setAlignment(Qt.AlignTop)
            table_status.setStyleSheet(f"""
                font-size: 12px; 
                font-weight: semi-bold; 
                color: {style_by_status[table.status]['color'] if table.status else '#000000'}; 
                padding: 4px 8px; 
                margin: 0; 
                background-color: {style_by_status[table.status]['background'] if table.status else 'rgba(118, 118, 128, 0.12)'};
                border-radius: 10px;
                max-height: 24px;
                max-width: {style_by_status[table.status]['width'] if table.status else '50px'};
            """)

            title_layout = QVBoxLayout()
            title_layout.setAlignment(Qt.AlignLeft)
            title_layout.setSpacing(2)

            title_description = QLabel(f"официант {table.employee_name}, заказ №{table.order_id}" if table.employee_name else f"официант не назначен")
            title_description.setAlignment(Qt.AlignTop)
            title_description.setStyleSheet("font-size: 14px; font-weight: regular; color: rgba(136, 136, 136, 1); padding: 0; margin: 0")

            table_number = QLabel(
                f"№ {table[1]}")
            table_number.setAlignment(Qt.AlignTop)
            table_number.setStyleSheet("font-size: 28px; font-weight: bold; color: #000000; padding: 0; margin: 0")

            title_layout.addWidget(table_number)
            title_layout.addWidget(title_description)

            table_desc = QLabel(table.items if table.items else "Заказа нет")
            table_desc.setAlignment(Qt.AlignTop)
            table_desc.setStyleSheet("font-size: 14px; font-weight: regular; color: #000000; padding: 0; margin: 0")

            card_layout.addWidget(table_status)
            card_layout.addLayout(title_layout)
            card_layout.addWidget(table_desc)

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