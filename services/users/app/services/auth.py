from passlib.context import CryptContext


class AuthService:
    @classmethod
    def verify_password(cls, raw_password: str, hashed_password: str) -> bool:
        return cls._get_pwd_context().verify(raw_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls._get_pwd_context().hash(password)

    @staticmethod
    def _get_pwd_context() -> CryptContext:
        return CryptContext(schemes=['bcrypt'], deprecated='auto')
