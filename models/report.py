# my_project/models/report.py

from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, Column, func, DateTime
from .base import BaseModel
from datetime import datetime

if TYPE_CHECKING:
    from .share import Share

class Report(BaseModel, table=True):
    __tablename__ = 'reports'

    reason: int = Field(description="举报原因代码")
    description: Optional[str] = Field(default=None, max_length=255, description="补充描述")
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
    
    # 外键
    share_id: int = Field(foreign_key="shares.id", index=True, description="被举报的分享ID")
    
    # 关系
    share: "Share" = Relationship(back_populates="reports")