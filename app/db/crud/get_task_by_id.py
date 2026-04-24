import uuid

from sqlalchemy import select

from app.db.models.task import Task
from app.db.session import AsyncSession


async def get_task_by_id(session: AsyncSession, task_id: uuid.UUID) -> Task | None:

    task = select(Task).where(Task.id == task_id)
    result = await session.execute(task)

    return result.scalar_one_or_none()
