# my_project/models/group.py

from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, text, Column, func, DateTime
from .base import BaseModel
from datetime import datetime

if TYPE_CHECKING:
    from .user import User

class Group(BaseModel, table=True):
    __tablename__ = 'groups'

    name: str = Field(max_length=255, unique=True, description="用户组名")
    policies: Optional[str] = Field(default=None, max_length=255, description="允许的策略ID列表，逗号分隔")
    max_storage: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="最大存储空间（字节）")
    share_enabled: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否允许创建分享")
    web_dav_enabled: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否允许使用WebDAV")
    speed_limit: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="速度限制 (KB/s), 0为不限制")
    options: Optional[str] = Field(default=None, description="其他选项 (JSON格式)")
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

    # 关系：一个组可以有多个用户
    users: List["User"] = Relationship(
        back_populates="group",
        sa_relationship_kwargs={"foreign_keys": "User.group_id"}
    )
    previous_users: List["User"] = Relationship(
        back_populates="previous_group",
        sa_relationship_kwargs={"foreign_keys": "User.previous_group_id"}
    )
    
    async def add_group(self, name: str, policies: Optional[str] = None, max_storage: int = 0, 
                     share_enabled: bool = False, web_dav_enabled: bool = False, 
                     speed_limit: int = 0, options: Optional[str] = None) -> "Group":
        """
        向数据库内添加用户组。
        
        :param name: 用户组名
        :type name: str
        :param policies: 允许的策略ID列表，逗号分隔，默认为 None
        :type policies: Optional[str]
        :param max_storage: 最大存储空间（字节），默认为 0
        :type max_storage: int
        :param share_enabled: 是否允许创建分享，默认为 False
        :type share_enabled: bool
        :param web_dav_enabled: 是否允许使用WebDAV，默认为 False
        :type web_dav_enabled: bool
        :param speed_limit: 速度限制 (KB/s), 0为不限制，默认为 0
        :type speed_limit: int
        :param options: 其他选项 (JSON格式)，默认为 None
        :type options: Optional[str]
        :return: 新创建的用户组对象
        :rtype: Group
        """
        
        from .database import get_session
        session = get_session()
        
        new_group = Group(
            name=name,
            policies=policies,
            max_storage=max_storage,
            share_enabled=share_enabled,
            web_dav_enabled=web_dav_enabled,
            speed_limit=speed_limit,
            options=options
        )
        session.add(new_group)
        
        session.commit()
        session.refresh(new_group)