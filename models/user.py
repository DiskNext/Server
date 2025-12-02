from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship
from pydantic import BaseModel

from .base import TableBase, SQLModelBase

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

"""
Option 需求
- 主题 跟随系统/浅色/深色
- 颜色方案 参考.response.ThemeModel
- 语言
- 时区
- 切换到不同存储策略是否提醒
"""

class WebAuthnInfo(BaseModel):
    """WebAuthn 信息模型"""

    credential_id: str
    """凭证 ID"""

    credential_public_key: str
    """凭证公钥"""

    sign_count: int
    """签名计数器"""

    credential_device_type: bool
    """是否为平台认证器"""

    credential_backed_up: bool
    """凭证是否已备份"""

    transports: list[str]
    """支持的传输方式"""

class User(TableBase, table=True):
    """用户模型"""

    username: str = Field(max_length=50, unique=True, index=True)
    """用户名，唯一，一经注册不可更改"""
    
    nick: str | None = Field(default=None, max_length=50)
    """用于公开展示的名字，可使用真实姓名或昵称"""

    password: str = Field(max_length=255)
    """用户密码（加密后）"""

    status: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
    """用户状态: True=正常, False=封禁"""

    storage: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, ge=0)
    """已用存储空间（字节）"""

    two_factor: str | None = Field(default=None, min_length=32, max_length=32)
    """两步验证密钥"""

    avatar: str | None = Field(default=None, max_length=255)
    """头像地址"""

    options: str | None = Field(default=None)
    """[TODO] 用户个人设置 需要更改，参考上方的需求"""

    authn: str | None = Field(default=None)
    """[TODO] WebAuthn 凭证，可不存，也可设置一个或多个"""

    github_open_id: str | None = Field(default=None, unique=True, index=True)
    """Github OpenID"""

    qq_open_id: str | None = Field(default=None, unique=True, index=True)
    """QQ OpenID"""

    score: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, ge=0)
    """用户积分"""

    group_expires: datetime | None = Field(default=None)
    """当前用户组过期时间"""

    phone: str | None = Field(default=None, max_length=32, unique=True, index=True)
    """手机号"""

    # 外键
    group_id: int = Field(foreign_key="group.id", index=True)
    """所属用户组ID"""

    previous_group_id: int | None = Field(default=None, foreign_key="group.id")
    """之前的用户组ID（用于过期后恢复）"""

    # [TODO] 待考虑：根目录 Object ID
    
    # 关系
    group: "Group" = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "foreign_keys": "User.group_id"
        }
    )
    previous_group: Optional["Group"] = Relationship(
        back_populates="previous_user",
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

    def to_public(self) -> "UserPublic":
        """转换为公开 DTO，排除敏感字段"""
        return UserPublic.model_validate(self)


class UserPublic(SQLModelBase):
    """用户公开信息 DTO，用于 API 响应"""

    id: int | None = None
    """用户ID"""

    username: str
    """用户名"""

    nick: str | None = None
    """昵称"""

    status: bool = True
    """用户状态"""

    storage: int = 0
    """已用存储空间（字节）"""

    avatar: str | None = None
    """头像地址"""

    score: int = 0
    """用户积分"""

    group_expires: datetime | None = None
    """用户组过期时间"""

    group_id: int
    """所属用户组ID"""

    created_at: datetime | None = None
    """创建时间"""

    updated_at: datetime | None = None
    """更新时间"""
    