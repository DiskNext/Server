
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, UniqueConstraint, CheckConstraint, Index
from .base import TableBase

if TYPE_CHECKING:
    from .user import User
    from .folder import Folder
    from .policy import Policy
    from .source_link import SourceLink

class File(TableBase, table=True):
    __table_args__ = (
        UniqueConstraint("folder_id", "name", name="uq_file_folder_name_active"),
        CheckConstraint("name NOT LIKE '%/%' AND name NOT LIKE '%\\%'", name="ck_file_name_no_slash"),
        Index("ix_file_user_updated", "user_id", "updated_at"),
        Index("ix_file_folder_updated", "folder_id", "updated_at"),
        Index("ix_file_user_size", "user_id", "size"),
    )

    name: str = Field(max_length=255, description="文件名")
    source_name: str | None = Field(default=None, description="源文件名")
    size: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="文件大小（字节）")
    upload_session_id: str | None = Field(default=None, max_length=255, unique=True, index=True, description="分块上传会话ID")
    file_metadata: str | None = Field(default=None, description="文件元数据 (JSON格式)") # 后续可以考虑模型继承？
    
    # 外键
    user_id: int = Field(foreign_key="user.id", index=True, description="所属用户ID")
    folder_id: int = Field(foreign_key="folder.id", index=True, description="所在目录ID")
    policy_id: int = Field(foreign_key="policy.id", index=True, description="所属存储策略ID")
    
    # 关系
    user: "User" = Relationship(back_populates="files")
    folder: "Folder" = Relationship(back_populates="files")
    policy: "Policy" = Relationship(back_populates="files")
    source_links: list["SourceLink"] = Relationship(back_populates="file")