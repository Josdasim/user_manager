import jwt
from datetime import datetime, timedelta, timezone
from src.config.settings import settings
from src.exceptions.user_exceptions import TokenExpiredError, TokenInvalidError
from src.constants import messages

class JWTManager:

    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.default_exp_minutes = settings.JWT_EXPIRE_MINUTES

    def generate_token(self, payload:dict, expire_minutes:int = 60) -> str:
        expiration = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes or self.default_exp_minutes)
        payload_copy = payload.copy()
        payload_copy["exp"] = expiration
        payload_copy["iat"] = datetime.now(timezone.utc)
        payload_copy["iss"] = "user-service"

        token = jwt.encode(payload_copy, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token:str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError(messages.TOKEN_EXPIRED)
        except jwt.InvalidTokenError:
            raise TokenInvalidError(messages.TOKEN_INVALID)

