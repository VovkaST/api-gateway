from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from srv_clients.models import Client


class ClientQueryset:
    model = Client

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id_: int) -> Client:
        return await session.scalar(
            select(cls.model).where(cls.model.id == id_)
        )
