import pytest
from pydantic import ValidationError
from datetime import datetime
from src.schemas.permission_schemas import (
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse,
    PermissionListResponse,
    permission_to_response,
)
from src.models.permission import Permission


# ==================== PERMISSION CREATE SCHEMA ====================

def test_permission_create_valid():
    """Test crear PermissionCreate con datos válidos"""
    perm_data = PermissionCreate(
        name="create_user",
        description="Can create users"
    )
    
    assert perm_data.name == "create_user"
    assert perm_data.description == "Can create users"


def test_permission_create_without_description():
    """Test crear PermissionCreate sin descripción"""
    perm_data = PermissionCreate(name="delete_user")
    
    assert perm_data.name == "delete_user"
    assert perm_data.description == ""


def test_permission_create_normalizes_name():
    """Test que el nombre se normaliza"""
    perm_data = PermissionCreate(
        name="  CREATE_USER  ",
        description="Create users"
    )
    
    assert perm_data.name == "create_user"


def test_permission_create_empty_name():
    """Test validación de nombre vacío"""
    with pytest.raises(ValidationError):
        PermissionCreate(name="")


def test_permission_create_whitespace_name():
    """Test validación de nombre solo espacios"""
    with pytest.raises(ValidationError):
        PermissionCreate(name="   ")


def test_permission_create_short_name():
    """Test validación de nombre muy corto"""
    with pytest.raises(ValidationError):
        PermissionCreate(name="a")


def test_permission_create_long_name():
    """Test validación de nombre muy largo"""
    with pytest.raises(ValidationError):
        PermissionCreate(name="a" * 51)


def test_permission_create_long_description():
    """Test validación de descripción muy larga"""
    with pytest.raises(ValidationError):
        PermissionCreate(name="create", description="a" * 256)


# ==================== PERMISSION UPDATE SCHEMA ====================

def test_permission_update_valid():
    """Test actualizar descripción de permiso"""
    update_data = PermissionUpdate(description="New description")
    
    assert update_data.description == "New description"


def test_permission_update_trims_description():
    """Test que la descripción se limpia"""
    update_data = PermissionUpdate(description="  Description  ")
    
    assert update_data.description == "Description"


def test_permission_update_empty_description_allowed():
    """Test que se permite descripción vacía"""
    update_data = PermissionUpdate(description="")
    
    assert update_data.description == ""


def test_permission_update_none_description_rejected():
    """Test que None no es permitido"""
    with pytest.raises(ValidationError):
        PermissionUpdate(description=None)


# ==================== PERMISSION RESPONSE SCHEMA ====================

def test_permission_response_valid():
    """Test crear PermissionResponse con datos válidos"""
    now = datetime.now()
    
    response = PermissionResponse(
        id="perm-id-123",
        name="create_user",
        description="Can create users",
        created_at=now,
        updated_at=now
    )
    
    assert response.id == "perm-id-123"
    assert response.name == "create_user"
    assert response.description == "Can create users"
    assert response.created_at == now
    assert response.updated_at == now


def test_permission_response_from_dict():
    """Test crear PermissionResponse desde diccionario"""
    now = datetime.now()
    
    data = {
        "id": "perm-456",
        "name": "delete_user",
        "description": "Delete users",
        "created_at": now,
        "updated_at": now
    }
    
    response = PermissionResponse(**data)
    
    assert response.name == "delete_user"


# ==================== PERMISSION LIST RESPONSE SCHEMA ====================

def test_permission_list_response_valid():
    """Test PermissionListResponse con lista de permisos"""
    now = datetime.now()
    
    permissions = [
        PermissionResponse(
            id="id-1",
            name="create_user",
            description="Create users",
            created_at=now,
            updated_at=now
        ),
        PermissionResponse(
            id="id-2",
            name="delete_user",
            description="Delete users",
            created_at=now,
            updated_at=now
        )
    ]
    
    response = PermissionListResponse(permissions=permissions, total=2)
    
    assert len(response.permissions) == 2
    assert response.total == 2


def test_permission_list_response_empty():
    """Test PermissionListResponse con lista vacía"""
    response = PermissionListResponse(permissions=[], total=0)
    
    assert response.permissions == []
    assert response.total == 0


def test_permission_list_response_count_mismatch():
    """Test que total puede no coincidir con longitud (para paginación)"""
    now = datetime.now()
    
    permissions = [
        PermissionResponse(
            id="id-1",
            name="create_user",
            description="Create",
            created_at=now,
            updated_at=now
        )
    ]
    
    # Total puede ser mayor (paginación)
    response = PermissionListResponse(permissions=permissions, total=50)
    
    assert len(response.permissions) == 1
    assert response.total == 50


# ==================== PERMISSION HELPER FUNCTIONS ====================

def test_permission_to_response_helper():
    """Test helper que convierte Permission a PermissionResponse"""
    permission = Permission(
        name="create_user",
        description="Can create users"
    )
    
    response = permission_to_response(permission)
    
    assert isinstance(response, PermissionResponse)
    assert response.name == "create_user"
    assert response.description == "Can create users"
    assert response.id == permission.id
    assert response.created_at == permission.created_at
    assert response.updated_at == permission.updated_at


def test_permission_to_response_preserves_timestamps():
    """Test que los timestamps se preservan en la conversión"""
    permission = Permission(name="delete_user", description="Delete users")
    
    response = permission_to_response(permission)
    
    assert response.created_at is not None
    assert response.updated_at is not None
    assert response.created_at == permission.created_at


def test_permission_to_response_preserves_id():
    """Test que el ID se preserva exactamente"""
    permission = Permission(name="update_user", description="Update")
    original_id = permission.id
    
    response = permission_to_response(permission)
    
    assert response.id == original_id


# ==================== INTEGRATION TESTS ====================

def test_permission_complete_workflow():
    """Test flujo completo de creación y conversión de Permission"""
    # Crear schema de request
    create_data = PermissionCreate(name="update_user", description="Update user data")
    
    # Simular creación de domain model
    permission = Permission(name=create_data.name, description=create_data.description)
    
    # Convertir a response
    response = permission_to_response(permission)
    
    assert response.name == create_data.name
    assert response.description == create_data.description
    assert response.id == permission.id


def test_permission_update_workflow():
    """Test flujo de actualización de permiso"""
    # Permiso existente
    permission = Permission(name="create_user", description="Original description")
    
    # Schema de actualización
    update_data = PermissionUpdate(description="Updated description")
    
    # Simular actualización
    permission.update_description(update_data.description)
    
    # Convertir a response
    response = permission_to_response(permission)
    
    assert response.description == "Updated description"


def test_multiple_permissions_list():
    """Test crear lista con múltiples permisos"""
    perm1 = Permission(name="create", description="Create")
    perm2 = Permission(name="read", description="Read")
    perm3 = Permission(name="update", description="Update")
    perm4 = Permission(name="delete", description="Delete")
    
    responses = [
        permission_to_response(perm1),
        permission_to_response(perm2),
        permission_to_response(perm3),
        permission_to_response(perm4)
    ]
    
    list_response = PermissionListResponse(permissions=responses, total=len(responses))
    
    assert list_response.total == 4
    assert len(list_response.permissions) == 4
    assert list_response.permissions[0].name == "create"
    assert list_response.permissions[3].name == "delete"


def test_permission_crud_naming_convention():
    """Test que los nombres CRUD siguen convención"""
    crud_permissions = ["create", "read", "update", "delete"]
    
    for perm_name in crud_permissions:
        perm_data = PermissionCreate(name=perm_name, description=f"{perm_name.title()} operation")
        permission = Permission(name=perm_data.name, description=perm_data.description)
        response = permission_to_response(permission)
        
        assert response.name == perm_name
        assert perm_name in response.description.lower()
