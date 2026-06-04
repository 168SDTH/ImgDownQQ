# core/logger.py
import logging
import sys

def setup_logger(name: str = "default", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # 标准化格式：[时间][级别][名称]:消息
        formatter = logging.Formatter(
            "[%(asctime)s][%(levelname)s][%(name)s]:%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger