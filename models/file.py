# my_project/models/file.py

from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, Column, func, DateTime
from .base import TableBase
from datetime import datetime

if TYPE_CHECKING:
    from .user import User
    from .folder import Folder
    from .policy import Policy
    from .source_link import SourceLink

class File(TableBase, table=True):
    __tablename__ = 'files'

    name: str = Field(max_length=255, description="文件名")
    source_name: Optional[str] = Field(default=None, description="源文件名")
    size: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="文件大小（字节）")
    pic_info: Optional[str] = Field(default=None, max_length=255, description="图片信息（如尺寸）")
    upload_session_id: Optional[str] = Field(default=None, max_length=255, unique=True, index=True, description="分块上传会话ID")
    file_metadata: Optional[str] = Field(default=None, description="文件元数据 (JSON格式)")
    
    # 外键
    user_id: int = Field(foreign_key="users.id", index=True, description="所属用户ID")
    folder_id: int = Field(foreign_key="folders.id", index=True, description="所在目录ID")
    policy_id: int = Field(foreign_key="policies.id", index=True, description="所属存储策略ID")
    
    # 关系
    user: list["User"] = Relationship(back_populates="files")
    folder: list["Folder"] = Relationship(back_populates="files")
    policy: list["Policy"] = Relationship(back_populates="files")
    source_links: list["SourceLink"] = Relationship(back_populates="file")