import pytest
from src.models.role_permission import RolePermission


#---------------------ADD/GET---------------------

def test_add_new_relation(role_permission_repo):
    relation = RolePermission(role_id="r1", permission_id="p1")
    role_permission_repo.add(relation)
    new_relation = role_permission_repo.find("r1", "p1")
    assert new_relation.role_id == "r1"
    assert new_relation.permission_id == "p1"

def test_add_existing_relation(role_permission_repo):
    relation = RolePermission(role_id="r1", permission_id="p1")
    role_permission_repo.add(relation)
    with pytest.raises(ValueError):
        role_permission_repo.add(relation)

def test_get_all_relations(role_permission_repo, sample_role1_perm1_data, sample_role2_perm2_data):
    role_permission_repo.add(RolePermission(**sample_role1_perm1_data))
    role_permission_repo.add(RolePermission(**sample_role2_perm2_data))
    all_relations = role_permission_repo.get_all()
    assert len(all_relations) == 2
    

def test_get_permissions_by_role(role_permission_repo, sample_role1_perm1_data, sample_role1_perm2_data, sample_role2_perm1_data):
    role_permission_repo.add(RolePermission(**sample_role1_perm1_data))
    role_permission_repo.add(RolePermission(**sample_role2_perm1_data))
    role_permission_repo.add(RolePermission(**sample_role1_perm2_data))
    list_permissions = role_permission_repo.get_permissions_by_role("r1")
    assert len(list_permissions) == 2
    assert list_permissions[0].role_id == "r1"
    assert list_permissions[0].permission_id == "p1"
    assert list_permissions[1].role_id == "r1"
    assert list_permissions[1].permission_id == "p2"


def test_get_permissions_by_nonexistent_role(role_permission_repo):
    list_permissions = role_permission_repo.get_permissions_by_role("r1")
    assert list_permissions == []

def test_get_roles_by_permission(role_permission_repo, sample_role1_perm1_data, sample_role1_perm2_data, sample_role2_perm1_data):
    role_permission_repo.add(RolePermission(**sample_role1_perm1_data))
    role_permission_repo.add(RolePermission(**sample_role2_perm1_data))
    role_permission_repo.add(RolePermission(**sample_role1_perm2_data))
    list_roles = role_permission_repo.get_roles_by_permission("p1")
    assert len(list_roles) == 2
    assert list_roles[0].permission_id == "p1"
    assert list_roles[0].role_id == "r1"
    assert list_roles[1].role_id == "r2"
    assert list_roles[1].permission_id == "p1"


def test_get_roles_by_nonexistent_permission(role_permission_repo):
    list_roles = role_permission_repo.get_roles_by_permission("p1")
    assert list_roles == []

#---------------------FIND---------------------

def test_find_role_permission_relation(role_permission_repo, sample_role1_perm1_data):
    role_permission_repo.add(RolePermission(**sample_role1_perm1_data))
    relation = role_permission_repo.find("r1", "p1")
    assert isinstance(relation, RolePermission)
    assert relation.role_id == "r1"
    assert relation.permission_id == "p1"

def test_find_nonexistent_role_permission_relation(role_permission_repo):
    relation = role_permission_repo.find("r1", "p1")
    assert relation is None

#---------------------Update---------------------

def test_update_role_permission_relation(role_permission_repo):
    role_permission_repo.add(RolePermission(role_id="r3", permission_id="p3"))
    relation_updated = role_permission_repo.update_permission_relation("r3", "p3", "p5")
    assert relation_updated.role_id == "r3"
    assert relation_updated.permission_id == "p5"

#---------------------Delete---------------------

def test_delete(role_permission_repo, sample_role1_perm1_data, sample_role2_perm2_data):
    role_permission_repo.add(RolePermission(**sample_role1_perm1_data))
    role_permission_repo.add(RolePermission(**sample_role2_perm2_data))
    list_relations = role_permission_repo.get_all()
    assert len(list_relations) == 2
    role_permission_repo.delete("r1", "p1")
    assert len(list_relations) == 1
