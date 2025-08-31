from fastapi import FastAPI
from routers import routers
from pkg.conf import appmeta
from models.database import init_db
from models.migration import migration
from pkg.lifespan import lifespan
from pkg.JWT import JWT
from pkg.log import log, set_log_level

# 添加初始化数据库启动项
lifespan.add_startup(init_db)
lifespan.add_startup(migration)
lifespan.add_startup(JWT.load_secret_key)

# 设置日志等级
if appmeta.debug:
    set_log_level('DEBUG')
else:
    set_log_level('INFO')

# 创建应用实例并设置元数据
app = FastAPI(
    title=appmeta.APP_NAME,
    summary=appmeta.summary,
    description=appmeta.description,
    version=appmeta.BackendVersion,
    openapi_tags=appmeta.tags_meta,
    license_info=appmeta.license_info,
    lifespan=lifespan.lifespan,
    debug=appmeta.debug,
)

# 挂载路由
for router in routers.Router:
    app.include_router(
        router,
        prefix='/api',
        responses={
            200: {"description": "成功响应 Successful operation"},
            401: {"description": "未授权 Unauthorized"},
            403: {"description": "禁止访问 Forbidden"},
            404: {"description": "未找到 Not found"},
            500: {"description": "内部服务器错误 Internal server error"}
        },)

# 启动时打印欢迎信息
if __name__ == "__main__":
    import uvicorn

    if appmeta.debug:
        uvicorn.run(app='main:app', host=appmeta.host, port=appmeta.port, reload=True)
    else:
        uvicorn.run(app=app, host=appmeta.host, port=appmeta.port)