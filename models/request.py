"""
请求模型定义
"""

from pydantic import BaseModel, Field
from typing import Literal, Union, Optional
from datetime import datetime, timezone
from uuid import uuid4

class LoginRequest(BaseModel):
    """
    登录请求模型
    """
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="用户密码")
    captcha: Optional[str] = Field(None, description="验证码")
    twoFaCode: Optional[str] = Field(None, description="两步验证代码")