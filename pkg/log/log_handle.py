import logging
from rich.logging import RichHandler

FOTMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FOTMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("rich")

def set_log_level(level: str):
    """
    设置日志等级。
    
    :param level: 日志等级 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    :type level: str
    """
    level = level.upper()
    if level == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif level == "INFO":
        logger.setLevel(logging.INFO)
    elif level == "WARNING":
        logger.setLevel(logging.WARNING)
    elif level == "ERROR":
        logger.setLevel(logging.ERROR)
    elif level == "CRITICAL":
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.INFO)
        logger.warning(f"未知的日志等级 '{level}'，已设置为默认等级 'INFO'。")