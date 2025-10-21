import pytest
from src.models.permission import Permission


#---------------------ADD/GET---------------------

def test_add_and_get_permission(permission_repo):
    permission = Permission(name="create_user",description="Puede crear usuarios")
    permission_repo.add(permission)
    retrieved = permission_repo.get(permission.name)
    assert retrieved.name == permission.name

def test_add_existing_permission(permission_repo):
    permission = Permission(name="delete_user")
    permission_repo.add(permission)
    with pytest.raises(ValueError):
        permission_repo.add(permission)

def test_get_nonexistent_permission(permission_repo):
    with pytest.raises(ValueError):
        permission_repo.get("not_exist")

#---------------------FIND---------------------

def test_find_permission(permission_repo):
    permission = Permission(name="edit_user", description="Puede editar los datos")
    permission_repo.add(permission)
    assert permission_repo.find("edit_user") == permission

def test_permission_not_found(permission_repo):
    assert permission_repo.find("notexist_permission") is None

#--------------------UPDATE---------------------

def test_update_existing_permission(permission_repo):
    permission = Permission(name="edit_user", description="Puede editar nombre del usuario")
    permission_repo.add(permission)
    permission_repo.update_description("edit_user", "Edita nombre y correo del usuario")
    assert permission.description == "Edita nombre y correo del usuario"

def test_update_nonexistent_permission(permission_repo):
    #TODO:Agregar error personalizado
    with pytest.raises(ValueError):
        permission_repo.update_description("edit_user", "Edita nombre y correo del usuario")

#---------------------DELETE---------------------

def test_delete_existing_permission(permission_repo):
    permission_repo.add (Permission("edit_user", "Edita nombre y correo del usuario"))
    assert permission_repo.find("edit_user") is not None
    permission_repo.delete("edit_user")
    assert permission_repo.find("edit_user") is None

def test_delete_nonexistent_permission(permission_repo):
    with pytest.raises(ValueError):
        permission_repo.delete("create_user")

#---------------------GET ALL---------------------

def test_get_all_permissions(permission_repo):
    permission_repo.add(Permission(name="create_user"))
    permission_repo.add(Permission(name="create_admin"))
    all_permissions = permission_repo.get_all()
    assert len(all_permissions) == 2

def test_get_all_without_permissions(permission_repo):
    all_permissions = permission_repo.get_all()
    assert len(all_permissions) == 0
    assert all_permissions == []