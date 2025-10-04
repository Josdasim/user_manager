import pytest
from src.models.user import User

def test_create_user_with_correct_attributes():
    user = User(username = "Tomas", email = "tomas01@correo.com", password = "secret01")

    assert user.username == "Tomas"
    assert user.email == "tomas01@correo.com"
    assert user.password == "secret01"

def test_create_user_with_empty_username():
    with pytest.raises(ValueError) as exc_info:
        User(username = "", email = "tomas", password = "secret01")
        assert "username" in str(exc_info.value)

def test_create_user_with_invalid_email():
    with pytest.raises(ValueError) as exc_info:
        User(username = "Tomas", email = "email_invalido", password = "secret01")
        assert "email" in str(exc_info.value)

def test_create_user_with_invalid_password():
    with pytest.raises(ValueError) as exc_info:
        User(username = "Tomas", email = "tomas@correo.com", password = "sec01")
        assert "password" in str(exc_info.value)
