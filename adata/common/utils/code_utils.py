# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/12/4
@log: change log
"""


def compile_exchange_by_stock_code(stock_code):
    """根据股票代码补全市场后缀"""
    exchange_suffix = {
        '0': '.SZ',
        '3': '.SZ',
        '6': '.SH',
        '9': '.SH',
        '4': '.BJ',
        '8': '.BJ'
    }
    prefix = stock_code[0]
    if prefix in exchange_suffix:
        return stock_code + exchange_suffix[prefix]
    return stock_code


def get_exchange_by_stock_code(stock_code):
    """根据股票代码补全市场后缀"""
    exchange_suffix = {
        '0': 'SZ',
        '3': 'SZ',
        '6': 'SH',
        '9': 'SH',
        '4': 'BJ',
        '8': 'BJ'
    }
    return exchange_suffix[stock_code[0]]
