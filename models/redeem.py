from sqlmodel import Field, text
from .base import TableBase

class Redeem(TableBase, table=True):
    """兑换码模型"""

    type: int = Field(description="兑换码类型")
    product_id: int | None = Field(default=None, description="关联的商品/权益ID")
    num: int = Field(default=1, sa_column_kwargs={"server_default": "1"}, description="可兑换数量/时长等")
    code: str = Field(unique=True, index=True, description="兑换码，唯一")
    used: bool = Field(default=False, sa_column_kwargs={"server_default": text("false")}, description="是否已使用")