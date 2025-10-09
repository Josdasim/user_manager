from src.models.user import User
from src.constants import messages
from src.exceptions.user_exceptions import UserValidationError, UserNotFoundError


class UserRepository():
    def __init__(self):
        self._data = {}

    #TODO: Se debe modificar para que retorne un User
    def add(self, user:User) -> None:
        if user.username in self._data:
            raise UserValidationError(messages.USER_ALREADY_EXISTS)
        self._data[user.username] = user

    #TODO: Crear un metodo find para mejorar y separar el control de errores

    #TODO: Mejorar el metodo get para lanzar la excepcion "UserNotFound"----
    def get(self, username:str) -> User | None:
        return self._data.get(username)
    
    def update_email(self, username:str, new_email:str) -> User:
        user = self.get(username)

        if not user:
            raise UserNotFoundError(messages.USER_NOT_FOUND)
        user.email = new_email
        self._data[username] = user
        return user

    def delete(self, username:str)-> None:
        user = self.get(username)

        if not user:
            raise UserNotFoundError(messages.USER_NOT_FOUND)
        del self._data[username]
 
