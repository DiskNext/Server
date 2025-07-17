from fastapi.security import OAuth2PasswordBearer
from models.setting import Setting
from datetime import datetime, timedelta, timezone
import jwt

oauth2_scheme = OAuth2PasswordBearer(
    scheme_name='获取 JWT Bearer 令牌',
    description='用于获取 JWT Bearer 令牌，需要以表单的形式提交',
    tokenUrl="/api/user/session",
    )

SECRET_KEY = ''

async def load_secret_key() -> None:
    """
    从数据库读取 JWT 的密钥。
    
    :param key: 用于加密和解密 JWT 的密钥
    :type key: str
    """
    global SECRET_KEY
    SECRET_KEY = await Setting.get(type='auth', name='secret_key')
    
# 访问令牌
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> tuple[str, datetime]:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=3)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')
    return encoded_jwt, expire

# 刷新令牌
def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> tuple[str, datetime]:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire, "token_type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')
    return encoded_jwt, expire