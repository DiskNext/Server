from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from models.database import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
"""数据库会话依赖，用于路由函数中获取数据库会话"""
