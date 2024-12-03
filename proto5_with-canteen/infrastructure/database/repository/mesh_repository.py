from db_manager import DBManager
from mesh import Mesh

class MeshRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def create_mesh(self, mesh):
        query = "INSERT INTO mesh (mesh_name) VALUES (?)"
        params = (mesh.mesh_name,)
        self.db_manager.execute_query(query, params)

    def update_mesh(self, mesh):
        query = "UPDATE mesh SET mesh_name=? WHERE mesh_id=?"
        params = (mesh.mesh_name, mesh.mesh_id)
        self.db_manager.execute_query(query, params)

    def delete_mesh(self, mesh_id):
        query = "DELETE FROM mesh WHERE mesh_id=?"
        params = (mesh_id,)
        self.db_manager.execute_query(query, params)

    def get_mesh_by_id(self, mesh_id):
        query = "SELECT * FROM mesh WHERE mesh_id=?"
        params = (mesh_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            return self._create_mesh_instance(result[0])
        return None

    def get_all_meshes(self, page=1, page_size=10):
        offset = (page - 1) * page_size
        query = "SELECT * FROM mesh LIMIT ? OFFSET ?"
        params = (page_size, offset)
        result = self.db_manager.fetch_data(query, params)
        return [self._create_mesh_instance(row) for row in result]

    def _create_mesh_instance(self, row):
        mesh_id, mesh_name = row
        return Mesh(mesh_id, mesh_name)

    def close_connection(self):
        self.db_manager.close_connection()
