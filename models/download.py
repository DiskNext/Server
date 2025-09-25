# my_project/models/download.py

from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, Column, func, DateTime
from .base import TableBase
from datetime import datetime

if TYPE_CHECKING:
    from .user import User
    from .task import Task
    from .node import Node

class Download(TableBase, table=True):
    __tablename__ = 'downloads'

    status: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="下载状态: 0=进行中, 1=完成, 2=错误")
    type: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="任务类型")
    source: str = Field(description="来源URL或标识")
    total_size: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="总大小（字节）")
    downloaded_size: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="已下载大小（字节）")
    g_id: Optional[str] = Field(default=None, index=True, description="Aria2 GID")
    speed: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="下载速度 (bytes/s)")
    parent: Optional[str] = Field(default=None, description="父任务标识")
    attrs: Optional[str] = Field(default=None, description="额外属性 (JSON格式)")
    error: Optional[str] = Field(default=None, description="错误信息")
    dst: str = Field(description="目标存储路径")
    
    # 外键
    user_id: int = Field(foreign_key="users.id", index=True, description="所属用户ID")
    task_id: Optional[int] = Field(default=None, foreign_key="tasks.id", index=True, description="关联的任务ID")
    node_id: int = Field(foreign_key="nodes.id", index=True, description="执行下载的节点ID")
    
    # 关系
    user: "User" = Relationship(back_populates="downloads")
    task: Optional["Task"] = Relationship(back_populates="downloads")
    node: "Node" = Relationship(back_populates="downloads")