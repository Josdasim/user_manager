from src.constants import messages
class User:
    def __init__(self, username: str, email: str, password: str):
        if not username.strip():
            raise ValueError(messages.USER_INVALID_USERNAME)
        if not email or "@" not in email:
            raise ValueError(messages.USER_INVALID_EMAIL)
        if len(password) < 6:
            raise ValueError(messages.USER_INVALID_PASSWORD)
        self.username = username
        self.email = email
        self.password = password