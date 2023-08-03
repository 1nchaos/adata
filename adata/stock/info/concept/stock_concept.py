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


if __name__ == '__main__':
    print(StockConcept().all_concept_code_ths())
    print(StockConcept().concept_constituent_ths(index_code="885556"))
    print(StockConcept().concept_constituent_ths(concept_code="300843"))
    print(StockConcept().concept_constituent_ths(name="5G"))
