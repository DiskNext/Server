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
    
    @staticmethod
    async def create(
        group: "Group"
    ) -> "Group":
        """
        向数据库内添加用户组。
        
        :param group: 用户组对象
        :type group: Group
        :return: 新创建的用户组对象
        :rtype: Group
        """
        
        from .database import get_session
        
        async for session in get_session():
            try:
                session.add(group)
                await session.commit()
                await session.refresh(group)
            except Exception as e:
                await session.rollback()
                raise e
        return group
    
    @staticmethod
    async def get(
        id: int = None
        ) -> Optional["Group"]:
        """
        获取用户组信息。
        
        :param id: 用户组ID，默认为 None
        :type id: int
        
        :return: 用户组对象或 None
        :rtype: Optional[Group]
        """
        from .database import get_session
        from sqlmodel import select
        
        session = get_session()
        
        if id is None:
            return None
        
        async for session in get_session():
            statement = select(Group).where(Group.id == id)
            result = await session.exec(statement)
            group = result.one_or_none()
            
            if group:
                return group
            else:
                return None