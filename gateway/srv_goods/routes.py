from typing import List

from fastapi import APIRouter, Request
from fastapi.params import Query
from gateway.common import router
from gateway.srv_goods.schemas import (
    CategoryItemViewSchema,
    GoodSchema,
    GoodViewSchema,
)
from starlette import status

goods_router = APIRouter(prefix="/goods")


@router(
    method=goods_router.get,
    path="/categories",
    response_model=List[CategoryItemViewSchema],
)
async def get_good_categories(request: Request):
    pass


@router(
    method=goods_router.get, path="/list", response_model=List[GoodViewSchema]
)
async def get_filtered_goods(
    request: Request,
    name: str = Query(None, description="Наименование товара"),
    category_id: int = Query(None, description="Категория"),
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
    method=goods_router.get, path="/{good_id}", response_model=GoodViewSchema
)
async def get_good(request: Request, good_id: int):
    pass


@router(
    method=goods_router.post,
    path="",
    response_model=GoodViewSchema,
    status_code=status.HTTP_201_CREATED,
    data_key="data",
)
async def create_good(request: Request, data: GoodSchema):
    pass


@router(
    method=goods_router.patch,
    path="/{good_id}",
    response_model=GoodViewSchema,
    status_code=status.HTTP_202_ACCEPTED,
    data_key="data",
)
async def update_good(request: Request, good_id: int, data: GoodSchema):
    pass


@router(
    method=goods_router.delete,
    path="/{good_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_good(request: Request, good_id: int):
    pass
