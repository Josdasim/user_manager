from pydantic import BaseModel, Field
from typing import Optional


# ==================== REQUEST SCHEMAS ====================

class TokenRequest(BaseModel):
    """Schema para solicitud de token (login)"""
    username: str = Field(
        description="Nombre de usuario",
        examples=["jon"]
    )
    password: str = Field(
        description="Contraseña",
        examples=["secret123"]
    )


class TokenRefresh(BaseModel):
    """Schema para refrescar token"""
    refresh_token: str = Field(
        description="Token de refresco",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )


# ==================== RESPONSE SCHEMAS ====================

class Token(BaseModel):
    """Schema para respuesta de token"""
    access_token: str = Field(
        description="Token de acceso JWT",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )
    refresh_token: Optional[str] = Field(
        default=None,
        description="Token de refresco (opcional)",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )
    token_type: str = Field(
        default="bearer",
        description="Tipo de token",
        examples=["bearer"]
    )
    expires_in: int = Field(
        description="Tiempo de expiración en segundos",
        examples=[3600]
    )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjQwOTk1MjAwfQ...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjQwOTk1MjAwfQ...",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }


class TokenData(BaseModel):
    """Schema para datos extraídos del token"""
    username: str = Field(description="Nombre de usuario del token")
    user_id: Optional[str] = Field(
        default=None,
        description="ID del usuario"
    )


# ==================== USER INFO SCHEMA ====================

class UserInfo(BaseModel):
    """Schema para información del usuario autenticado"""
    username: str = Field(description="Nombre de usuario")
    email: str = Field(description="Correo electrónico")
    status: str = Field(description="Estado del usuario")
    roles: list[str] = Field(
        default_factory=list,
        description="Roles del usuario"
    )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "username": "jon",
                "email": "jon@correo.com",
                "status": "active",
                "roles": ["admin", "editor"]
            }
        }


# ==================== MESSAGE SCHEMAS ====================

class MessageResponse(BaseModel):
    """Schema genérico para respuestas con mensaje"""
    message: str = Field(
        description="Mensaje de respuesta",
        examples=["Operación exitosa"]
    )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "message": "Operación completada exitosamente"
            }
        }


class ErrorResponse(BaseModel):
    """Schema para respuestas de error"""
    detail: str = Field(
        description="Detalle del error",
        examples=["Usuario no encontrado"]
    )
    error_code: Optional[str] = Field(
        default=None,
        description="Código de error",
        examples=["USER_NOT_FOUND"]
    )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "detail": "Usuario no encontrado",
                "error_code": "USER_NOT_FOUND"
            }
        }
