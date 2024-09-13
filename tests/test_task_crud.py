from httpx import AsyncClient
from src.task.schemas import DisplayTask
from tests.conftest import iso_date_string


async def test_create_task(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.post(
        "/tasks/",
        headers=header,
        json={
            "title": "1t",
            "description": "string",
            "status": "pending",
            "due_date": iso_date_string,
        },
    )
    response_data = response.json()
    assert response.status_code == 201
    assert DisplayTask(**response_data)


async def test_create_task_invalid_data(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.post(
        "/tasks/",
        headers=header,
        json={
            "title": "",
            "description": "string",
            "status": "pending",
            "due_date": iso_date_string,
        },
    )

    assert response.status_code == 422
    response_data = response.json()
    assert response_data["detail"] == "All fields must be provided and cannot be empty."


async def test_create_task_invalid_status(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.post(
        "/tasks/",
        headers=header,
        json={
            "title": "string",
            "description": "string",
            "status": "wrong",
            "due_date": iso_date_string,
        },
    )

    assert response.status_code == 422
    response_data = response.json()["detail"][0]
    assert (
        response_data["msg"]
        == "Input should be 'pending', 'in-progress' or 'completed'"
    )


async def test_create_task_not_authenticated(client: AsyncClient):
    header = {"Authorization": "wrongtoken"}
    response = await client.post(
        "/tasks/",
        headers=header,
        json={
            "title": "1t",
            "description": "string",
            "status": "pending",
            "due_date": iso_date_string,
        },
    )

    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Not authenticated"


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


async def test_get_tasks_five(client: AsyncClient, auth_token):
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


async def test_get_tasks_not_authenticated(client: AsyncClient):
    header = {"Authorization": "wrong_token"}
    response = await client.get("/tasks/", headers=header)

    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Not authenticated"


async def test_get_task_by_id(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.get("/tasks/id", headers=header, params={"task_id": 1})

    assert response.status_code == 200
    response_data = response.json()
    assert DisplayTask(**response_data)
    assert response_data["id"] == 1


async def test_get_task_by_id_not_found(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.get("/tasks/id", headers=header, params={"task_id": 9999})

    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Task not found"


async def test_get_task_by_id_not_authenticated(client: AsyncClient):
    header = {"Authorization": "wrongtoken"}
    response = await client.get("/tasks/id", headers=header, params={"task_id": 1})

    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Not authenticated"


async def test_edit_task(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.patch(
        "/tasks/id/edit",
        headers=header,
        params={"task_id": 1},
        json={
            "title": "string",
            "description": "string",
            "status": "completed",
        },
    )

    assert response.status_code == 200
    response_data = response.json()
    assert DisplayTask(**response_data)
    response_data["id"] == 1
    response_data["status"] == "completed"


async def test_edit_task_not_found(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.patch(
        "/tasks/id/edit",
        headers=header,
        params={"task_id": 9999},
        json={"title": "string", "description": "string", "status": "completed"},
    )

    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Task not found"


async def test_edit_task_invalid_data(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.patch(
        "/tasks/id/edit",
        headers=header,
        params={"task_id": 1},
        json={"description": "string", "status": "completed"},
    )

    assert response.status_code == 422
    response_data = response.json()["detail"][0]
    assert response_data["msg"] == "Field required"


async def test_edit_task_not_authenticated(client: AsyncClient):
    header = {"Authorization": "wrongtoken"}
    response = await client.patch(
        "/tasks/id/edit",
        headers=header,
        params={"task_id": 1},
        json={"title": "string", "description": "string", "status": "completed"},
    )

    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Not authenticated"


async def test_update_task_status(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.patch(
        "/tasks/id/edit/status",
        headers=header,
        params={"task_id": 1, "status": "in-progress"},
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["msg"] == "status updated"


async def test_update_task_invalid_status(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.patch(
        "/tasks/id/edit/status",
        headers=header,
        params={"task_id": 1, "status": "wrong"},
    )

    assert response.status_code == 422
    response_data = response.json()["detail"][0]
    assert (
        response_data["msg"]
        == "Input should be 'pending', 'in-progress' or 'completed'"
    )


async def test_update_task_status_task_not_found(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.patch(
        "/tasks/id/edit/status",
        headers=header,
        params={"task_id": 9999, "status": "in-progress"},
    )

    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Task not found"


async def test_update_task_status_not_authenticated(client: AsyncClient):
    header = {"Authorization": "wrongtoken"}
    response = await client.patch(
        "/tasks/id/edit/status",
        headers=header,
        params={"task_id": 1, "status": "in-progress"},
    )

    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Not authenticated"


async def test_edit_expiration_date(client: AsyncClient, auth_token):
    header = {
        "Authorization": f"Bearer {auth_token}",
    }
    response = await client.patch(
        "/tasks/id/edit/due_date",
        headers=header,
        json="2024-09-24",
        params={"task_id": 1},
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["msg"] == "Due data updated"


async def test_edit_expiration_past_date(client: AsyncClient, auth_token):
    header = {
        "Authorization": f"Bearer {auth_token}",
    }
    response = await client.patch(
        "/tasks/id/edit/due_date",
        headers=header,
        json="2024-08-24",
        params={"task_id": 1},
    )

    assert response.status_code == 422
    response_data = response.json()
    assert response_data["detail"] == "The new due date cannot be in the past"


async def test_edit_expiration_date_task_not_found(client: AsyncClient, auth_token):
    header = {
        "Authorization": f"Bearer {auth_token}",
    }
    response = await client.patch(
        "/tasks/id/edit/due_date",
        headers=header,
        json="2024-09-24",
        params={"task_id": 9999},
    )

    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Task not found"


async def test_edit_expiration_date_not_authenticated(client: AsyncClient):
    header = {
        "Authorization": "wrongtoken",
    }
    response = await client.patch(
        "/tasks/id/edit/due_date",
        headers=header,
        json="2024-09-24",
        params={"task_id": 22},
    )

    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Not authenticated"


async def test_delete_task(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.delete(
        "/tasks/id/delete",
        headers=header,
        params={"task_id": 1},
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["msg"] == "deleted"


async def test_delete_task_not_found(client: AsyncClient, auth_token):
    header = {"Authorization": f"Bearer {auth_token}"}
    response = await client.delete(
        "/tasks/id/delete",
        headers=header,
        params={"task_id": 9999},
    )

    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Task not found"


async def test_delete_task_not_authenticated(client: AsyncClient):
    header = {"Authorization": "wrongtoken"}
    response = await client.delete(
        "/tasks/id/delete",
        headers=header,
        params={"task_id": 1},
    )

    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Not authenticated"
