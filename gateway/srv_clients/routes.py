from typing import List

from fastapi import APIRouter, Response
from fastapi.params import Query
from gateway.common import router
from gateway.srv_clients.schemas import ClientSchema, ClientViewSchema
from starlette import status
from starlette.requests import Request

clients_router = APIRouter(prefix="/clients")


@router(
    method=clients_router.get,
    path="",
    response_model=List[ClientViewSchema],
)
async def get_filtered_clients(
    request: Request,
    response: Response,
    surname: str = Query(None, description="Фамилия"),
    name: str = Query(None, description="Имя"),
    country: str = Query(None, description="Страна"),
    limit: int = Query(
        None, description="Количество записей на странице результатов"
    ),
    offset: int = Query(
        None,
        description="Смещение страницы результатов относительно первой записи",
    ),
):
    pass


@router(
    method=clients_router.post,
    path="",
    response_model=ClientViewSchema,
    status_code=status.HTTP_201_CREATED,
    data_key="data",
)
async def create_client(
    request: Request, response: Response, data: ClientSchema
):
    pass


@router(
    method=clients_router.get,
    path="/{client_id}",
    response_model=ClientViewSchema,
)
async def get_client(request: Request, response: Response, client_id: int):
    pass


@router(
    method=clients_router.patch,
    path="/{client_id}",
    response_model=ClientViewSchema,
    status_code=status.HTTP_202_ACCEPTED,
    data_key="data",
)
async def update_client(
    request: Request, response: Response, client_id: int, data: ClientSchema
):
    pass


@router(
    method=clients_router.delete,
    path="/{client_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_client(request: Request, response: Response, client_id: int):
    pass
