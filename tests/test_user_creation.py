import pytest
from src.models.user import User
from src.exceptions.user_exceptions import UserValidationError
from src.constants import messages


def test_create_user_with_correct_attributes(sample_user_data_1):
    new_user=User(**sample_user_data_1)
    assert new_user.username == sample_user_data_1["username"]
    assert new_user.email == sample_user_data_1["email"]
    assert new_user.password == sample_user_data_1["password"]

@pytest.mark.parametrize(
        "username, email, password, expected_exception",[
            ("", "tomas01@correo.com", "secret01", messages.USER_INVALID_USERNAME),
            ("Tomas", "email_invalido", "secret01", messages.USER_INVALID_EMAIL)
        ],
        ids = lambda val: ""
)
def test_create_user_with_invalid_fields(username, email, password, expected_exception):
    with pytest.raises(UserValidationError, match=expected_exception):
        User(username, email, password)
