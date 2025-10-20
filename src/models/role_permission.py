class RolePermission:
    def __init__(self, role_id:str, permission_id:str):
        self.permission_id = permission_id
        self.role_id = role_id