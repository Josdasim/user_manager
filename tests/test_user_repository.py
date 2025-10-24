import pytest
from src.exceptions.user_exceptions import UserValidationError, UserNotFoundError
from src.constants import messages
from src.models.user_status import UserStatus
from src.models.user import User


#---------------------ADD/GET---------------------

def test_add_and_get_user(user_repo, sample_user_1):
    user_repo.add(sample_user_1)
    repo_retrieved = user_repo.get(sample_user_1.username)
    assert isinstance(repo_retrieved, User)
    assert repo_retrieved.username == sample_user_1.username
    assert repo_retrieved.email == sample_user_1.email

def test_add_existing_user(user_repo, sample_user_2):
    user_repo.add(sample_user_2)
    with pytest.raises(UserValidationError, match = messages.USER_ALREADY_EXISTS):
        user_repo.add(sample_user_2)
    
def test_get_nonexistent_user(user_repo):
    with pytest.raises(UserNotFoundError, match = messages.USER_NOT_FOUND):
        user_repo.get("Unknown")


#---------------------FIND BY USERNAME---------------------

def test_find_user(user_repo, sample_user_3):
    user_repo.add(sample_user_3)
    assert user_repo.find("Axel") == sample_user_3

def test_user_not_found(user_repo):
    assert user_repo.find("amiexist?") is None

#---------------------FIND BY EMAIL---------------------

def test_find_by_email_success(user_repo, sample_user_2):
    user_repo.add(sample_user_2)
    found_user = user_repo.find_by_email(sample_user_2.email)
    assert found_user is not None
    assert found_user.username == sample_user_2.username
    assert found_user.email == sample_user_2.email

def test_find_by_email_not_found(user_repo):
    result = user_repo.find_by_email("correo@correo.com")
    assert result is None


#--------------------UPDATE---------------------

def test_update_existing_user(user_repo, sample_user_3):
    user_repo.add(sample_user_3)
    user_updated = user_repo.update_email(sample_user_3.username, "newaxel@correo.com")
    assert user_repo.get(sample_user_3.username).email == "newaxel@correo.com"

def test_update_nonexistent_user(user_repo):
    with pytest.raises(UserNotFoundError, match = messages.USER_NOT_FOUND):
        user_repo.update_email("no_estoy", "correo@correo.com")
    

#---------------------UPDATE USERNAME---------------------

def test_update_username_success(user_repo, sample_user_1):
    user_repo.add(sample_user_1)
    old_username = sample_user_1.username
    updated_user = user_repo.update_username(sample_user_1.username, "tutancamon")
    assert updated_user.username == "tutancamon"
    assert user_repo.find("tutancamon") is not None
    assert user_repo.find(old_username) is None

def test_update_username_nonexistent_user(user_repo):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_repo.update_username("notexist", "newname")

def test_update_username_preserves_other_data(user_repo, sample_user_2):
    user_repo.add(sample_user_2)
    original_email = sample_user_2.email
    original_password = sample_user_2.password  
    updated_user = user_repo.update_username(sample_user_2.username, "joe")
    assert updated_user.email == original_email
    assert updated_user.password == original_password


#---------------------UPDATE PASSWORD---------------------

def test_update_password_success(user_repo, sample_user_3):
    user_repo.add(sample_user_3)
    updated_user = user_repo.update_password(sample_user_3.username, "newpass456")
    assert updated_user.password == "newpass456"

def test_update_password_nonexistent_user(user_repo):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_repo.update_password("notexist", "newpass")


#--------------------DELETE-------------------

def test_delete_exisiting_user(user_repo, sample_user_3):
    user_repo.add(sample_user_3)
    assert user_repo.get(sample_user_3.username) is not None 

    user_repo.delete("Axel")
    assert user_repo.find("Axel") is None

def test_delete_nonexistent_user(user_repo):
    with pytest.raises(UserNotFoundError, match = messages.USER_NOT_FOUND):
        user_repo.delete("nonexistent")

#--------------------GET ALL-------------------

def test_get_all_users(user_repo, sample_user_2, sample_user_3):
    user_repo.add(sample_user_2)
    user_repo.add(sample_user_3)
    all_users = user_repo.get_all()
    assert len(user_repo._data) == 2
    assert len(all_users) == 2
    assert all_users[0].username == sample_user_2.username
    assert all_users[1].username == sample_user_3.username

def test_get_all_without_users(user_repo):
    all_users = user_repo.get_all()
    assert all_users == []
    assert len(all_users) == 0


# -------------------- UPDATE STATUS --------------------

def test_update_status_to_active(user_repo,sample_user_1):
    user_repo.add(sample_user_1)
    updated_user = user_repo.update_status(sample_user_1.username, UserStatus.ACTIVE)
    assert updated_user.status == UserStatus.ACTIVE

def test_update_status_to_inactive(user_repo,sample_user_data_1):
    user = User(**sample_user_data_1, status=UserStatus.ACTIVE)
    user_repo.add(user)
    updated_user = user_repo.update_status(sample_user_data_1["username"], UserStatus.INACTIVE)
    assert updated_user.status == UserStatus.INACTIVE

def test_update_status_to_suspended(user_repo, sample_user_1):
    user_repo.add(sample_user_1)
    updated_user = user_repo.update_status(sample_user_1.username, UserStatus.SUSPENDED)
    assert updated_user.status == UserStatus.SUSPENDED

def test_update_status_to_blocked(user_repo,sample_user_2):
    user_repo.add(sample_user_2)
    updated_user = user_repo.update_status(sample_user_2.username, UserStatus.BLOCKED)
    assert updated_user.status == UserStatus.BLOCKED

def test_update_status_nonexistent_user(user_repo):
    with pytest.raises(UserNotFoundError, match=messages.USER_NOT_FOUND):
        user_repo.update_status("notexist", UserStatus.ACTIVE)

def test_update_status_multiple_changes(user_repo, sample_user_3):
    user_repo.add(sample_user_3)
    user_repo.update_status(sample_user_3.username, UserStatus.ACTIVE)
    assert user_repo.get(sample_user_3.username).status == UserStatus.ACTIVE
    
    user_repo.update_status(sample_user_3.username, UserStatus.SUSPENDED)
    assert user_repo.get(sample_user_3.username).status == UserStatus.SUSPENDED
    
    user_repo.update_status(sample_user_3.username, UserStatus.BLOCKED)
    assert user_repo.get(sample_user_3.username).status == UserStatus.BLOCKED
