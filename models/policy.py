# my_project/models/policy.py

from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, text, Column, func, DateTime
from .base import BaseModel
from datetime import datetime

if TYPE_CHECKING:
    from .file import File
    from .folder import Folder

class Policy(BaseModel, table=True):
    __tablename__ = 'policies'

    name: str = Field(max_length=255, unique=True, description="策略名称")
    type: str = Field(max_length=255, description="存储类型 (e.g. 'local', 's3')")
    server: Optional[str] = Field(default=None, max_length=255, description="服务器地址（本地策略为路径）")
    bucket_name: Optional[str] = Field(default=None, max_length=255, description="存储桶名称")
    is_private: bool = Field(default=True, sa_column_kwargs={"server_default": text("true")}, description="是否为私有空间")
    base_url: Optional[str] = Field(default=None, max_length=255, description="访问文件的基础URL")
    access_key: Optional[str] = Field(default=None, description="Access Key")
    secret_key: Optional[str] = Field(default=None, description="Secret Key")
    max_size: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="允许上传的最大文件尺寸（字节）")
    auto_rename: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否自动重命名")
    dir_name_rule: Optional[str] = Field(default=None, max_length=255, description="目录命名规则")
    file_name_rule: Optional[str] = Field(default=None, max_length=255, description="文件命名规则")
    is_origin_link_enable: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否开启源链接访问")
    options: Optional[str] = Field(default=None, description="其他选项 (JSON格式)")
    
    # 关系
    files: List["File"] = Relationship(back_populates="policy")
    folders: List["Folder"] = Relationship(back_populates="policy")