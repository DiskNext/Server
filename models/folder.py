# my_project/models/folder.py

from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, UniqueConstraint, Column, func, DateTime
from .base import BaseModel
from datetime import datetime

if TYPE_CHECKING:
    from .user import User
    from .policy import Policy
    from .file import File

class Folder(BaseModel, table=True):
    __tablename__ = 'folders'
    __table_args__ = (UniqueConstraint("name", "parent_id", name="uq_folder_name_parent"),)

    name: str = Field(max_length=255, description="目录名")
    
    # 外键
    parent_id: Optional[int] = Field(default=None, foreign_key="folders.id", index=True, description="父目录ID")
    owner_id: int = Field(foreign_key="users.id", index=True, description="所有者用户ID")
    policy_id: int = Field(foreign_key="policies.id", index=True, description="所属存储策略ID")
    
    # 关系
    owner: "User" = Relationship(back_populates="folders")
    policy: "Policy" = Relationship(back_populates="folders")
    
    # 自我引用关系
    parent: Optional["Folder"] = Relationship(back_populates="children", sa_relationship_kwargs={"remote_side": "Folder.id"})
    children: List["Folder"] = Relationship(back_populates="parent")

    files: List["File"] = Relationship(back_populates="folder")