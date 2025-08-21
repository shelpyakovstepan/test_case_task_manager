# STDLIB
from typing import AsyncGenerator
import uuid

# THIRDPARTY
import httpx
from httpx import AsyncClient
import pytest
from sqlalchemy import and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.database import SessionLocal
from app.main import app as fastapi_app
from app.tasks.models import StatusEnum, Tasks
from app.users.models import Users


@pytest.fixture(scope="function")
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Фикстура для создания экземпляра сессии базы данных для тестов.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy для проведения тестов.
    """
    test_session = SessionLocal
    async with test_session() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest.fixture
async def create_user(
    get_session: AsyncSession,
) -> AsyncGenerator[Users, None]:
    """Фикстура для создания тестового пользователя в БД.

    Args:
        get_session (AsyncSession): Асинхронная сессия базы данных.

    Yields:
        Users: Экземпляр модели Users, представляющий созданного пользователя.
    """
    uuid_ = uuid.uuid4()

    user = Users(
        uuid=uuid_,
        email="test@test.com",
        hashed_password="$2b$12$hTdYOVyjy.GCmFP2ArKncuG5Hg5Vlwh0qovYYNp10VRMc5129FmO6",
    )
    get_session.add(user)
    await get_session.commit()

    yield user

    delete_tasks_query = delete(Tasks).where(Tasks.user_id == uuid_)
    await get_session.execute(delete_tasks_query)

    query = delete(Users).where(
        and_(
            Users.uuid == uuid_,
        )
    )
    await get_session.execute(query)
    await get_session.commit()


@pytest.fixture
async def create_task(
    get_session: AsyncSession,
    create_user: Users,
) -> AsyncGenerator[Tasks, None]:
    """Фикстура для создания тестовой задачи в БД.

    Args:
        get_session (AsyncSession): Асинхронная сессия базы данных.
        create_user: Экземпляр модели Users.

    Yields:
        Tasks: Экземпляр модели Tasks, представляющий созданную задачу.
    """
    uuid_ = uuid.uuid4()
    user_id = create_user.uuid
    name = "Тестовая задача"
    description = "Тестовое описание задачи"
    status = StatusEnum.CREATED

    task = Tasks(
        uuid=uuid_,
        user_id=user_id,
        name=name,
        description=description,
        status=status,
    )

    get_session.add(task)
    await get_session.commit()

    yield task

    query = delete(Tasks).where(
        and_(
            Tasks.uuid == uuid_,
        )
    )
    await get_session.execute(query)
    await get_session.commit()


@pytest.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Отдаёт неаутентифицированного пользователя для тестов."""
    async with AsyncClient(
        base_url="http://test", transport=httpx.ASGITransport(app=fastapi_app)
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def authenticated_ac(create_user) -> AsyncGenerator[AsyncClient, None]:
    """Отдаёт аутентифицированного пользователя для тестов."""
    async with AsyncClient(
        base_url="http://test", transport=httpx.ASGITransport(app=fastapi_app)
    ) as ac:
        await ac.post(
            "/auth/login",
            json={
                "email": "test@test.com",
                "password": "kolobok",
            },
        )
        assert ac.cookies["access_token"]
        yield ac
