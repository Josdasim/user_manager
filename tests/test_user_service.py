import pytest
from src.exceptions.user_exceptions import UserValidationError, UserNotFoundError, SameEmailError
from src.constants import messages
from src.security.password_utils import verify_password
from src.models.user_status import UserStatus


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
    user_service.create_user(sample_user_data_1["username"],"tomax@correo.com", "tompax1")
    with pytest.raises(UserValidationError, match = messages.USER_ALREADY_EXISTS):
        user_service.create_user(**sample_user_data_1)

def test_create_user_with_duplicate_email(user_service):
    user_service.create_user("juanito_nieves", "jon@correo.com", "pass123")
    with pytest.raises(UserValidationError, match=messages.EMAIL_ALREADY_REGISTERED):
        user_service.create_user("jon_el_nieves", "jon@correo.com", "pass456")

#--------------------- GET USER ------------------

def test_get_existing_user(user_service, sample_user_data_1):
    user_service.create_user(**sample_user_data_1)
    user = user_service.get_user(sample_user_data_1["username"])
    assert user.username == sample_user_data_1["username"]
    assert user.email == sample_user_data_1["email"]

def test_get_unexistent_user(user_service):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_service.get_user("axel")

# -------------------- GET USER BY EMAIL --------------------

def test_get_user_by_email_success(user_service, sample_user_data_1):
    user_service.create_user(**sample_user_data_1)
    user = user_service.get_user_by_email(sample_user_data_1["email"])
    assert user is not None
    assert user.username == sample_user_data_1["username"]
    assert user.email == sample_user_data_1["email"]

def test_get_user_by_email_not_found(user_service):
    user = user_service.get_user_by_email("notexist@correo.com")
    assert user is None

#-------------------- UPDATE EMAIL ----------------

def test_update_email_success(user_service, sample_user_data_2):
    user_service.create_user(**sample_user_data_2)
    result = user_service.update_email(sample_user_data_2["username"], "newemail@correo.com")
    assert result["username"] == sample_user_data_2["username"]
    assert result["email"] == "newemail@correo.com"

def test_update_email_same_as_current(user_service, sample_user_data_1):
    user_service.create_user(**sample_user_data_1)
    with pytest.raises(SameEmailError, match=messages.SAME_EMAIL):
        user_service.update_email(sample_user_data_1["username"], "xion@correo.com")


# -------------------- UPDATE USERNAME --------------------

def test_update_username_success(user_service, sample_user_data_2):
    user_service.create_user(**sample_user_data_2)
    old_username = sample_user_data_2["username"]
    updated_user = user_service.update_username(old_username, "huan")
    assert updated_user.username == "huan"
    with pytest.raises(UserNotFoundError):
        user_service.get_user(old_username)  
    user = user_service.get_user("huan")
    assert user.username == "huan"


def test_update_username_same_as_current(user_service, sample_user_data_1):
    user_service.create_user(**sample_user_data_1) 
    with pytest.raises(UserValidationError, match=messages.SAME_USERNAME):
        user_service.update_username(sample_user_data_1["username"],sample_user_data_1["username"])

def test_update_username_already_exists(user_service,sample_user_data_1,sample_user_data_2):
    user_service.create_user(**sample_user_data_2)
    user_service.create_user(**sample_user_data_1)
    with pytest.raises(UserValidationError, match=messages.USER_ALREADY_EXISTS):
        user_service.update_username(sample_user_data_2["username"], sample_user_data_1["username"])

def test_update_username_nonexistent_user(user_service):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_service.update_username("notexist", "newname")


# -------------------- UPDATE EMAIL WITH VALIDATION --------------------

def test_update_email_with_duplicate_email(user_service,sample_user_data_1,sample_user_data_2):
    user_service.create_user(**sample_user_data_1)
    user_service.create_user(**sample_user_data_2)
    with pytest.raises(UserValidationError, match=messages.EMAIL_ALREADY_REGISTERED):
        user_service.update_email(sample_user_data_1["username"], sample_user_data_2["email"])


# -------------------- UPDATE PASSWORD --------------------

def test_update_password_success(user_service, sample_user_data_1):
    user_service.create_user(**sample_user_data_1)
    updated_user = user_service.update_password(sample_user_data_1["username"], sample_user_data_1["password"], "newpass456")
    assert updated_user.username == sample_user_data_1["username"]
    assert verify_password("newpass456", updated_user.password)
    assert not verify_password(sample_user_data_1["password"], updated_user.password)

def test_update_password_wrong_current_password(user_service, sample_user_data_2):
    user_service.create_user(**sample_user_data_2)
    with pytest.raises(UserValidationError, match=messages.WRONG_PASSWORD):
        user_service.update_password(sample_user_data_2["username"], "wrongpass", "newpass456")

def test_update_password_invalid_new_password(user_service,sample_user_data_1):
    user_service.create_user(**sample_user_data_1)
    with pytest.raises(UserValidationError, match=messages.USER_INVALID_PASSWORD):
        user_service.update_password(sample_user_data_1["username"], sample_user_data_1["password"], "nes56")

def test_update_password_nonexistent_user(user_service):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_service.update_password("notexist", "oldpass", "newpass123")


#-------------------- DELETE USER ----------------

def test_delete_user_success(user_service, sample_user_data_1):
    user_service.create_user(**sample_user_data_1)
    assert user_service.delete_user(sample_user_data_1["username"]) is None
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_service.get_user(sample_user_data_1["username"])

def test_delete_nonexistent_user(user_service):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_service.delete_user("iamnothere")

#-------------------- GET ALL USERS ----------------

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


# -------------------- ACTIVATE USER --------------------

def test_activate_user_success(user_service, sample_user_data_2):
    user_service.create_user(**sample_user_data_2)
    activated_user = user_service.activate_user(sample_user_data_2["username"])
    assert activated_user.status == UserStatus.ACTIVE
    assert activated_user.is_active() is True

def test_activate_nonexistent_user(user_service):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_service.activate_user("notexist")


# -------------------- DEACTIVATE USER --------------------

def test_deactivate_user_success(user_service, sample_user_data_1):
    user_service.create_user(**sample_user_data_1)
    user_service.activate_user(sample_user_data_1["username"])
    deactivated_user = user_service.deactivate_user(sample_user_data_1["username"])
    assert deactivated_user.status == UserStatus.INACTIVE
    assert deactivated_user.is_active() is False

def test_deactivate_nonexistent_user(user_service):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_service.deactivate_user("notexist")


# -------------------- SUSPEND USER --------------------

def test_suspend_user_success(user_service, sample_user_data_2):
    user_service.create_user(**sample_user_data_2)
    suspended_user = user_service.suspend_user(sample_user_data_2["username"])
    assert suspended_user.status == UserStatus.SUSPENDED
    assert suspended_user.is_active() is False

def test_suspend_nonexistent_user(user_service):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_service.suspend_user("notexist")


# -------------------- BLOCK USER --------------------

def test_block_user_success(user_service, sample_user_data_1):
    user_service.create_user(**sample_user_data_1)   
    blocked_user = user_service.block_user(sample_user_data_1["username"])   
    assert blocked_user.status == UserStatus.BLOCKED
    assert blocked_user.is_active() is False

def test_block_nonexistent_user(user_service):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_service.block_user("notexist")


# -------------------- VERIFY PASSWORD --------------------

def test_verify_user_password_correct(user_service, sample_user_data_2):
    user_service.create_user(**sample_user_data_2)
    result = user_service.verify_user_password(sample_user_data_2["username"], sample_user_data_2["password"])   
    assert result is True

def test_verify_user_password_incorrect(user_service,sample_user_data_1):
    user_service.create_user(**sample_user_data_1)
    result = user_service.verify_user_password(sample_user_data_1["username"], "wrongpass")
    assert result is False

def test_verify_password_nonexistent_user(user_service):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_service.verify_user_password("notexist", "anypass")


# -------------------- STATUS WORKFLOW --------------------

def test_user_status_workflow(user_service):
    """Test completo del ciclo de vida de estados de un usuario"""
    user_service.create_user("chris", "chris@correo.com", "pass123")
    
    # Usuario inicia inactivo
    user = user_service.get_user("chris")
    assert user.status == UserStatus.INACTIVE
    
    # Activar usuario
    user_service.activate_user("chris")
    user = user_service.get_user("chris")
    assert user.status == UserStatus.ACTIVE
    
    # Suspender usuario
    user_service.suspend_user("chris")
    user = user_service.get_user("chris")
    assert user.status == UserStatus.SUSPENDED
    
    # Reactivar usuario
    user_service.activate_user("chris")
    user = user_service.get_user("chris")
    assert user.status == UserStatus.ACTIVE
    
    # Bloquear usuario
    user_service.block_user("chris")
    user = user_service.get_user("chris")
    assert user.status == UserStatus.BLOCKED