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
        type: SETTINGS_TYPE = None,
        name: str = None,
        value: Optional[str] = None
    ) -> None:
        """
        向数据库内添加设置项目。
        
        :param type: 设置类型/分组
        :type type: SETTINGS_TYPE
        :param name: 设置项名称
        :type name: str
        :param value: 设置值，默认为 None
        :type value: Optional[str]
        """
        from .database import get_session
        
        if isinstance(value, (dict, list)):
            value = str(value)
        
        async for session in get_session():
            new_setting = Setting(type=type, name=name, value=value)
            session.add(new_setting)
        
            await session.commit()

    async def get(
        type: SETTINGS_TYPE,
        name: str
    ) -> Optional['Setting']:
        """
        从数据库中获取指定类型和名称的设置项。
        
        :param type: 设置类型/分组
        :type type: SETTINGS_TYPE
        :param name: 设置项名称
        :type name: str
        
        :return: 返回设置项对象，如果不存在则返回 None
        :rtype: Optional[Setting]
        """
        from .database import get_session
        from sqlmodel import select
        
        async for session in get_session():
            statment = select(Setting).where(
                Setting.type == type, 
                Setting.name == name
            )
            
            result = await session.exec(statment)
            return result.one_or_none()
    
    async def set(
        type: SETTINGS_TYPE,
        name: str,
        value: Optional[str] = None
    ) -> None:
        """
        更新指定类型和名称的设置项的值。
        
        :param type: 设置类型/分组
        :type type: SETTINGS_TYPE
        :param name: 设置项名称
        :type name: str
        :param value: 新的设置值，默认为 None
        :type value: Optional[str]
        
        :raises ValueError: 如果设置项不存在，则抛出异常
        """
        from .database import get_session
        from sqlmodel import select
        
        if isinstance(value, (dict, list)):
            value = str(value)
        
        async for session in get_session():
            statment = select(Setting).where(
                Setting.type == type, 
                Setting.name == name
            )
            
            result = await session.exec(statment)
            setting = result.one_or_none()
            
            if not setting:
                raise ValueError(f"Setting {type}.{name} does not exist.")
            
            # 设置项存在，更新数据
            setting.value = value
            await session.commit()
    
    async def delete(
        type: SETTINGS_TYPE,
        name: str
    ) -> None:
        """
        删除指定类型和名称的设置项。
        
        :param type: 设置类型/分组
        :type type: SETTINGS_TYPE
        :param name: 设置项名称
        :type name: str
        
        :raises ValueError: 如果设置项不存在，则抛出异常
        """
        from .database import get_session
        from sqlmodel import select, delete
        
        async for session in get_session():
            statment = select(Setting).where(
                Setting.type == type, 
                Setting.name == name
            )
            
            result = await session.exec(statment)
            setting = result.one_or_none()
            
            if not setting:
                raise ValueError(f"Setting {type}.{name} does not exist.")
            
            # 设置项存在，删除数据
            await session.delete(setting)
            await session.commit()
