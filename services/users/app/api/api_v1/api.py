from fastapi import APIRouter

from app.api.api_v1.endpoints.users import routes as users_routes

api_router = APIRouter()
api_router.include_router(users_routes.router, prefix="/users", tags=["users"])
