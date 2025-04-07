import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.core.config import db_settings
from app.core.database import Base, get_db


testing_async_engine = create_async_engine(
    db_settings.test_database_url, pool_pre_ping=True, echo=False
)

testing_async_session = async_sessionmaker(
    testing_async_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture
async def setup_database():
    """Create and drop test DB tables."""
    async with testing_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with testing_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await testing_async_engine.dispose()


@pytest.fixture
async def client(setup_database):
    """Provide a test client with overridden DB session."""
    async with testing_async_session() as session:

        async def override_get_db():
            yield session

        app.dependency_overrides[get_db] = override_get_db

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac

        app.dependency_overrides.clear()
        await session.close()
