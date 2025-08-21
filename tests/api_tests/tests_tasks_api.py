# THIRDPARTY
from httpx import AsyncClient
import pytest

# FIRSTPARTY
from app.tasks.models import Tasks
from app.users.models import Users


class TestTasksAPI:
    @pytest.mark.parametrize(
        "name, description, status_code",
        [
            ("Правильное название", "", 200),
            ("Правильное название", "Правильное описание", 200),
            ("", "Описание", 422),
        ],
    )
    async def test_create_task(
        self,
        create_user: Users,
        name: str,
        description: str,
        status_code: int,
        authenticated_ac: AsyncClient,
    ):
        response = await authenticated_ac.post(
            "/tasks/create", params={"name": name, "description": description}
        )

        assert response.status_code == status_code

    async def test_get_all_tasks(
        self, create_user: Users, create_task: Tasks, authenticated_ac: AsyncClient
    ):
        response = await authenticated_ac.get("/tasks/all")

        assert response.status_code == 200
        assert response.json() is not None

    @pytest.mark.parametrize(
        "task_id, status_code",
        [
            ("dcf11111-1111-1111-b1b1-c111c1fbe111", 409),
        ],
    )
    async def test_get_task(
        self,
        create_user: Users,
        create_task: Tasks,
        task_id: str,
        status_code: int,
        authenticated_ac: AsyncClient,
    ):
        response_error_status_code = await authenticated_ac.get(
            f"/tasks/{task_id}", params={"task_id": task_id}
        )

        assert response_error_status_code.status_code == status_code

        response = await authenticated_ac.get(
            f"/tasks/{str(create_task.uuid)}", params={"task_id": str(create_task.uuid)}
        )

        assert response.status_code == 200

    @pytest.mark.parametrize(
        "status, status_code",
        [("WORKING", 200), ("COMPLETED", 200), ("WRONG_STATUS", 422)],
    )
    async def test_update_task_status(
        self,
        create_user: Users,
        create_task: Tasks,
        status: str,
        status_code: int,
        authenticated_ac: AsyncClient,
    ):
        response = await authenticated_ac.patch(
            "/tasks/update", params={"task_id": str(create_task.uuid), "status": status}
        )

        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "task_id, status, status_code",
        [
            ("dcf11111-1111-1111-b1b1-c111c1fbe111", "WORKING", 409),
        ],
    )
    async def test_update_task_status_409_status_code(
        self,
        create_user: Users,
        create_task: Tasks,
        task_id: str,
        status: str,
        status_code: int,
        authenticated_ac: AsyncClient,
    ):
        response_409_status_code = await authenticated_ac.patch(
            "/tasks/update", params={"task_id": task_id, "status": status}
        )

        assert response_409_status_code.status_code == status_code

    async def test_delete_task(
        self, create_user: Users, create_task: Tasks, authenticated_ac: AsyncClient
    ):
        response = await authenticated_ac.delete(
            "/tasks/delete", params={"task_id": str(create_task.uuid)}
        )

        assert response.status_code == 200

    @pytest.mark.parametrize(
        "task_id, status_code", [("dcf11111-1111-1111-b1b1-c111c1fbe111", 409)]
    )
    async def test_delete_task_fail(
        self,
        create_user: Users,
        create_task: Tasks,
        task_id: str,
        status_code: int,
        authenticated_ac: AsyncClient,
    ):
        response = await authenticated_ac.delete(
            "/tasks/delete", params={"task_id": task_id}
        )

        assert response.status_code == status_code
