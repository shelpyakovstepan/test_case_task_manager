# THIRDPARTY
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.tasks.dao import TasksDAO
from app.tasks.models import Tasks
from app.users.models import Users


class TestTasksDAO:
    @pytest.mark.parametrize(
        "name, description",
        [("Правильное название", ""), ("Правильное название", "Правильное описание")],
    )
    async def test_add(
        self, get_session: AsyncSession, create_user: Users, name: str, description: str
    ):
        task = await TasksDAO.add(
            session=get_session,
            user_id=create_user.uuid,
            name=name,
            description=description,
            status="CREATED",
        )

        assert task is not None
        assert task.user_id == create_user.uuid
        assert task.name == name
        assert task.description == description

    @pytest.mark.parametrize("page, page_size", [(1, 5)])
    async def test_find_all_users_tasks(
        self,
        get_session: AsyncSession,
        create_user: Users,
        create_task: Tasks,
        page: int,
        page_size: int,
    ):
        tasks = await TasksDAO.find_all_users_tasks(
            session=get_session,
            user_id=str(create_user.uuid),
            page=page,
            page_size=page_size,
        )

        assert tasks is not None

    async def test_find_one_or_none(
        self, get_session: AsyncSession, create_user: Users, create_task: Tasks
    ):
        task = await TasksDAO.find_one_or_none(
            session=get_session, uuid=create_task.uuid, user_id=str(create_user.uuid)
        )

        assert task is not None
        assert task.uuid == create_task.uuid
        assert task.user_id == create_user.uuid

    async def test_find_one_or_none_fail(
        self, get_session: AsyncSession, create_user: Users
    ):
        task = await TasksDAO.find_one_or_none(
            session=get_session,
            uuid="dcf11111-1111-1111-b1b1-c111c1fbe111",
            user_id=str(create_user.uuid),
        )

        assert task is None

    @pytest.mark.parametrize("status", [("WORKING"), ("COMPLETED")])
    async def test_update(
        self,
        get_session: AsyncSession,
        create_user: Users,
        create_task: Tasks,
        status: str,
    ):
        updated_task = await TasksDAO.update(
            session=get_session, model_id=create_task.uuid, status=status
        )

        assert updated_task is not None

    async def test_delete(
        self, get_session: AsyncSession, create_user: Users, create_task: Tasks
    ):
        await TasksDAO.delete(session=get_session, uuid=create_task.uuid)

        assert (
            await TasksDAO.find_by_id(session=get_session, model_id=create_task.uuid)
            is None
        )
