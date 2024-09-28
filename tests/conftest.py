from typing import AsyncGenerator
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi.testclient import TestClient
from src.database import Model, get_async_session
from src.main import app


DATABASE_URL_TEST = "sqlite+aiosqlite:///warehouse_test.db"

engine_test = create_async_engine(DATABASE_URL_TEST, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=engine_test, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


from src.products.models import Product
from src.orders.models import Order, OrderItem


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


client = TestClient(app)


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_test_client:
        yield async_test_client
