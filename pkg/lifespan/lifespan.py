from fastapi import FastAPI
from contextlib import asynccontextmanager

__on_startup: list[callable] = []
__on_shutdown: list[callable] = []

def add_startup(func: callable):
    """
    注册一个函数，在应用启动时调用。
    
    :param func: 需要注册的函数。它应该是一个异步函数。
    """
    __on_startup.append(func)

def add_shutdown(func: callable):
    """
    注册一个函数，在应用关闭时调用。
    
    :param func: 需要注册的函数。
    """
    __on_shutdown.append(func)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用程序的生命周期管理器。
    
    此函数在应用启动时执行所有注册的启动函数，
    并在应用关闭时执行所有注册的关闭函数。
    """
    # Execute all startup functions
    for func in __on_startup:
        await func()
    
    yield
    
    # Execute all shutdown functions
    for func in __on_shutdown:
        await func()