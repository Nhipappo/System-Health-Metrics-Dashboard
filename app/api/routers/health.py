from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/ping")
async def ping():
    return {"status": "alive", "timestamp": datetime.now().isoformat()}


@router.get("/db", status_code=status.HTTP_200_OK)
async def health_check_database(session: AsyncSession = Depends(get_db)):

    try:
        result = await session.execute(text("SELECT version()"))
        version = result.scalar()

        return {
            "status": "healthy",
            "database": "connected",
            "version": version,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}",
        )


@router.get("/full")
async def health_check_full(session: AsyncSession = Depends(get_db)):
    """
    Более глубокая проверка: выполняет SELECT из таблицы tasks,
    чтобы убедиться, что не только соединение есть, но и схема БД работает.
    """
    from sqlalchemy import func, select

    from app.db.models import Task

    try:
        stmt = select(func.count()).select_from(Task)
        count = await session.execute(stmt)
        _ = count.scalar()

        return {
            "status": "healthy",
            "database": "connected",
            "schema": "valid",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database schema check failed: {str(e)}",
        )
