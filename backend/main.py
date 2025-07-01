# -*- coding: utf-8 -*-
# @author: xiaobai
from contextlib import asynccontextmanager

import click
from fastapi import FastAPI, Depends
from granian import Granian
from autotest.db.my_redis import redis_pool
from autotest.init.cors import init_cors
from autotest.init.dependencies import login_verification
from autotest.init.exception import init_exception
from autotest.init.logger_init import init_logger, logger
from autotest.init.middleware import init_middleware
from autotest.init.mount import init_mount
from autotest.init.routers import init_router
from config import config


@asynccontextmanager
async def start_app(app: FastAPI):
    click.echo(config.PROJECT_BANNER)
    init_logger()
    logger.info("日志初始化成功！！!")  # 初始化日志
    redis_pool.init_by_config(config=config)
    logger.info("Redis连接池初始化成功！！!")
    yield

    if redis_pool.redis:
        await redis_pool.redis.close()


def create_app():
    """ 注册中心 """
    app = FastAPI(title="zerorunner",
                  description=config.PROJECT_DESC,
                  version=config.PROJECT_VERSION,
                  lifespan=start_app,
                  dependencies=[Depends(login_verification)])

    init_mount(app)  # 挂载静态文件

    init_exception(app)  # 注册捕获全局异常

    init_router(app)  # 注册路由

    init_middleware(app)  # 注册请求响应拦截

    init_cors(app)  # 注册请求响应拦截

    return app


app = create_app()

# granian --interface asgi --workers 2 --http2 --host 0.0.0.0 --port 9101 main:app
# Create an instance of the Granian server
if __name__ == "__main__":
    Granian(
        "main:app",
        interface="asgi",
        address="0.0.0.0",
        port=9101,
        reload=True,
    ).serve()

