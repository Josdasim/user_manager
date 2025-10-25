import pytest
from pydantic import ValidationError
from datetime import datetime
from src.schemas.role_schemas import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    RoleListResponse,
    role_to_response,
)
from src.models.role import Role


# ==================== ROLE CREATE SCHEMA ====================

def test_role_create_valid():
    """Test crear RoleCreate con datos válidos"""
    role_data = RoleCreate(
        name="admin",
        description="Administrator role"
    )
    assert role_data.name == "admin"
    assert role_data.description == "Administrator role"


def test_role_create_without_description():
    """Test crear RoleCreate sin descripción"""
    role_data = RoleCreate(name="editor")  
    assert role_data.name == "editor"
    assert role_data.description == ""


def test_role_create_normalizes_name():
    """Test que el nombre se normaliza (lowercase, trim)"""
    role_data = RoleCreate(
        name="  ADMIN  ",
        description="Admin role"
    ) 
    assert role_data.name == "admin"


def test_role_create_empty_name():
    """Test validación de nombre vacío"""
    with pytest.raises(ValidationError):
        RoleCreate(name="")


def test_role_create_whitespace_name():
    """Test validación de nombre solo espacios"""
    with pytest.raises(ValidationError):
        RoleCreate(name="   ")


def test_role_create_short_name():
    """Test validación de nombre muy corto"""
    with pytest.raises(ValidationError):
        RoleCreate(name="a")


def test_role_create_long_name():
    """Test validación de nombre muy largo"""
    with pytest.raises(ValidationError):
        RoleCreate(name="a" * 51)


def test_role_create_long_description():
    """Test validación de descripción muy larga"""
    with pytest.raises(ValidationError):
        RoleCreate(name="admin", description="a" * 256)


# ==================== ROLE UPDATE SCHEMA ====================

def test_role_update_valid():
    """Test actualizar descripción de rol"""
    update_data = RoleUpdate(description="New description")
    
    assert update_data.description == "New description"


def test_role_update_trims_description():
    """Test que la descripción se limpia"""
    update_data = RoleUpdate(description="  Description  ")
    
    assert update_data.description == "Description"


def test_role_update_empty_description_allowed():
    """Test que se permite descripción vacía"""
    update_data = RoleUpdate(description="")
    
    assert update_data.description == ""


def test_role_update_none_description_rejected():
    """Test que None no es permitido"""
    with pytest.raises(ValidationError):
        RoleUpdate(description=None)


# ==================== ROLE RESPONSE SCHEMA ====================

def test_role_response_valid():
    """Test crear RoleResponse con datos válidos"""
    now = datetime.now()
    response = RoleResponse(
        id="role-id-123",
        name="admin",
        description="Administrator",
        created_at=now,
        updated_at=now
    )
    assert response.id == "role-id-123"
    assert response.name == "admin"
    assert response.description == "Administrator"
    assert response.created_at == now
    assert response.updated_at == now


def test_role_response_from_dict():
    """Test crear RoleResponse desde diccionario"""
    now = datetime.now()
    data = {
        "id": "role-123",
        "name": "editor",
        "description": "Editor role",
        "created_at": now,
        "updated_at": now
    }
    
    response = RoleResponse(**data)
    
    assert response.name == "editor"


# ==================== ROLE LIST RESPONSE SCHEMA ====================

def test_role_list_response_valid():
    """Test RoleListResponse con lista de roles"""
    now = datetime.now()
    roles = [
        RoleResponse(
            id="id-1",
            name="admin",
            description="Admin role",
            created_at=now,
            updated_at=now
        ),
        RoleResponse(
            id="id-2",
            name="editor",
            description="Editor role",
            created_at=now,
            updated_at=now
        )
    ]
    response = RoleListResponse(roles=roles, total=2)
    assert len(response.roles) == 2
    assert response.total == 2


def test_role_list_response_empty():
    """Test RoleListResponse con lista vacía"""
    response = RoleListResponse(roles=[], total=0)
    assert response.roles == []
    assert response.total == 0


def test_role_list_response_count_mismatch():
    """Test que total puede no coincidir con longitud (para paginación)"""
    now = datetime.now()
    roles = [
        RoleResponse(
            id="id-1",
            name="admin",
            description="Admin",
            created_at=now,
            updated_at=now
        )
    ]  
    # Total puede ser mayor (paginación)
    response = RoleListResponse(roles=roles, total=10)   
    assert len(response.roles) == 1
    assert response.total == 10


# ==================== ROLE HELPER FUNCTIONS ====================

def test_role_to_response_helper():
    """Test helper que convierte Role a RoleResponse"""
    role = Role(name="admin", description="Administrator")
    response = role_to_response(role) 
    assert isinstance(response, RoleResponse)
    assert response.name == "admin"
    assert response.description == "Administrator"
    assert response.id == role.id
    assert response.created_at == role.created_at
    assert response.updated_at == role.updated_at


def test_role_to_response_preserves_timestamps():
    """Test que los timestamps se preservan en la conversión"""
    role = Role(name="editor", description="Editor role")
    
    response = role_to_response(role)
    
    assert response.created_at is not None
    assert response.updated_at is not None
    assert response.created_at == role.created_at


def test_role_to_response_preserves_id():
    """Test que el ID se preserva exactamente"""
    role = Role(name="moderator", description="Moderator")
    original_id = role.id
    response = role_to_response(role)
    assert response.id == original_id


# ==================== INTEGRATION TESTS ====================

def test_role_complete_workflow():
    """Test flujo completo de creación y conversión de Role"""
    # Crear schema de request
    create_data = RoleCreate(name="moderator", description="Moderates content")
    
    # Simular creación de domain model
    role = Role(name=create_data.name, description=create_data.description)
    
    # Convertir a response
    response = role_to_response(role)
    
    assert response.name == create_data.name
    assert response.description == create_data.description
    assert response.id == role.id


def test_role_update_workflow():
    """Test flujo de actualización de rol"""
    # Rol existente
    role = Role(name="admin", description="Original description")
    
    # Schema de actualización
    update_data = RoleUpdate(description="Updated description")
    
    # Simular actualización
    role.update_description(update_data.description)
    
    # Convertir a response
    response = role_to_response(role)
    
    assert response.description == "Updated description"


def test_multiple_roles_list():
    """Test crear lista con múltiples roles"""
    now = datetime.now()
    
    role1 = Role(name="admin", description="Admin")
    role2 = Role(name="editor", description="Editor")
    role3 = Role(name="viewer", description="Viewer")
    
    responses = [
        role_to_response(role1),
        role_to_response(role2),
        role_to_response(role3)
    ]
    
    list_response = RoleListResponse(roles=responses, total=len(responses))
    
    assert list_response.total == 3
    assert len(list_response.roles) == 3
    assert list_response.roles[0].name == "admin"
    assert list_response.roles[1].name == "editor"
    assert list_response.roles[2].name == "viewer"
