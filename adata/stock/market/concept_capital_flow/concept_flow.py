# -*- coding: utf-8 -*-
"""
@desc: 概念资金流向

东方财富：概念
https://data.eastmoney.com/bkzj/gn.html
@author: 1nchaos
@time: 2024/11/14
@log: change log
"""
from adata.stock.market.concept_capital_flow.capital_flow_east import CapitalFlowEast


class ConceptCapitalFlow(CapitalFlowEast):
    """概念资金流向"""

    def __init__(self) -> None:
        super().__init__()
