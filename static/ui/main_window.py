from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QStackedWidget, QWidget

from static.pages.add_order_page import AddOrderPage
from static.ui.header import Header
from static.pages.tables_page import TablesPage
from static.pages.orders_page import OrdersPage
from static.pages.dishes_page import DishesPage
from static.pages.add_dish_page import AddDishPage

class MainWindow(QMainWindow):
    def __init__(self, models, parent=None):
        super().__init__(parent)
        self.models = models

        self.setWindowTitle("Ресторанное приложение")
        self.resize(1400, 914)

        # Главный виджет и макет
        central_widget = QWidget(self)
        central_widget.setStyleSheet("background-color: #F6F6F7")
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Хедер
        self.header = Header(self)
        layout.addWidget(self.header)

        # Контент: QStackedWidget
        self.stackedWidget = QStackedWidget(self)
        layout.addWidget(self.stackedWidget)

        # Создаем страницы
        self.pages = {
            "tables": TablesPage(self.models, self),
            "orders": OrdersPage(self.models,  self),
            "dishes": DishesPage(self.models, self),
            "add_dish": AddDishPage(self.models, self),
            "add_order": AddOrderPage(self.models, self),
        }

        self.pages["dishes"].addButtonClicked.connect(self.switch_page)
        self.pages["orders"].addButtonClicked.connect(self.switch_page)

        self.setup_pages()

        # Подключаем сигналы навигации из Header
        self.header.buttonClicked.connect(self.switch_page)

        # Устанавливаем начальную страницу
        self.switch_page("Столики")

    def setup_pages(self):
        """Создаем страницы."""
        self.stackedWidget.addWidget(self.pages["tables"])  # Страница "Столики"
        self.stackedWidget.addWidget(self.pages["orders"])  # Страница "Заказы"
        self.stackedWidget.addWidget(self.pages["dishes"])  # Страница "Блюда"
        self.stackedWidget.addWidget(self.pages["add_dish"])  # Страница "Добавления блюда"
        self.stackedWidget.addWidget(self.pages["add_order"])  # Страница "Добавления заказа"

    def switch_page(self, page_name):
        """Переключает активную страницу в QStackedWidget."""
        page_map = {
            "Столики": 0,
            "Заказы": 1,
            "Блюда": 2,
            "Добавление блюда": 3,
            "Добавление заказа": 4
        }
        page_index = page_map.get(page_name, 0)
        self.stackedWidget.setCurrentIndex(page_index)

        if page_name == "Столики":
            self.header.set_active_button(self.header.tables_button)
        elif page_name == "Заказы":
            self.header.set_active_button(self.header.orders_button)
        elif page_name == "Блюда":
            self.header.set_active_button(self.header.dishes_button)
        else:
            self.header.set_active_button(None)