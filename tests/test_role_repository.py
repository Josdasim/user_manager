import pytest
from src.models.role import Role
from src.exceptions.role_exceptions import RoleNotFoundError, RoleAlreadyExistsError
from src.constants import messages

#---------------------ADD/GET---------------------

def test_add_and_get_role(role_repo):
    role = Role(name="admin")
    role_repo.add(role)
    retrieved = role_repo.get(role.name)
    assert retrieved.name == "admin"

def test_add_existing_role(role_repo):
    role = Role(name="admin")
    role_repo.add(role)
    with pytest.raises(RoleAlreadyExistsError, match=messages.ROLE_ALREADY_EXISTS):
        role_repo.add(role)

def test_get_nonexistent_role(role_repo):
    with pytest.raises(RoleNotFoundError, match=messages.ROLE_NOT_FOUND):
        role_repo.get("not_exist")

#---------------------FIND---------------------

def test_find_role(role_repo):
    role = Role(name="editor", description="Puede editar los datos")
    role_repo.add(role)
    assert role_repo.find("editor") == role

def test_role_not_found(role_repo):
    assert role_repo.find("notexist_role") is None

#--------------------UPDATE---------------------

def test_update_existing_role(role_repo):
    role = Role(name="editor", description="Puede editar contenidos")
    role_repo.add(role)
    role_repo.update_description("editor", "Edita articulos y productos")
    assert role.description == "Edita articulos y productos"

def test_update_nonexistent_role(role_repo):
    #TODO:Agregar error personalizado
    with pytest.raises(RoleNotFoundError, match=messages.ROLE_NOT_FOUND):
        role_repo.update_description("editor", "Edita articulos y productos")

#---------------------DELETE---------------------

def test_delete_existing_role(role_repo):
    role_repo.add(Role("editor", "Edita articulos y productos"))
    assert role_repo.find("editor") is not None
    role_repo.delete("editor")
    assert role_repo.find("editor") is None

def test_delete_nonexistent_role(role_repo):
    with pytest.raises(RoleNotFoundError, match=messages.ROLE_NOT_FOUND):
        role_repo.delete("user")

#---------------------GET ALL---------------------

def test_get_all_roles(role_repo):
    role_repo.add(Role(name="admin"))
    role_repo.add(Role(name="user"))
    all_roles = role_repo.get_all()
    assert len(all_roles) == 2

def test_get_all_without_roles(role_repo):
    all_roles = role_repo.get_all()
    assert len(all_roles) == 0
    assert all_roles == []
