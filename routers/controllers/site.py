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
def router_site_config():
    """
    Get the configuration file.
    
    Returns:
        dict: The site configuration.
    """
    ...