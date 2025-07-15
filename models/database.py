# my_project/database.py

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from pkg.conf import appmeta
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

ASYNC_DATABASE_URL = appmeta.database_url

engine: AsyncEngine = create_async_engine(
    ASYNC_DATABASE_URL, 
    echo=appmeta.debug,
    connect_args={"check_same_thread": False}
        if ASYNC_DATABASE_URL.startswith("sqlite")
        else None,
    future=True,
    # pool_size=POOL_SIZE,
    # max_overflow=64,
)

_async_session_factory = sessionmaker(engine, class_=AsyncSession)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with _async_session_factory() as session:
        yield session

async def init_db(
    url: str = ASYNC_DATABASE_URL
):
    """创建数据库结构"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)