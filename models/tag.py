
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, UniqueConstraint, Column, func, DateTime
from .base import TableBase
from datetime import datetime

if TYPE_CHECKING:
    from .user import User

class Tag(TableBase, table=True):
    """标签模型"""

    __table_args__ = (UniqueConstraint("name", "user_id", name="uq_tag_name_user"),)

    name: str = Field(max_length=255, description="标签名称")
    icon: str | None = Field(default=None, max_length=255, description="标签图标")
    color: str | None = Field(default=None, max_length=255, description="标签颜色")
    type: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="标签类型: 0=手动, 1=自动")
    expression: str | None = Field(default=None, description="自动标签的匹配表达式")
    
    # 外键
    user_id: int = Field(foreign_key="user.id", index=True, description="所属用户ID")
    
    # 关系
    user: "User" = Relationship(back_populates="tags")