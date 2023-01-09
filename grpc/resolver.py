from typing import Tuple

import aiohttp

SERVICE_MAP = {
    "clients": "0.0.0.0:8001",
    "goods": "0.0.0.0:8002",
}


async def resolve(
    path: str, method: str, data: dict = None, headers: dict = None
) -> dict:
    _, service_name, *_ = path.split("/")
    service_host = SERVICE_MAP[service_name]
    url = f"http://{service_host}{path}"
    response, status_code = await make_request(url, method, data, headers)
    return response


async def make_request(
    url: str, method: str, data: dict = None, headers: dict = None
) -> Tuple[dict, int]:
    if not headers:
        headers = {}
    if not data:
        data = {}

    async with aiohttp.ClientSession() as session:
        request = getattr(session, method)
        async with await request(url, json=data, headers=headers) as response:
            response_json = await response.json()
            return response_json, response.status
