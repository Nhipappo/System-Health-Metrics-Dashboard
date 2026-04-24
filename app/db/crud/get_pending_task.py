from datetime import timezone

from sqlalchemy import func, select, update

from app.db.models.enums.task_status import TaskStatus
from app.db.models.task import Task
from app.db.session import AsyncSession


async def get_pending_task(session: AsyncSession) -> Task | None:
    async with session.begin():
        stmt = (
            select(Task)
            .where(Task.status == TaskStatus.PENDING)
            .order_by(Task.created_at)
            .limit(1)
            .with_for_update(skip_locked=True)
        )

        result = await session.execute(stmt)
        task = result.scalar_one_or_none()

        if not task:
            return None

        task.status = TaskStatus.PROCESSING

        return task
