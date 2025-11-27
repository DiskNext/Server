
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship
from .base import TableBase

if TYPE_CHECKING:
    from .user import User

class Order(TableBase, table=True):
    """订单模型"""

    order_no: str = Field(max_length=255, unique=True, index=True, description="订单号，唯一")
    type: int = Field(description="订单类型")
    method: str | None = Field(default=None, max_length=255, description="支付方式")
    product_id: int | None = Field(default=None, description="商品ID")
    num: int = Field(default=1, sa_column_kwargs={"server_default": "1"}, description="购买数量")
    name: str = Field(max_length=255, description="商品名称")
    price: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="订单价格（分）")
    status: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="订单状态: 0=待支付, 1=已完成, 2=已取消")
    
    # 外键
    user_id: int = Field(foreign_key="user.id", index=True, description="所属用户ID")
    
    # 关系
    user: "User" = Relationship(back_populates="orders")