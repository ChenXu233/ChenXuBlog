import logging
import sys
from pathlib import Path
from types import FrameType
from typing import cast

from loguru import logger

from .config import CONFIG

SAVING_PATH = Path(CONFIG.LOG_PATH)


# 劫持 FastAPI 的日志
class InterceptHandler(logging.Handler):
    """劫持 logging 模块日志到 Loguru"""

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        # 获取日志调用堆栈信息
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# 替换 FastAPI 的日志记录器
def configure_logging():
    # 移除 Loguru 默认处理器
    logger.remove()

    # 控制台输出配置
    logger.add(
        sys.stdout,
        format="<level>{level: <4}</level>|"
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green>| "
        "<level>{message}</level>",
        level=CONFIG.LOG_LEVEL,
        colorize=True,
    )

    # 文件输出配置
    logger.add(
        SAVING_PATH / "app_{time:YYYY-MM-DD}.log",
        rotation="00:00",  # 每天轮转
        retention="7 days",  # 保留7天
        compression="zip",  # 压缩旧日志
        enqueue=True,  # 异步写入
        format="{time:YYYY-MM-DD HH:mm:ss.SSS}|{level: <4}| "
        "{module}:{function}:{line}|{message}",
        level="DEBUG",
    )

    # 劫持标准 logging 模块
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    # 指定需要劫持的日志源
    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"):
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.propagate = False


configure_logging()
logger.info("logger is now configured!")
