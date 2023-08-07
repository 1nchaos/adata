# -*- coding: utf-8 -*-
"""
@desc: 行情相关的数据
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""
from adata.stock.market.concepth_market import StockMarketConcept
from adata.stock.market.index_market.market_index import StockMarketIndex
from .stock_dividend import StockDividend
from .stock_market import StockMarket


class Market(StockMarket, StockMarketConcept, StockDividend, StockMarketIndex):

    def __init__(self) -> None:
        super().__init__()


market = Market()
