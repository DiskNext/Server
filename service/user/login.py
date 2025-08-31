from typing import Optional
from models.setting import Setting
from models.request import LoginRequest
from models.response import TokenModel
from models.user import User
from pkg.log import log

async def Login(LoginRequest: LoginRequest) -> tuple[bool, TokenModel | str]:
    """
    根据账号密码进行登录。

    如果登录成功，返回一个 TokenModel 对象，包含访问令牌和刷新令牌以及它们的过期时间。
    如果登录异常，返回 `int` 状态码，`1` 为未完成注册，`2` 为账号被封禁。
    如果登录失败，返回 `None`。

    :param username: 用户名或邮箱
    :type username: str
    :param password: 用户密码
    :type password: str
    :param captcha: 验证码
    :type captcha: Optional[str]
    :param twoFaCode: 两步验证代码
    :type twoFaCode: Optional[str]

    :return: TokenModel 对象或状态码或 None
    :rtype: TokenModel | int | None
    """
    from pkg.password.pwd import Password
    
    isCaptchaRequired = await Setting.get(type='auth', name='login_captcha', format='bool')
    captchaType = await Setting.get(type='auth', name='captcha_type', format='str')

    # [TODO] 验证码校验
    
    # 验证用户是否存在
    user = await User.get(email=LoginRequest.username)

    if not user:
        log.debug(f"Cannot find user with email: {LoginRequest.username}")
        return False, "User not found"
    
    # 验证密码是否正确
    if not Password.verify(user.password, LoginRequest.password):
        log.debug(f"Password verification failed for user: {LoginRequest.username}")
        return False, "Incorrect password"
    
    # 验证用户是否可登录
    if user.status == None:
        # 未完成注册
        return False, "Need to complete registration"
    elif user.status == False:
        # 账号已被封禁
        return False, "Account is banned"
    
    # 创建令牌
    from pkg.JWT.JWT import create_access_token, create_refresh_token
    
    access_token, access_expire = create_access_token(data={'sub': user.email})
    refresh_token, refresh_expire = create_refresh_token(data={'sub': user.email})

    return True, TokenModel(
        access_token=access_token,
        access_expires=access_expire,
        refresh_token=refresh_token,
        refresh_expires=refresh_expire,
    )