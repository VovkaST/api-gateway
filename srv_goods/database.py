from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///goods.sqlite")
sm = sessionmaker(
    engine, autocommit=False, autoflush=False, class_=AsyncSession
)

Base = declarative_base()
