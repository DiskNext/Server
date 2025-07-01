from fastapi import APIRouter
from models.response import ResponseModel

site_router = APIRouter(
    prefix="/site",
    tags=["site"],
)

@site_router.get(
    path="/ping",
    summary="测试用路由",
    description="A simple endpoint to check if the site is up and running.",
    response_model=ResponseModel,)
def router_site_ping():
    """
    Ping the site to check if it is up and running.
    
    Returns:
        str: A message indicating the site is running.
    """
    from pkg.conf.appmeta import BackendVersion
    return ResponseModel(data=BackendVersion)

@site_router.get(
    path='/captcha',
    summary='验证码',
    description='Get a Base64 captcha image.',
    response_model=ResponseModel,
)
def router_site_captcha():
    """
    Get a Base64 captcha image.
    
    Returns:
        str: A Base64 encoded string of the captcha image.
    """
    ...
    
@site_router.get(
    path='/config',
    summary='站点全局配置',
    description='Get the configuration file.',
    response_model=ResponseModel,
)
async def router_site_config():
    """
    Get the configuration file.
    
    Returns:
        dict: The site configuration.
    """
    from models.setting import Setting
    
    return ResponseModel(
        data={
            "title": await Setting.get(type='basic', name='siteName'),
            "loginCaptcha": await Setting.get(type='login', name='login_captcha', format='bool'),
            "regCaptcha": await Setting.get(type='login', name='reg_captcha', format='bool'),
            "forgetCaptcha": await Setting.get(type='login', name='forget_captcha', format='bool'),
            "emailActive": await Setting.get(type='login', name='email_active', format='bool'),
            "QQLogin": None,
            "themes": await Setting.get(type='basic', name='themes'),
            "defaultTheme": await Setting.get(type='basic', name='defaultTheme'),
            "score_enabled": None,
            "share_score_rate": None,
            "home_view_method": await Setting.get(type='view', name='home_view_method'),
            "share_view_method": await Setting.get(type='view', name='share_view_method'),
            "authn": await Setting.get(type='authn', name='authn_enabled', format='bool'),
            "user": {},
            "captcha_type": None,
            "captcha_ReCaptchaKey": await Setting.get(type='captcha', name='captcha_ReCaptchaKey'),
            "captcha_CloudflareKey": await Setting.get(type='captcha', name='captcha_CloudflareKey'),
            "captcha_tcaptcha_appid": None,
            "site_notice": None,
            "registerEnabled": await Setting.get(type='register', name='register_enabled', format='bool'),
            "app_promotion": None,
            "wopi_exts": None,
            "app_feedback": None,
            "app_forum": None,
        }
    )