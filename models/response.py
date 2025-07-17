from pydantic import BaseModel, Field
from typing import Literal, Union, Optional
from datetime import datetime, timedelta, timezone
from uuid import uuid4

class ResponseModel(BaseModel):
    code: int = Field(default=0, description="系统内部状态码, 0表示成功，其他表示失败", lt=60000, gt=0)
    data: Union[dict, list, str, int, float, None] = Field(None, description="响应数据")
    msg: Optional[str] = Field(default=None, description="响应消息，可以是错误消息或信息提示")
    instance_id: str = Field(default_factory=lambda: str(uuid4()), description="实例ID，用于标识请求的唯一性")

class TokenModel(BaseModel):
    access_expires: datetime = Field(default=None, description="访问令牌的过期时间")
    access_token: str = Field(default=None, description="访问令牌")
    refresh_expires: datetime = Field(default=None, description="刷新令牌的过期时间")
    refresh_token: str = Field(default=None, description="刷新令牌")
    
class userModel(ResponseModel):
    id: str = Field(default=None, description="用户ID")
    username: str = Field(default=None, description="用户名")
    email: Optional[str] = Field(default=None, description="用户邮箱")
    avatar: Optional[str] = Field(default=None, description="用户头像URL")
    is_active: bool = Field(default=True, description="用户是否激活")
    is_admin: bool = Field(default=False, description="用户是否为管理员")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="账户创建时间")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="账户更新时间")
    
class SiteConfigModel(ResponseModel):
    title: str = Field(default="DiskNext", description="网站标题")
    themes: dict = Field(default_factory=dict, description="网站主题配置")
    default_theme: str = Field(default="default", description="默认主题RGB色号")
    site_notice: Optional[str] = Field(default=None, description="网站公告")
    user: dict = Field(default_factory=dict, description="用户信息")
    logo_light: Optional[str] = Field(default=None, description="网站Logo URL")
    logo_dark: Optional[str] = Field(default=None, description="网站Logo URL（深色模式）")
    captcha_type: Literal['none', 'default', 'gcaptcha', 'cloudflare turnstile'] = Field(default='none', description="验证码类型")
    captcha_key: Optional[str] = Field(default=None, description="验证码密钥")