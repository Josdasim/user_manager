import pytest
from pydantic import ValidationError
from src.schemas.auth_schemas import (
    TokenRequest,
    TokenRefresh,
    Token,
    TokenData,
    UserInfo,
    MessageResponse,
    ErrorResponse,
)


# ==================== TOKEN REQUEST SCHEMA ====================

def test_token_request_valid():
    """Test crear TokenRequest con datos válidos"""
    data = TokenRequest(
        username="jon",
        password="secret123"
    )
    
    assert data.username == "jon"
    assert data.password == "secret123"


def test_token_request_missing_username():
    """Test validación de username requerido"""
    with pytest.raises(ValidationError):
        TokenRequest(password="secret123")


def test_token_request_missing_password():
    """Test validación de password requerido"""
    with pytest.raises(ValidationError):
        TokenRequest(username="jon")


def test_token_request_both_missing():
    """Test validación de ambos campos requeridos"""
    with pytest.raises(ValidationError):
        TokenRequest()


# ==================== TOKEN REFRESH SCHEMA ====================

def test_token_refresh_valid():
    """Test crear TokenRefresh con token válido"""
    data = TokenRefresh(
        refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    
    assert data.refresh_token.startswith("eyJ")


def test_token_refresh_missing_token():
    """Test validación de token requerido"""
    with pytest.raises(ValidationError):
        TokenRefresh()


def test_token_refresh_empty_token():
    """Test que acepta string vacío (validación en backend)"""
    # Pydantic permite string vacío, validación JWT es en el handler
    data = TokenRefresh(refresh_token="")
    assert data.refresh_token == ""


# ==================== TOKEN SCHEMA ====================

def test_token_response_valid():
    """Test crear Token response con datos completos"""
    token = Token(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.access",
        refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refresh",
        token_type="bearer",
        expires_in=3600
    )
    
    assert token.access_token.endswith("access")
    assert token.refresh_token.endswith("refresh")
    assert token.token_type == "bearer"
    assert token.expires_in == 3600


def test_token_response_without_refresh():
    """Test crear Token sin refresh_token"""
    token = Token(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.access",
        expires_in=3600
    )
    
    assert token.access_token.endswith("access")
    assert token.refresh_token is None
    assert token.token_type == "bearer"  # Default value


def test_token_response_default_token_type():
    """Test que token_type tiene valor por defecto"""
    token = Token(
        access_token="token123",
        expires_in=3600
    )
    
    assert token.token_type == "bearer"


def test_token_response_custom_token_type():
    """Test que se puede especificar token_type personalizado"""
    token = Token(
        access_token="token123",
        token_type="custom",
        expires_in=3600
    )
    
    assert token.token_type == "custom"


def test_token_response_missing_access_token():
    """Test validación de access_token requerido"""
    with pytest.raises(ValidationError):
        Token(expires_in=3600)


def test_token_response_missing_expires_in():
    """Test validación de expires_in requerido"""
    with pytest.raises(ValidationError):
        Token(access_token="token123")


def test_token_response_negative_expires_in():
    """Test que acepta expires_in negativo (validación lógica en backend)"""
    token = Token(
        access_token="token123",
        expires_in=-100
    )
    assert token.expires_in == -100


def test_token_response_zero_expires_in():
    """Test que acepta expires_in en cero"""
    token = Token(
        access_token="token123",
        expires_in=0
    )
    assert token.expires_in == 0


# ==================== TOKEN DATA SCHEMA ====================

def test_token_data_valid():
    """Test crear TokenData con datos completos"""
    data = TokenData(
        username="jon",
        user_id="user-123"
    )
    
    assert data.username == "jon"
    assert data.user_id == "user-123"


def test_token_data_without_user_id():
    """Test crear TokenData sin user_id (opcional)"""
    data = TokenData(username="jon")
    
    assert data.username == "jon"
    assert data.user_id is None


def test_token_data_missing_username():
    """Test validación de username requerido"""
    with pytest.raises(ValidationError):
        TokenData(user_id="user-123")


def test_token_data_empty_username():
    """Test que acepta username vacío (validación en backend)"""
    data = TokenData(username="")
    assert data.username == ""


# ==================== USER INFO SCHEMA ====================

def test_user_info_valid():
    """Test crear UserInfo con datos completos"""
    info = UserInfo(
        username="jon",
        email="jon@correo.com",
        status="active",
        roles=["admin", "editor"]
    )
    
    assert info.username == "jon"
    assert info.email == "jon@correo.com"
    assert info.status == "active"
    assert info.roles == ["admin", "editor"]


def test_user_info_without_roles():
    """Test crear UserInfo sin roles"""
    info = UserInfo(
        username="jon",
        email="jon@correo.com",
        status="active"
    )
    
    assert info.roles == []  # Default empty list


def test_user_info_empty_roles_list():
    """Test crear UserInfo con lista vacía explícita"""
    info = UserInfo(
        username="jon",
        email="jon@correo.com",
        status="active",
        roles=[]
    )
    
    assert info.roles == []


def test_user_info_single_role():
    """Test UserInfo con un solo rol"""
    info = UserInfo(
        username="jon",
        email="jon@correo.com",
        status="active",
        roles=["user"]
    )
    
    assert len(info.roles) == 1
    assert info.roles[0] == "user"


def test_user_info_missing_username():
    """Test validación de username requerido"""
    with pytest.raises(ValidationError):
        UserInfo(email="jon@correo.com", status="active")


def test_user_info_missing_email():
    """Test validación de email requerido"""
    with pytest.raises(ValidationError):
        UserInfo(username="jon", status="active")


def test_user_info_missing_status():
    """Test validación de status requerido"""
    with pytest.raises(ValidationError):
        UserInfo(username="jon", email="jon@correo.com")


# ==================== MESSAGE RESPONSE SCHEMA ====================

def test_message_response_valid():
    """Test crear MessageResponse"""
    response = MessageResponse(message="Operation successful")
    
    assert response.message == "Operation successful"


def test_message_response_empty_message():
    """Test MessageResponse con mensaje vacío"""
    response = MessageResponse(message="")
    
    assert response.message == ""


def test_message_response_long_message():
    """Test MessageResponse con mensaje largo"""
    long_message = "A" * 1000
    response = MessageResponse(message=long_message)
    
    assert len(response.message) == 1000


def test_message_response_missing_message():
    """Test validación de mensaje requerido"""
    with pytest.raises(ValidationError):
        MessageResponse()


def test_message_response_special_characters():
    """Test MessageResponse con caracteres especiales"""
    response = MessageResponse(message="Success! ✅ User created 🎉")
    
    assert "✅" in response.message
    assert "🎉" in response.message


# ==================== ERROR RESPONSE SCHEMA ====================

def test_error_response_valid():
    """Test crear ErrorResponse con datos completos"""
    error = ErrorResponse(
        detail="User not found",
        error_code="USER_NOT_FOUND"
    )
    
    assert error.detail == "User not found"
    assert error.error_code == "USER_NOT_FOUND"


def test_error_response_without_code():
    """Test crear ErrorResponse sin código de error"""
    error = ErrorResponse(detail="Something went wrong")
    
    assert error.detail == "Something went wrong"
    assert error.error_code is None


def test_error_response_empty_detail():
    """Test ErrorResponse con detalle vacío"""
    error = ErrorResponse(detail="")
    
    assert error.detail == ""


def test_error_response_empty_code():
    """Test ErrorResponse con código vacío"""
    error = ErrorResponse(
        detail="Error occurred",
        error_code=""
    )
    
    assert error.error_code == ""


def test_error_response_missing_detail():
    """Test validación de detail requerido"""
    with pytest.raises(ValidationError):
        ErrorResponse(error_code="ERROR_CODE")


def test_error_response_long_detail():
    """Test ErrorResponse con detalle largo"""
    long_detail = "Error: " + "X" * 500
    error = ErrorResponse(detail=long_detail)
    
    assert len(error.detail) > 500


# ==================== INTEGRATION TESTS ====================

def test_token_workflow():
    """Test flujo completo de tokens"""
    # 1. Request de token
    request = TokenRequest(username="jon", password="secret123")
    assert request.username == "jon"
    
    # 2. Response con token
    token_response = Token(
        access_token="access.token.here",
        refresh_token="refresh.token.here",
        expires_in=3600
    )
    assert token_response.access_token == "access.token.here"
    
    # 3. Datos extraídos del token
    token_data = TokenData(
        username=request.username,
        user_id="user-123"
    )
    assert token_data.username == request.username
    
    # 4. Info del usuario
    user_info = UserInfo(
        username=token_data.username,
        email="jon@correo.com",
        status="active",
        roles=["user"]
    )
    assert user_info.username == token_data.username


def test_error_handling_workflow():
    """Test flujo de manejo de errores"""
    # Error sin código
    error1 = ErrorResponse(detail="Invalid credentials")
    assert error1.detail == "Invalid credentials"
    assert error1.error_code is None
    
    # Error con código
    error2 = ErrorResponse(
        detail="User not found",
        error_code="USER_NOT_FOUND"
    )
    assert error2.error_code == "USER_NOT_FOUND"
    
    # Mensaje de éxito
    success = MessageResponse(message="User created successfully")
    assert success.message == "User created successfully"


def test_schemas_json_serialization():
    """Test que los schemas se pueden serializar a JSON"""
    token = Token(
        access_token="token123",
        expires_in=3600
    )
    
    # Pydantic permite exportar a dict
    token_dict = token.model_dump()
    
    assert token_dict["access_token"] == "token123"
    assert token_dict["expires_in"] == 3600
    assert token_dict["token_type"] == "bearer"
    assert token_dict["refresh_token"] is None


def test_schemas_json_deserialization():
    """Test que los schemas se pueden crear desde JSON/dict"""
    data = {
        "username": "jon",
        "email": "jon@correo.com",
        "status": "active",
        "roles": ["admin"]
    }
    
    user_info = UserInfo(**data)
    
    assert user_info.username == "jon"
    assert user_info.roles == ["admin"]


def test_multiple_schemas_interaction():
    """Test interacción entre múltiples schemas"""
    # Login request
    login = TokenRequest(username="testuser", password="testpass")
    
    # Token response
    token = Token(
        access_token="jwt.token.here",
        expires_in=3600
    )
    
    # User info from token
    user_info = UserInfo(
        username=login.username,
        email="test@correo.com",
        status="active",
        roles=["user", "admin"]
    )
    
    # Success message
    message = MessageResponse(message=f"Welcome {user_info.username}")
    
    assert login.username in message.message
    assert len(user_info.roles) == 2


def test_token_refresh_workflow():
    """Test flujo de refresh token"""
    # Token original
    original = Token(
        access_token="original.access.token",
        refresh_token="original.refresh.token",
        expires_in=3600
    )
    
    # Request de refresh
    refresh_request = TokenRefresh(
        refresh_token=original.refresh_token
    )
    
    # Nuevo token
    new_token = Token(
        access_token="new.access.token",
        refresh_token="new.refresh.token",
        expires_in=3600
    )
    
    assert refresh_request.refresh_token == original.refresh_token
    assert new_token.access_token != original.access_token
