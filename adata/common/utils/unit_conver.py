# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2024/7/1
@log: change log
"""

import re


def convert_to_yuan(input_dict):
    """
    将字典中特定字段的值从带'亿'或'万'的字符串转换为以元为单位的浮点数。

    :param input_dict: 包含待转换值的字典
    """
    unit_multipliers = {'亿': 100000000, '万': 10000}

    for key, value in input_dict.items():
        input_dict[key] = value.replace('元', '')
        if isinstance(value, str) and any(unit in value for unit in unit_multipliers.keys()):
            number, unit = re.findall(r'([-+]?\d*\.\d+|\d+)([亿万]?)', value)[0]
            number = float(number)
            input_dict[key] = number * unit_multipliers[unit]
    return input_dict
