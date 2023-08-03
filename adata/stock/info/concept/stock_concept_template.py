# -*- coding: utf-8 -*-
"""
@desc: 
@author: 1nchaos
@time:2023/8/3
@log: 
"""


class StockConceptTemplate(object):
    """
    股票概念模板
    """
    _CONCEPT_CONSTITUENT_COLUMNS = ['stock_code', 'short_name']
    _CONCEPT_CODE_COLUMNS = ['concept_code', 'index_code', 'name', 'source']

    def __init__(self) -> None:
        super().__init__()
