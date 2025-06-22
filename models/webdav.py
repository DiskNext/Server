# my_project/models/webdav.py

from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, UniqueConstraint, text, Column, func, DateTime
from .base import BaseModel
from datetime import datetime

if TYPE_CHECKING:
    from .user import User

class WebDAV(BaseModel, table=True):
    __tablename__ = 'webdavs'
    __table_args__ = (UniqueConstraint("name", "user_id", name="uq_webdav_name_user"),)

    name: str = Field(max_length=255, description="WebDAV账户名")
    password: str = Field(max_length=255, description="WebDAV密码（加密后）")
    root: str = Field(default="/", sa_column_kwargs={"server_default": "'/'"}, description="根目录路径")
    readonly: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否只读")
    use_proxy: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否使用代理下载")
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
    user_id: int = Field(foreign_key="users.id", index=True, description="所属用户ID")
    
    # 关系
    user: "User" = Relationship(back_populates="webdavs")