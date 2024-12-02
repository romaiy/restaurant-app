from database.db_manager import DBManager

class Dishes:
  def __init__(self, db_manager: DBManager):
    """
    Инициализация класса Dishes.
    :param db_manager: Экземпляр DBManager для взаимодействия с базой данных.
    """
    self.db_manager = db_manager

  def add_dish(self, name, price, is_allergenic, description):
    """Добавляет новое блюдо в таблицу dishes."""
    query = '''
    INSERT INTO dishes (name, price, is_allergenic, description)
    VALUES (?, ?, ?, ?)
    '''
    self.db_manager.execute_query(query, (name, price, is_allergenic, description))

  def get_dish(self, dish_id):
    """Получает информацию о блюде по его id."""
    query = 'SELECT * FROM dishes WHERE id = ?'
    return self.db_manager.execute_query(query, (dish_id,), fetchone=True)

  def update_dish(self, dish_id, name=None, price=None, is_allergenic=None, description=None):
    """Обновляет информацию о блюде."""
    query = 'UPDATE dishes SET '
    fields = []
    values = []

    if name:
      fields.append('name = ?')
      values.append(name)
    if price:
      fields.append('price = ?')
      values.append(price)
    if is_allergenic is not None:
      fields.append('is_allergenic = ?')
      values.append(is_allergenic)
    if description:
      fields.append('description = ?')
      values.append(description)

    if fields:  # Проверяем, есть ли данные для обновления
      query += ', '.join(fields)
      query += ' WHERE id = ?'
      values.append(dish_id)
      self.db_manager.execute_query(query, values)

  def delete_dish(self, dish_id):
    """Удаляет блюдо по его id."""
    query = 'DELETE FROM dishes WHERE id = ?'
    self.db_manager.execute_query(query, (dish_id,))

  def list_dishes(self):
    """Возвращает список всех блюд."""
    query = 'SELECT * FROM dishes'
    return self.db_manager.execute_query(query, fetchall=True)

