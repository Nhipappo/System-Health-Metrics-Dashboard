import logging
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.shemas.task_create import TaskCreate
from app.api.shemas.task_response import TaskResponse
from app.core.db import get_db
from app.db.crud.create_task import create_task
from app.db.crud.get_task_by_id import get_task_by_id
from app.db.crud.get_tasks import get_tasks
from app.db.models.enums.task_status import TaskStatus
from app.db.models.task import Task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/")
async def add_task(task_data: TaskCreate, session: AsyncSession = Depends(get_db)):
    payload = task_data.payload
    if payload is None:
        raise HTTPException(400, "Payload cannot be empty")
    assert task_data.payload is not None

    try:
        task_id = await create_task(session, payload)

        logger.info(f"Task created: {task_id}")
        return {"task_id": task_id}
    except Exception as e:
        logger.error(f"Failed to create task: {str(e)}")
        raise HTTPException(500, "Internal server error")


@router.get("/")
async def get_tasks_from_db(
    limit: int = 10,
    offset: int = 0,
    status: TaskStatus | None = None,
    session: AsyncSession = Depends(get_db),
):

    result = await get_tasks(session=session, limit=limit, offset=offset, status=status)

    return {
        "items": [TaskResponse.model_validate(task) for task in result],
        "total": len(result),
        "limit": limit,
        "offset": offset,
    }


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_from_db(task_id: UUID, session: AsyncSession = Depends(get_db)):
    task = await get_task_by_id(session, task_id)

    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    return TaskResponse.model_validate(task)
