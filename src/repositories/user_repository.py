from src.models.user import User
from src.constants import messages
from src.exceptions.user_exceptions import UserValidationError


class UserRepository():
    def __init__(self):
        self._data = {}

    def add(self, user:User) -> None:
        if user.username in self._data:
            raise UserValidationError(messages.USER_ALREADY_EXISTS)
        self._data[user.username] = user

    def get(self, username:str) -> User | None:
        return self._data.get(username)
