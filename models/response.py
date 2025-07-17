from pydantic import BaseModel, Field
from typing import Literal, Union, Optional
from datetime import datetime, timezone
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

class groupModel(BaseModel):
    id: int = Field(default=None, description="用户组ID")
    name: str = Field(default=None, description="用户组名称")
    allowShare: bool = Field(default=False, description="是否允许分享")
    allowRomoteDownload: bool = Field(default=False, description="是否允许离线下载")
    allowArchiveDownload: bool = Field(default=False, description="是否允许打包下载")
    shareFree: bool = Field(default=False, description="是否允许免积分下载分享")
    shareDownload: bool = Field(default=False, description="是否允许下载分享")
    compress: bool = Field(default=False)
    webdav: bool = Field(default=False, description="是否允许WebDAV")
    allowWebDAVProxy: bool = Field(default=False, description="是否允许WebDAV代理")
    relocate: bool = Field(default=False, description="是否使用重定向的下载链接")
    sourceBatch: int = Field(default=0)
    selectNode: bool = Field(default=False, description="是否允许选择离线下载节点")
    advanceDelete: bool = Field(default=False, description="是否允许高级删除")

class userModel(BaseModel):
    id: int = Field(default=None, description="用户ID")
    username: str = Field(default=None, description="用户名")
    nickname: str = Field(default=None, description="用户昵称")
    status: int = Field(default=0, description="用户状态")
    avatar: Literal['default', 'gravatar', 'file'] = Field(default='default', description="头像类型")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="用户创建时间")
    preferred_theme: str = Field(default="#607D8B", description="用户首选主题")
    score: int = Field(default=0, description="用户积分")
    anonymous: bool = Field(default=False, description="是否为匿名用户")
    group: groupModel = Field(default_factory=None, description="用户所属用户组")
    tags: list = Field(default_factory=list, description="用户标签列表")
    
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