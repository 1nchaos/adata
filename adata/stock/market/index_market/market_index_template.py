# -*- coding: utf-8 -*-
"""
@summary: 股票指数 行情
@author: 1nchaos
@date: 2023/06/01 16:17
"""


class StockMarketIndexTemplate(object):
    """
    股票指数 行情
    """
    _MARKET_INDEX_BASE_COLUMNS = ['trade_time', 'open', 'high', 'low', 'close', 'volume', 'amount', 'change',
                                  'change_pct']
    _MARKET_INDEX_COLUMNS = ['index_code', 'trade_date'].extend(_MARKET_INDEX_BASE_COLUMNS)
    _MARKET_INDEX_MIN_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'price', 'avg_price', 'volume', 'amount',
                                 'change', 'change_pct']
    _MARKET_INDEX_CURRENT_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'open', 'high', 'low', 'price',
                                     'volume', 'amount']

    def __init__(self) -> None:
        super().__init__()

    def get_market_index(self, index_code: str = '000001', start_date='2020-01-01', k_type: int = 1):
        """
        获取指数行情
        """
        pass

    def get_market_index_min(self, index_code='000001'):
        """
        获取指数当日的分时行情
        :param index_code: 指数代码
        :return 时间，现价，成交额（元），均价，成交量（股） 涨跌额，涨跌幅
        ['index_code', 'trade_time', 'price', 'change', 'change_pct', 'volume', 'avg_price', 'amount']
        """
        pass

    def get_market_index_current(self, index_code: str = '000001'):
        """
        获取当前的指数行情
        :param index_code: 指数代码
        :return: [指数代码,交易时间，交易日期，开，高，低，当前价格,成交量，成交额]
        ['trade_time', 'trade_date', 'open', 'high', 'low', 'price', 'volume', 'amount']
        """
        pass
