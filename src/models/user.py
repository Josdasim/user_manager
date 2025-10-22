import re
from src.constants import messages
from src.exceptions.user_exceptions import UserValidationError
from uuid6 import uuid7
from datetime import datetime
from src.models.user_status import UserStatus


class User:

    EMAIL_PATTERN = r"^[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    def __init__(self, username: str, email: str, password: str, status:UserStatus = UserStatus.INACTIVE):
        self._validate_username(username)
        self._validate_email(email)
        self.id = str(uuid7())
        self.username = username
        self.email = email
        self.password = password
        self.status = status
        #TODO:Agregar nuevas variables para rol y permisos
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def _validate_username(self, username:str) -> None:
        if not username or not username.strip():
            raise UserValidationError(messages.USER_INVALID_USERNAME)
          
    def _validate_email(self, email:str) -> None:
        if not email or not re.match(self.EMAIL_PATTERN, email):
            raise UserValidationError(messages.USER_INVALID_EMAIL)  

    def _refresh_updated_at(self) -> None:
        self.updated_at = datetime.now()
    
    #TODO: Change username, password
    
    def update_email(self, new_email:str)-> None:
        self._validate_email(new_email)
        self.email = new_email
        self._refresh_updated_at()
    
    #TODO: metodos para cambiar los estados del usuario
    
    def __repr__(self) -> str:
        return f"User(username={self.username}, email={self.email}, created_at= {self.created_at}, updated_at={self.updated_at})"
        