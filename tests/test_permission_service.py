import pytest
from src.models.permission import Permission
from src.constants import messages
from src.exceptions.permission_exceptions import PermissionAlreadyExistsError, PermissionNotFoundError


# -------------------- CREATE PERMISSION --------------------

def test_create_permission_success(permission_service):
    permission = permission_service.create_permission("create_user", "Puede crear usuarios")
    
    assert isinstance(permission, Permission)
    assert permission.name == "create_user"
    assert permission.description == "Puede crear usuarios"
    assert permission.id is not None


def test_create_permission_without_description(permission_service):
    permission = permission_service.create_permission("delete_user")
    
    assert permission.name == "delete_user"
    assert permission.description == ""


def test_create_permission_without_name_raises_error(permission_service):
    with pytest.raises(ValueError) as excinfo:
        permission_service.create_permission("", "Descripcion")
    assert "obligatorio" in str(excinfo.value)


def test_create_duplicate_permission_raises_error(permission_service):
    permission_service.create_permission("edit_user", "Editar usuario")
    with pytest.raises(PermissionAlreadyExistsError, match=messages.PERMISSION_ALREADY_EXISTS):
        permission_service.create_permission("edit_user", "Duplicado")


def test_create_permission_normalizes_name(permission_service):
    permission = permission_service.create_permission("  CREATE_USER  ", "Descripcion")
    assert permission.name == "create_user"


# -------------------- GET PERMISSION --------------------

def test_get_existing_permission(permission_service):
    permission_service.create_permission("view_user", "Ver usuarios")
    
    permission = permission_service.get_permission("view_user")
    
    assert permission.name == "view_user"
    assert permission.description == "Ver usuarios"


def test_get_nonexistent_permission_raises_error(permission_service):
    with pytest.raises(PermissionNotFoundError):
        permission_service.get_permission("no_existe")


def test_get_permission_without_name_raises_error(permission_service):
    with pytest.raises(ValueError) as excinfo:
        permission_service.get_permission("")
    assert "obligatorio" in str(excinfo.value)


def test_get_permission_case_insensitive(permission_service):
    permission_service.create_permission("delete_user", "Eliminar usuario")
    
    permission = permission_service.get_permission("DELETE_USER")
    
    assert permission.name == "delete_user"


# -------------------- GET ALL PERMISSIONS --------------------

def test_get_all_permissions(permission_service):
    permission_service.create_permission("create_user", "Crear")
    permission_service.create_permission("edit_user", "Editar")
    permission_service.create_permission("delete_user", "Eliminar")
    
    all_permissions = permission_service.get_all_permissions()
    
    assert len(all_permissions) == 3
    assert all(isinstance(p, Permission) for p in all_permissions)


def test_get_all_permissions_empty(permission_service):
    all_permissions = permission_service.get_all_permissions()
    
    assert all_permissions == []
    assert len(all_permissions) == 0


# -------------------- UPDATE PERMISSION DESCRIPTION --------------------

def test_update_permission_description(permission_service):
    permission_service.create_permission("update_user", "Descripcion inicial")
    
    updated_permission = permission_service.update_permission_description(
        "update_user", 
        "Nueva descripcion actualizada"
    )
    
    assert updated_permission.description == "Nueva descripcion actualizada"


def test_update_nonexistent_permission_raises_error(permission_service):
    with pytest.raises(PermissionNotFoundError):
        permission_service.update_permission_description("no_existe", "Nueva descripcion")


def test_update_permission_description_with_empty_name(permission_service):
    with pytest.raises(ValueError) as excinfo:
        permission_service.update_permission_description("", "Descripcion")
    assert "obligatorio" in str(excinfo.value)


def test_update_permission_description_with_none(permission_service):
    permission_service.create_permission("test_perm", "Inicial")
    
    with pytest.raises(ValueError) as excinfo:
        permission_service.update_permission_description("test_perm", None)
    assert "no puede ser nula" in str(excinfo.value)


def test_update_permission_description_to_empty_string(permission_service):
    permission_service.create_permission("test_perm", "Inicial")
    
    updated = permission_service.update_permission_description("test_perm", "")
    
    assert updated.description == ""


# -------------------- DELETE PERMISSION --------------------

def test_delete_permission(permission_service):
    permission_service.create_permission("temp_perm", "Temporal")
    
    permission_service.delete_permission("temp_perm")
    
    with pytest.raises(PermissionNotFoundError):
        permission_service.get_permission("temp_perm")


def test_delete_nonexistent_permission(permission_service):
    with pytest.raises(PermissionNotFoundError):
        permission_service.delete_permission("no_existe")


def test_delete_permission_without_name(permission_service):
    with pytest.raises(ValueError) as excinfo:
        permission_service.delete_permission("")
    assert "obligatorio" in str(excinfo.value)


def test_delete_permission_case_insensitive(permission_service):
    permission_service.create_permission("delete_test", "Test")
    
    permission_service.delete_permission("DELETE_TEST")
    
    with pytest.raises(PermissionNotFoundError):
        permission_service.get_permission("delete_test")


# -------------------- INTEGRATION TESTS --------------------

def test_create_get_update_delete_flow(permission_service):
    """Test del flujo completo de operaciones con permisos"""
    # Crear
    perm = permission_service.create_permission("manage_roles", "Gestionar roles")
    assert perm.name == "manage_roles"
    
    # Obtener
    retrieved = permission_service.get_permission("manage_roles")
    assert retrieved.name == "manage_roles"
    assert retrieved.description == "Gestionar roles"
    
    # Actualizar
    updated = permission_service.update_permission_description(
        "manage_roles", 
        "Crear, editar y eliminar roles"
    )
    assert updated.description == "Crear, editar y eliminar roles"
    
    # Verificar actualización
    retrieved_again = permission_service.get_permission("manage_roles")
    assert retrieved_again.description == "Crear, editar y eliminar roles"
    
    # Eliminar
    permission_service.delete_permission("manage_roles")
    
    # Verificar eliminación
    with pytest.raises(PermissionNotFoundError):
        permission_service.get_permission("manage_roles")


def test_multiple_permissions_management(permission_service):
    """Test de manejo de múltiples permisos"""
    permissions = [
        ("create", "Crear recursos"),
        ("read", "Leer recursos"),
        ("update", "Actualizar recursos"),
        ("delete", "Eliminar recursos")
    ]
    
    # Crear múltiples permisos
    for name, desc in permissions:
        permission_service.create_permission(name, desc)
    
    # Verificar que todos existen
    all_perms = permission_service.get_all_permissions()
    assert len(all_perms) == 4
    
    # Eliminar uno
    permission_service.delete_permission("delete")
    assert len(permission_service.get_all_permissions()) == 3