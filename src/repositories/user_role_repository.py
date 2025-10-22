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
    
    #TODO: Considerar respuestas al buscar un usuario inexistente, actualmente retornaria vacio
    def get_roles_by_user(self, user_id:str) -> list[UserRole]:
        return [relation for relation in self._relations if relation.user_id == user_id]