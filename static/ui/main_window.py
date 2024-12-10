from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QStackedWidget, QWidget
from static.ui.header import Header
from static.pages.tables_page import TablesPage
from static.pages.orders_page import OrdersPage
from static.pages.dishes_page import DishesPage

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
        self.setup_pages()

        # Подключаем сигналы навигации из Header
        self.header.buttonClicked.connect(self.switch_page)

        # Устанавливаем начальную страницу
        self.switch_page("Столики")

    def setup_pages(self):
        """Создаем страницы."""
        self.stackedWidget.addWidget(TablesPage(self.models, self))  # Страница "Столики"
        self.stackedWidget.addWidget(OrdersPage(self.models, self))  # Страница "Заказы"
        self.stackedWidget.addWidget(DishesPage(self.models, self))  # Страница "Блюда"

    def switch_page(self, page_name):
        """Переключает активную страницу в QStackedWidget."""
        page_map = {
            "Столики": 0,
            "Заказы": 1,
            "Блюда": 2
        }
        page_index = page_map.get(page_name, 0)
        self.stackedWidget.setCurrentIndex(page_index)

        if page_name == "Столики":
            self.header.set_active_button(self.header.tables_button)
        elif page_name == "Заказы":
            self.header.set_active_button(self.header.orders_button)
        elif page_name == "Блюда":
            self.header.set_active_button(self.header.dishes_button)