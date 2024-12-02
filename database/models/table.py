from database.db_manager import DBManager

class Table:
  def __init__(self, db_manager: DBManager):
    """
    Инициализация класса Table.
    :param db_manager: Экземпляр DBManager для взаимодействия с базой данных.
    """
    self.db_manager = db_manager

  def add_table(self, table_number):
    """Добавляет новый стол в таблицу."""
    query = '''
    INSERT INTO tables (table_number) VALUES (?)
    '''
    self.db_manager.execute_query(query, (table_number,))
    return self.db_manager.cursor.lastrowid

  def update_table(self, table_id, table_number):
    """Обновляет номер стола по ID."""
    query = '''
    UPDATE tables
    SET table_number = ?
    WHERE id = ?
    '''
    self.db_manager.execute_query(query, (table_number, table_id))

  def delete_table(self, table_id):
    """Удаляет стол из таблицы по ID."""
    query = '''
    DELETE FROM tables
    WHERE id = ?
    '''
    self.db_manager.execute_query(query, (table_id,))

  def get_table(self, table_id):
    """Получает информацию о столе по ID."""
    query = '''
    SELECT * FROM tables
    WHERE id = ?
    '''
    return self.db_manager.execute_query(query, (table_id,), fetchone=True)

  def get_all_tables(self):
    """Получает список всех столов."""
    query = 'SELECT * FROM tables'
    return self.db_manager.execute_query(query, fetchall=True)
