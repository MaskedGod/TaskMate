from httpx import AsyncClient
import pytest
from sqlalchemy import text
from src.auth.schemas import UserCreate, UserOut
from tests.conftest import client, session, event_loop, auth_token


async def test_health(client: AsyncClient):
    response = await client.get("/user/health")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "Database connection is healthy!"


async def test_register_user_missing_email_field(client: AsyncClient):
    response = await client.post(
        "/user/",
        json={
            "email": "",
            "username": "tester",
            "password": "tester",
        },
    )

    assert response.status_code == 422
    response_data = response.json()["detail"][0]
    assert (
        response_data["msg"]
        == "value is not a valid email address: The email address is not valid. It must have exactly one @-sign."
    )


async def test_register_user_missing_username_field(client: AsyncClient):
    response = await client.post(
        "/user/",
        json={
            "email": "tester@example.com",
            "username": "",
            "password": "tester",
        },
    )

    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "All fields must be provided and cannot be empty."


async def test_register(client: AsyncClient):
    response = await client.post(
        "/user/",
        json={
            "email": "tester@example.com",
            "username": "tester",
            "password": "tester",
        },
    )

    assert response.status_code == 201
    response_data = response.json()
    assert UserOut(**response_data)


async def test_user_authentication(client: AsyncClient):
    response = await client.post(
        "/user/login",
        data={"username": "tester@example.com", "password": "tester"},
    )

    response_json = response.json()
    assert response.status_code == 202
    assert "access_token" in response_json
    assert response_json["token_type"] == "bearer"


async def test_login_invalid_credentials(client: AsyncClient):
    response = await client.post(
        "/login",
        data={"username": "wrong_username", "password": "wrong_password"},
    )
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Not Found"


async def test_get_current_user(client: AsyncClient, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await client.get("/user/me", headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["email"] == "tester@example.com"
