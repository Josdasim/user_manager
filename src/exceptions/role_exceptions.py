class RoleError(Exception):
    def _init_(self, message: str):
        super()._init_(message)
        self.message = message


class RoleValidationError(RoleError):
    def _init_(self, message: str):
        super()._init_(message)


class RoleNotFoundError(RoleError):
    def _init_(self, message: str):
        super()._init_(message)


class RoleAlreadyExistsError(RoleError):
    def _init_(self, message: str):
        super()._init_(message)