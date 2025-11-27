
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