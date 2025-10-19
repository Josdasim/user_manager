import pytest
from src.security.jwt_manager import JWTManager
from src.exceptions.user_exceptions import TokenExpiredError
from src.constants import messages
from datetime import datetime, timedelta, timezone


def test_generate_token(jwt, sample_payload):
    token = jwt.generate_token(sample_payload)
    assert isinstance(token, str)
    assert len(token) > 10

def test_verify_token(jwt, sample_payload):
    token = jwt.generate_token(sample_payload)
    data = jwt.verify_token(token)
    assert data["username"] == "test_user"

def test_expired_token(jwt, sample_payload):
    token = jwt.generate_token(sample_payload, expire_minutes=-1)
    with pytest.raises(TokenExpiredError, match=messages.TOKEN_EXPIRED):
        jwt.verify_token(token)
    
    
