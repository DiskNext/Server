"""
响应模型定义
"""

from pydantic import BaseModel, Field
from typing import Literal, Union, Optional
from datetime import datetime, timezone
from uuid import uuid4

class ResponseModel(BaseModel):
    '''
    默认响应模型
    '''
    code: int = Field(default=0, description="系统内部状态码, 0表示成功，其他表示失败", lt=60000, gt=0)
    data: Union[dict, list, str, int, float, None] = Field(None, description="响应数据")
    msg: Optional[str] = Field(default=None, description="响应消息，可以是错误消息或信息提示")
    instance_id: str = Field(default_factory=lambda: str(uuid4()), description="实例ID，用于标识请求的唯一性")
    
class ThemeModel(BaseModel):
    '''
    主题模型
    '''
    primary: str = Field(default="#3f51b5", description="Primary color")
    secondary: str = Field(default="#f50057", description="Secondary color")
    accent: str = Field(default="#9c27b0", description="Accent color")
    dark: str = Field(default="#1d1d1d", description="Dark color")
    dark_page: str = Field(default="#121212", description="Dark page color")
    positive: str = Field(default="#21ba45", description="Positive color")
    negative: str = Field(default="#c10015", description="Negative color")
    info: str = Field(default="#31ccec", description="Info color")
    warning: str = Field(default="#f2c037", description="Warning color")

class TokenModel(BaseModel):
    '''
    访问令牌模型
    '''
    access_expires: datetime = Field(default=None, description="访问令牌的过期时间")
    access_token: str = Field(default=None, description="访问令牌")
    refresh_expires: datetime = Field(default=None, description="刷新令牌的过期时间")
    refresh_token: str = Field(default=None, description="刷新令牌")

class groupModel(BaseModel):
    '''
    用户组模型
    '''
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
    '''
    用户模型
    '''
    id: int = Field(default=None, description="用户ID")
    username: str = Field(default=None, description="用户名")
    nickname: str = Field(default=None, description="用户昵称")
    status: int = Field(default=0, description="用户状态")
    avatar: Literal['default', 'gravatar', 'file'] = Field(default='default', description="头像类型")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="用户创建时间")
    preferred_theme: ThemeModel = Field(default_factory=ThemeModel, description="用户首选主题")
    score: int = Field(default=0, description="用户积分")
    anonymous: bool = Field(default=False, description="是否为匿名用户")
    group: groupModel = Field(default_factory=None, description="用户所属用户组")
    tags: list = Field(default_factory=list, description="用户标签列表")
    
class SiteConfigModel(ResponseModel):
    '''
    站点配置模型
    '''
    title: str = Field(default="DiskNext", description="网站标题")
    themes: dict = Field(default_factory=dict, description="网站主题配置")
    default_theme: str = Field(default="default", description="默认主题RGB色号")
    site_notice: Optional[str] = Field(default=None, description="网站公告")
    user: dict = Field(default_factory=dict, description="用户信息")
    logo_light: Optional[str] = Field(default=None, description="网站Logo URL")
    logo_dark: Optional[str] = Field(default=None, description="网站Logo URL（深色模式）")
    captcha_type: Literal['none', 'default', 'gcaptcha', 'cloudflare turnstile'] = Field(default='none', description="验证码类型")
    captcha_key: Optional[str] = Field(default=None, description="验证码密钥")

class AuthnModel(BaseModel):
    '''
    WebAuthn模型
    '''
    id: str = Field(default=None, description="ID")
    fingerprint: str = Field(default=None, description="指纹")

class UserSettingModel(BaseModel):
    '''
    用户设置模型
    '''
    authn: Optional[AuthnModel] = Field(default=None, description="认证信息")
    group_expires: Optional[datetime] = Field(default=None, description="用户组过期时间")
    prefer_theme: str = Field(default="#5898d4", description="用户首选主题")
    qq: str | bool = Field(default=False, description="QQ号")
    themes: dict = Field(default_factory=dict, description="用户主题配置")
    two_factor: bool = Field(default=False, description="是否启用两步验证")
    uid: int = Field(default=0, description="用户UID")

class FoldObjectModel(BaseModel):
    id: str = Field(default=..., description="对象ID")
    name: str = Field(default=..., description="对象名称")
    path: str = Field(default=..., description="对象路径")
    thumb: bool = Field(default=False, description="是否有缩略图")
    size: int = Field(default=None, description="对象大小，单位字节")
    type: Literal['file', 'folder'] = Field(default=..., description="对象类型，file表示文件，folder表示文件夹")
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="对象创建或修改时间")
    create_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="对象创建时间")
    source_enabled: bool = Field(default=False, description="是否启用离线下载源")

class PolicyModel(BaseModel):
    '''
    存储策略模型
    '''
    id: str = Field(default=..., description="策略ID")
    name: str = Field(default=..., description="策略名称")
    type: Literal['local', 'qiniu', 'tencent', 'aliyun', 'onedrive', 'google_drive', 'dropbox', 'webdav', 'remote'] = Field(default=..., description="存储类型")
    max_size: int = Field(default=0, description="单文件最大限制，单位字节，0表示不限制")
    file_type: list = Field(default_factory=list, description="允许的文件类型列表，空列表表示不限制")

class DirectoryModel(BaseModel):
    '''
    目录模型
    '''
    parent: str = Field(default=..., description="父目录ID")
    objects: list[FoldObjectModel] = Field(default_factory=list, description="目录下的对象列表")
    policy: PolicyModel = Field(default_factory=PolicyModel, description="存储策略")