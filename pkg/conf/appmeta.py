import os
from dotenv import load_dotenv
from pkg.log import log

load_dotenv()

APP_NAME = 'DiskNext Server'
summary = '一款基于 FastAPI 的可公私兼备的网盘系统'
description = 'DiskNext Server 是一款基于 FastAPI 的网盘系统，支持个人和企业使用。它提供了高性能的文件存储和管理功能，支持多种认证方式。'
license_info = {"name": "GPLv3", "url": "https://opensource.org/license/gpl-3.0"}

BackendVersion = "0.0.1"

IsPro = False

debug: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

if debug:
    log.info("Debug mode is enabled. This is not recommended for production use.")

host: str = os.getenv("HOST", "0.0.0.0")
port: int = int(os.getenv("PORT", 5213))

log.info(f"Starting DiskNext Server {BackendVersion} on {host}:{port}")

database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///disknext.db")

tags_meta = [
    {
        "name": "site",
        "description": "站点",
    },
    {
        "name": "user",
        "description": "用户",
    },
    {
        "name": "user_settings",
        "description": "用户设置",
    },
    {
        "name": "share",
        "description": "分享",
    },
    {
        "name": "file",
        "description": "文件",
    },
    {
        "name": "aria2",
        "description": "离线下载",
    },
    {
        "name": "directory",
        "description": "目录",
    },
    {
        "name": "object",
        "description": "对象，文件和目录的抽象",
    },
    {
        "name": "callback",
        "description": "回调接口",
    },
    {
        "name": "oauth",
        "description": "OAuth 认证",
    },
    {
        "name": "pay",
        "description": "支付回调",
    },
    {
        "name": "upload",
        "description": "上传回调",
    },
    {
        "name": "vas",
        "description": "增值服务",
    },
    {
        "name": "tag",
        "description": "用户标签",
    },
    {
        "name": "webdav",
        "description": "WebDAV管理相关",
    },
    {
        "name": "admin",
        "description": "管理员接口",
    },
    {
        "name": "admin_group",
        "description": "管理员组接口",
    },
    {
        "name": "admin_user",
        "description": "管理员用户接口",
    },
    {
        "name": "admin_file",
        "description": "管理员文件接口",
    },
    {
        "name": "admin_aria2",
        "description": "管理员离线下载接口",
    },
    {
        "name": "admin_policy",
        "description": "管理员策略接口",
    },
    {
        "name": "admin_task",
        "description": "管理员任务接口",
    },
    {
        "name": "admin_vas",
        "description": "管理员增值服务接口",
    }
]