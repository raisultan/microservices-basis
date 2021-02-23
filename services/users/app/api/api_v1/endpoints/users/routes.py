from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.dependencies import deps

from .errors import UsersAPIError

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        Authorize: AuthJWT = Depends(),
) -> Any:
    Authorize.jwt_required()

    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        password: str = Body(...),
        email: EmailStr = Body(...),
        first_name: str = Body(None),
        last_name: str = Body(None),
) -> Any:
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(status_code=400, detail=UsersAPIError.ALREADY_EXISTS)
    user_in = schemas.UserCreate(
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
        *,
        db: Session = Depends(deps.get_db),
        password: str = Body(None),
        first_name: str = Body(None),
        last_name: str = Body(None),
        email: EmailStr = Body(None),
        Authorize: AuthJWT = Depends(),
) -> Any:
    current_user_email = Authorize.get_jwt_subject()
    current_user = crud.user.get_by_email(db, email=current_user_email)
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)

    if password is not None:
        user_in.password = password
    if first_name is not None:
        user_in.first_name = first_name
    if last_name is not None:
        user_in.last_name = last_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
        db: Session = Depends(deps.get_db),
        Authorize: AuthJWT = Depends(),
) -> Any:
    Authorize.jwt_required()

    current_user_email = Authorize.get_jwt_subject()
    current_user = crud.user.get_by_email(db, email=current_user_email)
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
        user_id: int,
        Authorize: AuthJWT = Depends(),
        db: Session = Depends(deps.get_db),
) -> Any:
    Authorize.jwt_required()

    current_user_email = Authorize.get_jwt_subject()
    current_user = crud.user.get_by_email(db, email=current_user_email)

    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail=UsersAPIError.INACTIVE)
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
        *,
        db: Session = Depends(deps.get_db),
        user_id: int,
        user_in: schemas.UserUpdate,
        Authorize: AuthJWT = Depends(),
) -> Any:
    Authorize.jwt_required()

    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=UsersAPIError.NOT_FOUND)
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
