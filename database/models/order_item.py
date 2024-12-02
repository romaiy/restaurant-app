from database.db_manager import DBManager

class OrderItem:
  def __init__(self, db_manager: DBManager):
    """
    Инициализация класса OrderItem.
    :param db_manager: Экземпляр DBManager для взаимодействия с базой данных.
    """
    self.db_manager = db_manager

  def add_order_item(self, order_id, dish_id, quantity):
    """
    Добавляет пункт в заказ.
    :param order_id: ID заказа.
    :param dish_id: ID блюда.
    :param quantity: Количество блюда.
    :return: ID добавленного пункта заказа.
    """
    query = '''
    INSERT INTO order_items (order_id, dish_id, quantity)
    VALUES (?, ?, ?)
    '''
    self.db_manager.execute_query(query, (order_id, dish_id, quantity))
    return self.db_manager.cursor.lastrowid

  def update_order_item(self, order_item_id, quantity):
    """
    Обновляет количество блюда в пункте заказа.
    :param order_item_id: ID пункта заказа.
    :param quantity: Новое количество блюда.
    """
    query = '''
    UPDATE order_items
    SET quantity = ?
    WHERE id = ?
    '''
    self.db_manager.execute_query(query, (quantity, order_item_id))

  def delete_order_item(self, order_item_id):
    """
    Удаляет пункт заказа по его ID.
    :param order_item_id: ID пункта заказа.
    """
    query = '''
    DELETE FROM order_items
    WHERE id = ?
    '''
    self.db_manager.execute_query(query, (order_item_id,))

  def get_order_item(self, order_item_id):
    """
    Получает информацию о пункте заказа по его ID.
    :param order_item_id: ID пункта заказа.
    :return: Словарь с информацией о пункте заказа.
    """
    query = '''
    SELECT * FROM order_items
    WHERE id = ?
    '''
    return self.db_manager.execute_query(query, (order_item_id,), fetchone=True)

  def get_items_by_order(self, order_id):
    """
    Получает все пункты заказа по ID заказа.
    :param order_id: ID заказа.
    :return: Список пунктов заказа.
    """
    query = '''
    SELECT * FROM order_items
    WHERE order_id = ?
    '''
    return self.db_manager.execute_query(query, (order_id,), fetchall=True)