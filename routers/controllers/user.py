from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from middleware.auth import AuthRequired, SignRequired
import models
from models.response import ResponseModel, TokenModel, userModel, groupModel, UserSettingModel
from deprecated import deprecated
from pkg.log import log
import service

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

user_settings_router = APIRouter(
    prefix='/user/settings',
    tags=["user", "user_settings"],
    dependencies=[Depends(SignRequired)],
)

@user_router.post(
    path='/session',
    summary='用户登录',
    description='User login endpoint.',
)
async def router_user_session(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenModel:
    username = form_data.username
    password = form_data.password
    
    user = await service.user.Login(username=username, password=password)
    
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    elif user == 1:
        raise HTTPException(status_code=400, detail="User account is not fully registered")
    elif user == 2:
        raise HTTPException(status_code=403, detail="User account is banned")
    elif isinstance(user, TokenModel):
        return user
    else:
        log.error(f"Unexpected return type from login service: {type(user)}")
        raise HTTPException(status_code=500, detail="Internal server error during login")

@user_router.post(
    path='/',
    summary='用户注册',
    description='User registration endpoint.',
)
def router_user_register() -> ResponseModel:
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
def router_user_2fa() -> ResponseModel:
    """
    Two-factor authentication login endpoint.
    
    Returns:
        dict: A dictionary containing two-factor authentication information.
    """
    pass

@user_router.post(
    path='/reset',
    summary='发送密码重设邮件',
    description='Send a password reset email.',
)
def router_user_reset() -> ResponseModel:
    """
    Send a password reset email.
    
    Returns:
        dict: A dictionary containing information about the password reset email.
    """
    pass

@deprecated(
    version="0.0.1", 
    reason="邮件中带链接的激活易使得被收件服务器误判为垃圾邮件，新版更换为验证码方式"
)
@user_router.patch(
    path='/reset',
    summary='通过邮件里的链接重设密码',
    description='Reset password via email link.',
)
def router_user_reset_patch() -> ResponseModel:
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
def router_user_qq() -> ResponseModel: 
    """
    Initialize QQ login for a user.
    
    Returns:
        dict: A dictionary containing QQ login initialization information.
    """
    pass

@deprecated(
    version="0.0.1", 
    reason="邮件中带链接的激活易使得被收件服务器误判为垃圾邮件，新版更换为验证码方式"
)
@user_router.get(
    path='/activate/{id}',
    summary='邮件激活',
    description='Activate user account via email link.',
)
def router_user_activate(id: str) -> ResponseModel:
    """
    Activate user account via email link.
    
    Args:
        id (str): The activation ID from the email link.
    
    Returns:
        dict: A dictionary containing activation information.
    """
    pass

@user_router.get(
    path='authn/{username}',
    summary='WebAuthn登录初始化',
    description='Initialize WebAuthn login for a user.',
)
def router_user_authn(username: str) -> ResponseModel:
    """
    Initialize WebAuthn login for a user.
    
    Args:
        username (str): The username of the user.
    
    Returns:
        dict: A dictionary containing WebAuthn initialization information.
    """
    pass

@user_router.post(
    path='authn/finish/{username}',
    summary='WebAuthn登录',
    description='Finish WebAuthn login for a user.',
)
def router_user_authn_finish(username: str) -> ResponseModel:
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
def router_user_profile(id: str) -> ResponseModel:
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
def router_user_avatar(id: str, size: int = 128) -> ResponseModel:
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
    response_model=ResponseModel,
)
async def router_user_me(
    user: Annotated[models.user.User, Depends(AuthRequired)],
) -> ResponseModel:
    """
    获取用户信息.
    
    :return: ResponseModel containing user information.
    :rtype: ResponseModel
    """
    
    group = await models.Group.get(id=user.group_id)
    
    
    user_group = groupModel(
        id=group.id,
        name=group.name,
        allowShare=group.share_enabled,
    )
    
    users = userModel(
            id=user.id,
            username=user.email,
            nickname=user.nick,
            status=user.status,
            created_at=user.created_at,
            score=user.score,
            group=user_group,
        ).model_dump()
    
    
    return ResponseModel(
        data=users
    )

@user_router.get(
    path='/storage',
    summary='存储信息',
    description='Get user storage information.',
    dependencies=[Depends(SignRequired)],
)
def router_user_storage(
    user: Annotated[models.user.User, Depends(AuthRequired)],
) -> ResponseModel:
    """
    Get user storage information.
    
    Returns:
        dict: A dictionary containing user storage information.
    """
    return ResponseModel(
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
    dependencies=[Depends(SignRequired)],
)
def router_user_authn_start() -> ResponseModel:
    """
    Initialize WebAuthn login for a user.
    
    Returns:
        dict: A dictionary containing WebAuthn initialization information.
    """
    pass

@user_router.put(
    path='/authn/finish',
    summary='WebAuthn登录',
    description='Finish WebAuthn login for a user.',
    dependencies=[Depends(SignRequired)],
)
def router_user_authn_finish() -> ResponseModel:
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
def router_user_settings_policies() -> ResponseModel:
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
    dependencies=[Depends(SignRequired)],
)
def router_user_settings_nodes() -> ResponseModel:
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
    dependencies=[Depends(SignRequired)],
)
def router_user_settings_tasks() -> ResponseModel:
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
    dependencies=[Depends(SignRequired)],
)
def router_user_settings() -> ResponseModel:
    """
    Get current user settings.
    
    Returns:
        dict: A dictionary containing the current user settings.
    """
    return ResponseModel(data=UserSettingModel().model_dump())

@user_settings_router.post(
    path='/avatar',
    summary='从文件上传头像',
    description='Upload user avatar from file.',
    dependencies=[Depends(SignRequired)],
)
def router_user_settings_avatar() -> ResponseModel:
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
    dependencies=[Depends(SignRequired)],
)
def router_user_settings_avatar_gravatar() -> ResponseModel:
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
    dependencies=[Depends(SignRequired)],
)
def router_user_settings_patch(option: str) -> ResponseModel:
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
    dependencies=[Depends(SignRequired)],
)
def router_user_settings_2fa() -> ResponseModel:
    """
    Get two-factor authentication initialization information.
    
    Returns:
        dict: A dictionary containing two-factor authentication setup information.
    """
    pass