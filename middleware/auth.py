from typing import Annotated, Optional
from fastapi import Depends, HTTPException
from models.user import User
from pkg.JWT import JWT
import jwt
from jwt import InvalidTokenError

credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def AuthRequired(
    token: Annotated[str, Depends(JWT.oauth2_scheme)]
) -> Optional["User"]:
    """
    AuthRequired 需要登录
    """
    try:
        payload = jwt.decode(token, JWT.SECRET_KEY, algorithms="HS256")
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        # 从数据库获取用户信息
        user = await User.get(email=username)
        if not user:
            raise credentials_exception

        return user

    except InvalidTokenError:
        raise credentials_exception

async def SignRequired(
    token: Annotated[str, Depends(JWT.oauth2_scheme)]
) -> Optional["User"]:
    """
    SignAuthRequired 需要验证请求签名
    """
    pass

async def AdminRequired(
    token: Annotated[str, Depends(JWT.oauth2_scheme)]
) -> Optional["User"]:
    """
    验证是否为管理员。
    
    使用方法：
    >>> APIRouter(dependencies=[Depends(is_admin)])
    """
    pass