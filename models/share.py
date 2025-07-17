# my_project/models/share.py

from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship, text, Column, func, DateTime
from .base import BaseModel
from datetime import datetime

if TYPE_CHECKING:
    from .user import User
    from .report import Report

class Share(BaseModel, table=True):
    __tablename__ = 'shares'

    password: Optional[str] = Field(default=None, max_length=255, description="分享密码（加密后）")
    is_dir: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否为目录分享")
    source_id: int = Field(description="源文件或目录的ID")
    views: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="浏览次数")
    downloads: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="下载次数")
    remain_downloads: Optional[int] = Field(default=None, description="剩余下载次数 (NULL为不限制)")
    expires: Optional[datetime] = Field(default=None, description="过期时间 (NULL为永不过期)")
    preview_enabled: bool = Field(default=True, sa_column_kwargs={"server_default": text("true")}, description="是否允许预览")
    source_name: Optional[str] = Field(default=None, max_length=255, index=True, description="源名称（冗余字段，便于展示）")
    score: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="兑换此分享所需的积分")
    
    # 外键
    user_id: int = Field(foreign_key="users.id", index=True, description="创建分享的用户ID")
    
    # 关系
    user: "User" = Relationship(back_populates="shares")
    reports: list["Report"] = Relationship(back_populates="share")