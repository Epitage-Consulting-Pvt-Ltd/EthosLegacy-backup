from db_manager import DBManager
from menu import Menu

class MenuRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def create_menu(self, menu):
        query = "INSERT INTO menu (menugrp_id, menu_name) VALUES (?, ?)"
        params = (menu.menugrp_id, menu.menu_name)
        self.db_manager.execute_query(query, params)

    def update_menu(self, menu):
        query = "UPDATE menu SET menugrp_id=?, menu_name=? WHERE menu_id=?"
        params = (menu.menugrp_id, menu.menu_name, menu.menu_id)
        self.db_manager.execute_query(query, params)

    def delete_menu(self, menu_id):
        query = "DELETE FROM menu WHERE menu_id=?"
        params = (menu_id,)
        self.db_manager.execute_query(query, params)

    def get_menu_by_id(self, menu_id):
        query = "SELECT * FROM menu WHERE menu_id=?"
        params = (menu_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            return self._create_menu_instance(result[0])
        return None

    def get_all_menus(self, page=1, page_size=10):
        offset = (page - 1) * page_size
        query = "SELECT * FROM menu LIMIT ? OFFSET ?"
        params = (page_size, offset)
        result = self.db_manager.fetch_data(query, params)
        return [self._create_menu_instance(row) for row in result]

    def _create_menu_instance(self, row):
        menu_id, menugrp_id, menu_name = row
        return Menu(menu_id, menugrp_id, menu_name)

    def close_connection(self):
        self.db_manager.close_connection()
