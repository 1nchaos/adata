# -*- coding: utf-8 -*-
"""
@desc: 基本信息相关数据
@author: 1nchaos
@time: 2023/3/28
@log: change log
"""
from adata.stock.info.stock_code import StockCode
from adata.stock.info.concept.stock_concept import StockConcept
from adata.stock.info.stock_index import StockIndex
from adata.stock.info.trade_calendar import TradeCalendar


class Info(StockCode, StockConcept, TradeCalendar, StockIndex):

    def __init__(self) -> None:
        super().__init__()


info = Info()
