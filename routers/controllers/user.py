from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from middleware.auth import AuthRequired, AuthRequired
import models
from loguru import logger as log
import service

from webauthn import (
    generate_registration_options,
    verify_authentication_response,
    options_to_json,
    base64url_to_bytes,
)

from webauthn.helpers import options_to_json_dict

from webauthn.helpers.structs import (
    PublicKeyCredentialDescriptor,
    UserVerificationRequirement,
)

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

user_settings_router = APIRouter(
    prefix='/user/settings',
    tags=["user", "user_settings"],
    dependencies=[Depends(AuthRequired)],
)

@user_router.post(
    path='/session',
    summary='用户登录',
    description='User login endpoint.',
)
async def router_user_session(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> models.response.TokenModel:
    username = form_data.username
    password = form_data.password
    
    is_login, detail = await service.user.Login(
        models.request.LoginRequest(
            username=username, password=password
        )
    )
    
    if isinstance(detail, models.response.TokenModel):
        return detail
    elif detail is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    elif detail is False:
        raise HTTPException(status_code=403, detail="User account is banned or not fully registered")
    else:
        raise HTTPException(status_code=500, detail="Internal server error during login")

@user_router.post(
    path='/',
    summary='用户注册',
    description='User registration endpoint.',
)
def router_user_register() -> models.response.ResponseModel:
    """
    User registration endpoint.
    
    Returns:
        dict: A dictionary containing user registration information.
    """
    pass

@user_router.post(
    path='/2fa',
    summary='用两步验证登录',
    description='Two-factor authentication login endpoint.',
)
def router_user_2fa() -> models.response.ResponseModel:
    """
    Two-factor authentication login endpoint.
    
    Returns:
        dict: A dictionary containing two-factor authentication information.
    """
    pass

@user_router.post(
    path='/code',
    summary='发送验证码邮件',
    description='Send a verification code email.',
)
def router_user_email_code() -> models.response.ResponseModel:
    """
    Send a verification code email.
    
    Returns:
        dict: A dictionary containing information about the password reset email.
    """
    pass

@user_router.patch(
    path='/reset',
    summary='通过邮件里的链接重设密码',
    description='Reset password via email link.',
    deprecated=True,
)
def router_user_reset_patch() -> models.response.ResponseModel:
    """
    Reset password via email link.
    
    Returns:
        dict: A dictionary containing information about the password reset.
    """
    pass

@user_router.get(
    path='/qq',
    summary='初始化QQ登录',
    description='Initialize QQ login for a user.',
)
def router_user_qq() -> models.response.ResponseModel: 
    """
    Initialize QQ login for a user.
    
    Returns:
        dict: A dictionary containing QQ login initialization information.
    """
    pass

@user_router.get(
    path='authn/{username}',
    summary='WebAuthn登录初始化',
    description='Initialize WebAuthn login for a user.',
)
async def router_user_authn(username: str) -> models.response.ResponseModel:
    
    pass

@user_router.post(
    path='authn/finish/{username}',
    summary='WebAuthn登录',
    description='Finish WebAuthn login for a user.',
)
def router_user_authn_finish(username: str) -> models.response.ResponseModel:
    """
    Finish WebAuthn login for a user.
    
    Args:
        username (str): The username of the user.
    
    Returns:
        dict: A dictionary containing WebAuthn login information.
    """
    pass

@user_router.get(
    path='/profile/{id}',
    summary='获取用户主页展示用分享',
    description='Get user profile for display.',
)
def router_user_profile(id: str) -> models.response.ResponseModel:
    """
    Get user profile for display.
    
    Args:
        id (str): The user ID.
    
    Returns:
        dict: A dictionary containing user profile information.
    """
    pass

@user_router.get(
    path='/avatar/{id}/{size}',
    summary='获取用户头像',
    description='Get user avatar by ID and size.',
)
def router_user_avatar(id: str, size: int = 128) -> models.response.ResponseModel:
    """
    Get user avatar by ID and size.
    
    Args:
        id (str): The user ID.
        size (int): The size of the avatar image.
    
    Returns:
        str: A Base64 encoded string of the user avatar image.
    """
    pass

#####################
# 需要登录的接口
#####################

@user_router.get(
    path='/me',
    summary='获取用户信息',
    description='Get user information.',
    dependencies=[Depends(dependency=AuthRequired)],
    response_model=models.response.ResponseModel,
)
async def router_user_me(
    user: Annotated[models.user.User, Depends(AuthRequired)],
) -> models.response.ResponseModel:
    """
    获取用户信息.
    
    :return: response.ResponseModel containing user information.
    :rtype: response.ResponseModel
    """
    
    group = await models.Group.get(id=user.group_id)
    
    
    user_group = models.response.groupModel(
        id=group.id,
        name=group.name,
        allowShare=group.share_enabled,
    )
    
    users = models.response.userModel(
            id=user.id,
            username=user.email,
            nickname=user.nick,
            status=user.status,
            created_at=user.created_at,
            score=user.score,
            group=user_group,
        ).model_dump()
    
    
    return models.response.ResponseModel(
        data=users
    )

@user_router.get(
    path='/storage',
    summary='存储信息',
    description='Get user storage information.',
    dependencies=[Depends(AuthRequired)],
)
def router_user_storage(
    user: Annotated[models.user.User, Depends(AuthRequired)],
) -> models.response.ResponseModel:
    """
    Get user storage information.
    
    Returns:
        dict: A dictionary containing user storage information.
    """
    return models.response.ResponseModel(
        data={
            "used": 0,
            "free": 0,
            "total": 0,
        }
    )

@user_router.put(
    path='/authn/start',
    summary='WebAuthn登录初始化',
    description='Initialize WebAuthn login for a user.',
    dependencies=[Depends(AuthRequired)],
)
async def router_user_authn_start(
    user: Annotated[models.user.User, Depends(AuthRequired)]
) -> models.response.ResponseModel:
    """
    Initialize WebAuthn login for a user.
    
    Returns:
        dict: A dictionary containing WebAuthn initialization information.
    """
    # [TODO] 检查 WebAuthn 是否开启，用户是否有注册过 WebAuthn 设备等
    
    if not await models.Setting.get(type="authn", name="authn_enabled", format="bool"):
        raise HTTPException(status_code=400, detail="WebAuthn is not enabled")
    
    options = generate_registration_options(
        rp_id=await models.Setting.get(type="basic", name="siteURL"),
        rp_name=await models.Setting.get(type="basic", name="siteTitle"),
        user_name=user.email,
        user_display_name=user.nick or user.email,
    )
    
    return models.response.ResponseModel(
        data=options_to_json_dict(options)
    )

@user_router.put(
    path='/authn/finish',
    summary='WebAuthn登录',
    description='Finish WebAuthn login for a user.',
    dependencies=[Depends(AuthRequired)],
)
def router_user_authn_finish() -> models.response.ResponseModel:
    """
    Finish WebAuthn login for a user.
    
    Returns:
        dict: A dictionary containing WebAuthn login information.
    """
    pass

@user_settings_router.get(
    path='/policies',
    summary='获取用户可选存储策略',
    description='Get user selectable storage policies.',
)
def router_user_settings_policies() -> models.response.ResponseModel:
    """
    Get user selectable storage policies.
    
    Returns:
        dict: A dictionary containing available storage policies for the user.
    """
    pass

@user_settings_router.get(
    path='/nodes',
    summary='获取用户可选节点',
    description='Get user selectable nodes.',
    dependencies=[Depends(AuthRequired)],
)
def router_user_settings_nodes() -> models.response.ResponseModel:
    """
    Get user selectable nodes.
    
    Returns:
        dict: A dictionary containing available nodes for the user.
    """
    pass

@user_settings_router.get(
    path='/tasks',
    summary='任务队列',
    description='Get user task queue.',
    dependencies=[Depends(AuthRequired)],
)
def router_user_settings_tasks() -> models.response.ResponseModel:
    """
    Get user task queue.
    
    Returns:
        dict: A dictionary containing the user's task queue information.
    """
    pass

@user_settings_router.get(
    path='/',
    summary='获取当前用户设定',
    description='Get current user settings.',
    dependencies=[Depends(AuthRequired)],
)
def router_user_settings() -> models.response.ResponseModel:
    """
    Get current user settings.
    
    Returns:
        dict: A dictionary containing the current user settings.
    """
    return models.response.ResponseModel(data=models.response.UserSettingModel().model_dump())

@user_settings_router.post(
    path='/avatar',
    summary='从文件上传头像',
    description='Upload user avatar from file.',
    dependencies=[Depends(AuthRequired)],
)
def router_user_settings_avatar() -> models.response.ResponseModel:
    """
    Upload user avatar from file.
    
    Returns:
        dict: A dictionary containing the result of the avatar upload.
    """
    pass

@user_settings_router.put(
    path='/avatar',
    summary='设定为Gravatar头像',
    description='Set user avatar to Gravatar.',
    dependencies=[Depends(AuthRequired)],
)
def router_user_settings_avatar_gravatar() -> models.response.ResponseModel:
    """
    Set user avatar to Gravatar.
    
    Returns:
        dict: A dictionary containing the result of setting the Gravatar avatar.
    """
    pass

@user_settings_router.patch(
    path='/{option}',
    summary='更新用户设定',
    description='Update user settings.',
    dependencies=[Depends(AuthRequired)],
)
def router_user_settings_patch(option: str) -> models.response.ResponseModel:
    """
    Update user settings.
    
    Args:
        option (str): The setting option to update.
    
    Returns:
        dict: A dictionary containing the result of the settings update.
    """
    pass

@user_settings_router.get(
    path='/2fa',
    summary='获取两步验证初始化信息',
    description='Get two-factor authentication initialization information.',
    dependencies=[Depends(AuthRequired)],
)
def router_user_settings_2fa() -> models.response.ResponseModel:
    """
    Get two-factor authentication initialization information.
    
    Returns:
        dict: A dictionary containing two-factor authentication setup information.
    """
    pass