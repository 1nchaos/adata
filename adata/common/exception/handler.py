# -*- coding: utf-8 -*-
"""
@desc: 异常-空值处理
@author: 1nchaos
@time: 2023/8/14
@log: change log
"""

import pandas as pd


def handler_null(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return pd.DataFrame(data=[], columns=[])

    return wrapper
