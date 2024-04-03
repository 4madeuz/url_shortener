import asyncio
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select, text
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from main import app
from src.core.config import settings
from src.db.postgres import Base
from src.models.url_models import URL


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_engine() -> AsyncEngine:
    async_engine = create_async_engine(settings.dsn, echo=False, future=True)
    yield async_engine
    await async_engine.dispose()


@pytest_asyncio.fixture(scope='function')
async def async_session(async_engine: AsyncEngine):
    async_session: type[AsyncEngine] = sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
    )

    async with async_session() as session:
        yield session

    async with async_engine.begin() as conn:
        await conn.execute(
            text("TRUNCATE {} CASCADE;".format(",".join(table.name for table in reversed(Base.metadata.sorted_tables))))
        )


@pytest_asyncio.fixture(scope='session')
def test_client():
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture
async def sample_url(async_session: AsyncSession) -> URL:
    url = URL(
        original_url='original_url',
        short_url='short_url',
        timestamps=[datetime.now(tz=None), datetime.now(tz=None)]
    )
    async_session.add(url)
    await async_session.commit()
    await async_session.refresh(url)
    return url
