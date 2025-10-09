import pytest
from src.services.user_service import UserService
from src.exceptions.user_exceptions import UserValidationError, UserNotFoundError, SameEmailError

#TODO: Optimizar la creacion de instancias de UserService
def test_create_user_service():
    service = UserService()
    user = service.create_user("Jhon", "jhon@correo.com", "passsupersecret!")
    assert user.username == "Jhon"
    assert user.email == "jhon@correo.com"
    assert user.password == "passsupersecret!"

def test_create_user_with_empty_username():
    service = UserService()
    with pytest.raises(UserValidationError):
        service.create_user("", "jhon@correo", "passsupersecret!")

def test_create_user_with_invalid_email():
    service = UserService()
    with pytest.raises(UserValidationError):
        service.create_user("Jhon", "jhoncorreo", "passsupersecret!")

def test_create_user_with_invalid_password():
    service = UserService()
    with pytest.raises(UserValidationError):
        service.create_user("Jhon", "jhon@correo", "paset")

def test_create_user_with_existing_username():
    service = UserService()
    service.create_user("Jhon", "jhon@correo.com", "passsupersecret!")
    with pytest.raises(UserValidationError):
        service.create_user("Jhon", "jhon2@correo.com", "passsecret!")

"""def test_create_user_with_existing_email():
    service = UserService()
    service.create_user("Jhon", "jhon@correo.com", "passsupersecret!")
    with pytest.raises(UserValidationError):
        service.create_user("Jhon2", "jhon@correo.com", "passsecret!")"""

#---------------------test_get_user------------------

def test_get_existing_user():
    service = UserService()
    service.create_user("axel", "axel@correo.com", "passasxel")
    user = service.get_user("axel")

    assert user.username == "axel"
    assert user.email == "axel@correo.com"

def test_get_unexistent_user():
    service = UserService()

    with pytest.raises(UserNotFoundError):
        service.get_user("axel")

#--------------------test_update_user----------------

def test_update_email_success():
    service = UserService()
    service.create_user("juan", "juan@correo.com", "passhuan")
    result = service.update_email("juan", "newemail@correo.com")

    assert result["username"] == "juan"
    assert result["email"] == "newemail@correo.com"
    assert service.get_user("juan").email == "newemail@correo.com"

def test_update_email_same_as_current():
    service = UserService()
    service.create_user("xion", "xion@correo.com", "passxion")

    with pytest.raises(SameEmailError) as e:
        service.update_email("xion", "xion@correo.com")

#--------------------test_delete_user----------------

def test_delete_user_success():
    service = UserService()
    service.create_user("xion", "xion@correo.com", "passxion")

    assert service.delete_user("xion") is None
    with pytest.raises(UserNotFoundError):
        service.get_user("xion")

def test_delete_nonexistent_user():
    service = UserService()
    with pytest.raises(UserNotFoundError):
        service.delete_user("iamnothere")
