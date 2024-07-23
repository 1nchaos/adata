# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2024/7/23
@log: change log
"""
from datetime import datetime, timedelta


def get_n_days_date(days=0, fmt="%Y-%m-%d"):
    """
    获取 N 天后的日期，
    :param days: 天数；N可以是负数，表示N天前的日期
    :param fmt: 日期格式；默认：%Y-%m-%d
    :return: 对应的日期
    """
    # 获取当前日期
    current_date = datetime.now().date()
    # 计算前N天的日期
    target_date = current_date + timedelta(days=days)
    # 将日期格式化为指定格式
    return target_date.strftime(fmt)


def get_cur_time(fmt="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间，
    """
    return datetime.now().strftime(fmt)
