from src.models.role_permission import RolePermission
from src.repositories.role_permission_repository import RolePermissionRepository


class RolePermissionService:
    def __init__(self, repository: RolePermissionRepository | None = None) :
        self.repository = repository or RolePermissionRepository()

    def add_permission_to_role(self, role_id: str, permission_id: str) -> RolePermission:
        if not role_id or not permission_id:
            raise ValueError("role_id y permission_id son requeridos")

        relation = RolePermission(role_id=role_id, permission_id=permission_id)
        self.repository.add(relation)
        return relation

    def get_all_relations(self) -> list[RolePermission]:
        return self.repository.get_all()

    def get_permissions_by_role(self, role_id: str) -> list[RolePermission]:
        return self.repository.get_permissions_by_role(role_id)

    def get_roles_by_permission(self, permission_id: str) -> list[RolePermission]:
        return self.repository.get_roles_by_permission(permission_id)

    def update_permission_relation(self, role_id: str, permission_id: str, new_permission_id: str) -> RolePermission:
        return self.repository.update_permission_relation(role_id, permission_id, new_permission_id)

    def remove_permission_from_role(self, role_id: str, permission_id: str) -> None:
        self.repository.delete(role_id, permission_id)
