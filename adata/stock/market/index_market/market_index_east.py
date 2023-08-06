# -*- coding: utf-8 -*-
"""
@summary: 股票指数 行情
@author: 1nchaos
@date: 2023/06/01 16:17
"""

from adata.stock.market.index_market.market_index_template import StockMarketIndexTemplate


class StockMarketIndexEast(StockMarketIndexTemplate):
    def __init__(self) -> None:
        super().__init__()

    def get_market_index(self, index_code: str = '000001', start_date='2020-01-01', k_type: int = 1):
        """
        获取指数行情
        """

    def get_market_index_min(self, index_code='000001'):
        """
        获取指数当日的分时行情
        :param index_code: 指数代码
        :return 时间，现价，成交额（元），均价，成交量（股） 涨跌额，涨跌幅
        ['index_code', 'trade_time', 'price', 'change', 'change_pct', 'volume', 'avg_price', 'amount']
        """

    def get_market_index_current(self, index_code: str = '000001', k_type: int = 1):
        """
        获取当前的指数行情
        :param index_code: 指数代码
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :return: [指数代码,交易时间，交易日期，开，高，低，当前价格,成交量，成交额]
        ['trade_time', 'trade_date', 'open', 'high', 'low', 'price', 'volume', 'amount']
        """


if __name__ == '__main__':
    print(StockMarketIndexEast().get_market_index(index_code='000001', start_date='2022-12-01'))
    print(StockMarketIndexEast().get_market_index_min(index_code='000001'))
    print(StockMarketIndexEast().get_market_index_current(index_code='000001'))
