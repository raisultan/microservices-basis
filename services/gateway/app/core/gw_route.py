import functools
from json import JSONDecodeError
from typing import Any, List

from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError
from fastapi import HTTPException, Request, Response, status

from app.network import make_request
from app.config import settings
from .errors import GWRouteError
from .utils import import_function


def gw_route(
        request_method,
        path: str,
        status_code: int,
        service_url: str,
        post_processing_func: str = None,
        response_model: str = None,
        is_response_list: bool = False,
) -> Any:
    if response_model:
        response_model = import_function(response_model)
        if is_response_list:
            response_model = List[response_model]

    app_any = request_method(
        path,
        status_code=status_code,
        response_model=response_model,
    )

    def wrapper(func: Any) -> Any:
        @app_any
        @functools.wraps(func)
        async def inner(request: Request, response: Response, **kwargs) -> Any:
            scope = request.scope

            method = scope['method'].lower()
            url = f'{service_url}{scope["path"]}'

            if auth_header := request.headers.get('authorization'):
                headers = {'authorization': auth_header}
            else:
                headers = {}

            try:
                data = await request.json()
            except JSONDecodeError:
                data = {}

            try:
                resp_data, status_code_from_service = await make_request(
                    url=url,
                    method=method,
                    headers=headers,
                    data=data,
                )
            except ClientConnectorError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=GWRouteError.SERVICE_UNAVAILABLE,
                )
            except ContentTypeError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=GWRouteError.SERVICE_ERROR,
                )
            if status_code_from_service != status_code:
                raise HTTPException(
                    status_code=status_code_from_service,
                    detail=resp_data.get(settings.SERVICE_ERROR_RESPONSE_DETAIL_KEY),
                )

            response.status_code = status_code_from_service

            if  post_processing_func:
                post_processing_f = import_function(post_processing_func)
                resp_data = post_processing_f(resp_data)

            return resp_data

    return wrapper
