from database.models.base_model import BaseModel

class Employee(BaseModel):

  def add(self, name):
    """Добавляет нового сотрудника в таблицу."""
    query = '''
    INSERT INTO employees (name) VALUES (?)
    '''
    self.db_manager.execute_query(query, (name,))
    return self.db_manager.cursor.lastrowid

  def update(self, emp_id, **name):
    """Обновляет информацию о сотруднике по ID."""
    query = '''
    UPDATE employees
    SET name = ?
    WHERE id = ?
    '''
    self.db_manager.execute_query(query, (name, emp_id))

  def delete(self, emp_id):
    """Удаляет сотрудника из таблицы по ID."""
    query = '''
    DELETE FROM employees
    WHERE id = ?
    '''
    self.db_manager.execute_query(query, (emp_id,))

  def get(self, emp_id):
    """Получает информацию о сотруднике по ID."""
    query = '''
    SELECT * FROM employees
    WHERE id = ?
    '''
    return self.db_manager.execute_query(query, (emp_id,), fetchone=True)

  def get_list(self):
    """Получает список всех сотрудников."""
    query = 'SELECT * FROM employees'
    return self.db_manager.execute_query(query, fetchall=True)
