# -*- coding: utf-8 -*-
"""
@summary: 股票概念

概念，指数成分
来源于同花顺
http://q.10jqka.com.cn/gn
https://data.eastmoney.com/bkzj/gn.html

@author: 1nchaos
@date: 2023/3/30 16:17
"""
from adata.stock.info.concept.stock_concept_east import StockConceptEast
from adata.stock.info.concept.stock_concept_ths import StockConceptThs


class StockConcept(StockConceptThs, StockConceptEast):

    def __init__(self) -> None:
        super().__init__()
