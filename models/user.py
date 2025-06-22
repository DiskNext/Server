# my_project/models/user.py

from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship, Column, func, DateTime
from .base import BaseModel

# TYPE_CHECKING 用于解决循环导入问题，只在类型检查时导入
if TYPE_CHECKING:
    from .group import Group
    from .download import Download
    from .file import File
    from .folder import Folder
    from .order import Order
    from .share import Share
    from .storage_pack import StoragePack
    from .tag import Tag
    from .task import Task
    from .webdav import WebDAV

class User(BaseModel, table=True):
    __tablename__ = 'users'

    email: str = Field(max_length=100, unique=True, index=True, description="用户邮箱，唯一")
    nick: Optional[str] = Field(default=None, max_length=50, description="用户昵称")
    password: str = Field(max_length=255, description="用户密码（加密后）")
    status: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="用户状态: 0=正常, 1=未激活, 2=封禁")
    storage: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="已用存储空间（字节）")
    two_factor: Optional[str] = Field(default=None, max_length=255, description="两步验证密钥")
    avatar: Optional[str] = Field(default=None, max_length=255, description="头像地址")
    options: Optional[str] = Field(default=None, description="用户个人设置 (JSON格式)")
    authn: Optional[str] = Field(default=None, description="WebAuthn 凭证")
    open_id: Optional[str] = Field(default=None, max_length=255, unique=True, index=True, description="第三方登录OpenID")
    score: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="用户积分")
    group_expires: Optional[datetime] = Field(default=None, description="当前用户组过期时间")
    phone: Optional[str] = Field(default=None, max_length=255, unique=True, index=True, description="手机号")
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

    # 外键
    group_id: int = Field(foreign_key="groups.id", index=True, description="所属用户组ID")
    previous_group_id: Optional[int] = Field(default=None, foreign_key="groups.id", description="之前的用户组ID（用于过期后恢复）")
    
    # 关系
    group: "Group" = Relationship(back_populates="users")
    previous_group: Optional["Group"] = Relationship(back_populates="previous_users")
    
    downloads: list["Download"] = Relationship(back_populates="user")
    files: list["File"] = Relationship(back_populates="user")
    folders: list["Folder"] = Relationship(back_populates="owner")
    orders: list["Order"] = Relationship(back_populates="user")
    shares: list["Share"] = Relationship(back_populates="user")
    storage_packs: list["StoragePack"] = Relationship(back_populates="user")
    tags: list["Tag"] = Relationship(back_populates="user")
    tasks: list["Task"] = Relationship(back_populates="user")
    webdavs: list["WebDAV"] = Relationship(back_populates="user")