from fastapi import APIRouter

from app.api.api_v1.endpoints.users import routes as users_routes
from app.api.api_v1.endpoints.auth import routes as auth_routes

api_router = APIRouter()
api_router.include_router(auth_routes.router, tags=['auth'])
api_router.include_router(users_routes.router, prefix='/users', tags=['users'])
