from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from .config import db_settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    db_settings.database_url, pool_pre_ping=True, echo=False
)

async_session = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    """
    Возвращает асинхронную сессию базы данных.

    Создает сессию, обеспечивает её корректное закрытие и откат изменений
    в случае ошибок. Предназначена для использования как зависимость в FastAPI.

    Обработка ошибок:
        При исключении выполняется rollback, затем сессия закрывается.
    """
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.aclose()
