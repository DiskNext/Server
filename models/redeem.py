# my_project/models/redeem.py

from typing import Optional
from sqlmodel import Field, text, Column, func, DateTime
from .base import BaseModel
from datetime import datetime

class Redeem(BaseModel, table=True):
    __tablename__ = 'redeems'

    type: int = Field(description="兑换码类型")
    product_id: Optional[int] = Field(default=None, description="关联的商品/权益ID")
    num: int = Field(default=1, sa_column_kwargs={"server_default": "1"}, description="可兑换数量/时长等")
    code: str = Field(unique=True, index=True, description="兑换码，唯一")
    used: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否已使用")
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