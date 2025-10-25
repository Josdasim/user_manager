import pytest
from pydantic import ValidationError
from datetime import datetime
from src.schemas.user_schemas import (
    UserCreate,
    UserUpdateEmail,
    UserUpdateUsername,
    UserChangePassword,
    UserUpdateStatus,
    UserLogin,
    UserResponse,
    UserResponseWithRoles,
    UserListResponse,
    user_to_response,
    user_to_response_with_roles,
)
from src.models.user import User
from src.models.user_status import UserStatus


# ==================== USER CREATE SCHEMA ====================

def test_user_create_valid():
    """Test crear schema UserCreate con datos válidos"""
    user_data = UserCreate(
        username="jonx",
        email="jon@correo.com",
        password="secret123"
    )   
    assert user_data.username == "jonx"
    assert user_data.email == "jon@correo.com"
    assert user_data.password == "secret123"

def test_user_create_trims_username():
    """Test que el username se limpia de espacios"""
    user_data = UserCreate(
        username="  jonx  ",
        email="jon@correo.com",
        password="secret123"
    )  
    assert user_data.username == "jonx"

def test_user_create_invalid_email():
    """Test validación de email inválido"""
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            username="jonx",
            email="invalid-email",
            password="secret123"
        )   
    errors = exc_info.value.errors()
    assert any(error['type'] == 'value_error' for error in errors)

def test_user_create_empty_username():
    """Test validación de username vacío"""
    with pytest.raises(ValidationError):
        UserCreate(
            username="",
            email="jon@correo.com",
            password="secret123"
        ) 

def test_user_create_whitespace_username():
    """Test validación de username solo con espacios"""
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            username="   ",
            email="jon@correo.com",
            password="secret123"
        )
    assert "username no puede estar vacío" in str(exc_info.value)

def test_user_create_short_username():
    """Test validación de username muy corto"""
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            username="ab",
            email="jon@correo.com",
            password="secret123"
        )
    errors = exc_info.value.errors()
    assert any(error['type'] == 'string_too_short' for error in errors)

def test_user_create_short_password():
    """Test validación de contraseña muy corta"""
    with pytest.raises(ValidationError):
        UserCreate(
            username="jonx",
            email="jon@correo.com",
            password="12345"
        )

def test_user_create_missing_fields():
    """Test validación de campos requeridos faltantes"""
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(username="jonx")
    errors = exc_info.value.errors()
    assert len(errors) >= 2  # Faltan email y password


# ==================== USER UPDATE SCHEMA ====================

def test_user_update_valid():
    """Test crear schema UserUpdate con email válido"""
    update_data = UserUpdateEmail(email="newemail@correo.com")   
    assert update_data.email == "newemail@correo.com"

def test_user_update_optional_fields():
    """Test que todos los campos de UserUpdate son opcionales"""
    update_data = UserUpdateEmail()  
    assert update_data.email is None

def test_user_update_invalid_email():
    """Test validación de email inválido en update"""
    with pytest.raises(ValidationError):
        UserUpdateEmail(email="invalid-email")


# ==================== USER UPDATE USERNAME SCHEMA ====================

def test_user_update_username_valid():
    """Test actualizar username con datos válidos"""
    data = UserUpdateUsername(new_username="jonx_new")
    assert data.new_username == "jonx_new"

def test_user_update_username_trims():
    """Test que el nuevo username se limpia"""
    data = UserUpdateUsername(new_username="  newusername  ") 
    assert data.new_username == "newusername"

def test_user_update_username_empty():
    """Test validación de username vacío"""
    with pytest.raises(ValidationError):
        UserUpdateUsername(new_username="")

def test_user_update_username_too_short():
    """Test validación de username muy corto"""
    with pytest.raises(ValidationError):
        UserUpdateUsername(new_username="ab")


# ==================== USER CHANGE PASSWORD SCHEMA ====================

def test_user_change_password_valid():
    """Test cambio de contraseña con datos válidos"""
    data = UserChangePassword(
        current_password="oldpass123",
        new_password="newpass456"
    )  
    assert data.current_password == "oldpass123"
    assert data.new_password == "newpass456"

def test_user_change_password_short_new_password():
    """Test validación de nueva contraseña muy corta"""
    with pytest.raises(ValidationError):
        UserChangePassword(
            current_password="oldpass123",
            new_password="short"
        )

def test_user_change_password_missing_fields():
    """Test validación de campos requeridos"""
    with pytest.raises(ValidationError):
        UserChangePassword(new_password="newpass123")


# ==================== USER UPDATE STATUS SCHEMA ====================

def test_user_update_status_valid():
    """Test actualizar estado con valor válido"""
    data = UserUpdateStatus(status=UserStatus.ACTIVE)  
    assert data.status == UserStatus.ACTIVE

def test_user_update_status_all_values():
    """Test todos los valores posibles de estado"""
    statuses = [
        UserStatus.ACTIVE,
        UserStatus.INACTIVE,
        UserStatus.SUSPENDED,
        UserStatus.BLOCKED
    ]  
    for status in statuses:
        data = UserUpdateStatus(status=status)
        assert data.status == status

def test_user_update_status_invalid():
    """Test validación de estado inválido"""
    with pytest.raises(ValidationError):
        UserUpdateStatus(status="invalid_status")


# ==================== USER LOGIN SCHEMA ====================

def test_user_login_valid():
    """Test schema de login con datos válidos"""
    data = UserLogin(username="jonx", password="secret123") 
    assert data.username == "jonx"
    assert data.password == "secret123"

def test_user_login_missing_fields():
    """Test validación de campos requeridos en login"""
    with pytest.raises(ValidationError):
        UserLogin(username="jonx")


# ==================== USER RESPONSE SCHEMA ====================

def test_user_response_valid():
    """Test crear UserResponse con datos válidos"""
    now = datetime.now()
    response = UserResponse(
        id="test-id-123",
        username="jonx",
        email="jon@correo.com",
        status=UserStatus.ACTIVE,
        created_at=now,
        updated_at=now
    )
    assert response.id == "test-id-123"
    assert response.username == "jonx"
    assert response.email == "jon@correo.com"
    assert response.status == UserStatus.ACTIVE
    assert response.created_at == now
    assert response.updated_at == now

def test_user_response_from_dict():
    """Test crear UserResponse desde diccionario"""
    now = datetime.now()  
    data = {
        "id": "test-id-123",
        "username": "jonx",
        "email": "jon@correo.com",
        "status": "active",
        "created_at": now,
        "updated_at": now
    }  
    response = UserResponse(**data)  
    assert response.username == "jonx"


# ==================== USER RESPONSE WITH ROLES SCHEMA ====================

def test_user_response_with_roles_valid():
    """Test UserResponseWithRoles con roles"""
    now = datetime.now()
    response = UserResponseWithRoles(
        id="test-id-123",
        username="jonx",
        email="jon@correo.com",
        status=UserStatus.ACTIVE,
        roles=["admin", "editor"],
        created_at=now,
        updated_at=now
    ) 
    assert response.roles == ["admin", "editor"]
    assert len(response.roles) == 2

def test_user_response_with_roles_empty_list():
    """Test UserResponseWithRoles con lista vacía de roles"""
    now = datetime.now()
    response = UserResponseWithRoles(
        id="test-id-123",
        username="jonx",
        email="jon@correo.com",
        status=UserStatus.ACTIVE,
        created_at=now,
        updated_at=now
    )
    assert response.roles == []


# ==================== USER LIST RESPONSE SCHEMA ====================

def test_user_list_response_valid():
    """Test UserListResponse con lista de usuarios"""
    now = datetime.now() 
    users = [
        UserResponse(
            id="id-1",
            username="jon",
            email="jon@correo.com",
            status=UserStatus.ACTIVE,
            created_at=now,
            updated_at=now
        ),
        UserResponse(
            id="id-2",
            username="jane",
            email="jane@correo.com",
            status=UserStatus.ACTIVE,
            created_at=now,
            updated_at=now
        )
    ]
    response = UserListResponse(users=users, total=2)
    assert len(response.users) == 2
    assert response.total == 2

def test_user_list_response_empty():
    """Test UserListResponse con lista vacía"""
    response = UserListResponse(users=[], total=0)
    assert response.users == []
    assert response.total == 0


# ==================== HELPER FUNCTIONS ====================

def test_user_to_response_helper():
    """Test helper que convierte User a UserResponse"""
    user = User(
        username="jonx",
        email="jon@correo.com",
        password="hashed_password"
    )
    response = user_to_response(user)   
    assert isinstance(response, UserResponse)
    assert response.username == "jonx"
    assert response.email == "jon@correo.com"
    assert response.id == user.id
    assert response.status == user.status

def test_user_to_response_with_roles_helper():
    """Test helper que convierte User a UserResponseWithRoles"""
    user = User(
        username="jonx",
        email="jon@correo.com",
        password="hashed_password"
    )
    user.roles = ["admin", "editor"]   
    response = user_to_response_with_roles(user)   
    assert isinstance(response, UserResponseWithRoles)
    assert response.username == "jonx"
    assert response.roles == ["admin", "editor"]

def test_user_to_response_with_roles_custom_roles():
    """Test helper con roles personalizados"""
    user = User(
        username="jonx",
        email="jon@correo.com",
        password="hashed_password"
    ) 
    custom_roles = ["role1", "role2", "role3"]
    response = user_to_response_with_roles(user, roles=custom_roles) 
    assert response.roles == custom_roles
