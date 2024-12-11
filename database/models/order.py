from database.models.base_model import BaseModel

class Order(BaseModel):

  def add(self, dish_ids, employee_id, table_id):
    """
    Создает заказ и заполняет таблицу order_items.

    :param dish_ids: Список идентификаторов блюд.
    :param employee_id: Идентификатор официанта.
    :param table_id: Идентификатор столика.
    """
    try:
      # Создаем запись в таблице orders
      order_query = """
          INSERT INTO orders (employee_id, table_id, status, created_at)
          VALUES (?, ?, 'CREATE', datetime('now'))
      """
      self.db_manager.execute_query(order_query, (employee_id, table_id))

      # Получаем ID созданного заказа
      order_id_query = "SELECT last_insert_rowid()"
      order_id = self.db_manager.execute_query(order_id_query, fetchone=True)[0]

      # Создаем записи в таблице order_items
      order_items_query = """
          INSERT INTO order_items (order_id, dish_id, quantity)
          VALUES (?, ?, 1)
      """
      order_items_data = [(order_id, dish_id) for dish_id in dish_ids]
      self.db_manager.execute_query_many(order_items_query, order_items_data)

      return order_id
    except Exception as e:
      print(f"Ошибка при создании заказа: {e}")
      return None

  def update(self, order_id, **status):
    """
    Обновляет статус заказа.
    :param order_id: ID заказа.
    :param status: Новый статус.
    """
    query = '''
    UPDATE orders
    SET status = ?
    WHERE id = ?
    '''
    self.db_manager.execute_query(query, (status, order_id))

  def delete(self, order_id):
    """
    Удаляет заказ и связанные с ним записи в таблице order_items.
    :param order_id: Идентификатор заказа.
    """
    try:
      # Удаляем записи из таблицы order_items
      delete_order_items_query = "DELETE FROM order_items WHERE order_id = ?"
      self.db_manager.execute_query(delete_order_items_query, (order_id,))

      # Удаляем запись из таблицы orders
      delete_order_query = "DELETE FROM orders WHERE id = ?"
      self.db_manager.execute_query(delete_order_query, (order_id,))
    except Exception as e:
      print(f"Ошибка при удалении заказа: {e}")

  def get(self, order_id):
    """
    Получает информацию о заказе по его ID.
    :param order_id: ID заказа.
    :return: Словарь с информацией о заказе.
    """
    query = '''
    SELECT * FROM orders
    WHERE id = ?
    '''
    return self.db_manager.execute_query(query, (order_id,), fetchone=True)

  def get_list(self):
    """
    Получает список всех заказов.
    :return: Список словарей с информацией о заказах.
    """
    query = 'SELECT * FROM orders'
    return self.db_manager.execute_query(query, fetchall=True)

