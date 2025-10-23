from src.models.role import Role
from src.repositories.role_repository import RoleRepository


class RoleService:
    def __init__(self, repository: RoleRepository | None = None):
        self.repository = repository or RoleRepository()

    def create_role(self, name: str, description: str = "") -> Role:
        if not name:
            raise ValueError("El nombre del rol es obligatorio")
        role = Role(name=name.strip().lower(), description=description)
        return self.repository.add(role)

    def get_role(self, name: str) -> Role:
        if not name:
            raise ValueError("El nombre del rol es obligatorio")
        return self.repository.get(name.strip().lower())

    def get_all_roles(self) -> list[Role]:
        return self.repository.get_all()

    def update_role_description(self, name: str, new_description: str) -> Role:
        if not name:
            raise ValueError("El nombre del rol es obligatorio")
        if new_description is None:
            raise ValueError("La descripción no puede ser nula")
        return self.repository.update_description(name.strip().lower(), new_description)

    def delete_role(self, name: str) -> None:
        if not name:
            raise ValueError("El nombre del rol es obligatorio")
        self.repository.delete(name.strip().lower())
