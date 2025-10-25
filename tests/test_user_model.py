import pytest
from src.models.user import User
from src.exceptions.user_exceptions import UserValidationError
from src.constants import messages
from src.models.user_status import UserStatus


# -------------------- CREATE USER --------------------

def test_create_user_with_correct_attributes(sample_user_data_1):
    new_user=User(**sample_user_data_1)
    assert new_user.username == sample_user_data_1["username"]
    assert new_user.email == sample_user_data_1["email"]
    assert new_user.password == sample_user_data_1["password"]

@pytest.mark.parametrize(
        "username, email, password, expected_exception",[
            ("", "tomas01@correo.com", "secret01", messages.USER_INVALID_USERNAME),
            ("Tomas", "email_invalido", "secret01", messages.USER_INVALID_EMAIL)
        ],
        ids = lambda val: ""
)
def test_create_user_with_invalid_fields(username, email, password, expected_exception):
    with pytest.raises(UserValidationError, match=expected_exception):
        User(username, email, password)

# -------------------- UPDATE USERNAME --------------------

def test_update_username_success(sample_user_1):
    old_updated_at = sample_user_1.updated_at
    sample_user_1.update_username("tomax")
    assert sample_user_1.username == "tomax"
    assert sample_user_1.updated_at > old_updated_at

def test_update_username_with_empty_name(sample_user_2):
    with pytest.raises(UserValidationError, match=messages.USER_INVALID_USERNAME):
        sample_user_2.update_username("")
    
def test_update_username_with_empty_name(sample_user_3):
    with pytest.raises(UserValidationError, match=messages.USER_INVALID_USERNAME):
        sample_user_3.update_username("  ")

# -------------------- UPDATE EMAIL --------------------

def test_update_email_success(sample_user_1):
    old_updated_at = sample_user_1.updated_at
    sample_user_1.update_email("tomax@correo.com")
    assert sample_user_1.email == "tomax@correo.com"
    assert sample_user_1.updated_at > old_updated_at

def test_update_email_with_invalid_email(sample_user_2):
    with pytest.raises(UserValidationError, match=messages.USER_INVALID_EMAIL):
        sample_user_2.update_email("invalid-email")

# -------------------- UPDATE PASSWORD --------------------

def test_update_password_success(sample_user_3):
    old_password = sample_user_3.password
    old_updated_at = sample_user_3.updated_at
    sample_user_3.update_password("newpaxal")
    assert sample_user_3.password == "newpaxal"
    assert sample_user_3.password != old_password
    assert sample_user_3.updated_at > old_updated_at

def test_update_password_with_empty_password(sample_user_1):
    with pytest.raises(UserValidationError, match=messages.USER_INVALID_PASSWORD):
        sample_user_1.update_password("")

# -------------------- USER STATUS CHANGES --------------------

def test_activate_user(sample_user_2):
    assert sample_user_2.status == UserStatus.INACTIVE
    sample_user_2.activate()
    assert sample_user_2.status == UserStatus.ACTIVE
    assert sample_user_2.is_active() is True

def test_deactivate_user(sample_user_data_1):
    user = User(**sample_user_data_1, status = UserStatus.ACTIVE)
    assert user.status == UserStatus.ACTIVE
    user.deactivate()
    assert user.status == UserStatus.INACTIVE
    assert user.is_active() is False

def test_suspend_user(sample_user_data_2):
    user = User(**sample_user_data_2, status=UserStatus.ACTIVE)
    user.suspend()
    assert user.status == UserStatus.SUSPENDED
    assert user.is_active() is False

def test_block_user(sample_user_data_1):
    user = User(**sample_user_data_1, status=UserStatus.ACTIVE)
    user.block()
    assert user.status == UserStatus.BLOCKED
    assert user.is_active() is False

def test_is_active_returns_false_for_inactivate_user(sample_user_1):
    assert sample_user_1.status == UserStatus.INACTIVE
    assert sample_user_1.is_active() is False

def test_is_active_returns_false_for_suspended_user(sample_user_data_1):
    user = User(**sample_user_data_1, status=UserStatus.SUSPENDED)
    assert user.is_active() is False

def test_is_active_returns_false_for_blocked_user(sample_user_data_2):
    user = User(**sample_user_data_2, status=UserStatus.BLOCKED)
    assert user.is_active() is False

def test_status_changes_update_timestamp(sample_user_2):
    old_updated_at = sample_user_2.updated_at
    sample_user_2.activate()
    assert sample_user_2.updated_at > old_updated_at

    old_updated_at = sample_user_2.updated_at
    sample_user_2.block()
    assert sample_user_2.updated_at > old_updated_at

# -------------------- USER ROLES --------------------

def test_user_has_roles_list(sample_user_3):
    assert hasattr(sample_user_3, 'roles')
    assert isinstance(sample_user_3.roles, list)
    assert len(sample_user_3.roles) == 0
