import pytest
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService
from src.repositories.role_repository import RoleRepository
from src.repositories.user_role_repository import UserRoleRepository


@pytest.fixture
def user_repo():
    return UserRepository()

@pytest.fixture
def user_service():
    return UserService()

@pytest.fixture
def role_repo():
    return RoleRepository()

@pytest.fixture
def user_role_repo():
    return UserRoleRepository()

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

@pytest.fixture
def sample_user1_role1_data():
    return {"user_id":"u1","role_id":"r1"}

@pytest.fixture
def sample_user1_role2_data():
    return {"user_id":"u1","role_id":"r2"}

@pytest.fixture
def sample_user2_role1_data():
    return {"user_id":"u2","role_id":"r1"}

@pytest.fixture
def sample_user2_role2_data():
    return {"user_id":"u2","role_id":"r2"}

