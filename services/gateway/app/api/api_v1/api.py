from fastapi import APIRouter

from app.config import settings
from app.api.api_v1.endpoints.auth import routes as auth_routes
from app.api.api_v1.endpoints.users import routes as users_routes

api_router = APIRouter()
api_router.include_router(auth_routes.router, prefix=f'{settings.API_V1_STR}/auth', tags=['auth'])  # TODO: temp solution
api_router.include_router(users_routes.router, prefix='', tags=['users'])
