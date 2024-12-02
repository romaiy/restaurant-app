from database.db_manager import DBManager

class Order:
  def __init__(self, db_manager: DBManager):
    """
    Инициализация класса Order.
    :param db_manager: Экземпляр DBManager для взаимодействия с базой данных.
    """
    self.db_manager = db_manager

  def add_order(self, table_id, employee_id, status, created_at):
    """
    Создаёт новый заказ.
    :param table_id: ID стола.
    :param employee_id: ID сотрудника.
    :param status: Статус заказа (например, 'новый', 'готовится', 'завершён').
    :param created_at: Дата и время создания заказа.
    :return: ID созданного заказа.
    """
    query = '''
    INSERT INTO orders (table_id, employee_id, status, created_at)
    VALUES (?, ?, ?, ?)
    '''
    self.db_manager.execute_query(query, (table_id, employee_id, status, created_at))
    return self.db_manager.cursor.lastrowid

  def update_order_status(self, order_id, status):
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

  def delete_order(self, order_id):
    """
    Удаляет заказ по его ID.
    :param order_id: ID заказа.
    """
    query = '''
    DELETE FROM orders
    WHERE id = ?
    '''
    self.db_manager.execute_query(query, (order_id,))

  def get_order(self, order_id):
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

  def get_all_orders(self):
    """
    Получает список всех заказов.
    :return: Список словарей с информацией о заказах.
    """
    query = 'SELECT * FROM orders'
    return self.db_manager.execute_query(query, fetchall=True)