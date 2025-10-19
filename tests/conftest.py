import pytest
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService
from src.security.jwt_manager import JWTManager


@pytest.fixture
def repo():
    return UserRepository()

@pytest.fixture
def service():
    return UserService()

@pytest.fixture
def jwt():
    return JWTManager()

@pytest.fixture
def sample_payload():
    return {"username":"test_user"}

@pytest.fixture
def sample_user_1():
    return User(username="Tomas", email="tomas01@correo.com", password="secret01")

@pytest.fixture
def sample_user_2():
    return User(username="Juan", email="juan@correo.com", password="passhuan")

@pytest.fixture
def sample_user_3():
    return User(username="Axel", email="axel@correo.com", password="passasxel")

@pytest.fixture
def sample_user_data_1():
    return {"username":"xion","email":"xion@correo.com","password":"passxion"}

@pytest.fixture
def sample_user_data_2():
    return {"username":"juan","email":"juan@correo.com","password":"passhuan"}

