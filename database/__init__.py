from .db_manager import DBManager

# Экземпляр глобального менеджера базы данных
db_manager = DBManager()

# Создаем таблицы при первом импорте модуля
db_manager.create_tables()