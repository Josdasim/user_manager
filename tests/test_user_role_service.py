import pytest
from src.models.user_role import UserRole


# -------------------- ASSIGN ROLE TO USER --------------------

def test_assign_role_success(user_role_service, sample_user1_role1_data):
    relation = user_role_service.assign_role(**sample_user1_role1_data)
    assert isinstance(relation, UserRole)
    assert relation.user_id == sample_user1_role1_data["user_id"]
    assert relation.role_id == sample_user1_role1_data["role_id"]

def test_assign_existing_role_raises_error(user_role_service, sample_user2_role1_data):
    user_role_service.assign_role(**sample_user2_role1_data)
    with pytest.raises(ValueError):
        user_role_service.assign_role(**sample_user2_role1_data)

def test_assign_role_without_user_id(user_role_service):
    with pytest.raises(ValueError):
        user_role_service.assign_role("", "role456")


def test_assign_role_without_role_id(user_role_service):
    with pytest.raises(ValueError):
        user_role_service.assign_role("user123", "")

def test_assign_multiple_roles_to_user(user_role_service, sample_user1_role1_data,sample_user1_role2_data):
    user_role_service.assign_role(**sample_user1_role1_data)
    user_role_service.assign_role(**sample_user1_role2_data)
    user_roles = user_role_service.get_user_roles("u1")
    assert len(user_roles) == 2

# -------------------- GET USER ROLES --------------------

def test_get_user_roles_success(user_role_service,sample_user1_role1_data,sample_user1_role2_data,sample_user2_role1_data):
    user_role_service.assign_role(**sample_user1_role1_data)
    user_role_service.assign_role(**sample_user1_role2_data)
    user_role_service.assign_role(**sample_user2_role1_data)
    user_roles = user_role_service.get_user_roles("u1")
    assert len(user_roles) == 2
    assert all(relation.user_id == "u1" for relation in user_roles)

def test_get_user_roles_empty(user_role_service):
    roles = user_role_service.get_user_roles("user_without_roles")
    assert roles == []

def test_get_user_roles_without_user_id(user_role_service):
    with pytest.raises(ValueError):
        user_role_service.get_user_roles("")

# -------------------- GET USERS BY ROLE --------------------

def test_get_users_by_role_success(user_role_service,sample_user1_role1_data,sample_user1_role2_data,sample_user2_role1_data):
    user_role_service.assign_role(**sample_user1_role1_data)
    user_role_service.assign_role(**sample_user1_role2_data)
    user_role_service.assign_role(**sample_user2_role1_data) 
    users = user_role_service.get_users_by_role("r1")   
    assert len(users) == 2
    assert all(relation.role_id == "r1" for relation in users)

def test_get_users_by_role_empty(user_role_service):
    users = user_role_service.get_users_by_role("role_without_users")   
    assert users == []

def test_get_users_by_role_without_role_id(user_role_service):
    with pytest.raises(ValueError):
        user_role_service.get_users_by_role("")


# -------------------- GET ALL RELATIONS --------------------

def test_get_all_relations_success(user_role_service, sample_user1_role1_data,sample_user1_role2_data,sample_user2_role1_data):
    user_role_service.assign_role(**sample_user1_role1_data)
    user_role_service.assign_role(**sample_user1_role2_data)
    user_role_service.assign_role(**sample_user2_role1_data)   
    all_relations = user_role_service.get_all_relations()   
    assert len(all_relations) == 3


def test_get_all_relations_empty(user_role_service):
    all_relations = user_role_service.get_all_relations()   
    assert all_relations == []


# -------------------- UPDATE USER ROLE --------------------

def test_update_user_role_success(user_role_service, sample_user1_role1_data):
    user_role_service.assign_role(**sample_user1_role1_data)   
    updated = user_role_service.update_user_role("u1","r1", "admin")
    assert updated.user_id == "u1"
    assert updated.role_id == "admin"

def test_update_nonexistent_relation_raises_error(user_role_service):
    with pytest.raises(ValueError):
        user_role_service.update_user_role("user123", "role1", "role2")


def test_update_user_role_without_parameters(user_role_service):
    with pytest.raises(ValueError):
        user_role_service.update_user_role("", "role1", "role2")


# -------------------- USER HAS ROLE --------------------

def test_user_has_role_returns_true(user_role_service,sample_user2_role1_data):
    user_role_service.assign_role(**sample_user2_role1_data)
    result = user_role_service.user_has_role(**sample_user2_role1_data)
    assert result is True


def test_user_has_role_returns_false(user_role_service):
    result = user_role_service.user_has_role("user123", "admin")
    assert result is False


def test_user_has_role_without_user_id(user_role_service):
    result = user_role_service.user_has_role("", "admin")
    assert result is False


def test_user_has_role_without_role_id(user_role_service):
    result = user_role_service.user_has_role("user123", "")
    assert result is False


def test_user_has_role_after_removal(user_role_service,sample_user1_role1_data):
    user_role_service.assign_role(**sample_user1_role1_data)
    assert user_role_service.user_has_role(**sample_user1_role1_data) is True
    
    user_role_service.remove_role(**sample_user1_role1_data)
    assert user_role_service.user_has_role(**sample_user1_role1_data) is False

# -------------------- REMOVE ROLE FROM USER --------------------

def test_remove_role_success(user_role_service, sample_user2_role2_data):
    user_role_service.assign_role(**sample_user2_role2_data)
    user_role_service.remove_role(**sample_user2_role2_data)
    roles = user_role_service.get_user_roles("u2")
    assert len(roles) == 0


def test_remove_nonexistent_role_raises_error(user_role_service,sample_user1_role2_data):
    with pytest.raises(ValueError):
        user_role_service.remove_role(**sample_user1_role2_data)


def test_remove_role_without_user_id(user_role_service):
    with pytest.raises(ValueError) as excinfo:
        user_role_service.remove_role("", "role456")
    assert "requeridos" in str(excinfo.value)


def test_remove_role_without_role_id(user_role_service):
    with pytest.raises(ValueError) as excinfo:
        user_role_service.remove_role("user123", "")
    assert "requeridos" in str(excinfo.value)

# -------------------- INTEGRATION TESTS --------------------

def test_complete_user_role_workflow(user_role_service):
    """Test del flujo completo de gestión de roles de usuario"""
    # Asignar múltiples roles a un usuario
    user_role_service.assign_role("john", "admin")
    user_role_service.assign_role("john", "editor")
    user_role_service.assign_role("john", "viewer")
    
    # Verificar roles del usuario
    john_roles = user_role_service.get_user_roles("john")
    assert len(john_roles) == 3
    
    # Verificar si tiene un rol específico
    assert user_role_service.user_has_role("john", "admin") is True
    assert user_role_service.user_has_role("john", "superadmin") is False
    
    # Actualizar un rol
    user_role_service.update_user_role("john", "viewer", "moderator")
    assert user_role_service.user_has_role("john", "moderator") is True
    assert user_role_service.user_has_role("john", "viewer") is False
    
    # Remover un rol
    user_role_service.remove_role("john", "editor")
    john_roles = user_role_service.get_user_roles("john")
    assert len(john_roles) == 2
    
    # Verificar todos los usuarios con rol admin
    user_role_service.assign_role("jane", "admin")
    admins = user_role_service.get_users_by_role("admin")
    assert len(admins) == 2


def test_multiple_users_same_role(user_role_service):
    """Test de múltiples usuarios con el mismo rol"""
    users = ["user1", "user2", "user3", "user4", "user5"]
    
    for user in users:
        user_role_service.assign_role(user, "member")
    
    members = user_role_service.get_users_by_role("member")
    assert len(members) == 5
    
    # Remover uno
    user_role_service.remove_role("user3", "member")
    members = user_role_service.get_users_by_role("member")
    assert len(members) == 4


def test_user_with_multiple_roles_management(user_role_service):
    """Test de gestión de usuario con múltiples roles"""
    roles = ["admin", "editor", "moderator", "viewer", "contributor"]
    
    for role in roles:
        user_role_service.assign_role("power_user", role)
    
    user_roles = user_role_service.get_user_roles("power_user")
    assert len(user_roles) == 5
    
    # Verificar cada rol
    for role in roles:
        assert user_role_service.user_has_role("power_user", role) is True
    
    # Remover todos los roles
    for role in roles:
        user_role_service.remove_role("power_user", role)
    user_roles = user_role_service.get_user_roles("power_user")
    assert len(user_roles) == 0