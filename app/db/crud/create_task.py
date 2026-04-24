from app.db.models.task import Task
from app.db.session import AsyncSession


async def create_task(session: AsyncSession, payload: dict) -> int:
    async with session.begin():
        task = Task(payload=payload)
        session.add(task)
        await session.flush()

        return task.id
