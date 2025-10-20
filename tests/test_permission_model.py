import pytest
from src.models.permission import Permission

def test_create_permission_success():
    perm = Permission(name="create_user", description="Puede crear Usuarios")
    assert perm.name == "create_user"
    assert perm.description == "Puede crear Usuarios"
    assert perm.id is not None

def test_create_permission_without_description():
    perm = Permission(name="delete_user")
    assert perm.description == ""

def test_create_permission_with_empty_name():
    with pytest.raises(ValueError):
        Permission(name="")

def test_update_permission_description():
    perm = Permission(name="update_user", description="Modificar datos")
    perm.update_description("Puede modificar correo y nombre")
    assert perm.description == "Puede modificar correo y nombre"