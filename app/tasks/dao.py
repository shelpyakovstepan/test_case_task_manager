# THIRDPARTY
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.dao.base import BaseDao
from app.tasks.models import Tasks


class TasksDAO(BaseDao):
    model = Tasks

    @classmethod
    async def find_all_users_tasks(
        cls,
        session: AsyncSession,
        user_id: str,
        page: int,
        page_size: int,
    ):
        offset = (page - 1) * page_size

        all_tasks_query = (
            select(Tasks)
            .where(Tasks.user_id == user_id)
            .offset(offset)
            .limit(page_size)
        )

        all_tasks = await session.execute(all_tasks_query)

        return all_tasks.scalars().all()
