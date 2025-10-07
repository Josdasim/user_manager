from src.models.user import User
from src.exceptions.user_exceptions import UserValidationError
from src.constants import messages
from src.repositories.user_repository import UserRepository


class UserService():
    
    def __init__(self, repository:UserRepository | None = None):
        self.repository = repository or UserRepository()

    def create_user(self, username:str, email:str, password:str) -> User:
        if self.repository.get(username):
            raise UserValidationError(messages.USER_ALREADY_EXISTS)
        
        user = User(username, email, password)
        self.repository.add(user)
        return user
