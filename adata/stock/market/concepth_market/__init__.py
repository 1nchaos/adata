# -*- coding: utf-8 -*-
"""
@desc: 
@author: 1nchaos
@time:2023/8/3
@log: 
"""
from adata.stock.market.concepth_market.concept_market_east import ConceptMarketEase
from adata.stock.market.concepth_market.concept_market_ths import ConceptMarketThs


class StockMarketConcept(ConceptMarketEase, ConceptMarketThs):
    def __init__(self) -> None:
        super().__init__()
