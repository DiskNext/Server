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
    
    # 外键
    file_id: int = Field(foreign_key="files.id", index=True, description="关联的文件ID")
    
    # 关系
    file: "File" = Relationship(back_populates="source_links")