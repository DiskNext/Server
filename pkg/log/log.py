from rich import print
from rich.console import Console
from rich.markdown import Markdown
from typing import Literal, Optional, Dict, Union
from enum import Enum
import time
import os
import inspect

class LogLevelEnum(str, Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    SUCCESS = 'success'

# 默认日志级别
LogLevel = LogLevelEnum.INFO

def set_log_level(level: Union[str, LogLevelEnum]) -> None:
    """设置日志级别"""
    global LogLevel
    if isinstance(level, str):
        try:
            LogLevel = LogLevelEnum(level.lower())
        except ValueError:
            print(f"[bold red]无效的日志级别: {level}，使用默认级别: {LogLevel}[/bold red]")
    else:
        LogLevel = level

def truncate_path(full_path: str, marker: str = "HeyAuth") -> str:
    """截断路径，只保留从marker开始的部分"""
    try:
        marker_index = full_path.find(marker)
        if marker_index != -1:
            return '.' + full_path[marker_index + len(marker):]
        return full_path
    except Exception:
        return full_path

def get_caller_info(depth: int = 2) -> tuple:
    """获取调用者信息"""
    try:
        frame = inspect.currentframe()
        # 向上查找指定深度的调用帧
        for _ in range(depth):
            if frame.f_back is None:
                break
            frame = frame.f_back
            
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        return truncate_path(filename), lineno
    except Exception:
        return "<unknown>", 0
    finally:
        # 确保引用被释放
        del frame

def log(level: str = 'debug', message: str = ''):
    """
    输出日志
    ---
    通过传入的`level`和`message`参数，输出不同级别的日志信息。<br>
    `level`参数为日志级别，支持`红色error`、`紫色info`、`绿色success`、`黄色warning`、`淡蓝色debug`。<br>
    `message`参数为日志信息。<br>
    """
    level_colors: Dict[str, str] = {
        'debug': '[bold cyan][DEBUG][/bold cyan]',
        'info': '[bold blue][INFO][/bold blue]',
        'warning': '[bold yellow][WARN][/bold yellow]',
        'error': '[bold red][ERROR][/bold red]',
        'success': '[bold green][SUCCESS][/bold green]'
    }
    
    level_value = level.lower()
    lv = level_colors.get(level_value, '[bold magenta][UNKNOWN][/bold magenta]')
    
    # 获取调用者信息
    filename, lineno = get_caller_info(3)  # 考虑lambda调用和包装函数，深度为3
    timestamp = time.strftime('%Y/%m/%d %H:%M:%S %p', time.localtime())
    log_message = f"{lv}\t{timestamp} [bold]From {filename}, line {lineno}[/bold] {message}"
    
    # 根据日志级别判断是否输出
    global LogLevel
    should_log = False
    
    if level_value == 'debug' and LogLevel == LogLevelEnum.DEBUG:
        should_log = True
    elif level_value == 'info' and LogLevel in [LogLevelEnum.DEBUG, LogLevelEnum.INFO]:
        should_log = True
    elif level_value == 'warning' and LogLevel in [LogLevelEnum.DEBUG, LogLevelEnum.INFO, LogLevelEnum.WARNING]:
        should_log = True
    elif level_value == 'error':
        should_log = True
    elif level_value == 'success':
        should_log = False
        
    if should_log:
        print(log_message)

# 便捷日志函数
debug = lambda message: log('debug', message)
info = lambda message: log('info', message)
warning = lambda message: log('warn', message)
error = lambda message: log('error', message)
success = lambda message: log('success', message)

def title(title: str = '海枫授权系统 HeyAuth', size: Optional[Literal['h1', 'h2', 'h3', 'h4', 'h5']] = 'h1'):
    """
    输出标题
    ---
    通过传入的`title`参数，输出一个整行的标题。<br>
    `title`参数为标题内容。<br>
    """
    try:
        console = Console()
        markdown_sizes = {
            'h1': '# ',
            'h2': '## ',
            'h3': '### ',
            'h4': '#### ',
            'h5': '##### '
        }
        
        markdown_tag = markdown_sizes.get(size, '# ')
        console.print(Markdown(markdown_tag + title))
    except Exception as e:
        error(f"输出标题失败: {e}")
    finally:
        if 'console' in locals():
            del console

if True:
    pass


if __name__ == '__main__':
    # 测试代码
    title('海枫授权系统 日志组件测试', 'h1')
    title('测试h2标题', 'h2')
    title('测试h3标题', 'h3')
    title('测试h4标题', 'h4')
    title('测试h5标题', 'h5')
    
    print("\n默认日志级别(INFO)测试:")
    debug('这是一个debug日志')  # 不会显示
    info('这是一个info日志')
    warning('这是一个warning日志')
    error('这是一个error日志')
    success('这是一个success日志')
    
    print("\n设置为DEBUG级别测试:")
    set_log_level(LogLevelEnum.DEBUG)
    debug('这是一个debug日志')  # 现在会显示