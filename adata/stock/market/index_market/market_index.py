# -*- coding: utf-8 -*-
"""
@summary: 股票指数 行情
@author: 1nchaos
@date: 2023/06/01 16:17
"""
from adata.stock.market.index_market.market_index_baidu import StockMarketIndexBaidu
from adata.stock.market.index_market.market_index_east import StockMarketIndexEast
from adata.stock.market.index_market.market_index_ths import StockMarketIndexThs


class StockMarketIndex(object):
    """
    股票指数 行情
    """

    def __init__(self) -> None:
        self.ths_index = StockMarketIndexThs()
        self.east_index = StockMarketIndexEast()
        self.baidu_index = StockMarketIndexBaidu()

    def get_market_index(self, index_code: str = '000001', start_date='2020-01-01', k_type: int = 1):
        """
        获取指数行情
        """
        res_df = self.baidu_index.get_market_index(index_code=index_code, start_date=start_date, k_type=k_type)
        if res_df.empty:
            res_df = self.ths_index.get_market_index(index_code=index_code, start_date=start_date, k_type=k_type)
        return res_df

    def get_market_index_min(self, index_code='000001'):
        """
        获取指数当日的分时行情
        :param index_code: 指数代码
        :return 时间，现价，成交额（元），均价，成交量（股） 涨跌额，涨跌幅
        ['index_code', 'trade_time', 'price', 'change', 'change_pct', 'volume', 'avg_price', 'amount']
        """
        res_df = self.east_index.get_market_index_min(index_code=index_code)
        if res_df.empty:
            res_df = self.ths_index.get_market_index_min(index_code=index_code)
        return res_df

    def get_market_index_current(self, index_code: str = '000001'):
        """
        获取当前的指数行情
        :param index_code: 指数代码
        :return: [指数代码,交易时间，交易日期，开，高，低，当前价格,成交量，成交额]
        ['trade_time', 'trade_date', 'open', 'high', 'low', 'price', 'volume', 'amount']
        """
        return self.east_index.get_market_index_current(index_code=index_code)


if __name__ == '__main__':
    print(StockMarketIndex().get_market_index(index_code='000001', start_date='2022-12-01', k_type=1))
    print(StockMarketIndex().get_market_index_min(index_code='000001'))
    print(StockMarketIndex().get_market_index_current(index_code='000001'))
