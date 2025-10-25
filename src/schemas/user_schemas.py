from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from src.models.user_status import UserStatus


# ==================== REQUEST SCHEMAS ====================

class UserCreate(BaseModel):
    """Schema para crear un nuevo usuario"""
    username: str = Field(
        min_length=3, 
        max_length=50,
        description="Nombre de usuario único",
        examples=["joe"]
    )
    email: EmailStr = Field(
        description="Correo electrónico válido",
        examples=["jon@example.com"]
    )
    password: str = Field(
        min_length=6,
        description="Contraseña (mínimo 6 caracteres)",
        examples=["xecret1"]
    )

    @field_validator('username')
    @classmethod
    def username_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El username no puede estar vacío')
        return v.strip()

    @field_validator('password')
    @classmethod
    def password_must_be_strong(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v

#considerar cambio de nombre
class UserUpdateEmail(BaseModel):
    """Schema para actualizar datos de usuario"""
    email: Optional[EmailStr] = Field(
        None,
        description="Nuevo correo electrónico",
        examples=["newemail@example.com"]
    )
    class ConfigDictDict:
        # Permite actualización parcial
        extra = "forbid"


class UserUpdateUsername(BaseModel):
    """Schema para actualizar username"""
    new_username: str = Field(
        min_length=3,
        max_length=50,
        description="Nuevo nombre de usuario",
        examples=["joe_new"]
    )

    @field_validator('new_username')
    @classmethod
    def username_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El username no puede estar vacío')
        return v.strip()

#Considerar evitar espacios al inicio y final de la contraseña
class UserChangePassword(BaseModel):
    """Schema para cambiar contraseña"""
    current_password: str = Field(
        description="Contraseña actual",
        examples=["oldpassword"]
    )
    new_password: str = Field(
        min_length=6,
        description="Nueva contraseña (mínimo 6 caracteres)",
        examples=["newpassword123"]
    )

    @field_validator('new_password')
    @classmethod
    def password_must_be_strong(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v


class UserUpdateStatus(BaseModel):
    """Schema para cambiar el estado del usuario"""
    status: UserStatus = Field(
        description="Nuevo estado del usuario",
        examples=["active"]
    )


class UserLogin(BaseModel):
    """Schema para login"""
    username: str = Field(
        description="Nombre de usuario",
        examples=["joe"]
    )
    password: str = Field(
        description="Contraseña",
        examples=["xecret1"]
    )


# ==================== RESPONSE SCHEMAS ====================

class UserResponse(BaseModel):
    """Schema para respuestas con datos de usuario"""
    id: str = Field(description="ID único del usuario")
    username: str = Field(description="Nombre de usuario")
    email: EmailStr = Field(description="Correo electrónico")
    status: UserStatus = Field(description="Estado del usuario")
    created_at: datetime = Field(description="Fecha de creación")
    updated_at: datetime = Field(description="Fecha de última actualización")

    class ConfigDict:
        from_attributes = True  # Permite crear desde objetos ORM/Domain
        json_schema_extra = {
            "example": {
                "id": "01234567-89ab-cdef-0123-456789abcdef",
                "username": "joe",
                "email": "jon@example.com",
                "status": "active",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


class UserResponseWithRoles(UserResponse):
    """Schema de usuario incluyendo sus roles"""
    roles: list[str] = Field(
        default_factory=list,
        description="Lista de roles asignados al usuario"
    )

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "01234567-89ab-cdef-0123-456789abcdef",
                "username": "joe",
                "email": "jon@example.com",
                "status": "active",
                "roles": ["admin", "editor"],
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


class UserListResponse(BaseModel):
    """Schema para lista de usuarios"""
    users: list[UserResponse] = Field(description="Lista de usuarios")
    total: int = Field(description="Total de usuarios")

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "users": [
                    {
                        "id": "01234567-89ab-cdef-0123-456789abcdef",
                        "username": "joe",
                        "email": "jon@example.com",
                        "status": "active",
                        "created_at": "2024-01-15T10:30:00",
                        "updated_at": "2024-01-15T10:30:00"
                    }
                ],
                "total": 1
            }
        }


# ==================== HELPER FUNCTIONS ====================

def user_to_response(user) -> UserResponse:
    """Convierte un objeto User del dominio a UserResponse"""
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        status=user.status,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


def user_to_response_with_roles(user, roles: list[str] = None) -> UserResponseWithRoles:
    """Convierte un objeto User del dominio a UserResponseWithRoles"""
    return UserResponseWithRoles(
        id=user.id,
        username=user.username,
        email=user.email,
        status=user.status,
        roles=roles or user.roles,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
