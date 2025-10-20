import pytest
from src.models.role import Role

def test_create_role_success():
    role = Role(name="admin", description="Acceso total al sistema")
    assert role.name == "admin"
    assert role.description == "Acceso total al sistema"
    assert role.id is not None

def test_create_role_without_description():
    role = Role(name="user")
    assert role.description == ""

def test_create_role_with_empty_name():
    with pytest.raises(ValueError):
        Role(name="")

def test_update_role_description():
    role = Role(name="editor", description="Puede editar contenidos")
    role.update_description("Edita articulos y productos")
    assert role.description == "Edita articulos y productos"