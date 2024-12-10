from .dish import Dishes
from .table import Table
from .employee import Employee
from .order import Order
from .order_item import OrderItem

# Собираем все модели в один объект (словарь или класс)
class Models:
    def __init__(self, db_manager):
        self.dishes = Dishes(db_manager)
        self.tables = Table(db_manager)
        self.employees = Employee(db_manager)
        self.orders = Order(db_manager)
        self.order_items = OrderItem(db_manager)

__all__ = ["Models"]
