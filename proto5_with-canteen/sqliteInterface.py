import sqlite3

class SQLiteInterface:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return []

    def execute_non_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error executing non-query: {e}")

    def create_table(self, table_name, schema):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
        self.execute_non_query(query)

    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute_non_query(query, list(data.values()))

    def select_data(self, table_name, conditions=None):
        query = f"SELECT * FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"
        return self.execute_query(query)

    def update_data(self, table_name, data, conditions=None):
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause}"
        if conditions:
            query += f" WHERE {conditions}"
        self.execute_non_query(query, list(data.values()))

    def delete_data(self, table_name, conditions=None):
        query = f"DELETE FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"
        self.execute_non_query(query)

    def commit(self):
        if self.connection:
            self.connection.commit()

    def disconnect_from_serial(self):
        if self.ser:
            self.ser.close()

    def disconnect_from_database(self):
        if self.connection:
            self.connection.close()


# Example usage:
if __name__ == "__main__":
    db_name = "my_database.db"
    db = SQLiteInterface(db_name)
    db.connect()

    # Create a table
    db.create_table("students", "id INTEGER PRIMARY KEY, name TEXT, age INTEGER")

    # Insert data
    student_data = {"name": "Alice", "age": 25}
    db.insert_data("students", student_data)

    # Select data
    students = db.select_data("students")
    for student in students:
        print(student["name"], student["age"])

    db.disconnect()
