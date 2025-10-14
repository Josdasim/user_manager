from src.models.user import User
from src.exceptions.user_exceptions import UserValidationError, UserNotFoundError, SameEmailError
from src.constants import messages
from src.repositories.user_repository import UserRepository


class UserService():
    
    def __init__(self, repository:UserRepository | None = None):
        self.repository = repository or UserRepository()

    def create_user(self, username:str, email:str, password:str) -> User:
        user = User(username, email, password)
        self.repository.add(user)
        return user
    
    def get_user(self, username:str) -> User:
        user = self.repository.get(username)
        return user
 
    def get_all_users(self) -> list[User]:
        all_users = self.repository.get_all()
        return all_users
       
    def update_email(self, username:str, new_email:str) -> dict:
        #TODO: Aplicar validaciones como: correo ya registrado
        user = self.get_user(username)
        
        if user.email == new_email:
            raise SameEmailError(messages.SAME_EMAIL)
        
        user_updated = self.repository.update_email(username, new_email)
        return {"username":user_updated.username, "email":user_updated.email}

    def delete_user(self, username:str) -> None:
        self.repository.delete(username)