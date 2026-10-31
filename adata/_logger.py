# -*- coding: utf-8 -*-
"""
@desc: adata 统一日志入口
@author: 1nchaos
@time: 2026/11/01
@log: logger 实现下沉，避免子模块反向依赖 adata 包导致循环导入
"""

import logging

LOGGER_NAME = "adata"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

logger = logging.getLogger(LOGGER_NAME)

# 库默认不输出日志：未配置 handler 时 propagate 到 root，由调用方决定是否展示
if not logger.handlers:
    logger.addHandler(logging.NullHandler())


def get_logger(name=None):
    """
    获取 adata 命名空间下的 logger
    :param name: 模块名，一般传 __name__；为空时返回 adata 根 logger
    :return: logging.Logger
    """
    if not name or name == LOGGER_NAME:
        return logger
    # 模块名本身以 adata 开头，去掉前缀避免出现 adata.adata.xxx
    if name.startswith(LOGGER_NAME + "."):
        name = name[len(LOGGER_NAME) + 1:]
    return logger.getChild(name)


def set_logger(level=None):
    """
    为 adata logger 挂载控制台输出，重复调用不会叠加 handler
    :param level: 日志级别，如 logging.DEBUG；为空时保持原有级别
    :return: logging.Logger
    """
    has_console = any(getattr(handler, "_adata_console", False) for handler in logger.handlers)
    if not has_console:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
        handler._adata_console = True
        logger.addHandler(handler)
    if level is not None:
        logger.setLevel(level)
    return logger
