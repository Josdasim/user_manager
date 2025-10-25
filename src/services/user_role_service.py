from src.models.user_role import UserRole
from src.repositories.user_role_repository import UserRoleRepository


class UserRoleService:
    def __init__(self, repository: UserRoleRepository | None = None):
        self.repository = repository or UserRoleRepository()

    def assign_role(self, user_id: str, role_id: str) -> UserRole:
        """Asigna un rol a un usuario"""
        if not user_id or not role_id:
            raise ValueError("user_id y role_id son requeridos")
        relation = UserRole(user_id, role_id)
        self.repository.add(relation)
        return relation

    def get_user_roles(self, user_id: str) -> list[UserRole]:
        """Obtiene todos los roles de un usuario"""
        if not user_id:
            raise ValueError("user_id es requerido")
        return self.repository.get_roles_by_user(user_id)

    def get_users_by_role(self, role_id: str) -> list[UserRole]:
        """Obtiene todos los usuarios que tienen un rol específico"""
        if not role_id:
            raise ValueError("role_id es requerido")      
        return self.repository.get_users_by_role(role_id)

    def get_all_relations(self) -> list[UserRole]:
        """Obtiene todas las relaciones usuario-rol"""
        return self.repository.get_all()

    def update_user_role(self, user_id: str, old_role_id: str, new_role_id: str) -> UserRole:
        """Actualiza el rol de un usuario"""
        if not user_id or not old_role_id or not new_role_id:
            raise ValueError("user_id, old_role_id y new_role_id son requeridos")
        return self.repository.update_role_relation(user_id, old_role_id, new_role_id)

    def user_has_role(self, user_id: str, role_id: str) -> bool:
        """Verifica si un usuario tiene un rol específico"""
        if not user_id or not role_id:
            return False
        relation = self.repository.find(user_id, role_id)
        return relation is not None
    
    def remove_role(self, user_id: str, role_id: str) -> None:
        """Remueve un rol de un usuario"""
        if not user_id or not role_id:
            raise ValueError("user_id y role_id son requeridos")      
        self.repository.delete(user_id, role_id)