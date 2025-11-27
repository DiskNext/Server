
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, text, Column, JSON
from .base import TableBase
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from .user import User

class GroupOptions(SQLModel):
    archive_download: bool | None = False
    archive_task: bool | None = False
    share_download: bool | None = False
    share_free: bool | None = False
    webdav_proxy: bool | None = False
    aria2: bool | None = False
    relocate: bool | None = False
    source_batch: int | None = 10
    redirected_source: bool | None = False
    available_nodes: List[int] | None = []
    select_node: bool | None = False
    advance_delete: bool | None = False

class Group(TableBase, table=True):
    """用户组模型"""

    name: str = Field(max_length=255, unique=True, description="用户组名")
    policies: str | None = Field(default=None, max_length=255, description="允许的策略ID列表，逗号分隔")
    max_storage: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="最大存储空间（字节）")
    share_enabled: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否允许创建分享")
    web_dav_enabled: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否允许使用WebDAV")
    admin: bool = Field(default=False, description="是否为管理员组")
    speed_limit: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="速度限制 (KB/s), 0为不限制")
    options: GroupOptions = Field(default=GroupOptions, sa_column=Column(JSON), description="其他选项")

    # 关系：一个组可以有多个用户
    user: List["User"] = Relationship(
        back_populates="group",
        sa_relationship_kwargs={"foreign_keys": "User.group_id"}
    )
    previous_user: List["User"] = Relationship(
        back_populates="previous_group",
        sa_relationship_kwargs={"foreign_keys": "User.previous_group_id"}
    )
    
    @staticmethod
    async def create(
        group: Optional["Group"] = None,
        name: str | None = None,
        policies: str | None = None,
        max_storage: int = 0,
        share_enabled: bool = False,
        web_dav_enabled: bool = False,
        speed_limit: int = 0,
        options: dict | None = None,
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
        name: str | None = None,
        policies: str | None = None,
        max_storage: int | None = None,
        share_enabled: bool | None = None,
        web_dav_enabled: bool | None = None,
        speed_limit: int | None = None,
        options: str | None = None
    ) -> Optional["Group"]:
        """
        更新用户组信息。
        
        :param id: 用户组ID
        :type id: int
        :param name: 用户组名
        :type name: str | None
        :param policies: 允许的策略ID列表，逗号分隔
        :type policies: str | None
        :param max_storage: 最大存储空间（字节）
        :type max_storage: int | None
        :param share_enabled: 是否允许创建分享
        :type share_enabled: bool | None
        :param web_dav_enabled: 是否允许使用WebDAV
        :type web_dav_enabled: bool | None
        :param speed_limit: 速度限制 (KB/s), 0为不限制
        :type speed_limit: int | None
        :param options: 其他选项 (JSON格式)
        :type options: str | None
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