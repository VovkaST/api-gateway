from typing import List

from fastapi import APIRouter
from gateway.common import router
from gateway.srv_clients.schemas import ClientSchema, ClientViewSchema
from starlette import status
from starlette.requests import Request

clients_router = APIRouter(prefix="/clients")


@router(
    method=clients_router.get,
    path="/list",
    response_model=List[ClientViewSchema],
)
async def get_all_clients(request: Request):
    pass


@router(
    method=clients_router.get,
    path="/{client_id}",
    response_model=ClientViewSchema,
)
async def get_client(request: Request, client_id: int):
    pass


@router(
    method=clients_router.post,
    path="",
    data_key="data",
    response_model=ClientViewSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_client(request: Request, data: ClientSchema):
    pass


@router(
    method=clients_router.patch,
    path="/{client_id}",
    data_key="data",
    response_model=ClientViewSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_client(request: Request, client_id: int, data: ClientSchema):
    pass


@router(
    method=clients_router.delete,
    path="/{client_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_client(request: Request, client_id: int):
    pass
