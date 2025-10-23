import pytest
from src.models.role_permission import RolePermission






# --------------------- ADD ---------------------

def test_add_new_relation(role_permission_service):
    relation = role_permission_service.add_permission_to_role("r1", "p1")
    assert isinstance(relation, RolePermission)
    assert relation.role_id == "r1"
    assert relation.permission_id == "p1"


def test_add_existing_relation(role_permission_service):
    role_permission_service.add_permission_to_role("r1", "p1")
    with pytest.raises(ValueError):
        role_permission_service.add_permission_to_role("r1", "p1")


def test_add_invalid_relation(role_permission_service):
    with pytest.raises(ValueError):
        role_permission_service.add_permission_to_role("", "p1")
    with pytest.raises(ValueError):
        role_permission_service.add_permission_to_role("r1", "")


# --------------------- GET ---------------------

def test_get_all_relations(role_permission_service, sample_role1_perm1_data, sample_role2_perm2_data):
    role_permission_service.add_permission_to_role(**sample_role1_perm1_data)
    role_permission_service.add_permission_to_role(**sample_role2_perm2_data)
    all_relations = role_permission_service.get_all_relations()
    assert len(all_relations) == 2


def test_get_permissions_by_role(role_permission_service, sample_role1_perm1_data, sample_role1_perm2_data, sample_role2_perm1_data):
    role_permission_service.add_permission_to_role(**sample_role1_perm1_data)
    role_permission_service.add_permission_to_role(**sample_role1_perm2_data)
    role_permission_service.add_permission_to_role(**sample_role2_perm1_data)
    result = role_permission_service.get_permissions_by_role("r1")
    assert len(result) == 2
    assert all(rel.role_id == "r1" for rel in result)


def test_get_permissions_by_nonexistent_role(role_permission_service):
    result = role_permission_service.get_permissions_by_role("rX")
    assert result == []


def test_get_roles_by_permission(role_permission_service, sample_role1_perm1_data, sample_role2_perm1_data):
    role_permission_service.add_permission_to_role(**sample_role1_perm1_data)
    role_permission_service.add_permission_to_role(**sample_role2_perm1_data)
    result = role_permission_service.get_roles_by_permission("p1")
    assert len(result) == 2
    assert all(rel.permission_id == "p1" for rel in result)


def test_get_roles_by_nonexistent_permission(role_permission_service):
    result = role_permission_service.get_roles_by_permission("pX")
    assert result == []


# --------------------- UPDATE ---------------------

def test_update_permission_relation(role_permission_service):
    role_permission_service.add_permission_to_role("r1", "p1")
    updated = role_permission_service.update_permission_relation("r1", "p1", "p9")
    assert updated.role_id == "r1"
    assert updated.permission_id == "p9"


def test_update_nonexistent_relation(role_permission_service):
    with pytest.raises(ValueError):
        role_permission_service.update_permission_relation("r1", "p1", "p2")


# --------------------- DELETE ---------------------

def test_delete_relation(role_permission_service, sample_role1_perm1_data, sample_role2_perm2_data):
    role_permission_service.add_permission_to_role(**sample_role1_perm1_data)
    role_permission_service.add_permission_to_role(**sample_role2_perm2_data)
    all_before = role_permission_service.get_all_relations()
    assert len(all_before) == 2
    role_permission_service.remove_permission_from_role("r1", "p1")
    all_after = role_permission_service.get_all_relations()
    assert len(all_after) == 1


def test_delete_nonexistent_relation(role_permission_service):
    with pytest.raises(ValueError):
        role_permission_service.remove_permission_from_role("rX", "pX")
