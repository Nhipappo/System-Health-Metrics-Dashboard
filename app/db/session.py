import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

ECHO_ENABLE = os.getenv("DB_ECHO_ENABLE", "").lower() in ("true", "1", "yes")

engine = create_async_engine(
    DATABASE_URL, echo=ECHO_ENABLE, pool_pre_ping=True, pool_size=20, max_overflow=10
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def dispose_engine():
    await engine.dispose()
