from fastapi import APIRouter, Depends
from middleware.auth import SignRequired
from models.response import ResponseModel

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
def router_user_session() -> ResponseModel:
    """
    User login endpoint.
    
    Returns:
        dict: A dictionary containing user session information.
    """
    pass

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
    dependencies=[Depends(SignRequired)],
)
def router_user_me() -> ResponseModel:
    """
    Get user information.
    
    Returns:
        dict: A dictionary containing user information.
    """
    pass

@user_router.get(
    path='/storage',
    summary='存储信息',
    description='Get user storage information.',
    dependencies=[Depends(SignRequired)],
)
def router_user_storage() -> ResponseModel:
    """
    Get user storage information.
    
    Returns:
        dict: A dictionary containing user storage information.
    """
    pass

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
        dict: A dictionary containing the user's current settings.
    """
    pass

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