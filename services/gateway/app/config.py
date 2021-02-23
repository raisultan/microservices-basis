import secrets
from datetime import timedelta
from typing import Union

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api_v1'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    AUTHJWT_SECRET_KEY: str
    AUTHJWT_ACCESS_TOKEN_EXPIRES: Union[int, timedelta] = timedelta(days=5)
    GATEWAY_TIMEOUT: int = 59

    PROJECT_NAME: str = 'gateway-microservice'

    USERS_SERVICE_URL: str = 'http://users:8000'

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str

    class Config:
        case_sensitive = True


settings = Settings()


@AuthJWT.load_config
def get_config():
    return Settings()
