from src.models.user_role import UserRole

def test_create_user_role_success():
    relation = UserRole(user_id="user-1", role_id="role-1")
    assert relation.user_id == "user-1"
    assert relation.role_id == "role-1"
