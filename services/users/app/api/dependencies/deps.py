from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from app import crud, models
from app.db.session import SessionLocal
from .errors import DBError


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
) -> models.User:
    Authorize.jwt_required()

    user_email = Authorize.get_jwt_subject()
    user = crud.user.read_by_email(db, email=user_email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=DBError.USER_NOT_FOUND)
    return user


def get_current_active_user(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=DBError.INACTIVE_USER)
    return current_user
