from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from srv_clients.models import Client


class ClientQueryset:
    model = Client

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id_: int) -> Client:
        return await session.scalar(
            select(cls.model).where(cls.model.id == id_)
        )

    @classmethod
    async def update(cls, session: AsyncSession, id_: int, **kwargs) -> None:
        await session.execute(
            update(cls.model).where(cls.model.id == id_).values(**kwargs)
        )

    @classmethod
    async def delete(cls, session: AsyncSession, id_: int):
        await session.execute(delete(cls.model).where(cls.model.id == id_))
