from src.models.permission import Permission
from src.constants import messages
from src.exceptions.permission_exceptions import PermissionAlreadyExistsError, PermissionNotFoundError


class PermissionRepository():
    def __init__(self):
        self._data: dict[str, Permission] = {}

    def add(self, permission:Permission) -> Permission:
        if permission.name in self._data:
            raise PermissionAlreadyExistsError(messages.PERMISSION_ALREADY_EXISTS)
        self._data[permission.name] = permission
        return self._data[permission.name]
    
    def find(self, name:str) -> Permission | None:
        return self._data.get(name.strip().lower())

    def get(self, name:str) -> Permission:
        permission = self.find(name)
        if not permission:
            raise PermissionNotFoundError(messages.PERMISSION_NOT_FOUND)
        return permission
    
    def get_all(self) -> list[Permission]:
        return list(self._data.values())
    
    def update_description(self, name:str, new_description:str) -> Permission:
        permission = self.get(name)
        permission.update_description(new_description)
        self._data[name] = permission
        return permission
    
    def delete(self, name:str)-> None:
        permission = self.get(name)
        del self._data[name]