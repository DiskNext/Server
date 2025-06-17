from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from middleware.auth import SignRequired
from models.response import ResponseModel

callback_router = APIRouter(
    prefix='/callback',
    tags=["callback"],
)

oauth_router = APIRouter(
    prefix='/callback/oauth',
    tags=["callback", "oauth"],
)

pay_router = APIRouter(
    prefix='/callback/pay',
    tags=["callback", "pay"],
)

upload_router = APIRouter(
    prefix='/callback/upload',
    tags=["callback", "upload"],
)

callback_router.include_router(oauth_router)
callback_router.include_router(pay_router)
callback_router.include_router(upload_router)

@oauth_router.post(
    path='/qq',
    summary='QQ互联回调',
    description='Handle QQ OAuth callback and return user information.',
)
def router_callback_qq() -> ResponseModel:
    """
    Handle QQ OAuth callback and return user information.
    
    Returns:
        ResponseModel: A model containing the response data for the QQ OAuth callback.
    """
    ...

@oauth_router.post(
    path='/github',
    summary='GitHub OAuth 回调',
    description='Handle GitHub OAuth callback and return user information.',
)
def router_callback_github() -> ResponseModel:
    """
    Handle GitHub OAuth callback and return user information.
    
    Returns:
        ResponseModel: A model containing the response data for the GitHub OAuth callback.
    """
    ...

@pay_router.post(
    path='/alipay',
    summary='支付宝支付回调',
    description='Handle Alipay payment callback and return payment status.',
)
def router_callback_alipay() -> ResponseModel:
    """
    Handle Alipay payment callback and return payment status.
    
    Returns:
        ResponseModel: A model containing the response data for the Alipay payment callback.
    """
    ...

@pay_router.post(    
    path='/wechat',
    summary='微信支付回调',
    description='Handle WeChat Pay payment callback and return payment status.',
)
def router_callback_wechat() -> ResponseModel:
    """
    Handle WeChat Pay payment callback and return payment status.
    
    Returns:
        ResponseModel: A model containing the response data for the WeChat Pay payment callback.
    """
    ...

@pay_router.post(
    path='/stripe',
    summary='Stripe支付回调',
    description='Handle Stripe payment callback and return payment status.',
)
def router_callback_stripe() -> ResponseModel:
    """
    Handle Stripe payment callback and return payment status.
    
    Returns:
        ResponseModel: A model containing the response data for the Stripe payment callback.
    """
    ...

@pay_router.get(
    path='/easypay',
    summary='易支付回调',
    description='Handle EasyPay payment callback and return payment status.',
)
def router_callback_easypay() -> PlainTextResponse:
    """
    Handle EasyPay payment callback and return payment status.
    
    Returns:
        PlainTextResponse: A response containing the payment status for the EasyPay payment callback.
    """
    ...
    # return PlainTextResponse("success", status_code=200)

@pay_router.get(
    path='/custom/{order_no}/{id}',
    summary='自定义支付回调',
    description='Handle custom payment callback and return payment status.',
)
def router_callback_custom(order_no: str, id: str) -> ResponseModel:
    """
    Handle custom payment callback and return payment status.
    
    Args:
        order_no (str): The order number for the payment.
        id (str): The ID associated with the payment.
    
    Returns:
        ResponseModel: A model containing the response data for the custom payment callback.
    """
    ...

@upload_router.post(
    path='/remote/{session_id}/{key}',
    summary='远程上传回调',
    description='Handle remote upload callback and return upload status.',
)
def router_callback_remote(session_id: str, key: str) -> ResponseModel:
    """
    Handle remote upload callback and return upload status.
    
    Args:
        session_id (str): The session ID for the upload.
        key (str): The key for the uploaded file.
    
    Returns:
        ResponseModel: A model containing the response data for the remote upload callback.
    """
    ...

@upload_router.post(
    path='/qiniu/{session_id}',
    summary='七牛云上传回调',
    description='Handle Qiniu Cloud upload callback and return upload status.',
)
def router_callback_qiniu(session_id: str) -> ResponseModel:
    """
    Handle Qiniu Cloud upload callback and return upload status.
    
    Args:
        session_id (str): The session ID for the upload.
    
    Returns:
        ResponseModel: A model containing the response data for the Qiniu Cloud upload callback.
    """
    ...
    
@upload_router.post(
    path='/tencent/{session_id}',
    summary='腾讯云上传回调',
    description='Handle Tencent Cloud upload callback and return upload status.',
)
def router_callback_tencent(session_id: str) -> ResponseModel:
    """
    Handle Tencent Cloud upload callback and return upload status.
    
    Args:
        session_id (str): The session ID for the upload.
    
    Returns:
        ResponseModel: A model containing the response data for the Tencent Cloud upload callback.
    """
    ...

@upload_router.post(    
    path='/aliyun/{session_id}',
    summary='阿里云上传回调',
    description='Handle Aliyun upload callback and return upload status.',
)
def router_callback_aliyun(session_id: str) -> ResponseModel:
    """
    Handle Aliyun upload callback and return upload status.
    
    Args:
        session_id (str): The session ID for the upload.
    
    Returns:
        ResponseModel: A model containing the response data for the Aliyun upload callback.
    """
    ...

@upload_router.post(   
    path='/upyun/{session_id}',
    summary='又拍云上传回调',
    description='Handle Upyun upload callback and return upload status.',
)
def router_callback_upyun(session_id: str) -> ResponseModel:
    """
    Handle Upyun upload callback and return upload status.
    
    Args:
        session_id (str): The session ID for the upload.
    
    Returns:
        ResponseModel: A model containing the response data for the Upyun upload callback.
    """
    ...

@upload_router.post(
    path='/aws/{session_id}',
    summary='AWS S3上传回调',
    description='Handle AWS S3 upload callback and return upload status.',
)
def router_callback_aws(session_id: str) -> ResponseModel:
    """
    Handle AWS S3 upload callback and return upload status.
    
    Args:
        session_id (str): The session ID for the upload.
    
    Returns:
        ResponseModel: A model containing the response data for the AWS S3 upload callback.
    """
    ...

@upload_router.post(
    path='/onedrive/finish/{session_id}',
    summary='OneDrive上传完成回调',
    description='Handle OneDrive upload completion callback and return upload status.',
)
def router_callback_onedrive_finish(session_id: str) -> ResponseModel:
    """
    Handle OneDrive upload completion callback and return upload status.
    
    Args:
        session_id (str): The session ID for the upload.
    
    Returns:
        ResponseModel: A model containing the response data for the OneDrive upload completion callback.
    """
    ...

@upload_router.get(
    path='/ondrive/auth',
    summary='OneDrive授权回调',
    description='Handle OneDrive authorization callback and return authorization status.',
)
def router_callback_onedrive_auth() -> ResponseModel:
    """
    Handle OneDrive authorization callback and return authorization status.
    
    Returns:
        ResponseModel: A model containing the response data for the OneDrive authorization callback.
    """
    ...

@upload_router.get(
    path='/google/auth',
    summary='Google OAuth 完成',
    description='Handle Google OAuth completion callback and return authorization status.',
)
def router_callback_google_auth() -> ResponseModel:
    """
    Handle Google OAuth completion callback and return authorization status.
    
    Returns:
        ResponseModel: A model containing the response data for the Google OAuth completion callback.
    """
    ...