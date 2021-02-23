from typing import Any
from fastapi import FastAPI, Request, status, Response
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from app.api.api_v1.api import api_router
from app.config import settings
from app.core import gw_route

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@gw_route(
    request_method=app.get,
    path='/api_v1/users',
    status_code=status.HTTP_200_OK,
    service_url=settings.USERS_SERVICE_URL,
    response_schema='app.schemas.User',
)
async def read_users(request: Request, response: Response) -> Any:
    pass


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.message}
    )
