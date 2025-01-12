from database.models.base_model import BaseModel
from collections import namedtuple

Table = namedtuple('Table', ['id', 'table_number', 'status', 'items', 'order_id', 'employee_name'])
Free_Table = namedtuple('Free_Table', ['id', 'table_number'])

class Tables(BaseModel):

  def add(self, table_number):
    """Добавляет новый стол в таблицу."""
    query = '''
    INSERT INTO tables (table_number) VALUES (?)
    '''
    self.db_manager.execute_query(query, (table_number,))
    return self.db_manager.cursor.lastrowid

  def update(self, table_id, **table_number):
    """Обновляет номер стола по ID."""
    query = '''
    UPDATE tables
    SET table_number = ?
    WHERE id = ?
    '''
    self.db_manager.execute_query(query, (table_number, table_id))

  def delete(self, table_id):
    """Удаляет стол из таблицы по ID."""
    query = '''
    DELETE FROM tables
    WHERE id = ?
    '''
    self.db_manager.execute_query(query, (table_id,))

  def get(self, table_id):
    """Получает информацию о столе по ID."""
    query = '''
    SELECT * FROM tables
    WHERE id = ?
    '''
    return self.db_manager.execute_query(query, (table_id,), fetchone=True)

  def get_list(self):
    """Получает список всех столов."""
    query = """
      SELECT
        t.id,
        t.table_number,
        o.status,
        GROUP_CONCAT(d.name, ', ') AS items,
        o.id AS order_id,
        e.name AS employee_name
      FROM tables t
        LEFT JOIN orders o ON t.id = o.table_id
        LEFT JOIN order_items oi ON o.id = oi.order_id
        LEFT JOIN dishes d ON oi.dish_id = d.id
        LEFT JOIN employees e ON o.employee_id = e.id
      GROUP BY 
        t.id
    """

    rows = self.db_manager.execute_query(query, fetchall=True)
    return [Table(*row) for row in rows]

  def get_free_tables(self):
    """
    Возвращает список столов, на которых нет заказов.
    """
    query = """
      SELECT t.id, t.table_number
      FROM tables t
      LEFT JOIN orders o ON t.id = o.table_id
      WHERE o.id IS NULL
    """
    rows = self.db_manager.execute_query(query, fetchall=True)
    return [Free_Table(*row) for row in rows]
