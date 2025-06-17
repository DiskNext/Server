from pydantic import BaseModel, Field
from typing import Union, Optional

class ResponseModel(BaseModel):
    code: int = Field(default=0, description="系统内部状态码, 0表示成功，其他表示失败", lt=60000, gt=0)
    data: Union[dict, list, str, int, float, None] = Field(None, description="响应数据")
    msg: Optional[str] = Field(default=None, description="响应消息，可以是错误消息或信息提示")