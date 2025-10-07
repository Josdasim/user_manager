import pytest
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.exceptions.user_exceptions import UserValidationError
from src.constants import messages


def test_add_and_get_user():
    repo = UserRepository()
    user = User("Juan", "juan@correo.com", "supersecret!")
    repo.add(user)

    repo_retrieved = repo.get("Juan")
    assert repo_retrieved.username == "Juan"
    assert repo_retrieved.email == "juan@correo.com"

def test_add_existing_user():
    repo = UserRepository()
    user = User("axel", "axel@correo.com", "passasxel")
    repo.add(user)

    with pytest.raises(UserValidationError) as e:
        repo.add(user)
        assert str(e.value) == messages.USER_ALREADY_EXISTS
    
def test_get_nonexistent_user():
    repo = UserRepository()
    assert repo.get("Unknown") is None
