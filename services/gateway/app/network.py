import aiohttp
import async_timeout

from app.config import settings


async def make_request(
        *,
        url: str,
        method: str,
        data: dict = None,
        headers: dict = None
):
    data = data or {}

    with async_timeout.timeout(settings.GATEWAY_TIMEOUT):
        async with aiohttp.ClientSession() as session:
            request = getattr(session, method)
            async with request(url, json=data, headers=headers) as response:
                data = await response.json()
                return (data, response.status)
