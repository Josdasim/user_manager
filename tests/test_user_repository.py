import pytest
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.exceptions.user_exceptions import UserValidationError, UserNotFoundError
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

    with pytest.raises(UserNotFoundError):
        repo.get("Unknown")

def test_find_user():
    repo = UserRepository()
    user = User("axel", "axel@correo.com", "passasxel")
    repo.add(user)

    assert repo.find("axel") == user

def test_user_not_found():
    repo = UserRepository()
    assert repo.find("amiexist?") is None

#--------------------test_update--------------------

def test_update_existing_user():
    repo = UserRepository()
    user = User("axel", "axel@correo.com", "passasxel")
    repo.add(user)
    user_updated = repo.update_email("axel", "newaxel@correo.com")

    assert repo.get("axel").email == "newaxel@correo.com"

def test_update_nonexistent_user():
    repo = UserRepository()

    with pytest.raises(UserNotFoundError) as e:
        repo.update_email("no_estoy", "correo@correo.com")
    assert str(e.value) == messages.USER_NOT_FOUND
    
#--------------------test_delete-------------------

def test_delete_exisiting_user():
    repo = UserRepository()
    user = User("axel", "axel@correo.com", "passasxel")
    repo.add(user)
    assert repo.get(user.username) is not None 

    repo.delete("axel")
    assert repo.find("axel") is None

def test_delete_nonexistent_user():
    repo = UserRepository()

    with pytest.raises(UserNotFoundError):
        repo.delete("nonexistent")
