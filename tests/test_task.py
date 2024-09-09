from src.task.schemas import DisplayTask
from tests.conftest import client, auth_token
from httpx import AsyncClient


async def test_create_task(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.post(
        "/tasks/",
        headers=header,
        json={"title": "string", "description": "string", "status": "pending"},
    )

    assert response.status_code == 201
    response_data = response.json()
    assert DisplayTask(**response_data)


async def test_create_task_invalid_data(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.post(
        "/tasks/",
        headers=header,
        json={"title": "", "description": "string", "status": "pending"},
    )

    assert response.status_code == 422
    response_data = response.json()
    assert response_data["detail"] == "All fields must be provided and cannot be empty."


async def test_create_task_invalid_status(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.post(
        "/tasks/",
        headers=header,
        json={"title": "string", "description": "string", "status": "wrong"},
    )

    assert response.status_code == 422
    response_data = response.json()["detail"][0]
    assert (
        response_data["msg"]
        == "Input should be 'pending', 'in-progress' or 'completed'"
    )
