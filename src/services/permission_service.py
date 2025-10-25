from src.models.permission import Permission
from src.repositories.permission_repository import PermissionRepository
from src.exceptions.permission_exceptions import PermissionAlreadyExistsError, PermissionNotFoundError, PermissionValidationError
from src.constants import messages

class PermissionService:
    def __init__(self, repository: PermissionRepository | None = None):
        self.repository = repository or PermissionRepository()

    def create_permission(self, name: str, description: str = "") -> Permission:
        """Crea un nuevo permiso"""
        if not name or not name.strip():
            raise PermissionValidationError(messages.PERMISSION_INVALID_NAME)
        permission = Permission(name=name.strip().lower(), description=description)
        return self.repository.add(permission)

    def get_permission(self, name: str) -> Permission:
        """Obtiene un permiso por nombre"""
        if not name:
            raise PermissionValidationError(messages.PERMISSION_INVALID_NAME)
        return self.repository.get(name.strip().lower())

    def get_all_permissions(self) -> list[Permission]:
        """Obtiene todos los permisos"""
        return self.repository.get_all()

    def update_permission_description(self, name: str, new_description: str) -> Permission:
        """Actualiza la descripción de un permiso"""
        if not name:
            #TODO: crear error y mensaje personalizado (ej: Campos vacios | campos obligatorios)
            raise PermissionValidationError(messages.PERMISSION_INVALID_NAME)
        if new_description is None:
            raise PermissionValidationError(messages.PERMISSION_INVALID_TYPE)
        return self.repository.update_description(name.strip().lower(), new_description)

    def delete_permission(self, name: str) -> None:
        """Elimina un permiso"""
        if not name:
            raise PermissionValidationError(messages.PERMISSION_INVALID_NAME)
        self.repository.delete(name.strip().lower())