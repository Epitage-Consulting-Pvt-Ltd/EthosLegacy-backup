from infrastructure.database.repository.role_repository import RoleRepository

class RoleController:
    def __init__(self):
        self.role_repository = RoleRepository()

    def get_all_roles(self):
        return self.role_repository.get_all_roles()