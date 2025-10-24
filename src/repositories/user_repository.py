from src.models.user import User
from src.constants import messages
from src.exceptions.user_exceptions import UserValidationError, UserNotFoundError
from src.models.user_status import UserStatus


class UserRepository():
    def __init__(self):
        self._data: dict[str, User] = {}

    #TODO: Se debe modificar para que retorne un User
    def add(self, user:User) -> User:
        """Agrega un nuevo usuario al repositorio, retorna el usuario agregado"""
        if user.username in self._data:
            raise UserValidationError(messages.USER_ALREADY_EXISTS)
        self._data[user.username] = user
        return self._data[user.username]

    def find(self, username:str) -> User | None:
        """Busca un usuario por username, retorna el usuario o None si no existe"""
        return self._data.get(username.strip())

    def find_by_email(self, email:str) -> User | None:
        """Busca un usuario por email, retorna el usuario o None si no existe"""
        for user in self._data.values():
            if user.email == email:
                return user
        return None

    def get(self, username:str) -> User:
        """Obtiene un usuario por username, lanza una excepcion si no existe"""
        user = self.find(username)
        if not user:
            raise UserNotFoundError(messages.USER_NOT_FOUND)
        return user
    
    def get_all(self) -> list[User]:
        """Obtiene todos los usuarios"""
        all_users = list(self._data.values())
        return all_users
        
    def update_username(self, username:str, new_username:str) -> User:
        """Actualiza el username de un usuario, retorna el usuario o una exception en caso de no existir"""
        user = self.get(username)
        del self._data[username]
        user.update_username(new_username)
        self._data[user.username] = user
        return user

    def update_email(self, username:str, new_email:str) -> User:
        """Actualiza el email de un usuario, retorna el usuario actualizado"""
        user = self.get(username)
        user.update_email(new_email)
        self._data[user.username] = user
        return user

    def update_password(self, username:str, new_password:str) -> User:
        """Actualiza la contraseña del usuario"""
        user = self.get(username)
        user.update_password(new_password)
        self._data[user.username] = user
        return user

    def update_status(self, username:str, new_status:UserStatus) -> User:
        """Actualiza el estado de un usuario, retorna el usuario o una Excepcion en caso de que se ingrese un estado no válido"""
        user = self.get(username)
        #TODO:Crear mensajes y excepciones personalizadas para en casos de errores con estatus
        if new_status not in UserStatus.list():
            raise ValueError("Estado invalido") 
        actions = {
            UserStatus.ACTIVE:user.activate,
            UserStatus.INACTIVE:user.deactivate,
            UserStatus.SUSPENDED:user.suspend,
            UserStatus.BLOCKED:user.block
        }
        action = actions.get(new_status)
        action()
        self._data[user.username] = user
        return user

    def delete(self, username:str)-> None:
        """Elimina un usuario del repositorio"""
        self.get(username)
        del self._data[username]
 
