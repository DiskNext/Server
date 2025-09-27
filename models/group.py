# my_project/models/group.py

from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, text, Column, JSON
from .base import TableBase
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from .user import User

class GroupOptions(SQLModel):
    archive_download: Optional[bool] = False
    archive_task: Optional[bool] = False
    share_download: Optional[bool] = False
    share_free: Optional[bool] = False
    webdav_proxy: Optional[bool] = False
    aria2: Optional[bool] = False
    relocate: Optional[bool] = False
    source_batch: Optional[int] = 10
    redirected_source: Optional[bool] = False
    available_nodes: Optional[List[int]] = []
    select_node: Optional[bool] = False
    advance_delete: Optional[bool] = False

class Group(TableBase, table=True):
    __tablename__ = 'groups'

    name: str = Field(max_length=255, unique=True, description="用户组名")
    policies: Optional[str] = Field(default=None, max_length=255, description="允许的策略ID列表，逗号分隔")
    max_storage: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="最大存储空间（字节）")
    share_enabled: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否允许创建分享")
    web_dav_enabled: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否允许使用WebDAV")
    admin: bool = Field(default=False, description="是否为管理员组")
    speed_limit: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="速度限制 (KB/s), 0为不限制")
    options: GroupOptions = Field(default=GroupOptions, sa_column=Column(JSON), description="其他选项")

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
        group: Optional["Group"] = None,
        name: Optional[str] = None,
        policies: Optional[str] = None,
        max_storage: int = 0,
        share_enabled: bool = False,
        web_dav_enabled: bool = False,
        speed_limit: int = 0,
        options: Optional[dict] = None,
    ) -> "Group":
        """
        向数据库内添加用户组。如果提供了 `group` 参数，则使用该对象，否则创建一个新的用户组对象。
        
        :param group: 用户组对象
        :type group: Group
        :return: 新创建的用户组对象
        :rtype: Group
        """
        
        from .database import get_session
        import json
        
        if not group:
            
            if not name:
                raise ValueError("Group name is required.")
            
            group = Group(
                name=name,
                policies=policies,
                max_storage=max_storage,
                share_enabled=share_enabled,
                web_dav_enabled=web_dav_enabled,
                speed_limit=speed_limit,
                options=json.dumps(options) if options else None,   
            )
        
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
            try:
                statement = select(Group).where(Group.id == id)
                result = await session.exec(statement)
                group = result.one_or_none()
                
                if group:
                    return group
                else:
                    return None
            except Exception as e:
                raise e
    
    @staticmethod
    async def set(
        id: int,
        name: Optional[str] = None,
        policies: Optional[str] = None,
        max_storage: Optional[int] = None,
        share_enabled: Optional[bool] = None,
        web_dav_enabled: Optional[bool] = None,
        speed_limit: Optional[int] = None,
        options: Optional[str] = None
    ) -> Optional["Group"]:
        """
        更新用户组信息。
        
        :param id: 用户组ID
        :type id: int
        :param name: 用户组名
        :type name: Optional[str]
        :param policies: 允许的策略ID列表，逗号分隔
        :type policies: Optional[str]
        :param max_storage: 最大存储空间（字节）
        :type max_storage: Optional[int]
        :param share_enabled: 是否允许创建分享
        :type share_enabled: Optional[bool]
        :param web_dav_enabled: 是否允许使用WebDAV
        :type web_dav_enabled: Optional[bool]
        :param speed_limit: 速度限制 (KB/s), 0为不限制
        :type speed_limit: Optional[int]
        :param options: 其他选项 (JSON格式)
        :type options: Optional[str]
        :return: 更新后的用户组对象或 None
        :rtype: Optional[Group]
        """
        
        from .database import get_session
        from sqlmodel import select
        
        async for session in get_session():
            try:
                statement = select(Group).where(Group.id == id)
                result = await session.exec(statement)
                group = result.one_or_none()
                
                if not group:
                    raise ValueError(f"Group with id {id} not found.")
                
                if name is not None:
                    group.name = name
                if policies is not None:
                    group.policies = policies
                if max_storage is not None:
                    group.max_storage = max_storage
                if share_enabled is not None:
                    group.share_enabled = share_enabled
                if web_dav_enabled is not None:
                    group.web_dav_enabled = web_dav_enabled
                if speed_limit is not None:
                    group.speed_limit = speed_limit
                if options is not None:
                    group.options = options
                
                session.add(group)
                await session.commit()
                
                return group
            except Exception as e:
                await session.rollback()
                raise e

    @staticmethod
    async def delete(
        id: int
    ) -> None:
        """
        删除用户组。
        
        :param id: 用户组ID
        :type id: int
        """
        from .database import get_session
        from sqlmodel import select
        
        async for session in get_session():
            try:
                statement = select(Group).where(Group.id == id)
                result = await session.exec(statement)
                group = result.one_or_none()
                
                if group is None:
                    raise ValueError(f"Group with id {id} not found.")
                
                await session.delete(group)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e