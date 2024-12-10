from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt


class TablesPage(QWidget):
    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.models = models

        self.setup_ui()

    def setup_ui(self):
        """Создает интерфейс страницы."""
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

            card.setFixedSize(450, 154)

            card_layout = QVBoxLayout()
            card_layout.setAlignment(Qt.AlignLeft)
            card_layout.setSpacing(12)

            table_status = QLabel("Пустой")
            table_status.setAlignment(Qt.AlignTop)
            table_status.setStyleSheet("""
                font-size: 12px; 
                font-weight: semi-bold; 
                color: #000000; 
                padding: 4px 8px; 
                margin: 0; 
                background-color: rgba(118, 118, 128, 0.12);
                border-radius: 10px;
                max-height: 24px;
                width: fit-content
            """)

            table_number = QLabel(
                f"№ {table[1]}")
            table_number.setAlignment(Qt.AlignTop)
            table_number.setStyleSheet("font-size: 28px; font-weight: bold; color: #000000; padding: 0; margin: 0")

            table_desc = QLabel("Заказа нет")
            table_desc.setAlignment(Qt.AlignTop)
            table_desc.setStyleSheet("font-size: 14px; font-weight: medium; color: #000000; padding: 0; margin: 0")

            card_layout.addWidget(table_status)
            card_layout.addWidget(table_number)
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