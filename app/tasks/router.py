# STDLIB
from typing import List

# THIRDPARTY
from fastapi import APIRouter, Depends, Query

# FIRSTPARTY
from app.database import DbSession
from app.exceptions import NotTaskException, YouCanNotUpdateTaskException
from app.tasks.dao import TasksDAO
from app.tasks.models import StatusEnum
from app.tasks.schemas import SAddTasks, STasks, SUpdateTasks
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.post("/create")
async def create_task(
    session: DbSession,
    new_task_data: SAddTasks = Depends(),
    user: Users = Depends(get_current_user),
) -> STasks:
    """
    Добавляет задачу.

    Args:
        session: DbSession(AsyncSession) - Асинхронная сессия базы данных.
        new_task_data: Pydantic модель SAddTasks, содержащая данные для добавления новой задачи.
        user: Экземпляр модели Users, представляющий текущего пользователя, полученный через зависимость get_current_user().

    Returns:
        new_task: Экземпляр Pydantic модели STasks, представляющий созданную задачу.
    """
    new_task = await TasksDAO.add(
        session=session,
        user_id=user.uuid,
        name=new_task_data.name,
        description=new_task_data.description,
        status="CREATED",
    )

    return new_task


@router.get("/all")
async def get_all_tasks(
    session: DbSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(5, le=10, ge=5),
    user: Users = Depends(get_current_user),
) -> List[STasks]:
    """
    Отдаёт все задачи пользователя.

    Args:
        session: DbSession(AsyncSession) - Асинхронная сессия базы данных.
        page: Номер страницы, которую хочет получить пользователь.
        page_size: Размер страницы.
        user: Экземпляр модели Users, представляющий текущего пользователя, полученный через зависимость get_current_user().

    Returns:
        all_tasks: Список экземпляров Pydantic модели STasks, представляющий все задачи пользователя.
    """
    all_tasks = await TasksDAO.find_all_users_tasks(
        session=session, user_id=str(user.uuid), page=page, page_size=page_size
    )

    return all_tasks


@router.get("/{task_id}")
async def get_task(
    session: DbSession, task_id: str, user: Users = Depends(get_current_user)
) -> STasks:
    """
    Отдаёт задачу по ID.

    Args:
        session: DbSession(AsyncSession) - Асинхронная сессия базы данных.
        task_id: ID задачи, которая должна быть получена.
        user: Экземпляр модели Users, представляющий текущего пользователя, полученный через зависимость get_current_user().

    Returns:
        new_task: Экземпляр Pydantic модели STasks, представляющий задачу с указанным ID.
    """
    task = await TasksDAO.find_one_or_none(
        session=session, uuid=task_id, user_id=str(user.uuid)
    )

    if not task:
        raise NotTaskException

    return task


@router.patch("/update")
async def update_task_status(
    session: DbSession,
    update_task_data: SUpdateTasks = Depends(),
    user: Users = Depends(get_current_user),
) -> STasks:
    """
    Обновляет статус задачи.

    Args:
        session: DbSession(AsyncSession) - Асинхронная сессия базы данных.
        update_task_data: Pydantic модель SUpdateTasks, содержащая данные для изменения статуса задачи.
        user: Экземпляр модели Users, представляющий текущего пользователя, полученный через зависимость get_current_user().

    Returns:
        updated_task: Экземпляр Pydantic модели STasks, представляющий задачу с обновлённым статусом.
    """
    task = await TasksDAO.find_one_or_none(
        session=session, uuid=update_task_data.task_id, user_id=str(user.uuid)
    )
    if not task:
        raise NotTaskException

    if (
        task.status == StatusEnum.WORKING and update_task_data.status != "COMPLETED"
    ) or task.status == StatusEnum.COMPLETED:
        raise YouCanNotUpdateTaskException

    updated_task = await TasksDAO.update(
        session=session,
        model_id=update_task_data.task_id,
        status=update_task_data.status,
    )

    return updated_task


@router.delete("/delete")
async def delete_task(
    session: DbSession, task_id: str, user: Users = Depends(get_current_user)
) -> None:
    """
    Удаляет задачу.

    Args:
        session: DbSession(AsyncSession) - Асинхронная сессия базы данных.
        task_id: ID задачи, которая должна быть удалена.
        user: Экземпляр модели Users, представляющий текущего пользователя, полученный через зависимость get_current_user().

    Returns:
        None
    """
    task = await TasksDAO.find_one_or_none(
        session=session, uuid=task_id, user_id=str(user.uuid)
    )
    if not task:
        raise NotTaskException

    await TasksDAO.delete(session=session, uuid=task_id)
