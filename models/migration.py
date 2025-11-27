
from .setting import Setting
from pkg.conf.appmeta import BackendVersion
from .response import ThemeModel
from pkg.password.pwd import Password
from loguru import logger as log

async def migration() -> None:
    """
    数据库迁移函数，初始化默认设置和用户组。
    
    :return: None
    """
    
    log.info('开始进行数据库初始化...')
    
    await init_default_settings()
    await init_default_group()
    await init_default_user()
    
    log.info('数据库初始化结束')

default_settings: list[Setting] = [
    Setting(name="siteURL", value="http://localhost", type="basic"),
    Setting(name="siteName", value="DiskNext", type="basic"),
    Setting(name="register_enabled", value="1", type="register"),
    Setting(name="default_group", value="2", type="register"),
    Setting(name="siteKeywords", value="网盘，网盘", type="basic"),
    Setting(name="siteDes", value="DiskNext", type="basic"),
    Setting(name="siteTitle", value="云星启智", type="basic"),
    Setting(name="fromName", value="DiskNext", type="mail"),
    Setting(name="mail_keepalive", value="30", type="mail"),
    Setting(name="fromAdress", value="no-reply@yxqi.cn", type="mail"),
    Setting(name="smtpHost", value="smtp.yxqi.cn", type="mail"),
    Setting(name="smtpPort", value="25", type="mail"),
    Setting(name="replyTo", value="feedback@yxqi.cn", type="mail"),
    Setting(name="smtpUser", value="no-reply@yxqi.cn", type="mail"),
    Setting(name="smtpPass", value="", type="mail"),
    Setting(name="maxEditSize", value="4194304", type="file_edit"),
    Setting(name="archive_timeout", value="60", type="timeout"),
    Setting(name="download_timeout", value="60", type="timeout"),
    Setting(name="preview_timeout", value="60", type="timeout"),
    Setting(name="doc_preview_timeout", value="60", type="timeout"),
    Setting(name="upload_credential_timeout", value="1800", type="timeout"),
    Setting(name="upload_session_timeout", value="86400", type="timeout"),
    Setting(name="slave_api_timeout", value="60", type="timeout"),
    Setting(name="onedrive_monitor_timeout", value="600", type="timeout"),
    Setting(name="share_download_session_timeout", value="2073600", type="timeout"),
    Setting(name="onedrive_callback_check", value="20", type="timeout"),
    Setting(name="aria2_call_timeout", value="5", type="timeout"),
    Setting(name="onedrive_chunk_retries", value="1", type="retry"),
    Setting(name="onedrive_source_timeout", value="1800", type="timeout"),
    Setting(name="reset_after_upload_failed", value="0", type="upload"),
    Setting(name="login_captcha", value="0", type="login"),
    Setting(name="reg_captcha", value="0", type="login"),
    Setting(name="email_active", value="0", type="register"),
    Setting(name="mail_activation_template", value="""<!DOCTYPE html PUBLIC"-//W3C//DTD XHTML 1.0 Transitional//EN""http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; box-sizing: border-box; 
font-size: 14px; margin: 0;"><head><meta name="viewport"content="width=device-width"/><meta http-equiv="Content-Type"content="text/html; charset=UTF-8"/><title>激活您的账户</title><style type="text/css">img{max-width:100%}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width:100%!important;height:100%;line-height:1.6em}body{background-color:#f6f6f6}@media only screen and(max-width:640px){body{padding:0!important}h1{font-weight:800!important;margin:20px 0 5px!important}h2{font-weight:800!important;margin:20px 0 5px!important}h3{font-weight:800!important;margin:20px 0 5px!important}h4{font-weight:800!important;margin:20px 0 5px!important}h1{font-size:22px!important}h2{font-size:18px!important}h3{font-size:16px!important}.container{padding:0!important;width:100%!important}.content{padding:0!important}.content-wrap{padding:10px!important}.invoice{width:100%!important}}</style></head><body itemscope itemtype="http://schema.org/EmailMessage"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: 
border-box; font-size: 14px; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: none; width: 100% !important; height: 100%; line-height: 1.6em; background-color: #f6f6f6; margin: 0;"bgcolor="#f6f6f6"><table class="body-wrap"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; background-color: #f6f6f6; margin: 0;"bgcolor="#f6f6f6"><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; 
box-sizing: border-box; font-size: 14px; margin: 0;"><td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;"valign="top"></td><td class="container"width="600"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; display: block !important; max-width: 600px !important; clear: both !important; margin: 0 auto;"valign="top"><div class="content"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; max-width: 600px; display: block; margin: 0 auto; padding: 20px;"><table class="main"width="100%"cellpadding="0"cellspacing="0"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; border-radius: 3px; background-color: #fff; margin: 0; border: 1px 
solid #e9e9e9;"bgcolor="#fff"><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 
14px; margin: 0;"><td class="alert alert-warning"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 16px; vertical-align: top; color: #fff; font-weight: 500; text-align: center; border-radius: 3px 3px 0 0; background-color: #009688; margin: 0; padding: 20px;"align="center"bgcolor="#FF9F00"valign="top">激活{siteTitle}账户</td></tr><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><td class="content-wrap"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 20px;"valign="top"><table width="100%"cellpadding="0"cellspacing="0"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><td class="content-block"style="font-family: 'Helvetica 
Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;"valign="top">亲爱的<strong style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">{userName}</strong>：</td></tr><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><td class="content-block"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;"valign="top">感谢您注册{siteTitle},请点击下方按钮完成账户激活。</td></tr><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><td class="content-block"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;"valign="top"><a href="{activationUrl}"class="btn-primary"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; color: #FFF; text-decoration: none; line-height: 2em; font-weight: bold; text-align: center; cursor: pointer; display: inline-block; border-radius: 5px; text-transform: capitalize; background-color: #009688; margin: 0; border-color: #009688; border-style: solid; border-width: 10px 20px;">激活账户</a></td></tr><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><td class="content-block"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;"valign="top">感谢您选择{siteTitle}。</td></tr></table></td></tr></table><div class="footer"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; clear: both; color: #999; margin: 0; padding: 20px;"><table width="100%"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><td class="aligncenter content-block"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 12px; vertical-align: top; color: #999; text-align: center; margin: 0; padding: 0 0 20px;"align="center"valign="top">此邮件由系统自动发送，请不要直接回复。</td></tr></table></div></div></td><td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;"valign="top"></td></tr></table></body></html>""", type="mail_template"),
    Setting(name="forget_captcha", value="0", type="login"),
    Setting(name="mail_reset_pwd_template", value="""<!DOCTYPE html PUBLIC"-//W3C//DTD XHTML 1.0 Transitional//EN""http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; box-sizing: border-box; 
font-size: 14px; margin: 0;"><head><meta name="viewport"content="width=device-width"/><meta http-equiv="Content-Type"content="text/html; charset=UTF-8"/><title>重设密码</title><style type="text/css">img{max-width:100%}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width:100%!important;height:100%;line-height:1.6em}body{background-color:#f6f6f6}@media only screen and(max-width:640px){body{padding:0!important}h1{font-weight:800!important;margin:20px 0 5px!important}h2{font-weight:800!important;margin:20px 0 5px!important}h3{font-weight:800!important;margin:20px 0 5px!important}h4{font-weight:800!important;margin:20px 0 5px!important}h1{font-size:22px!important}h2{font-size:18px!important}h3{font-size:16px!important}.container{padding:0!important;width:100%!important}.content{padding:0!important}.content-wrap{padding:10px!important}.invoice{width:100%!important}}</style></head><body itemscope itemtype="http://schema.org/EmailMessage"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: 
border-box; font-size: 14px; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: none; width: 100% !important; height: 100%; line-height: 1.6em; background-color: #f6f6f6; margin: 0;"bgcolor="#f6f6f6"><table class="body-wrap"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; background-color: #f6f6f6; margin: 0;"bgcolor="#f6f6f6"><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; 
box-sizing: border-box; font-size: 14px; margin: 0;"><td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;"valign="top"></td><td class="container"width="600"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; display: block !important; max-width: 600px !important; clear: both !important; margin: 0 auto;"valign="top"><div class="content"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; max-width: 600px; display: block; margin: 0 auto; padding: 20px;"><table class="main"width="100%"cellpadding="0"cellspacing="0"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; border-radius: 3px; background-color: #fff; margin: 0; border: 1px 
solid #e9e9e9;"bgcolor="#fff"><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 
14px; margin: 0;"><td class="alert alert-warning"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 16px; vertical-align: top; color: #fff; font-weight: 500; text-align: center; border-radius: 3px 3px 0 0; background-color: #2196F3; margin: 0; padding: 20px;"align="center"bgcolor="#FF9F00"valign="top">重设{siteTitle}密码</td></tr><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><td class="content-wrap"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 20px;"valign="top"><table width="100%"cellpadding="0"cellspacing="0"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><td class="content-block"style="font-family: 'Helvetica 
Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;"valign="top">亲爱的<strong style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">{userName}</strong>：</td></tr><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><td class="content-block"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;"valign="top">请点击下方按钮完成密码重设。如果非你本人操作，请忽略此邮件。</td></tr><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><td class="content-block"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;"valign="top"><a href="{resetUrl}"class="btn-primary"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; color: #FFF; text-decoration: none; line-height: 2em; font-weight: bold; text-align: center; cursor: pointer; display: inline-block; border-radius: 5px; text-transform: capitalize; background-color: #2196F3; margin: 0; border-color: #2196F3; border-style: solid; border-width: 10px 20px;">重设密码</a></td></tr><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><td class="content-block"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;"valign="top">感谢您选择{siteTitle}。</td></tr></table></td></tr></table><div class="footer"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; clear: both; color: #999; margin: 0; padding: 20px;"><table width="100%"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;"><td class="aligncenter content-block"style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 12px; vertical-align: top; color: #999; text-align: center; margin: 0; padding: 0 0 20px;"align="center"valign="top">此邮件由系统自动发送，请不要直接回复。</td></tr></table></div></div></td><td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;"valign="top"></td></tr></table></body></html>""", type="mail_template"),
    Setting(name=f"db_version_{BackendVersion}", value="installed", type="version"),
    Setting(name="hot_share_num", value="10", type="share"),
    Setting(name="gravatar_server", value="https://www.gravatar.com/", type="avatar"),
    Setting(name="defaultTheme", value="#3f51b5", type="basic"),
    Setting(name="themes", value=ThemeModel().model_dump(), type="basic"),
    Setting(name="aria2_token", value="", type="aria2"),
    Setting(name="aria2_rpcurl", value="", type="aria2"),
    Setting(name="aria2_temp_path", value="", type="aria2"),
    Setting(name="aria2_options", value="{}", type="aria2"),
    Setting(name="aria2_interval", value="60", type="aria2"),
    Setting(name="max_worker_num", value="10", type="task"),
    Setting(name="max_parallel_transfer", value="4", type="task"),
    Setting(name="secret_key", value=Password.generate(256), type="auth"),
    Setting(name="temp_path", value="temp", type="path"),
    Setting(name="avatar_path", value="avatar", type="path"),
    Setting(name="avatar_size", value="2097152", type="avatar"),
    Setting(name="avatar_size_l", value="200", type="avatar"),
    Setting(name="avatar_size_m", value="130", type="avatar"),
    Setting(name="avatar_size_s", value="50", type="avatar"),
    Setting(name="home_view_method", value="icon", type="view"),
    Setting(name="share_view_method", value="list", type="view"),
    Setting(name="cron_garbage_collect", value="@hourly", type="cron"),
    Setting(name="authn_enabled", value="0", type="authn"),
    Setting(name="captcha_height", value="60", type="captcha"),
    Setting(name="captcha_width", value="240", type="captcha"),
    Setting(name="captcha_mode", value="3", type="captcha"),
    Setting(name="captcha_ComplexOfNoiseText", value="0", type="captcha"),
    Setting(name="captcha_ComplexOfNoiseDot", value="0", type="captcha"),
    Setting(name="captcha_IsShowHollowLine", value="0", type="captcha"),
    Setting(name="captcha_IsShowNoiseDot", value="1", type="captcha"),
    Setting(name="captcha_IsShowNoiseText", value="0", type="captcha"),
    Setting(name="captcha_IsShowSlimeLine", value="1", type="captcha"),
    Setting(name="captcha_IsShowSineLine", value="0", type="captcha"),
    Setting(name="captcha_CaptchaLen", value="6", type="captcha"),
    Setting(name="captcha_IsUseReCaptcha", value="0", type="captcha"),
    Setting(name="captcha_ReCaptchaKey", value="defaultKey", type="captcha"),
    Setting(name="captcha_ReCaptchaSecret", value="defaultSecret", type="captcha"),
    Setting(name="thumb_width", value="400", type="thumb"),
    Setting(name="thumb_height", value="300", type="thumb"),
    Setting(name="pwa_small_icon", value="/static/img/favicon.ico", type="pwa"),
    Setting(name="pwa_medium_icon", value="/static/img/logo192.png", type="pwa"),
    Setting(name="pwa_large_icon", value="/static/img/logo512.png", type="pwa"),
    Setting(name="pwa_display", value="standalone", type="pwa"),
    Setting(name="pwa_theme_color", value="#000000", type="pwa"),
    Setting(name="pwa_background_color", value="#ffffff", type="pwa"),
]

async def init_default_settings() -> None:
    from .setting import Setting
    
    log.info('初始化设置...')
    
    try:
        # 检查是否已经存在版本设置
        ver = await Setting.get(type="version", name=f"db_version_{BackendVersion}")
        if ver == "installed":
            return
        else: raise ValueError("Database version mismatch or not installed.")
    except:
        for setting in default_settings:
            await Setting.add(
                type=setting.type, 
                name=setting.name, 
                value=setting.value
            )

async def init_default_group() -> None:
    from .group import Group
    
    log.info('初始化用户组...')
    
    try:
        # 未找到初始管理组时，则创建
        if not await Group.get(id=1):
            await Group.create(
                name="管理员",
                max_storage=1 * 1024 * 1024 * 1024,  # 1GB
                share_enabled=True,
                web_dav_enabled=True,
                options={
                    "ArchiveDownload": True,
                    "ArchiveTask": True,
                    "ShareDownload": True,
                    "Aria2": True,
                }
            )
    except Exception as e:
        raise RuntimeError(f"无法创建管理员用户组: {e}")

    try:
        # 未找到初始注册会员时，则创建
        if not await Group.get(id=2):
            await Group.create(
                name="注册会员",
                max_storage=1 * 1024 * 1024 * 1024,  # 1GB
                share_enabled=True,
                web_dav_enabled=True,
                options={
                    "ShareDownload": True,
                }
            )
    except Exception as e:
        raise RuntimeError(f"无法创建初始注册会员用户组: {e}")
    
    try:
        # 未找到初始游客组时，则创建
        if not await Group.get(id=3):
            await Group.create(
                name="游客",
                policies="[]",
                share_enabled=False,
                web_dav_enabled=False,
                options={
                    "ShareDownload": True,
                }
            )
    except Exception as e:
        raise RuntimeError(f"无法创建初始游客用户组: {e}")

async def init_default_user() -> None:

    log.info('初始化管理员用户...')

    from .user import User
    from .group import Group
    from .database import get_session

    async for session in get_session():
        # 检查管理员用户是否存在
        admin_user = await User.get(session, User.id == 1)

        if not admin_user:
            # 创建初始管理员用户

            # 获取管理员组
            admin_group = await Group.get(id=1)
            if not admin_group:
                raise RuntimeError("管理员用户组不存在，无法创建管理员用户")

            # 生成管理员密码
            from pkg.password.pwd import Password
            admin_password = Password.generate(8)
            hashed_admin_password = Password.hash(admin_password)

            admin_user = User(
                email="admin@yxqi.cn",
                nick="admin",
                status=True,  # 正常状态
                group_id=admin_group.id,
                password=hashed_admin_password,
            )

            admin_user = await admin_user.save(session)

            log.info(f'初始管理员账号：[bold]admin@yxqi.cn[/bold]')
            log.info(f'初始管理员密码：[bold]{admin_password}[/bold]')