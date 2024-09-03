# -*- coding: utf-8 -*-
"""
@desc: 专注股票相关的数据，为量化而生
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""
from adata.stock.finance import finance
from adata.stock.index import index
from adata.stock.info import info
from adata.stock.market import market


class Stock(object):

    def __init__(self) -> None:
        self.info = info
        self.index = index
        self.market = market
        self.finance = finance


stock = Stock()
