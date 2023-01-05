from typing import List

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from srv_goods.models import Category, Good


class BaseQueryset:
    model = None

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id_: int):
        return await session.scalar(
            select(cls.model).where(cls.model.id == id_)
        )

    @classmethod
    async def get_multiple(
        cls,
        session: AsyncSession,
        limit: int = None,
        offset: int = None,
        *filters,
    ) -> List:
        return await session.scalars(
            select(cls.model).where(*filters).limit(limit).offset(offset)
        )

    @classmethod
    async def update(cls, session: AsyncSession, id_: int, **kwargs) -> None:
        await session.execute(
            update(cls.model).where(cls.model.id == id_).values(**kwargs)
        )

    @classmethod
    async def delete(cls, session: AsyncSession, id_: int) -> None:
        await session.execute(delete(cls.model).where(cls.model.id == id_))


class GoodQueryset(BaseQueryset):
    model = Good

    @classmethod
    async def get_multiple(
        cls,
        session: AsyncSession,
        limit: int = None,
        offset: int = None,
        **filters,
    ) -> List:
        where = list()
        if name := filters.get("name"):
            where.append(cls.model.name.ilike(f"%{name}%"))
        if category_id := filters.get("category_id"):
            where.append(cls.model.category_id == category_id)
        return await super().get_multiple(
            session=session, limit=limit, offset=offset, *where
        )


class CategoryQueryset(BaseQueryset):
    model = Category
