
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship
from .base import TableBase

if TYPE_CHECKING:
    from .share import Share

class Report(TableBase, table=True):
    """举报模型"""

    reason: int = Field(description="举报原因代码")
    description: str | None = Field(default=None, max_length=255, description="补充描述")
    
    # 外键
    share_id: int = Field(foreign_key="share.id", index=True, description="被举报的分享ID")
    
    # 关系
    share: "Share" = Relationship(back_populates="reports")