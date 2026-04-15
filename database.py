from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
import os

# To easily switch between local docker and AWS RDS later
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://admin:password@localhost:5432/salijang_db"
)

# Use asyncpg for high performance I/O
engine = create_async_engine(DATABASE_URL, echo=True)

# Schema specifies 'user_schema' for isolation
metadata_obj = declarative_base().metadata
metadata_obj.schema = "user_schema"
Base = declarative_base(metadata=metadata_obj)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
