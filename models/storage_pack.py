# my_project/models/storage_pack.py

from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship, Column, func, DateTime
from .base import TableBase
from datetime import datetime

if TYPE_CHECKING:
    from .user import User

class StoragePack(TableBase, table=True):
    __tablename__ = 'storage_packs'

    name: str = Field(max_length=255, description="容量包名称")
    active_time: Optional[datetime] = Field(default=None, description="激活时间")
    expired_time: Optional[datetime] = Field(default=None, index=True, description="过期时间")
    size: int = Field(description="容量包大小（字节）")
    
    # 外键
    user_id: int = Field(foreign_key="users.id", index=True, description="所属用户ID")
    
    # 关系
    user: "User" = Relationship(back_populates="storage_packs")