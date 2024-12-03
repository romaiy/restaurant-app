from database.models.base_model import BaseModel

class Table(BaseModel):

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
    query = 'SELECT * FROM tables'
    return self.db_manager.execute_query(query, fetchall=True)
