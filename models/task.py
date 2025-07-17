# my_project/models/task.py

from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, Column, func, DateTime
from .base import BaseModel
from datetime import datetime

if TYPE_CHECKING:
    from .user import User
    from .download import Download

class Task(BaseModel, table=True):
    __tablename__ = 'tasks'

    status: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="任务状态: 0=排队中, 1=处理中, 2=完成, 3=错误")
    type: int = Field(description="任务类型")
    progress: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="任务进度 (0-100)")
    error: Optional[str] = Field(default=None, description="错误信息")
    props: Optional[str] = Field(default=None, description="任务属性 (JSON格式)")
    
    # 外键
    user_id: "int" = Field(foreign_key="users.id", index=True, description="所属用户ID")
    
    # 关系
    user: "User" = Relationship(back_populates="tasks")
    downloads: list["Download"] = Relationship(back_populates="task")