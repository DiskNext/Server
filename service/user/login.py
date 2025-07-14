from models.setting import Setting

async def login(
    username: str,
    password: str
):
    """
    """
    
    isCaptchaRequired = await Setting.get(type='auth', name='login_captcha', type=bool)
    captchaType = await Setting.get(type='auth', name='captcha_type', type=str)

    # [TODO] 验证码校验
    
    