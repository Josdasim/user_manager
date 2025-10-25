class PermissionError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class PermissionValidationError(PermissionError):
    def __init__(self, message: str):
        super().__init__(message)


class PermissionNotFoundError(PermissionError):
    def __init__(self, message: str):
        super().__init__(message)


class PermissionAlreadyExistsError(PermissionError):
    def __init__(self, message: str):
        super().__init__(message)