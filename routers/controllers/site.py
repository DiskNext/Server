from fastapi import APIRouter
from sqlalchemy import and_

from middleware.dependencies import SessionDep
from models.response import ResponseModel
from models.setting import Setting

site_router = APIRouter(
    prefix="/site",
    tags=["site"],
)


async def _get_setting(session: SessionDep, type_: str, name: str) -> str | None:
    """获取设置值"""
    setting = await Setting.get(session, and_(Setting.type == type_, Setting.name == name))
    return setting.value if setting else None


async def _get_setting_bool(session: SessionDep, type_: str, name: str) -> bool:
    """获取布尔类型设置值"""
    value = await _get_setting(session, type_, name)
    return value == "1" if value else False


@site_router.get(
    path="/ping",
    summary="测试用路由",
    description="A simple endpoint to check if the site is up and running.",
    response_model=ResponseModel,
)
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
    pass


@site_router.get(
    path='/config',
    summary='站点全局配置',
    description='Get the configuration file.',
    response_model=ResponseModel,
)
async def router_site_config(session: SessionDep):
    """
    Get the configuration file.

    Returns:
        dict: The site configuration.
    """
    return ResponseModel(
        data={
            "title": await _get_setting(session, "basic", "siteName"),
            "loginCaptcha": await _get_setting_bool(session, "login", "login_captcha"),
            "regCaptcha": await _get_setting_bool(session, "login", "reg_captcha"),
            "forgetCaptcha": await _get_setting_bool(session, "login", "forget_captcha"),
            "emailActive": await _get_setting_bool(session, "login", "email_active"),
            "QQLogin": None,
            "themes": await _get_setting(session, "basic", "themes"),
            "defaultTheme": await _get_setting(session, "basic", "defaultTheme"),
            "score_enabled": None,
            "share_score_rate": None,
            "home_view_method": await _get_setting(session, "view", "home_view_method"),
            "share_view_method": await _get_setting(session, "view", "share_view_method"),
            "authn": await _get_setting_bool(session, "authn", "authn_enabled"),
            "user": {},
            "captcha_type": None,
            "captcha_ReCaptchaKey": await _get_setting(session, "captcha", "captcha_ReCaptchaKey"),
            "captcha_CloudflareKey": await _get_setting(session, "captcha", "captcha_CloudflareKey"),
            "captcha_tcaptcha_appid": None,
            "site_notice": None,
            "registerEnabled": await _get_setting_bool(session, "register", "register_enabled"),
            "app_promotion": None,
            "wopi_exts": None,
            "app_feedback": None,
            "app_forum": None,
        }
    )