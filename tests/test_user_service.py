import pytest
from src.exceptions.user_exceptions import UserValidationError, UserNotFoundError, SameEmailError
from src.constants import messages


def test_create_user_service(user_service, sample_user_data_2):
    user = user_service.create_user(**sample_user_data_2)
    assert user.username == sample_user_data_2["username"]
    assert user.email == sample_user_data_2["email"]
    assert user.password != sample_user_data_2["password"]

@pytest.mark.parametrize(
        "username, email, password, expected_exception",[
            ("", "jhon@correo", "passsupersecret!", messages.USER_INVALID_USERNAME),
            ("Jhon", "jhoncorreo", "passsupersecret!", messages.USER_INVALID_EMAIL),
            ("Jhon", "jhon@correo", "paset", messages.USER_INVALID_PASSWORD)
        ], 
        ids = lambda val: ""
)
def test_create_user_with_invalid_field(user_service, username, email, password, expected_exception):
    with pytest.raises(UserValidationError, match = expected_exception):
        user_service.create_user(username, email, password)

def test_create_user_with_existing_username(user_service, sample_user_data_1):
    user_service.create_user(**sample_user_data_1)
    with pytest.raises(UserValidationError, match = messages.USER_ALREADY_EXISTS):
        user_service.create_user(**sample_user_data_1)

"""def test_create_user_with_existing_email():
    service = UserService()
    service.create_user("Jhon", "jhon@correo.com", "passsupersecret!")
    with pytest.raises(UserValidationError):
        service.create_user("Jhon2", "jhon@correo.com", "passsecret!")"""

#---------------------test_get_user------------------

def test_get_existing_user(user_service, sample_user_data_1):
    user_service.create_user(**sample_user_data_1)
    user = user_service.get_user(sample_user_data_1["username"])
    assert user.username == sample_user_data_1["username"]
    assert user.email == sample_user_data_1["email"]

def test_get_unexistent_user(user_service):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_service.get_user("axel")

#--------------------test_update_user----------------

def test_update_email_success(user_service, sample_user_data_2):
    user_service.create_user(**sample_user_data_2)
    result = user_service.update_email(sample_user_data_2["username"], "newemail@correo.com")
    assert result["username"] == sample_user_data_2["username"]
    assert result["email"] == "newemail@correo.com"
    assert user_service.get_user("juan").email == "newemail@correo.com"

def test_update_email_same_as_current(user_service, sample_user_data_1):
    user_service.create_user(**sample_user_data_1)
    with pytest.raises(SameEmailError, match=messages.SAME_EMAIL):
        user_service.update_email(sample_user_data_1["username"], "xion@correo.com")

#--------------------test_delete_user----------------

def test_delete_user_success(user_service, sample_user_data_1):
    user_service.create_user(**sample_user_data_1)
    assert user_service.delete_user(sample_user_data_1["username"]) is None
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_service.get_user(sample_user_data_1["username"])

def test_delete_nonexistent_user(user_service):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_service.delete_user("iamnothere")

#--------------------test_get_all_users----------------

def test_get_all_users(user_service, sample_user_data_1,sample_user_data_2):
    user_service.create_user(**sample_user_data_1)
    user_service.create_user(**sample_user_data_2)
    all_users = user_service.get_all_users()
    assert len(all_users) == 2
    assert all_users[0].username == sample_user_data_1["username"]
    assert all_users[1].username == sample_user_data_2["username"]

def test_get_all_without_users(user_service):
    all_users = user_service.get_all_users()
    assert all_users == []
    assert len(all_users) == 0