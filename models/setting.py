# my_project/models/setting.py

from typing import Optional, Literal
from sqlmodel import Field, UniqueConstraint, Column, func, DateTime
from .base import BaseModel
from datetime import datetime

SETTINGS_TYPE = Literal[
    "auth",
    "authn",
    "avatar",
    "basic",
    "captcha",
    "cron",
    "file_edit",
    "login",
    "mail",
    "mail_template",
    "mobile",
    "path",
    "preview",
    "pwa",
    "register",
    "retry",
    "share",
    "slave",
    "task",
    "thumb",
    "timeout",
    "upload",
    "version",
    "view",
    "wopi"
]

# 数据库模型
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
    
    delete_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime,
            nullable=True,
            comment="删除时间",
        ),
    )

async def add(
    type: SETTINGS_TYPE,
    name: str,
    value: Optional[str] = None
):
    pass

async def get(
    type: SETTINGS_TYPE,
    name: str
):
    pass