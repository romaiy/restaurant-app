from database.db_manager import DBManager

class Employee:
  def __init__(self, db_manager: DBManager):
    """
    Инициализация класса Employee.
    :param db_manager: Экземпляр DBManager для взаимодействия с базой данных.
    """
    self.db_manager = db_manager

  def add_employee(self, name):
    """Добавляет нового сотрудника в таблицу."""
    query = '''
    INSERT INTO employees (name) VALUES (?)
    '''
    self.db_manager.execute_query(query, (name,))
    return self.db_manager.cursor.lastrowid

  def update_employee(self, emp_id, name):
    """Обновляет информацию о сотруднике по ID."""
    query = '''
    UPDATE employees
    SET name = ?
    WHERE id = ?
    '''
    self.db_manager.execute_query(query, (name, emp_id))

  def delete_employee(self, emp_id):
    """Удаляет сотрудника из таблицы по ID."""
    query = '''
    DELETE FROM employees
    WHERE id = ?
    '''
    self.db_manager.execute_query(query, (emp_id,))

  def get_employee(self, emp_id):
    """Получает информацию о сотруднике по ID."""
    query = '''
    SELECT * FROM employees
    WHERE id = ?
    '''
    return self.db_manager.execute_query(query, (emp_id,), fetchone=True)

  def get_all_employees(self):
    """Получает список всех сотрудников."""
    query = 'SELECT * FROM employees'
    return self.db_manager.execute_query(query, fetchall=True)
