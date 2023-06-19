# -*- coding: utf-8 -*-
"""
@desc: 股票行情
@author: 1nchaos
@time: 2023/3/29
@log: change log
TODO 数据返回类型转换
"""

import pandas as pd

from adata.stock.market.stock_market import *


class StockMarket(object):
    """
    股票行情
    """

    def __init__(self) -> None:
        super().__init__()

    def get_market(self, stock_code: str = '000001', start_date='1990-01-01', k_type=1, adjust_type: int = 1):
        """
        获取单个股票的行情
        :param stock_code: 股票代码
        :param start_date: 开始时间
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权 （目前：只有前复权,作为股票交易已经可用）
        :return: k线行情数据
        """
        return StockMarketBaiDu().get_market(stock_code=stock_code, start_date=start_date, k_type=k_type)

    def get_market_min(self, stock_code: str = '000001'):
        """
        获取单个股票的今日分时行情
        :param stock_code: 股票代码
        :return: 当日分钟行情数据
        """
        return StockMarketBaiDu().get_market_min(stock_code=stock_code)

    def list_market_current(self, code_list=None):
        """
        获取多个股票最新行情信息
        :param code_list: 股票代码
        :return: 当前最新的行情价格信息
        stock_code: 股票代码
        short_name: 股票简称
        price: 当前价格（元）
        change: 涨跌额（元）
        change_pct: 涨跌幅（%）
        volume: 成交量（股）
        amount: 成交金额（元）
        """
        if code_list is None:
            return pd.DataFrame()
        # 1. 先查询新浪
        df = StockMarketSina().list_market_current(code_list=code_list)
        # 2. 然后腾讯
        if df.empty:
            df = StockMarketQQ().list_market_current(code_list=code_list)
        return df


if __name__ == '__main__':
    print(StockMarket().get_market(stock_code='000001', start_date='2021-01-01', k_type=1))
    print(StockMarket().get_market_min(stock_code='000001'))
    print(StockMarket().list_market_current(code_list=['000001', '600001', '000795', '872925']))
