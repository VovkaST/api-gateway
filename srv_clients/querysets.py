from typing import List

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from srv_clients.models import Client


class ClientQueryset:
    model = Client

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> int:
        created = cls.model(**kwargs)
        session.add(created)
        await session.flush([created])
        return created.id

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id_: int) -> Client:
        return await session.scalar(
            select(cls.model).where(cls.model.id == id_)
        )

    @classmethod
    async def get_multiple(
        cls,
        session: AsyncSession,
        limit: int = None,
        offset: int = None,
        **filters,
    ) -> List[Client]:
        where = list()
        if surname := filters.get("surname"):
            where.append(cls.model.surname == surname)
        if name := filters.get("name"):
            where.append(cls.model.name == name)
        if country := filters.get("country"):
            where.append(cls.model.country == country)
        return await session.scalars(
            select(cls.model).where(*where).limit(limit).offset(offset)
        )

    @classmethod
    async def update(cls, session: AsyncSession, id_: int, **kwargs) -> None:
        await session.execute(
            update(cls.model).where(cls.model.id == id_).values(**kwargs)
        )

    @classmethod
    async def delete(cls, session: AsyncSession, id_: int) -> None:
        await session.execute(delete(cls.model).where(cls.model.id == id_))
