class AppError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class UserValidationError(AppError):
    def __init__(self, message: str):
        super().__init__(message) 

class UserNotFoundError(AppError):
    def __init__(self, message: str):
        super().__init__(message)

class SameEmailError(AppError):
    def __init__(self, message: str):
        super().__init__(message)

class TokenExpiredError(AppError):
    def __init__(self, message:str):
        super().__init__(message)

class TokenInvalidError(AppError):
    def __init__(self, message:str):
        super().__init__(message)