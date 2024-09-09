from httpx import AsyncClient

from src.task.schemas import DisplayTask


async def test_create_task(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.post(
        "/tasks/",
        headers=header,
        json={"title": "1t", "description": "string", "status": "pending"},
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


async def test_get_tasks_default_params(client: AsyncClient, auth_token, create_posts):
    """
    :param offset: int = 0,
    :param limit: int = 10,
    """
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.get(
        "/tasks/",
        headers=header,
    )

    assert response.status_code == 200
    response_data = response.json()
    assert DisplayTask(**response_data[0])
    assert len(response_data) == 10


async def test_get_five_tasks(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.get(
        "/tasks/",
        headers=header,
        params={"offset": 10, "limit": 15},
    )

    assert response.status_code == 200
    response_data = response.json()
    assert DisplayTask(**response_data[0])
    assert len(response_data) == 5


async def test_get_tasks_empty_list(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.get(
        "/tasks/",
        headers=header,
        params={"offset": 16, "limit": 17},
    )

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 0


async def test_get_tasks_unauthorized(client: AsyncClient):
    header = {"Authorization": "wrong_token"}
    response = await client.get("/tasks/", headers=header)

    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Not authenticated"
