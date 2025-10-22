from src.models.user_role import UserRole


class UserRoleRepository():
    def __init__(self):
        self._relations : list[UserRole] = []
    
    def add(self, relation:UserRole):
        if self.find(relation.user_id, relation.role_id):
            raise ValueError("Relacion ya existe")
        self._relations.append(relation)


    def find(self, user_id:str, role_id:str) -> UserRole | None:
        for relation in self._relations:
            if relation.user_id == user_id and relation.role_id == role_id:
                return relation
        return None
    
    def get_all(self) -> list[UserRole]:
        return self._relations

    #TODO: Considerar respuestas al buscar un usuario inexistente, actualmente retornaria vacio
    def get_roles_by_user(self, user_id:str) -> list[UserRole]:
        return [relation for relation in self._relations if relation.user_id == user_id]
    
    def get_users_by_role(self, role_id:str) -> list[UserRole]:
        return [relation for relation in self._relations if relation.role_id == role_id]
    
    def update_role_relation(self, user_id:str, role_id:str, new_role:str) -> UserRole:
        old_relation = self.find(user_id, role_id)
        if not old_relation:
            raise ValueError("El usuario no cuenta con ese permiso")
        if old_relation.role_id == new_role:
            raise ValueError("El usuario ya cuenta con ese rol")
        new_relation = UserRole(user_id, new_role)
        index = self._relations.index(old_relation)
        self._relations[index] = new_relation
        return new_relation
    
    #TODO: refactorizar
    def delete(self, user_id:str,role_id:str) -> None:
        relation = self.find(user_id, role_id)
        if not relation:
            raise ValueError("El usuario no cuenta con ese permiso")
        self._relations.remove(relation)

