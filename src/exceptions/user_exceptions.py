from src.constants import messages

class AppError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class UserValidationError(AppError):
    def __init__(self, message: str):
        super().__init__(message) 