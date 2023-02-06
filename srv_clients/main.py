from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.params import Query
from starlette import status

from srv_clients.database import Base, engine
from srv_clients.database import sm as session_maker
from srv_clients.querysets import ClientQueryset
from srv_clients.schemas import ClientSchema, ClientViewSchema

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


@app.get("/clients", response_model=List[ClientViewSchema])
async def get_filtered_clients(
    request: Request,
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
    async with request.app.state.session_maker() as session:
        rows = await ClientQueryset.get_multiple(
            session,
            surname=surname,
            name=name,
            country=country,
            limit=limit,
            offset=offset,
        )
        return [row.to_dict() for row in rows.all()]


@app.post(
    "/clients",
    response_model=ClientViewSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_client(request: Request, data: ClientSchema):
    sm = request.app.state.session_maker
    async with sm.begin() as session:
        id_ = await ClientQueryset.create(session, **data.dict())
    async with sm() as session:
        client = await ClientQueryset.get_by_id(session, id_)
        return client.to_dict()


@app.get("/clients/{client_id}", response_model=ClientViewSchema)
async def get_client(request: Request, client_id: int):
    async with request.app.state.session_maker() as session:
        client = await ClientQueryset.get_by_id(session, client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found",
            )
        return client.to_dict()


@app.patch(
    "/clients/{client_id}",
    response_model=ClientViewSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_client(request: Request, client_id: int, data: ClientSchema):
    sm = request.app.state.session_maker
    async with sm.begin() as session:
        client = await ClientQueryset.get_by_id(session, client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found",
            )
        await ClientQueryset.update(session, client_id, **data.dict())

    async with sm() as session:
        client = await ClientQueryset.get_by_id(session, client_id)
        return client.to_dict()


@app.delete(
    "/clients/{client_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_client(request: Request, client_id: int):
    sm = request.app.state.session_maker
    async with sm.begin() as session:
        client = await ClientQueryset.get_by_id(session, client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        await ClientQueryset.delete(session, client_id)
