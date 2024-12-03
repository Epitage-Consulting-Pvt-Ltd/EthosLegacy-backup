from db_manager import DBManager
from menugroup import MenuGroup

class MenuGroupRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def create_menugroup(self, menugroup):
        query = "INSERT INTO menugroup (menugrp_name) VALUES (?)"
        params = (menugroup.menugrp_name,)
        self.db_manager.execute_query(query, params)

    def update_menugroup(self, menugroup):
        query = "UPDATE menugroup SET menugrp_name=? WHERE menugrp_id=?"
        params = (menugroup.menugrp_name, menugroup.menugrp_id)
        self.db_manager.execute_query(query, params)

    def delete_menugroup(self, menugrp_id):
        query = "DELETE FROM menugroup WHERE menugrp_id=?"
        params = (menugrp_id,)
        self.db_manager.execute_query(query, params)

    def get_menugroup_by_id(self, menugrp_id):
        query = "SELECT * FROM menugroup WHERE menugrp_id=?"
        params = (menugrp_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            return self._create_menugroup_instance(result[0])
        return None

    def get_all_menugroups(self, page=1, page_size=10):
        offset = (page - 1) * page_size
        query = "SELECT * FROM menugroup LIMIT ? OFFSET ?"
        params = (page_size, offset)
        result = self.db_manager.fetch_data(query, params)
        return [self._create_menugroup_instance(row) for row in result]

    def _create_menugroup_instance(self, row):
        menugrp_id, menugrp_name = row
        return MenuGroup(menugrp_id, menugrp_name)

    def close_connection(self):
        self.db_manager.close_connection()
