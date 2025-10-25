from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    BLOCKED = "blocked"

    @classmethod
    def list(cls):
        return [status.value for status in cls]