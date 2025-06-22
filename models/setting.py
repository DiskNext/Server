# my_project/models/setting.py

from typing import Optional
from sqlmodel import Field, UniqueConstraint, Column, func, DateTime
from .base import BaseModel
from datetime import datetime

class Setting(BaseModel, table=True):
    __tablename__ = 'settings'
    __table_args__ = (UniqueConstraint("type", "name", name="uq_setting_type_name"),)

    type: str = Field(max_length=255, description="设置类型/分组")
    name: str = Field(max_length=255, description="设置项名称")
    value: Optional[str] = Field(default=None, description="设置值")
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