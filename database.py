from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://admin:password@localhost:5432/salijang_db"
)

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base(metadata=MetaData(schema="user_schema"))

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    """FastAPI dependency: DB 세션을 생성하고 요청 처리 후 자동 종료합니다."""
    async with AsyncSessionLocal() as session:
        yield session
