from datetime import datetime, timedelta
from typing import Any, Final, Union

from jose import jwt
from passlib.context import CryptContext

from .config import settings


class AuthService:
    ALGORITHM: Final[str] = 'HS256'
    PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    def create_access_token(
            cls,
            subject: Union[str, Any],
            expires_delta: timedelta = None,
    ) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {'exp': expire, 'sub': str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def verify_password(cls, raw_password: str, hashed_password: str) -> bool:
        return cls.PWD_CONTEXT.verify(raw_password, hashed_password)


    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.PWD_CONTEXT.hash(password)
