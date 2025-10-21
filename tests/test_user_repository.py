import pytest
from src.exceptions.user_exceptions import UserValidationError, UserNotFoundError
from src.constants import messages


#---------------------ADD/GET---------------------

def test_add_and_get_user(user_repo, sample_user_1):
    user_repo.add(sample_user_1)
    repo_retrieved = user_repo.get("Tomas")

    assert repo_retrieved.username == sample_user_1.username
    assert repo_retrieved.email == sample_user_1.email

def test_add_existing_user(user_repo, sample_user_2):
    user_repo.add(sample_user_2)
    with pytest.raises(UserValidationError, match = messages.USER_ALREADY_EXISTS):
        user_repo.add(sample_user_2)
    
def test_get_nonexistent_user(user_repo):
    with pytest.raises(UserNotFoundError, match = messages.USER_NOT_FOUND):
        user_repo.get("Unknown")

#---------------------FIND---------------------

def test_find_user(user_repo, sample_user_3):
    user_repo.add(sample_user_3)
    assert user_repo.find("Axel") == sample_user_3

def test_user_not_found(user_repo):
    assert user_repo.find("amiexist?") is None

#--------------------UPDATE---------------------

def test_update_existing_user(user_repo, sample_user_3):
    user_repo.add(sample_user_3)
    user_updated = user_repo.update_email(sample_user_3.username, "newaxel@correo.com")
    assert user_repo.get(sample_user_3.username).email == "newaxel@correo.com"

def test_update_nonexistent_user(user_repo):
    with pytest.raises(UserNotFoundError, match = messages.USER_NOT_FOUND):
        user_repo.update_email("no_estoy", "correo@correo.com")
    
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
