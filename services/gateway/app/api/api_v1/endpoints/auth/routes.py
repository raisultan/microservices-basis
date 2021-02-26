from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from app import crud, schemas
from app.api.dependencies import deps
from .errors import AuthError

router = APIRouter()


@router.post('/access', response_model=schemas.AccessToken)
def get_access_token(
        db: Session = Depends(deps.get_db),
        *,
        user: schemas.UserLoginForm,
        Authorize: AuthJWT = Depends(),
) -> dict:
    user = crud.user.authenticate(
        db,
        email=user.email,
        password=user.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=AuthError.INCORRECT_CREDS,
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=AuthError.INACTIVE_USER,
        )

    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
    }


@router.post('/refresh', response_model=schemas.RefreshToken)
def get_refresh_token(
        db: Session = Depends(deps.get_db),
        Authorize: AuthJWT = Depends()
) -> dict:
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {
        'access_token': new_access_token,
        'token_type': 'bearer',
    }
