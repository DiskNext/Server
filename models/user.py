from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship, UniqueConstraint
from .base import TableBase

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

class User(TableBase, table=True):
    __tablename__ = 'users'

    email: str = Field(max_length=100, unique=True, index=True)
    """用户邮箱，唯一"""
    
    phone: str | None = Field(default=None, nullable=True, index=True)
    """用户手机号，唯一"""
    
    nick: str | None = Field(default=None, max_length=50)
    """用户昵称"""
    password: str = Field(max_length=255)
    """用户密码（加密后）"""
    status: bool | None = Field(default=None, sa_column_kwargs={"server_default": "0"})
    """用户状态: True=正常, None=未激活, False=封禁"""
    storage: int = Field(default=0, sa_column_kwargs={"server_default": "0"})
    """已用存储空间（字节）"""
    two_factor: str | None = Field(default=None, max_length=255)
    """两步验证密钥"""
    avatar: str | None = Field(default=None, max_length=255)
    """头像地址"""
    options: str | None = Field(default=None)
    """用户个人设置 (JSON格式)"""
    authn: str | None = Field(default=None)
    """WebAuthn 凭证"""
    open_id: str | None = Field(default=None, max_length=255, unique=True, index=True)
    """第三方登录OpenID"""
    score: int = Field(default=0, sa_column_kwargs={"server_default": "0"})
    """用户积分"""
    group_expires: datetime | None = Field(default=None)
    """当前用户组过期时间"""
    phone: str | None = Field(default=None, max_length=255, unique=True, index=True)
    """手机号"""

    # 外键
    group_id: int = Field(foreign_key="groups.id", index=True)
    """所属用户组ID"""
    previous_group_id: int | None = Field(default=None, foreign_key="groups.id")
    """之前的用户组ID（用于过期后恢复）"""
    
    # 关系
    group: "Group" = Relationship(
        back_populates="users",
        sa_relationship_kwargs={
            "foreign_keys": "User.group_id"
        }
    )
    previous_group: Optional["Group"] = Relationship(
        back_populates="previous_users",
        sa_relationship_kwargs={
            "foreign_keys": "User.previous_group_id"
        }
    )
    
    downloads: list["Download"] = Relationship(back_populates="user")
    files: list["File"] = Relationship(back_populates="user")
    folders: list["Folder"] = Relationship(back_populates="owner")
    orders: list["Order"] = Relationship(back_populates="user")
    shares: list["Share"] = Relationship(back_populates="user")
    storage_packs: list["StoragePack"] = Relationship(back_populates="user")
    tags: list["Tag"] = Relationship(back_populates="user")
    tasks: list["Task"] = Relationship(back_populates="user")
    webdavs: list["WebDAV"] = Relationship(back_populates="user")
    