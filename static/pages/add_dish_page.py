from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor


class AddDishPage(QWidget):
    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.models = models

        self.parent = parent

        self.fields = {
            "name": '',
            "price": 0,
            "gram": 0,
            "description": '',
        }

        # Создаём элементы формы
        self.inputs = {
            "name": QLineEdit(self.fields["name"]),
            "price": QLineEdit(str(self.fields["price"])),
            "gram": QLineEdit(str(self.fields["gram"])),
            "description": QLineEdit(self.fields["description"]),
        }

        for field, input_field in self.inputs.items():
            input_field.textChanged.connect(lambda text, f=field: self.update_field(f, text))

        self.is_allergenic = False

        self.add_button = None

        self.setStyleSheet("""
            QLabel {
                color: #2E2E2E;
                font-size: 16px;
                margin-bottom: 8px
            }
            
            QLineEdit {
                color: #2E2E2E;
                margin-bottom: 24px;
                background-color: white;
                padding: 16px;
                border: 1px solid #E2E2E2;
                border-radius: 8px;
                font-size: 16px;
                max-width: 584px
            }
            
            QLineEdit#desc {
                height: 164px
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        """Создает интерфейс страницы."""
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(24, 40, 24, 40)
        main_layout.setSpacing(40)
        main_layout.setAlignment(Qt.AlignTop)

        label = QLabel("Новое блюдо", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 32px; font-weight: bold; color: #000000")

        main_layout.addWidget(label)
        main_layout.addWidget(self.create_form())

        self.add_button = QPushButton("Сохранить блюдо")
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_button.setStyleSheet("""
            background-color: #007AFF;
            color: #FFFFFF;
            font-size: 16px;
            border-radius: 8px
        """)
        self.add_button.setFixedSize(624, 54)

        self.add_button.clicked.connect(self.add_dish)

        main_layout.addWidget(self.add_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def add_dish(self):
        if all(input_field.text().strip() for input_field in self.inputs.values()):
            self.models.dishes.add(
                self.inputs["name"].text(),
                int(self.inputs["price"].text()),
                int(self.inputs["gram"].text()),
                self.is_allergenic,
                self.inputs["description"].text()
            )

            # Очистка всех полей ввода
            for input_field in self.inputs.values():
                input_field.setText("")

            # Сброс состояния переменных
            self.fields["name"] = ''
            self.fields["price"] = 0
            self.fields["gram"] = 0
            self.fields["description"] = ''
            self.is_allergenic = False

            self.parent.switch_page("Блюда")
            self.parent.pages["dishes"].setup_ui()
            self.parent.pages["add_order"].setup_ui()


    def update_field(self, field, text):
        """Универсальная функция для обновления поля."""
        if field in ["price", "gram"]:
            try:
                self.fields[field] = float(text)
            except ValueError:
                self.fields[field] = 0
        else:
            self.fields[field] = text

    def create_form(self):
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setSpacing(0)
        form_layout.setContentsMargins(0, 0, 0, 0)

        name_label = QLabel("Название блюда")

        row_layout = QHBoxLayout()
        row_layout.setAlignment(Qt.AlignCenter)
        row_layout.setSpacing(24)
        row_layout.setContentsMargins(0, 0, 0, 0)

        column_layout_left = QVBoxLayout()
        column_layout_left.setSpacing(0)
        column_layout_left.setContentsMargins(0, 0, 0, 0)

        column_layout_right = QVBoxLayout()
        column_layout_right.setSpacing(0)
        column_layout_right.setContentsMargins(0, 0, 0, 0)

        price_label = QLabel("Цена блюда  (в руб.)")

        column_layout_left.addWidget(price_label)
        column_layout_left.addWidget(self.inputs['price'])

        weight_label = QLabel("Граммовка блюда")

        column_layout_right.addWidget(weight_label)
        column_layout_right.addWidget(self.inputs['gram'])

        left_widget = QWidget()
        left_widget.setFixedSize(295, 104)
        left_widget.setLayout(column_layout_left)
        row_layout.addWidget(left_widget)

        right_widget = QWidget()
        right_widget.setFixedSize(295, 104)
        right_widget.setLayout(column_layout_right)
        row_layout.addWidget(right_widget)

        row_widget = QWidget()
        row_widget.setFixedSize(624, 104)
        row_widget.setLayout(row_layout)

        description_label = QLabel("Описание блюда")
        self.inputs['description'].setAlignment(Qt.AlignTop)
        self.inputs['description'].setObjectName('desc')

        form_layout.addWidget(name_label)
        form_layout.addWidget(self.inputs["name"])
        form_layout.addWidget(row_widget)
        form_layout.addWidget(description_label)
        form_layout.addWidget(self.inputs['description'])

        container_widget = QWidget()
        container_widget.setLayout(form_layout)

        return container_widget