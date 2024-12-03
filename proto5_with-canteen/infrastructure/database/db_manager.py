import sqlite3
import os
from infrastructure.env_config import EnvConfig


class DBManager:
    def __init__(self):
        self.config = EnvConfig()
        current_directory = os.getcwd()
        db_file_path = os.path.join(current_directory, self.config.DB_PATH)
        self.db_name =  db_file_path
        self.connection = None
        self.cursor = None
        self.create_connection()

    def     create_connection(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Connected to SQLite database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully.")
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")

    def execute_query_without_commit(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            print("Query executed successfully.")
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")

    def fetch_data(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def begin_transaction(self):
        self.cursor.execute("BEGIN TRANSACTION")

    def commit_transaction(self):
        self.connection.commit()

    def rollback_transaction(self):
        self.connection.rollback()

    def last_row_id(self):
        return self.cursor.lastrowid