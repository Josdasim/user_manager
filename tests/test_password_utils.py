from src.security.password_utils import hash_password, verify_password

def test_hash_password_create_valid_hash():
    password = "testpassword"
    password_hashed = hash_password(password)
    assert password != password_hashed

def test_verify_fail_with_wrong_password():
    password = "testpassword"
    password_hashed = hash_password(password)
    assert verify_password("newtest1",password_hashed) == False