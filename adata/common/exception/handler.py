# -*- coding: utf-8 -*-
"""
@desc: 异常-空值处理
@author: 1nchaos
@time: 2023/8/14
@log: change log
"""

import functools

import pandas as pd

from adata._logger import get_logger

logger = get_logger(__name__)


def handler_null(func):
    """
    空值处理装饰器：被装饰方法抛出异常时返回空 DataFrame
    异常信息会以 warning 级别记录，便于定位数据源问题，默认不输出到控制台
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:  # pylint: disable=broad-except
            logger.warning("%s 执行异常，返回空结果", func.__qualname__, exc_info=True)
            return pd.DataFrame(data=[], columns=[])

    return wrapper
