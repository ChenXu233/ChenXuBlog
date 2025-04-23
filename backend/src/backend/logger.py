import logging
import sys
from pathlib import Path

from fastapi.logger import logger as fastapi_logger
from loguru import logger

from .config import CONFIG

SAVING_PATH = Path(CONFIG.log_path)

# 配置 loguru 日志
logger.remove()

# 添加控制台日志输出
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)

# 添加日志文件输出
logger.add(
    SAVING_PATH / "app_{time:YYYY-MM-DD}.log",  # 日志文件路径，按日期分割
    rotation="00:00",  # 每天午夜创建新日志文件
    retention="7 days",  # 保留 7 天的日志
    compression="zip",  # 压缩旧日志文件
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)


# 劫持 FastAPI 的日志
class InterceptHandler(logging.Handler):
    """
    自定义日志处理器，用于将标准日志记录器的输出重定向到 loguru。
    """

    def emit(self, record):
        # 将标准日志记录器的日志转换为 loguru 的日志
        loguru_level = (
            logger.level(record.levelname).name
            if logger.level(record.levelname, no=None) is not None
            else "INFO"
        )
        logger.opt(depth=6, exception=record.exc_info).log(
            loguru_level, record.getMessage()
        )


# 替换 FastAPI 的日志记录器
def setup_fastapi_logger():
    fastapi_logger.handlers = [InterceptHandler()]
    fastapi_logger.propagate = False


setup_fastapi_logger()
logger.info("Loguru logger is now configured!")
