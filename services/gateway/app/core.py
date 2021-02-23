import functools
from importlib import import_module
from typing import Any, List

from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError
from fastapi import HTTPException, Request, Response, status

from app.network import make_request


def gw_route(
        request_method,
        path: str,
        status_code: int,
        service_url: str,
        post_processing_func: str = None,
        response_schema: str = None,
        is_response_list: bool = False
) -> Any:
    if response_schema:
        response_schema = import_function(response_schema)
        if is_response_list:
            response_schema = List[response_schema]

    app_any = request_method(
        path,
        status_code=status_code,
        response_model=response_schema,
    )

    def wrapper(f):
        @app_any
        @functools.wraps(f)
        async def inner(request: Request, response: Response, **kwargs):
            scope = request.scope

            method = scope['method'].lower()
            path = scope['path']

            url = f'{service_url}{path}'
            try:
                resp_data, status_code_from_service = await make_request(
                    url=url,
                    method=method,
                    data={},
                    headers={},
                )
            except ClientConnectorError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail='Service is unavailable.',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            except ContentTypeError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='Service error.',
                    headers={'WWW-Authenticate': 'Bearer'},
                )

            response.status_code = status_code_from_service

            if all([
                status_code_from_service == status_code,
                post_processing_func
            ]):
                post_processing_f = import_function(post_processing_func)
                resp_data = post_processing_f(resp_data)

            return resp_data

    return wrapper


def import_function(method_path: str) -> Any:
    module, method = method_path.rsplit('.', 1)
    mod = import_module(module)
    return getattr(mod, method, lambda *args, **kwargs: None)
