from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from .config import db_settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    db_settings.database_url, poll_pre_ping=True, echo=False
)

async_session = async_sessionmaker(
    async_engine, _class=AsyncSession, expire_on_commit=False
)


async def get_db():
    "Yields database session"
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.aclose()
