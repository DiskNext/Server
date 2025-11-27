from loguru import logger as log
from sqlalchemy import and_
from sqlmodel.ext.asyncio.session import AsyncSession

from models.request import LoginRequest
from models.response import TokenModel
from models.setting import Setting
from models.user import User
from pkg.JWT.jwt import create_access_token, create_refresh_token


async def Login(session: AsyncSession, login_request: LoginRequest) -> TokenModel | bool | None:
    """
    根据账号密码进行登录。

    如果登录成功，返回一个 TokenModel 对象，包含访问令牌和刷新令牌以及它们的过期时间。
    如果登录异常，返回 `False`（未完成注册或账号被封禁）。
    如果登录失败，返回 `None`。

    :param session: 数据库会话
    :param login_request: 登录请求

    :return: TokenModel 对象或状态码或 None
    """
    from pkg.password.pwd import Password

    # TODO: 验证码校验
    # captcha_setting = await Setting.get(
    #     session,
    #     and_(Setting.type == "auth", Setting.name == "login_captcha")
    # )
    # is_captcha_required = captcha_setting and captcha_setting.value == "1"

    # 获取用户信息
    user = await User.get(session, User.username == login_request.username)

    # 验证用户是否存在
    if not user:
        log.debug(f"Cannot find user with username: {login_request.username}")
        return None

    # 验证密码是否正确
    if not Password.verify(user.password, login_request.password):
        log.debug(f"Password verification failed for user: {login_request.username}")
        return None

    # 验证用户是否可登录
    if not user.status:
        # 未完成注册 or 账号已被封禁
        return False

    # 创建令牌
    access_token, access_expire = create_access_token(data={'sub': user.username})
    refresh_token, refresh_expire = create_refresh_token(data={'sub': user.username})

    return TokenModel(
        access_token=access_token,
        access_expires=access_expire,
        refresh_token=refresh_token,
        refresh_expires=refresh_expire,
    )