from typing import Generator, Final

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from ..core.auth import AuthService
from ..core.config import settings
from ..db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


class DBService:
    class Error:
        INVALID_CREDS: Final[str] = 'Could not validate credentials'
        USER_NOT_FOUND: Final[str] = 'User was not found'
        INACTIVE_USER: Final[str] = 'User is inactive'
        NOT_SUPERUSER: Final[str] = 'The user does not have enough privileges'

    @staticmethod
    def get_db() -> Generator:
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()

    @classmethod
    def get_current_user(
            cls,
            db: Session = Depends(get_db),
            token: str = Depends(reusable_oauth2)
    ) -> models.User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[AuthService.ALGORITHM]
            )
            token_data = schemas.TokenPayload(**payload)
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=cls.Error.INVALID_CREDS,
            )

        user = crud.user.get(db, id=token_data.sub)
        if not user:
            raise HTTPException(status_code=404, detail=cls.Error.USER_NOT_FOUND)
        return user

    @classmethod
    def get_current_active_user(
            cls,
            current_user: models.User = Depends(get_current_user),
    ) -> models.User:
        if not crud.user.is_active(current_user):
            raise HTTPException(status_code=400, detail=cls.Error.INACTIVE_USER)
        return current_user

    @classmethod
    def get_current_active_superuser(
            cls,
            current_user: models.User = Depends(get_current_user),
    ) -> models.User:
        if not crud.user.is_superuser(current_user):
            raise HTTPException(status_code=400, detail=cls.Error.NOT_SUPERUSER)
        return current_user
