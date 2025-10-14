from src.models.user import User
from src.constants import messages
from src.exceptions.user_exceptions import UserValidationError, UserNotFoundError


class UserRepository():
    def __init__(self):
        self._data: dict[str, User] = {}

    #TODO: Se debe modificar para que retorne un User
    def add(self, user:User) -> None:
        if user.username in self._data:
            raise UserValidationError(messages.USER_ALREADY_EXISTS)
        self._data[user.username] = user

    def find(self, username:str) -> User | None:
        return self._data.get(username.strip())

    def get(self, username:str) -> User:
        user = self.find(username)
        if not user:
            raise UserNotFoundError(messages.USER_NOT_FOUND)
        return user
    
    def update_email(self, username:str, new_email:str) -> User:
        user = self.get(username)
        #TODO: Se debe buscar la forma de validar el correo antes de intentar actualiarlo
        user.email = new_email
        self._data[username] = user
        return user

    def delete(self, username:str)-> None:
        user = self.get(username)
        del self._data[username]
 
