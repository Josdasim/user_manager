import pytest
from src.exceptions.user_exceptions import UserValidationError, UserNotFoundError
from src.constants import messages


#---------------------ADD/GET---------------------

def test_add_and_get_user(repo, sample_user_1):
    repo.add(sample_user_1)
    repo_retrieved = repo.get("Tomas")

    assert repo_retrieved.username == sample_user_1.username
    assert repo_retrieved.email == sample_user_1.email

def test_add_existing_user(repo, sample_user_2):
    repo.add(sample_user_2)
    with pytest.raises(UserValidationError, match = messages.USER_ALREADY_EXISTS):
        repo.add(sample_user_2)
    
def test_get_nonexistent_user(repo):
    with pytest.raises(UserNotFoundError, match = messages.USER_NOT_FOUND):
        repo.get("Unknown")

#---------------------FIND---------------------

def test_find_user(repo, sample_user_3):
    repo.add(sample_user_3)
    assert repo.find("Axel") == sample_user_3

def test_user_not_found(repo):
    assert repo.find("amiexist?") is None

#--------------------UPDATE---------------------

def test_update_existing_user(repo, sample_user_3):
    repo.add(sample_user_3)
    user_updated = repo.update_email(sample_user_3.username, "newaxel@correo.com")
    assert repo.get(sample_user_3.username).email == "newaxel@correo.com"

def test_update_nonexistent_user(repo):
    with pytest.raises(UserNotFoundError, match = messages.USER_NOT_FOUND):
        repo.update_email("no_estoy", "correo@correo.com")
    
#--------------------DELETE-------------------

def test_delete_exisiting_user(repo, sample_user_3):
    repo.add(sample_user_3)
    assert repo.get(sample_user_3.username) is not None 

    repo.delete("Axel")
    assert repo.find("Axel") is None

def test_delete_nonexistent_user(repo):
    with pytest.raises(UserNotFoundError, match = messages.USER_NOT_FOUND):
        repo.delete("nonexistent")

#--------------------GET ALL-------------------

def test_get_all_users(repo, sample_user_2, sample_user_3):
    repo.add(sample_user_2)
    repo.add(sample_user_3)
    all_users = repo.get_all()
    assert len(repo._data) == 2
    assert len(all_users) == 2
    assert all_users[0].username == sample_user_2.username
    assert all_users[1].username == sample_user_3.username

def test_get_all_without_users(repo):
    all_users = repo.get_all()
    assert all_users == []
    assert len(all_users) == 0
