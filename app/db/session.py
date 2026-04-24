from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,               
    async_sessionmaker   
    )
from sqlalchemy.pool import NullPool
import os


DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://user:pass@localhost:5432/mydb"
)
ECHO_ENABLE = os.getenv(
    "DB_ECHO_ENABLE", 
    False
)


engine = create_async_engine(
    DATABASE_URL,
    echo=ECHO_ENABLE,
    pool_pre_ping=True,
    pool_size = 20,
    max_overflow=10
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def dispose_engine():
    await engine.dispose()