from functools import wraps

import aiohttp
from starlette.requests import Request
from starlette.responses import Response


def router(method, path: str, service_url: str, data_key: str = None):
    app_method = method(path)

    def wrapper(endpoint):
        @app_method
        @wraps(endpoint)
        async def decorator(request: Request, response: Response, **kwargs):
            path = request.scope["path"]
            request_method = request.scope["method"].lower()
            url = f"{service_url}{path}"
            data = kwargs.get(data_key)
            data = data.dict() if data else {}
            return await make_request(url, method=request_method, data=data)

    return wrapper


async def make_request(
    url: str, method: str, data: dict = None, headers: dict = None
):
    if not headers:
        headers = {}
    async with aiohttp.ClientSession() as session:
        request = getattr(session, method)
        async with request(url, json=data, headers=headers) as response:
            data = await response.json()
            return data, response.status
