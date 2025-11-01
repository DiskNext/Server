import secrets
from argon2 import PasswordHasher

class Password:
    
    @staticmethod
    def generate(
        length: int = 16,
        url_safe: bool = False
        ) -> str:
        """
        生成一个随机密码。
        
        :param length: 密码长度，默认为 `16` 个字符。
        :param url_safe: 是否生成URL安全的密码，默认为 `False` 。
        :return: 生成的随机密码字符串。
        """
        if url_safe:
            return secrets.token_urlsafe(length)
        return secrets.token_hex(length)
    
    @staticmethod
    def hash(
        password: str,
    ) -> str:
        """
        生成密码的Argon2哈希值。
        
        :param password: 要哈希的密码。
        :return: 使用Argon2算法生成的密码哈希。
        :rtype: str
        """
        ph = PasswordHasher()
        return ph.hash(password)
    
    @staticmethod
    def verify(
        stored_password: str, 
        provided_password: str, 
    ) -> bool:
        """
        验证存储的Argon2密码哈希值与用户提供的密码是否匹配。
        
        :param stored_password: 存储的Argon2密码哈希值。
        :param provided_password: 用户提供的密码。
        
        :return: 如果密码匹配返回 `True` ,否则返回 `False` 。
        :rtype: bool
        """
        ph = PasswordHasher()
        try:
            ph.verify(stored_password, provided_password)
            return True
        except:
            return False
