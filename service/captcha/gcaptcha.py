import aiohttp

async def verify_captcha(token: str, secret_key: str) -> bool:
    """
    验证 Google reCAPTCHA v2/v3 的 token 是否有效。
    
    :param token: 用户提交的 reCAPTCHA token
    :type token: str
    :param secret_key: Google reCAPTCHA 的密钥
    :type secret_key: str
    
    :return: 如果验证成功返回 True，否则返回 False
    :rtype: bool
    """
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        'secret': secret_key,
        'response': token
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(verify_url, data=payload) as response:
            if response.status != 200:
                return False
            
            result = await response.json()
            return result.get('success', False)