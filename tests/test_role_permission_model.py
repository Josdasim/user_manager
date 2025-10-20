from src.models.role_permission import RolePermission


def test_create_role_permission_succes():
    relation = RolePermission(role_id="role-1", permission_id="perm-1")
    assert relation.role_id == "role-1"
    assert relation.permission_id == "perm-1"
