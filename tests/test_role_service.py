import pytest
from src.models.role import Role
from src.exceptions.role_exceptions import RoleValidationError, RoleAlreadyExistsError, RoleNotFoundError
from src.constants import messages

def test_create_role_success(role_service):
    role = role_service.create_role("admin", "Administrador del sistema")
    assert isinstance(role, Role)
    assert role.name == "admin"
    assert role.description == "Administrador del sistema"


def test_create_role_without_name_raises_error(role_service):
    with pytest.raises(RoleValidationError, match=messages.ROLE_INVALID_NAME):
        role_service.create_role("", "Descripción")


def test_create_duplicate_role_raises_error(role_service):
    role_service.create_role("admin", "Administrador")
    with pytest.raises(RoleAlreadyExistsError, match=messages.ROLE_ALREADY_EXISTS):
        role_service.create_role("admin", "Duplicado")


def test_get_existing_role(role_service):
    role_service.create_role("user", "Usuario regular")
    role = role_service.get_role("user")
    assert role.name == "user"
    assert role.description == "Usuario regular"


def test_get_nonexistent_role_raises_error(role_service):
    with pytest.raises(RoleNotFoundError, match=messages.ROLE_NOT_FOUND):
        role_service.get_role("no_existe")


def test_get_all_roles(role_service):
    role_service.create_role("admin", "Administrador")
    role_service.create_role("user", "Usuario")
    all_roles = role_service.get_all_roles()
    assert len(all_roles) == 2
    assert all(isinstance(r, Role) for r in all_roles)


def test_update_role_description(role_service):
    role_service.create_role("admin", "Descripción inicial")
    updated_role = role_service.update_role_description("admin", "Nueva descripción")
    assert updated_role.description == "Nueva descripción"


def test_update_role_description_with_invalid_data(role_service):
    role_service.create_role("admin", "Inicial")
    with pytest.raises(RoleValidationError, match=messages.ROLE_INVALID_NAME):
        role_service.update_role_description("", "Descripción")

    with pytest.raises(RoleValidationError, match=messages.ROLE_INVALID_TYPE):
        role_service.update_role_description("admin", None)


def test_delete_role(role_service):
    role_service.create_role("guest", "Invitado temporal")
    role_service.delete_role("guest")
    with pytest.raises(RoleNotFoundError, match=messages.ROLE_NOT_FOUND):
        role_service.get_role("guest")
