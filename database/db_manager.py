import sqlite3

class DBManager:
    def __init__(self, db_name='restaurant.db'):
        self.db_name = db_name

        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_dishes_table(self):
        query = '''
      CREATE TABLE IF NOT EXISTS dishes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        gram INTEGER NOT NULL,
        is_allergenic BOOLEAN NOT NULL,
        description TEXT
      )
    '''
        self.execute_query(query)

    def create_tables_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER NOT NULL
        )
        '''
        self.execute_query(query)

        # Добавление начальных данных, если таблица пустая
        check_query = 'SELECT COUNT(*) FROM tables'
        count = self.execute_query(check_query, fetchone=True)[0]

        if count == 0:  # Если в таблице нет записей
            initial_tables = [(1,), (2,), (3,), (4,), (5,)]
            insert_query = 'INSERT INTO tables (table_number) VALUES (?)'
            self.execute_query_many(insert_query, initial_tables)
            print("Начальные значения для таблицы 'tables' добавлены.")

    def create_employees_table(self):
        query = '''
      CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
      )
    '''
        self.execute_query(query)

        # Добавление начальных данных, если таблица пустая
        check_query = 'SELECT COUNT(*) FROM employees'
        count = self.execute_query(check_query, fetchone=True)[0]

        if count == 0:  # Если в таблице нет записей
            initial_employees = [("Виктор",), ("Алексей",), ("Егор",), ("Павел",), ("Афанасий",)]
            insert_query = 'INSERT INTO employees (name) VALUES (?)'
            self.execute_query_many(insert_query, initial_employees)
            print("Начальные значения для таблицы 'employees' добавлены.")

    def create_orders_table(self):
        query = '''
      CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_id INTEGER NOT NULL,
        employee_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (table_id) REFERENCES tables(id),
        FOREIGN KEY (employee_id) REFERENCES employees(id)
      )
    '''
        self.execute_query(query)

    def create_order_items_table(self):
        query = '''
      CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        dish_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (dish_id) REFERENCES dishes(id)
      )
    '''
        self.execute_query(query)

    def create_tables(self):
        """
        Последовательно создает все таблицы.
        """
        self.create_dishes_table()
        self.create_tables_table()
        self.create_employees_table()
        self.create_orders_table()
        self.create_order_items_table()

    def execute_query(self, query, params=None, fetchone=False, fetchall=False):
        """
        Выполняет запрос и возвращает результат, если нужно.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
            self.connection.commit()
            return cursor  # Вернуть курсор для доступа к lastrowid
        except Exception as e:
            self.connection.rollback()
            raise e

    def close(self):
        self.connection.close()

    def execute_query_many(self, query, values):
        """
        Выполняет запрос с несколькими значениями (массовая вставка).
        """
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

