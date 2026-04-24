import uuid

from sqlalchemy import case, func, select, text

from app.db.models.enums.task_status import TaskStatus
from app.db.models.task import Task
from app.db.session import AsyncSession


async def get_task_stats(session: AsyncSession) -> dict:

    count_stmt = select(Task.status, func.count().label("count")).group_by(Task.status)
    count_result = await session.execute(count_stmt)
    count_by_status = {status.value: count for status, count in count_result.all()}

    avg_stmt = select(
        func.avg(func.extract("epoch", Task.updated_at - Task.created_at)).label(
            "avg_seconds"
        )
    ).where(Task.status == TaskStatus.COMPLETED)

    avg_result = await session.execute(avg_stmt)
    avg_seconds = avg_result.scalar_one_or_none()

    return {
        "count_by_status": count_by_status,
        "avg_execution_seconds": float(avg_seconds) if avg_seconds else 0.0,
    }
