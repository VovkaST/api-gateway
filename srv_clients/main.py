from typing import List

from fastapi import APIRouter, FastAPI, HTTPException
from sqlalchemy import delete, select, update
from starlette import status
from starlette.requests import Request

from srv_clients.database import Base, engine
from srv_clients.database import sm as session_maker
from srv_clients.models import Client
from srv_clients.querysets import ClientQueryset
from srv_clients.schemas import ClientSchema, ClientViewSchema

app = FastAPI()
app.state.engine = engine
app.state.session_maker = session_maker

router = APIRouter(prefix="/clients")


@router.on_event("startup")
async def on_startup():
    async with app.state.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def on_shutdown():
    # async with app.state.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    await app.state.engine.dispose()


@router.get("/list", response_model=List[ClientViewSchema])
async def get_all_clients(request: Request):
    async with request.app.state.session_maker() as session:
        rows = await session.scalars(select(Client))
        return [row.__dict__ for row in rows.all()]


@router.get("/{client_id}")
async def get_client(request: Request, client_id: int):
    async with request.app.state.session_maker() as session:
        client = await ClientQueryset.get_by_id(session, client_id)
        return client.__dict__


@router.post(
    "", response_model=ClientViewSchema, status_code=status.HTTP_201_CREATED
)
async def create_client(request: Request, data: ClientSchema):
    sm = request.app.state.session_maker
    async with sm.begin() as session:
        created = Client(**data.dict())
        session.add(created)
        await session.flush([created])
        id_ = created.id
    async with sm() as session:
        client = await ClientQueryset.get_by_id(session, id_)
        return client.__dict__


@router.patch(
    "/{client_id}",
    response_model=ClientViewSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_client(request: Request, client_id: int, data: ClientSchema):
    sm = request.app.state.session_maker
    async with sm.begin() as session:
        client = await ClientQueryset.get_by_id(session, client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        await ClientQueryset.update(session, client_id, **data.dict())

    async with sm() as session:
        client = await ClientQueryset.get_by_id(session, client_id)
        return client.__dict__


@router.delete(
    "/{client_id}",
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


app.include_router(router)
