import re
from src.constants import messages
from src.exceptions.user_exceptions import UserValidationError


class User:

    EMAIL_PATTERN = r"^[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    def __init__(self, username: str, email: str, password: str):
        self._validate_username(username)
        self._validate_email(email)
        self._validate_password(password)
        self.username = username
        self.email = email
        self.password = password

    def _validate_username(self, username:str) -> None:
        if not username or not username.strip():
            raise UserValidationError(messages.USER_INVALID_USERNAME)
        
    def _validate_email(self, email:str) -> None:
        if not email or not re.match(self.EMAIL_PATTERN, email):
            raise UserValidationError(messages.USER_INVALID_EMAIL)
        
    def _validate_password(self, password:str) -> None:
        if not password or len(password) < 6:
            raise UserValidationError(messages.USER_INVALID_PASSWORD)
        
    def __repr__(self) -> str:
        return f"User(username='{self.username}', email='{self.email}')"
        