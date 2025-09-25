# my_project/models/order.py

from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, Column, func, DateTime
from .base import TableBase
from datetime import datetime

if TYPE_CHECKING:
    from .user import User

class Order(TableBase, table=True):
    __tablename__ = 'orders'

    order_no: str = Field(max_length=255, unique=True, index=True, description="订单号，唯一")
    type: int = Field(description="订单类型")
    method: Optional[str] = Field(default=None, max_length=255, description="支付方式")
    product_id: Optional[int] = Field(default=None, description="商品ID")
    num: int = Field(default=1, sa_column_kwargs={"server_default": "1"}, description="购买数量")
    name: str = Field(max_length=255, description="商品名称")
    price: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="订单价格（分）")
    status: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="订单状态: 0=待支付, 1=已完成, 2=已取消")
    
    # 外键
    user_id: int = Field(foreign_key="users.id", index=True, description="所属用户ID")
    
    # 关系
    user: "User" = Relationship(back_populates="orders")