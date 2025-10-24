from src.models.role import Role
from src.exceptions.role_exceptions import RoleAlreadyExistsError, RoleNotFoundError
from src.constants import messages

class RoleRepository():
    def __init__(self):
        self._data: dict[str, Role] = {}

    def add(self, role:Role) -> Role:
        """Agrega un nuevo rol, retorna el rol creado o una excepcion si ya se encontraba registrado"""
        if role.name in self._data:
            raise RoleAlreadyExistsError(messages.ROLE_ALREADY_EXISTS)
        self._data[role.name] = role
        return self._data[role.name]
    
    def find(self, name:str) -> Role | None:
        """Busca un rol por el nombre, retorna el rol o None en caso de no encontrarlo"""
        return self._data.get(name.strip().lower())

    def get(self, name:str) -> Role:
        """Obtiene un rol usando el nombre, retorna una excepcion en caso de no existir"""
        role = self.find(name)
        if not role:
            raise RoleNotFoundError(messages.ROLE_NOT_FOUND)
        return role
    
    def get_all(self) -> list[Role]:
        """Obtiene todos los roles registrados"""
        return list(self._data.values())
    
    def update_description(self, name:str, new_description:str) -> Role:
        """Actualiza la descripción de un rol, retorna el rol actualizado"""
        role = self.get(name)
        role.update_description(new_description)
        self._data[name] = role
        return role
    
    def delete(self, name:str)-> None:
        """Elimina un rol registrado"""
        role = self.get(name)
        del self._data[name]