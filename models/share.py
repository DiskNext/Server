
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship, text, CheckConstraint, UniqueConstraint, Index
from .base import TableBase
from datetime import datetime

if TYPE_CHECKING:
    from .user import User
    from .report import Report

class Share(TableBase, table=True):
    """分享模型"""

    __table_args__ = (
        UniqueConstraint("code", name="uq_share_code"),
        CheckConstraint("(file_id IS NOT NULL) <> (folder_id IS NOT NULL)", name="ck_share_xor"),
        Index("ix_share_source_name", "source_name"),
        Index("ix_share_user_created", "user_id", "created_at"),
    )

    code: str = Field(max_length=64, nullable=False, index=True, description="分享码")
    password: str | None = Field(default=None, max_length=255, description="分享密码（加密后）")
    
    is_dir: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否为目录分享")
    file_id: int | None = Field(default=None, foreign_key="file.id", index=True, description="文件ID（二选一）")
    folder_id: int | None = Field(default=None, foreign_key="folder.id", index=True, description="目录ID（二选一）")
    
    views: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="浏览次数")
    downloads: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="下载次数")
    remain_downloads: int | None = Field(default=None, description="剩余下载次数 (NULL为不限制)")
    expires: datetime | None = Field(default=None, description="过期时间 (NULL为永不过期)")
    preview_enabled: bool = Field(default=True, sa_column_kwargs={"server_default": text("true")}, description="是否允许预览")
    source_name: str | None = Field(default=None, max_length=255, index=True, description="源名称（冗余字段，便于展示）")
    score: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="兑换此分享所需的积分")
    
    # 外键
    user_id: int = Field(foreign_key="user.id", index=True, description="创建分享的用户ID")
    
    # 关系
    user: "User" = Relationship(back_populates="shares")
    reports: list["Report"] = Relationship(back_populates="share")