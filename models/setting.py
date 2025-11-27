from sqlmodel import Field, UniqueConstraint
from .base import TableBase
from enum import StrEnum

class SettingsType(StrEnum):
    """设置类型枚举"""

    ARIA2 = "aria2"
    AUTH = "auth"
    AUTHN = "authn"
    AVATAR = "avatar"
    BASIC = "basic"
    CAPTCHA = "captcha"
    CRON = "cron"
    FILE_EDIT = "file_edit"
    LOGIN = "login"
    MAIL = "mail"
    MAIL_TEMPLATE = "mail_template"
    MOBILE = "mobile"
    PATH = "path"
    PREVIEW = "preview"
    PWA = "pwa"
    REGISTER = "register"
    RETRY = "retry"
    SHARE = "share"
    SLAVE = "slave"
    TASK = "task"
    THUMB = "thumb"
    TIMEOUT = "timeout"
    UPLOAD = "upload"
    VERSION = "version"
    VIEW = "view"
    WOPI = "wopi"

# 数据库模型
class Setting(TableBase, table=True):
    """设置模型"""

    __table_args__ = (UniqueConstraint("type", "name", name="uq_setting_type_name"),)

    type: SettingsType = Field(max_length=255, description="设置类型/分组")
    name: str = Field(max_length=255, description="设置项名称")
    value: str | None = Field(default=None, description="设置值")