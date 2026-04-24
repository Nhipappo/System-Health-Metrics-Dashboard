import uuid
from typing import Any

from sqlalchemy import update

from app.db.models.enums.task_status import TaskStatus
from app.db.models.task import Task
from app.db.session import AsyncSession


async def update_task_status(
    session: AsyncSession,
    task_id: uuid.UUID,
    status: TaskStatus,
    result: dict | None = None,
) -> bool:

    async with session.begin():
        values: dict[str, Any] = {"status": status}
        if result is not None:
            values["result"] = result

        stmt = (
            update(Task).where(Task.id == task_id).values(**values).returning(Task.id)
        )

        db_result = await session.execute(stmt)
        updated_id = db_result.scalar_one_or_none()
        return updated_id is not None
