class UserError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class UserValidationError(UserError):
    def __init__(self, message: str):
        super().__init__(message) 

class UserNotFoundError(UserError):
    def __init__(self, message: str):
        super().__init__(message)

class SameEmailError(UserError):
    def __init__(self, message: str):
        super().__init__(message)
    