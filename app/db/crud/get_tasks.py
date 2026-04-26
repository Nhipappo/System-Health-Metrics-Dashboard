from typing import Optional, Sequence

from sqlalchemy import select

from app.db.models.enums.task_status import TaskStatus
from app.db.models.task import Task
from app.db.session import AsyncSession


async def get_tasks(
    session: AsyncSession,
    limit: int = 10,
    offset: int = 0,
    status: Optional[TaskStatus] = None,
) -> Sequence[Task]:

    query = select(Task)

    if status:
        query = query.where(Task.status == status)

    query = query.order_by(Task.created_at.desc())

    query = query.offset(offset).limit(limit)

    result = await session.execute(query)
    tasks = result.scalars().all()

    return tasks
