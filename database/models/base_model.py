from abc import ABC, abstractmethod
from database.db_manager import DBManager

class BaseModel(ABC):
    """
    Абстрактный базовый класс для всех моделей.
    Определяет интерфейс, который должны реализовать все наследники.
    """
    def __init__(self, db_manager: DBManager):
        """
        Инициализация класса.
        :param db_manager: Экземпляр DBManager для взаимодействия с базой данных.
        """
        self.db_manager = db_manager

    @abstractmethod
    def add(self, **fields):
        """
        Добавление записи.
        :param fields: Словарь с данными для записи.
        """
        pass

    @abstractmethod
    def update(self, record_id, **fields):
        """
        Обновление записи.
        :param record_id: ID записи для обновления.
        :param fields: Словарь с новыми данными.
        """
        pass

    @abstractmethod
    def delete(self, record_id):
        """
        Удаление записи.
        :param record_id: ID записи для удаления.
        """
        pass

    @abstractmethod
    def get(self, record_id):
        """
        Получение записи по ID.
        :param record_id: ID записи.
        :return: Данные записи.
        """
        pass

    @abstractmethod
    def get_list(self, **filters):
        """
        Получение списка записей с возможными фильтрами.
        :param filters: Словарь с фильтрами.
        :return: Список записей.
        """
        pass
