from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


# ==================== REQUEST SCHEMAS ====================

class RoleCreate(BaseModel):
    """Schema para crear un nuevo rol"""
    name: str = Field(
        min_length=2,
        max_length=50,
        description="Nombre del rol",
        examples=["admin"]
    )
    description: Optional[str] = Field(
        default="",
        max_length=255,
        description="Descripción del rol",
        examples=["Administrador del sistema"]
    )

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El nombre del rol no puede estar vacío')
        return v.strip().lower()


class RoleUpdate(BaseModel):
    """Schema para actualizar un rol"""
    description: str = Field(
        max_length=255,
        description="Nueva descripción del rol",
        examples=["Administrador con acceso total"]
    )

    @field_validator('description')
    @classmethod
    def description_must_not_be_none(cls, v: str) -> str:
        if v is None:
            raise ValueError('La descripción no puede ser None')
        return v.strip()


# ==================== RESPONSE SCHEMAS ====================

class RoleResponse(BaseModel):
    """Schema para respuestas con datos de rol"""
    id: str = Field(description="ID único del rol")
    name: str = Field(description="Nombre del rol")
    description: str = Field(description="Descripción del rol")
    created_at: datetime = Field(description="Fecha de creación")
    updated_at: datetime = Field(description="Fecha de última actualización")

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "01234567-89ab-cdef-0123-456789abcdef",
                "name": "admin",
                "description": "Administrador del sistema",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


class RoleListResponse(BaseModel):
    """Schema para lista de roles"""
    roles: list[RoleResponse] = Field(description="Lista de roles")
    total: int = Field(description="Total de roles")

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "roles": [
                    {
                        "id": "01234567-89ab-cdef-0123-456789abcdef",
                        "name": "admin",
                        "description": "Administrador del sistema",
                        "created_at": "2024-01-15T10:30:00",
                        "updated_at": "2024-01-15T10:30:00"
                    }
                ],
                "total": 1
            }
        }


# ==================== HELPER FUNCTIONS ====================

def role_to_response(role) -> RoleResponse:
    """Convierte un objeto Role del dominio a RoleResponse"""
    return RoleResponse(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=role.created_at,
        updated_at=role.updated_at
    )
