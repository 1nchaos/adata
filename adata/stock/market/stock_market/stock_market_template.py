# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""


class StockMarketTemplate(object):
    """
    股票行情
    """
    _MARKET_COLUMNS = ['trade_time', 'open', 'close', 'volume', 'high', 'low', 'amount', 'change', 'change_pct',
                       'turnover_ratio', 'pre_close']
    _MARKET_MIN_COLUMNS = ['stock_code', 'trade_time', 'price', 'change', 'change_pct', 'volume', 'avg_price', 'amount']
    _MARKET_CURRENT_COLUMNS = ['stock_code', 'short_name', 'price', 'change', 'change_pct', 'volume', 'amount']
    _MARKET_FIVE_COLUMNS = ['stock_code', 'short_name', 's5', 'sv5', 's4', 'sv4', 's3', 'sv3', 's2', 'sv2', 's1', 'sv1',
                            'b1', 'bv1', 'b2', 'bv2', 'b3', 'bv3', 'b4', 'bv4', 'b5', 'bv5']
    _MARKET_BAR_COLUMNS = ['stock_code', 'trade_time', 'price', 'volume', 'bs_type']

    def get_market(self, stock_code: str = '000001', start_date='1990-01-01', end_date=None, k_type=1,
                   adjust_type: int = 1):
        """
        获取单个股票的行情
        :param stock_code: 股票代码
        :param start_date: 开始时间
        :param end_date: 结束日期
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权 （目前：只有前复权,作为股票交易已经可用）
        :return: k线行情数据
        _MARKET_COLUMNS
        """
        pass

    def get_market_min(self, stock_code: str = '000001'):
        """
        获取单个股票的今日分时行情
        :param stock_code: 股票代码
        :return: 当日分钟行情数据
        _MARKET_MIN_COLUMNS
        """
        pass

    def list_market_current(self, code_list=None):
        """
        获取多个股票最新行情信息
        :param code_list: 股票代码
        :return: 当前最新的行情价格信息
        _MARKET_CURRENT_COLUMNS
        """
        pass

    def get_market_five(self, stock_code: str = '000001'):
        """
        获取单个股票的5档行情
        :param stock_code: 股票代码
        :return: 最新的五档行情
        """
        pass

    def list_market_five(self, code_list=None):
        """
         https://web.sqt.gtimg.cn/q=sh601666,sh600691
        :param code_list: 股票代码列表
        :return:
        """
        pass

    def get_market_bar(self, stock_code: str = '000001'):
        """
        获取单个股票的分时成交
        :param stock_code: 股票代码
        :return: 最新当天的分时成交
        """
        pass
