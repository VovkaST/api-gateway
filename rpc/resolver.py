from typing import Tuple

import aiohttp

SERVICE_MAP = {
    "clients": "0.0.0.0:8001",
    "goods": "0.0.0.0:8002",
}


async def resolve(
    method: str,
    path: str,
    params: dict = None,
    data: dict = None,
    headers: dict = None,
) -> Tuple[dict, int]:
    """
    Функция определяет по первой части url-запроса к какому сервису происходит обращение, перенаправляет в него
    запрос и возвращает ответ в виде словаря и код статуса.
    """
    _, service_name, *_ = path.split("/")
    service_host = SERVICE_MAP[service_name]
    url = f"http://{service_host}{path}"
    response, status_code = await make_request(
        url, method, params, data, headers
    )
    return response, status_code


async def make_request(
    url: str,
    method: str,
    params: dict = None,
    data: dict = None,
    headers: dict = None,
) -> Tuple[dict, int]:
    """
    Выполнение запроса, тип которого определяется параметром method, по url-адресу. Возвращает ответ в виде словаря
    и код статуса.
    """

    if not headers:
        headers = {}
    if not data:
        data = {}

    async with aiohttp.ClientSession() as session:
        request = getattr(session, method)
        async with await request(
            url, params=params, json=data, headers=headers
        ) as response:
            response_json = await response.json()
            return response_json, response.status
