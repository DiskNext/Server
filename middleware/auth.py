from typing import Annotated, Literal
from fastapi import Depends
from pkg.JWT import jwt

async def AuthRequired(
    token: Annotated[str, Depends(jwt.oauth2_scheme)]
) -> Literal[True]:
    '''
    AuthRequired 需要登录
    '''
    return True

async def SignRequired(
    token: Annotated[str, Depends(jwt.oauth2_scheme)]
) -> Literal[True]:
    '''
    SignAuthRequired 需要登录并验证请求签名
    '''
    return True

async def AdminRequired(
    token: Annotated[str, Depends(jwt.oauth2_scheme)]
) -> Literal[True]:
    '''
    验证是否为管理员。
    
    使用方法：
    >>> APIRouter(dependencies=[Depends(is_admin)])
    '''
    ...