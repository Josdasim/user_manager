from src.models.role_permission import RolePermission


class RolePermissionRepository:
    def __init__(self):
        self._relations: list[RolePermission] = []

    def add(self, relation: RolePermission):
        if self.find(relation.role_id, relation.permission_id):
            raise ValueError("La relación ya existe")
        self._relations.append(relation)

    def find(self, role_id: str, permission_id: str) -> RolePermission | None:
        for relation in self._relations:
            if relation.role_id == role_id and relation.permission_id == permission_id:
                return relation
        return None

    def get_all(self) -> list[RolePermission]:
        return self._relations

    def get_permissions_by_role(self, role_id: str) -> list[RolePermission]:
        return [relation for relation in self._relations if relation.role_id == role_id]

    def get_roles_by_permission(self, permission_id: str) -> list[RolePermission]:
        return [relation for relation in self._relations if relation.permission_id == permission_id]

    def update_permission_relation(self, role_id: str, permission_id: str, new_permission: str) -> RolePermission:
        old_relation = self.find(role_id, permission_id)
        if not old_relation:
            raise ValueError("El rol no cuenta con ese permiso")
        if old_relation.permission_id == new_permission:
            raise ValueError("El rol ya cuenta con ese permiso")
        new_relation = RolePermission(role_id, new_permission)
        index = self._relations.index(old_relation)
        self._relations[index] = new_relation
        return new_relation

    def delete(self, role_id: str, permission_id: str) -> None:
        relation = self.find(role_id, permission_id)
        if not relation:
            raise ValueError("El rol no cuenta con ese permiso")
        self._relations.remove(relation)
