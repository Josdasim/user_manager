from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


# ==================== REQUEST SCHEMAS ====================

class PermissionCreate(BaseModel):
    """Schema para crear un nuevo permiso"""
    name: str = Field(
        min_length=2,
        max_length=50,
        description="Nombre del permiso",
        examples=["create_user"]
    )
    description: Optional[str] = Field(
        default="",
        max_length=255,
        description="Descripción del permiso",
        examples=["Permite crear nuevos usuarios"]
    )

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El nombre del permiso no puede estar vacío')
        return v.strip().lower()


class PermissionUpdate(BaseModel):
    """Schema para actualizar un permiso"""
    description: str = Field(
        max_length=255,
        description="Nueva descripción del permiso",
        examples=["Permite crear y gestionar usuarios"]
    )

    @field_validator('description')
    @classmethod
    def description_must_not_be_none(cls, v: str) -> str:
        if v is None:
            raise ValueError('La descripción no puede ser None')
        return v.strip()


# ==================== RESPONSE SCHEMAS ====================

class PermissionResponse(BaseModel):
    """Schema para respuestas con datos de permiso"""
    id: str = Field(description="ID único del permiso")
    name: str = Field(description="Nombre del permiso")
    description: str = Field(description="Descripción del permiso")
    created_at: datetime = Field(description="Fecha de creación")
    updated_at: datetime = Field(description="Fecha de última actualización")

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "01234567-89ab-cdef-0123-456789abcdef",
                "name": "create_user",
                "description": "Permite crear nuevos usuarios",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


class PermissionListResponse(BaseModel):
    """Schema para lista de permisos"""
    permissions: list[PermissionResponse] = Field(description="Lista de permisos")
    total: int = Field(description="Total de permisos")

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "permissions": [
                    {
                        "id": "01234567-89ab-cdef-0123-456789abcdef",
                        "name": "create_user",
                        "description": "Permite crear nuevos usuarios",
                        "created_at": "2024-01-15T10:30:00",
                        "updated_at": "2024-01-15T10:30:00"
                    }
                ],
                "total": 1
            }
        }


# ==================== HELPER FUNCTIONS ====================

def permission_to_response(permission) -> PermissionResponse:
    """Convierte un objeto Permission del dominio a PermissionResponse"""
    return PermissionResponse(
        id=permission.id,
        name=permission.name,
        description=permission.description,
        created_at=permission.created_at,
        updated_at=permission.updated_at
    )
