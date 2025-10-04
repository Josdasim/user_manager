from src.models.user import User
def test_create_user_with_correct_attributes():
    user = User(username = "Tomas", email = "tomas01@correo.com", password = "secret01")

    assert user.username == "Tomas"
    assert user.email == "tomas01@correo.com"
    assert user.password == "secret01"