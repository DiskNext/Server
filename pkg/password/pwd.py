import secrets

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
        生成密码的加盐哈希值。
        
        :return: 包含盐值和哈希值的字符串。
        :rtype: str
        """
        import os, hashlib, binascii
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    @staticmethod
    def verify(
        stored_password: str, 
        provided_password: str, 
    ) -> bool:
        """
        验证存储的密码哈希值与用户提供的密码是否匹配。
        
        :param stored_password: 存储的密码哈希值(包含盐值)。
        :param provided_password: 用户提供的密码。
        :param debug: 是否输出调试信息，将会输出原密码和哈希值。
        :return: 如果密码匹配返回 `True` ,否则返回 `False` 。
        """
        import hashlib, binascii
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha256', 
                                      provided_password.encode('utf-8'), 
                                      salt.encode('ascii'), 
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        
        return secrets.compare_digest(pwdhash, stored_password)