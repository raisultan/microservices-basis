from fastapi import APIRouter

from app.api.api_v1.endpoints.auth import routes as auth_routes

api_router = APIRouter()
api_router.include_router(auth_routes.router, prefix='/auth', tags=['auth'])
