from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncAttrs

utcnow = lambda: datetime.now(tz=timezone.utc)

class TableBase(SQLModel, AsyncAttrs):
    __abstract__ = True
    
    id: Optional[int] = Field(default=None, primary_key=True, description="主键ID")
    created_at: datetime = Field(
        default_factory=utcnow,
        description="创建时间",
        )
    updated_at: datetime = Field(
        sa_type=DateTime,
        description="更新时间",
        sa_column_kwargs={"default": utcnow, "onupdate": utcnow},
        default_factory=utcnow
    )
    deleted_at: Optional[datetime] = Field(
        default=None, 
        description="删除时间",
        sa_column={"nullable": True}
    )