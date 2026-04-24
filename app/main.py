import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.health import router as health_router
from app.db.models import Base
from app.db.session import dispose_engine, engine

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Диагностика
print(f"Ищу .env по пути: {env_path}")
print(f"Файл существует: {env_path.exists()}")
print(f"DATABASE_URL = {os.getenv('DATABASE_URL')}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    print("Shutting down...")
    await dispose_engine()


app = FastAPI(
    title="Task Queue API",
    description="Асинхронная очередь задач на FastAPI + SQLAlchemy",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(health_router)


@app.get("/")
async def root():
    return {"message": "Task Queue API", "docs": "/docs", "health": "/health/db"}
