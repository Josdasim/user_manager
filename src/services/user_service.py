from src.models.user import User
from src.exceptions.user_exceptions import UserValidationError
from src.constants import messages


class UserService():
    
    def __init__(self):
        self._users = {}

    def create_user(self, username:str, email:str, password:str) -> User:
        if username in self._users:
            raise UserValidationError(messages.USER_ALREADY_EXISTS)
        
        user = User(username, email, password)
        self._users[username] = user
        return user
