from fastapi import FastAPI
from routers import routers
from pkg.conf import appmeta
from models.database import init_db
from models.migration import init_default_settings
from pkg.lifespan import lifespan
from pkg.JWT import jwt

# 添加初始化数据库启动项
lifespan.add_startup(init_db)
lifespan.add_startup(init_default_settings)
lifespan.add_startup(jwt.load_secret_key)

# 创建应用实例并设置元数据
app = FastAPI(
    title=appmeta.APP_NAME,
    summary=appmeta.summary,
    description=appmeta.description,
    version=appmeta.BackendVersion,
    openapi_tags=appmeta.tags_meta,
    license_info=appmeta.license_info,
    lifespan=lifespan.lifespan,
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
    # uvicorn.run(app=app, host="0.0.0.0", port=5213) # 生产环境
    uvicorn.run(app='main:app', host="0.0.0.0", port=5213, reload=True) # 开发环境