from database.models.base_model import BaseModel
from collections import namedtuple

Order = namedtuple('Order', ['id', 'table_id', 'employee_id','status', 'created_at', 'items', 'item_ids'])

class Orders(BaseModel):

  def add(self, dish_ids, employee_id, table_id, status):
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
          VALUES (?, ?, ?, datetime('now'))
      """
      self.db_manager.execute_query(order_query, (table_id, table_id, status))

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

  def update(self, order_id, status=None, table_id=None, dish_ids=None):
    """
    Обновляет данные заказа, включая статус, table_id и блюда.
    :param order_id: ID заказа.
    :param status: Новый статус (опционально).
    :param table_id: Новый ID столика (опционально).
    :param dish_ids: Новый список идентификаторов блюд (опционально).
    """
    try:
        # Обновление статуса или table_id, если переданы
        if status or table_id is not None:
            query = "UPDATE orders SET "
            updates = []
            values = []

            if status:
                updates.append("status = ?")
                values.append(status)

            if table_id is not None:
                updates.append("table_id = ?")
                values.append(table_id)

            query += ", ".join(updates) + " WHERE id = ?"
            values.append(order_id)
            self.db_manager.execute_query(query, tuple(values))

        # Обновление order_items, если переданы новые dish_ids
        if dish_ids is not None:
            # Удаляем старые записи для данного заказа
            delete_items_query = "DELETE FROM order_items WHERE order_id = ?"
            self.db_manager.execute_query(delete_items_query, (order_id,))

            # Добавляем новые записи в order_items
            add_items_query = """
                INSERT INTO order_items (order_id, dish_id, quantity)
                VALUES (?, ?, 1)
            """
            items_data = [(order_id, dish_id) for dish_id in dish_ids]
            self.db_manager.execute_query_many(add_items_query, items_data)

        print(f"Заказ {order_id} успешно обновлен.")
    except Exception as e:
        print(f"Ошибка при обновлении заказа {order_id}: {e}")


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

  def delete_all_orders(self):
    """
    Удаляет все заказы и связанные с ними записи в таблице order_items.
    """
    try:
      # Удаляем все записи из таблицы order_items
      delete_order_items_query = "DELETE FROM order_items"
      self.db_manager.execute_query(delete_order_items_query)

      # Удаляем все записи из таблицы orders
      delete_orders_query = "DELETE FROM orders"
      self.db_manager.execute_query(delete_orders_query)

      print("Все заказы и связанные записи успешно удалены.")
    except Exception as e:
      print(f"Ошибка при удалении всех заказов: {e}")

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
    :return: Список объектов Order с добавленным полем items.
    """
    query = """
            SELECT 
                o.id,
                o.table_id,
                o.employee_id,
                o.status,
                o.created_at,
                GROUP_CONCAT(d.name, ', ') AS items,
                GROUP_CONCAT(d.id, ',') AS item_ids
            FROM 
                orders o
            LEFT JOIN 
                order_items oi 
            ON 
                o.id = oi.order_id
            LEFT JOIN 
                dishes d 
            ON 
                oi.dish_id = d.id
            GROUP BY 
                o.id
        """
    rows = self.db_manager.execute_query(query, fetchall=True)
    return [Order(*row) for row in rows]




