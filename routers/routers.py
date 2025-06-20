from fastapi import APIRouter

from .controllers import (
    share,
    site,
    user,
    file,
    aria2,
    directory,
    object,
    callback,
    vas,
    tag,
    webdav,
    admin,
    slave
)

Router: list[APIRouter] = [
    share.share_router,
    site.site_router,
    user.user_router,
    user.user_settings_router,
    file.file_router,
    file.file_upload_router,
    aria2.aria2_router,
    directory.directory_router,
    object.object_router,
    callback.callback_router,
    callback.oauth_router,
    callback.pay_router,
    callback.upload_router,
    vas.vas_router,
    tag.tag_router,
    webdav.webdav_router,
    admin.admin_router,
    admin.admin_group_router,
    admin.admin_user_router,
    admin.admin_file_router,
    admin.admin_aria2_router,
    admin.admin_policy_router,
    admin.admin_task_router,
    admin.admin_vas_router,
    slave.slave_router,
    slave.slave_aria2_router
]