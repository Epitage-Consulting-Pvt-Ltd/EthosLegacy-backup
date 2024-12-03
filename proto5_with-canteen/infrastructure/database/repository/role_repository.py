from infrastructure.database.db_manager import DBManager
from infrastructure.database.entity.role import Role

class RoleRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def create_role(self, role):
        query = "INSERT INTO role (role_name) VALUES (?)"
        params = (role.role_name,)
        self.db_manager.execute_query(query, params)

    def update_role(self, role):
        query = "UPDATE role SET role_name=? WHERE role_id=?"
        params = (role.role_name, role.role_id)
        self.db_manager.execute_query(query, params)

    def delete_role(self, role_id):
        query = "DELETE FROM role WHERE role_id=?"
        params = (role_id,)
        self.db_manager.execute_query(query, params)

    def get_role_by_id(self, role_id):
        query = "SELECT * FROM role WHERE role_id=?"
        params = (role_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            return self._create_role_instance(result[0])
        return None

    def get_all_roles(self, page=1, page_size=10):
        offset = (page - 1) * page_size
        query = "SELECT * FROM role LIMIT ? OFFSET ?"
        params = (page_size, offset)
        result = self.db_manager.fetch_data(query, params)
        return [self._create_role_instance(row) for row in result]

    def _create_role_instance(self, row):
        role_id, role_name = row
        return Role(role_id, role_name)

    def close_connection(self):
        self.db_manager.close_connection()
