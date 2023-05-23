# -*- coding: utf-8 -*-
"""
@desc: 行情相关的数据
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""
from .stock_dividend import StockDividend
from .stock_market import StockMarket
from .stock_market_concept import StockMarketConcept


class Market(StockMarket, StockMarketConcept, StockDividend):

    def __init__(self) -> None:
        super().__init__()


market = Market()
