
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, UniqueConstraint, text, Column, func, DateTime
from .base import TableBase

if TYPE_CHECKING:
    from .user import User

class WebDAV(TableBase, table=True):
    __tablename__ = 'webdavs'
    __table_args__ = (UniqueConstraint("name", "user_id", name="uq_webdav_name_user"),)

    name: str = Field(max_length=255, description="WebDAV账户名")
    password: str = Field(max_length=255, description="WebDAV密码（加密后）")
    root: str = Field(default="/", sa_column_kwargs={"server_default": "'/'"}, description="根目录路径")
    readonly: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否只读")
    use_proxy: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否使用代理下载")
    
    # 外键
    user_id: int = Field(foreign_key="users.id", index=True, description="所属用户ID")
    
    # 关系
    user: "User" = Relationship(back_populates="webdavs")