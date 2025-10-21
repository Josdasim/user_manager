from src.models.role import Role


class RoleRepository():
    def __init__(self):
        self._data: dict[str, Role] = {}

    def add(self, role:Role) -> Role:
        if role.name in self._data:
            #TODO: crear error y mensaje personalizado
            raise ValueError("El Rol ya se encuentra registrado")
        self._data[role.name] = role
        return self._data[role.name]
    
    def find(self, name:str) -> Role | None:
        return self._data.get(name.strip().lower())

    def get(self, name:str) -> Role:
        role = self.find(name)
        if not role:
            #TODO: crear error y mensaje personalizado
            raise ValueError("Rol no encontrado")
        return role
    
    def get_all(self) -> list[Role]:
        return list(self._data.values())
    
    def update_description(self, name:str, new_description:str) -> Role:
        role = self.get(name)
        role.update_description(new_description)
        self._data[name] = role
        return role
    
    def delete(self, name:str)-> None:
        role = self.get(name)
        del self._data[name]