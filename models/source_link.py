# my_project/models/source_link.py

from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, Column, func, DateTime
from .base import BaseModel
from datetime import datetime

if TYPE_CHECKING:
    from .file import File

class SourceLink(BaseModel, table=True):
    __tablename__ = 'source_links'

    name: str = Field(max_length=255, description="链接名称")
    downloads: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="通过此链接的下载次数")
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=func.now(),
            comment="创建时间",
        ),
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
            comment="更新时间",
        ),
    )
    
    delete_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="删除时间",
        ),
    )
    
    # 外键
    file_id: int = Field(foreign_key="files.id", index=True, description="关联的文件ID")
    
    # 关系
    file: "File" = Relationship(back_populates="source_links")