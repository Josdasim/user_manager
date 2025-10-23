from src.models.permission import Permission
from src.repositories.permission_repository import PermissionRepository


class PermissionService:
    def __init__(self, repository: PermissionRepository | None = None):
        self.repository = repository or PermissionRepository()

    def create_permission(self, name: str, description: str = "") -> Permission:
        """Crea un nuevo permiso"""
        if not name:
            raise ValueError("El nombre del permiso es obligatorio")
        permission = Permission(name=name.strip().lower(), description=description)
        return self.repository.add(permission)

    def get_permission(self, name: str) -> Permission:
        """Obtiene un permiso por nombre"""
        if not name:
            raise ValueError("El nombre del permiso es obligatorio")
        return self.repository.get(name.strip().lower())

    def get_all_permissions(self) -> list[Permission]:
        """Obtiene todos los permisos"""
        return self.repository.get_all()

    def update_permission_description(self, name: str, new_description: str) -> Permission:
        """Actualiza la descripción de un permiso"""
        if not name:
            #TODO: crear error y mensaje personalizado (ej: Campos vacios | campos obligatorios)
            raise ValueError("El nombre del permiso es obligatorio")
        if new_description is None:
            raise ValueError("La descripcion no puede ser nula")
        return self.repository.update_description(name.strip().lower(), new_description)

    def delete_permission(self, name: str) -> None:
        """Elimina un permiso"""
        if not name:
            raise ValueError("El nombre del permiso es obligatorio")
        self.repository.delete(name.strip().lower())