import pytest
from src.models.user_role import UserRole


#---------------------ADD/GET---------------------

def test_add_new_relation(user_role_repo):
    relation = UserRole(user_id="u1",role_id="r1")
    user_role_repo.add(relation)
    new_relation = user_role_repo.find("u1","r1")
    assert new_relation.user_id == "u1"
    assert new_relation.role_id == "r1"

def test_add_existing_relation(user_role_repo):
    relation = UserRole(user_id="u1",role_id="r1")
    user_role_repo.add(relation)
    with pytest.raises(ValueError):
        user_role_repo.add(relation)

def test_get_roles_by_user(user_role_repo, sample_user1_role1_data, sample_user1_role2_data, sample_user2_role1_data):
    user_role_repo.add(UserRole(**sample_user1_role1_data))
    user_role_repo.add(UserRole(**sample_user2_role1_data))
    user_role_repo.add(UserRole(**sample_user1_role2_data))
    list_roles = user_role_repo.get_roles_by_user("u1")
    assert len(list_roles) == 2
    assert list_roles[0].user_id == "u1"
    assert list_roles[0].role_id == "r1"
    assert list_roles[1].user_id == "u1"
    assert list_roles[1].role_id == "r2"


def test_get_roles_by_nonexistent_user(user_role_repo):
    list_roles = user_role_repo.get_roles_by_user("u1")
    assert list_roles == []

#---------------------FIND---------------------

def test_find_user_role_relation(user_role_repo, sample_user1_role1_data):
    user_role_repo.add(UserRole(**sample_user1_role1_data))
    relation = user_role_repo.find("u1","r1")
    assert isinstance(relation, UserRole)
    assert relation.user_id == "u1"
    assert relation.role_id == "r1"
def test_find_nonexistent_user_role_relation(user_role_repo):
    relation = user_role_repo.find("u1","r1")
    assert relation is None

