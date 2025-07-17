# my_project/models/node.py

from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, text, Column, func, DateTime
from .base import BaseModel
from datetime import datetime

if TYPE_CHECKING:
    from .download import Download

class Node(BaseModel, table=True):
    __tablename__ = 'nodes'
    
    status: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="节点状态: 0=正常, 1=离线")
    name: str = Field(max_length=255, unique=True, description="节点名称")
    type: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="节点类型")
    server: str = Field(max_length=255, description="节点地址（IP或域名）")
    slave_key: Optional[str] = Field(default=None, description="从机通讯密钥")
    master_key: Optional[str] = Field(default=None, description="主机通讯密钥")
    aria2_enabled: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否启用Aria2")
    aria2_options: Optional[str] = Field(default=None, description="Aria2配置 (JSON格式)")
    rank: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="节点排序权重")

    # 关系
    downloads: list["Download"] = Relationship(back_populates="node")