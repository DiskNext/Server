from typing import Annotated

from fastapi import Depends, HTTPException
from jwt import InvalidTokenError
import jwt

from models.user import User
from pkg.JWT import jwt as JWT
from .dependencies import SessionDep

credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def AuthRequired(
    session: SessionDep,
    token: Annotated[str, Depends(JWT.oauth2_scheme)],
) -> User:
    """
    AuthRequired 需要登录
    """
    try:
        payload = jwt.decode(token, JWT.SECRET_KEY, algorithms="HS256")
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        # 从数据库获取用户信息
        user = await User.get(session, User.username == username)
        if not user:
            raise credentials_exception

        return user

    except InvalidTokenError:
        raise credentials_exception

async def SignRequired(
    session: SessionDep,
    token: Annotated[str, Depends(JWT.oauth2_scheme)],
) -> User | None:
    """
    SignAuthRequired 需要验证请求签名
    """
    pass

async def AdminRequired(
    user: Annotated[User, Depends(AuthRequired)],
) -> User:
    """
    验证是否为管理员。

    使用方法：
    >>> APIRouter(dependencies=[Depends(AdminRequired)])
    """
    # TODO: 跨表联查时需要使用 awaitable_attrs
    # if await user.awaitable_attrs.group.admin:
    if user.group.admin:
        return user
    raise HTTPException(status_code=403, detail="Admin Required")