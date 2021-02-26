from typing import Any

from fastapi import APIRouter, Request, Response, status

from app.config import settings
from app.core import gw_route

router = APIRouter()


@gw_route(
    request_method=router.get,
    path='/api_v1/users',
    status_code=status.HTTP_200_OK,
    service_url=settings.USERS_SERVICE_URL,
    response_model='app.schemas.UserRead',
    is_response_list=True,
)
async def read_users(request: Request, response: Response) -> Any:
    pass


@gw_route(
    request_method=router.post,
    path='/api_v1/users',
    status_code=status.HTTP_201_CREATED,
    service_url=settings.USERS_SERVICE_URL,
    response_model='app.schemas.UserCreate',
)
async def create_user(request: Request, response: Response) -> Any:
    pass


@gw_route(
    request_method=router.get,
    path='/api_v1/users/me',
    status_code=status.HTTP_200_OK,
    service_url=settings.USERS_SERVICE_URL,
    response_model='app.schemas.UserRead',
)
async def read_user_me(request: Request, response: Response) -> Any:
    pass


@gw_route(
    request_method=router.put,
    path='/api_v1/users/me',
    status_code=status.HTTP_200_OK,
    service_url=settings.USERS_SERVICE_URL,
    response_model='app.schemas.UserUpdate',
)
async def update_user_me(request: Request, response: Response) -> Any:
    pass


@gw_route(
    request_method=router.get,
    path='/api_v1/users/{user_id}',
    status_code=status.HTTP_200_OK,
    service_url=settings.USERS_SERVICE_URL,
    response_model='app.schemas.UserRead',
)
async def read_user(request: Request, response: Response) -> Any:
    pass


@gw_route(
    request_method=router.put,
    path='/api_v1/users/{user_id}',
    status_code=status.HTTP_200_OK,
    service_url=settings.USERS_SERVICE_URL,
    response_model='app.schemas.UserUpdate',
)
async def update_user(request: Request, response: Response) -> Any:
    pass


@gw_route(
    request_method=router.delete,
    path='/api_v1/users/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    service_url=settings.USERS_SERVICE_URL,
)
async def delete_user(request: Request, response: Response) -> Any:
    pass
