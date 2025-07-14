from fastapi.security import OAuth2PasswordBearer
from models.setting import Setting

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