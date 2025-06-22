# my_project/database.py

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(
    ASYNC_DATABASE_URL, 
    echo=True,
    connect_args={"check_same_thread": False}
        if ASYNC_DATABASE_URL.startswith("sqlite")
        else None,
    future=True,
    # pool_size=POOL_SIZE,
    # max_overflow=64,
)

_async_session_factory = sessionmaker(engine, class_=AsyncSession)

async def get_session():
    async with _async_session_factory() as session:
        yield session

async def init_db():
    """初始化数据库"""
    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)