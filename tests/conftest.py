import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.database import get_session, metadata
from src.main import app

async_engine_test = create_async_engine(url=settings.test_database_url)

async_session_test = async_sessionmaker(
    async_engine_test, class_=AsyncSession, expire_on_commit=False
)

metadata.bind = async_engine_test


today_date = datetime.now(timezone.utc).date() + timedelta(days=7)
# Combine date with time set to 00:00:00
# date_with_time = datetime.combine(today_date, datetime.min.time(), tzinfo=timezone.utc)
# Convert to ISO 8601 string
# iso_date_string = date_with_time.isoformat()
iso_date_string = today_date.isoformat()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def session(event_loop):
    async with async_engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)

    async with async_session_test() as session:
        yield session

    async with async_engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
async def client(session):
    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        try:
            yield session
        finally:
            await session.close()

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# @pytest.fixture(scope="session")
# async def auth_token(client):
#     login_response = await client.post(
#         "/user/login",
#         data={"username": "tester@example.com", "password": "tester"},
#     )

#     assert login_response.status_code == 202
#     token = login_response.json()["access_token"]
#     yield token


@pytest.fixture(scope="session")
async def auth_token(client):

    register_response = await client.post(
        "/user/",
        json={
            "email": "tester@example.com",
            "username": "tester",
            "password": "tester",
        },
    )

    if register_response.status_code == 422:
        assert register_response.json()["detail"] == "User already exist"
    else:
        assert register_response.status_code == 201

    login_response = await client.post(
        "/user/login",
        data={"username": "tester@example.com", "password": "tester"},
    )

    assert login_response.status_code == 202
    token = login_response.json()["access_token"]
    yield token


@pytest.fixture(scope="session")
async def create_posts(client, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    for i in range(2, 16):
        response = await client.post(
            "/tasks/",
            headers=header,
            json={
                "title": f"{i}t",
                "description": "string",
                "status": "pending",
                "due_date": iso_date_string,
            },
        )

        assert response.status_code == 201
