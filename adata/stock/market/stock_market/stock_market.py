# -*- coding: utf-8 -*-
"""
@desc: 股票行情
@author: 1nchaos
@time: 2023/3/29
@log: change log
TODO 数据返回类型转换
"""

import pandas as pd

from adata.stock.market.stock_market.stock_market_baidu import StockMarketBaiDu
from adata.stock.market.stock_market.stock_market_east import StockMarketEast
from adata.stock.market.stock_market.stock_market_qq import StockMarketQQ
from adata.stock.market.stock_market.stock_market_sina import StockMarketSina


class StockMarket(object):
    """
    股票行情
    """

    def __init__(self) -> None:
        super().__init__()
        self.sina_market = StockMarketSina()
        self.qq_market = StockMarketQQ()
        self.baidu_market = StockMarketBaiDu()
        self.east_market = StockMarketEast()

    def get_market(self, stock_code: str = '000001', start_date='1990-01-01', end_date=None, k_type=1,
                   adjust_type: int = 1):
        """
        获取单个股票的行情
        :param stock_code: 股票代码
        :param start_date: 开始时间
        :param end_date: 结束日期
        :param k_type: k线类型：1.日；2.周；3.月,4季度，5.5min，15.15min，30.30min，60.60min 默认：1 日k
        :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权 （目前：只有前复权,作为股票交易已经可用）
        :return: k线行情数据
        """
        df = self.east_market.get_market(stock_code=stock_code, start_date=start_date, end_date=end_date,
                                         k_type=k_type, adjust_type=adjust_type)
        # if df.empty:
        #     df = self.baidu_market.get_market(stock_code=stock_code, start_date=start_date, k_type=k_type)
        return df

    def get_market_min(self, stock_code: str = '000001'):
        """
        获取单个股票的今日分时行情
        :param stock_code: 股票代码
        :return: 当日分钟行情数据
        """
        return self.baidu_market.get_market_min(stock_code=stock_code)

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
        df = self.sina_market.list_market_current(code_list=code_list)
        # 2. 然后腾讯
        if df.empty:
            df = self.qq_market.list_market_current(code_list=code_list)
        return df

    def get_market_five(self, stock_code: str = '000001'):
        """
        获取单个股票的5档行情
        其中：百度的接口数据更精准，精确到了股。腾讯的精确到手
        :param stock_code: 股票代码
        :return: 最新的五档行情
        """
        res_df = self.qq_market.get_market_five(stock_code=stock_code)
        if res_df.empty:
            res_df = self.baidu_market.get_market_five(stock_code=stock_code)
        return res_df

    def get_market_bar(self, stock_code: str = '000001'):
        """
        获取单个股票的分时成交
        :param stock_code: 股票代码
        :return: 最新当天的分时成交
        """
        return self.baidu_market.get_market_bar(stock_code=stock_code)


if __name__ == '__main__':
    print(StockMarket().get_market(stock_code='002230', start_date='2024-07-22', k_type=1))
    print(StockMarket().get_market_min(stock_code='000001'))
    print(StockMarket().list_market_current(code_list=['000001', '600001', '000795', '872925']))
    print(StockMarket().get_market_five(stock_code='000001'))
    print(StockMarket().get_market_bar(stock_code='872925'))
