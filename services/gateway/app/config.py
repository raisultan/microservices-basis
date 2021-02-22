import secrets
from fastapi_jwt_auth import AuthJWT

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api_v1'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    AUTHJWT_SECRET_KEY: str

    PROJECT_NAME: str = 'gateway-microservice'

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
