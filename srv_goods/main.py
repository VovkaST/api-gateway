from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.params import Query
from starlette import status
from starlette.requests import Request

from srv_goods.database import Base, engine
from srv_goods.database import sm as session_maker
from srv_goods.querysets import CategoryQueryset, GoodQueryset
from srv_goods.schemas import (
    CategoryItemViewSchema,
    GoodSchema,
    GoodViewSchema,
)

app = FastAPI()
app.state.engine = engine
app.state.session_maker = session_maker


@app.on_event("startup")
async def on_startup():
    async with app.state.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def on_shutdown():
    # async with app.state.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    await app.state.engine.dispose()


@app.get("/goods/categories", response_model=List[CategoryItemViewSchema])
async def get_good_categories(request: Request):
    async with request.app.state.session_maker() as session:
        rows = await CategoryQueryset.get_multiple(session)
        return [row.to_dict() for row in rows.all()]


@app.get("/goods/list", response_model=List[GoodViewSchema])
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
    async with request.app.state.session_maker() as session:
        rows = await GoodQueryset.get_multiple(
            session,
            limit=limit,
            offset=offset,
            name=name,
            category_id=category_id,
        )
        return [row.to_dict() for row in rows.all()]


@app.get("/goods/{good_id}", response_model=GoodViewSchema)
async def get_good(request: Request, good_id: int):
    async with request.app.state.session_maker() as session:
        good = await GoodQueryset.get_by_id(session, good_id)
        if not good:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Good not found"
            )
        return good.to_dict()


@app.post(
    "/goods",
    response_model=GoodViewSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_good(request: Request, data: GoodSchema):
    sm = request.app.state.session_maker
    async with sm.begin() as session:
        id_ = await GoodQueryset.create(session, **data.dict())
    async with sm() as session:
        good = await GoodQueryset.get_by_id(session, id_)
        return good.to_dict()


@app.patch(
    "/goods/{good_id}",
    response_model=GoodViewSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_good(request: Request, good_id: int, data: GoodSchema):
    sm = request.app.state.session_maker
    async with sm.begin() as session:
        good = await GoodQueryset.get_by_id(session, good_id)
        if not good:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Good not found"
            )
        await GoodQueryset.update(session, good_id, **data.dict())

    async with sm() as session:
        good = await GoodQueryset.get_by_id(session, good_id)
        return good.to_dict()


@app.delete(
    "/goods/{good_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_good(request: Request, good_id: int):
    sm = request.app.state.session_maker
    async with sm.begin() as session:
        good = await GoodQueryset.get_by_id(session, good_id)
        if not good:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Good not found"
            )
        await GoodQueryset.delete(session, good_id)
