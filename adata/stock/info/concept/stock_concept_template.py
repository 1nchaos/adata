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
    _CONCEPT_INFO_COLUMNS = ['stock_code', 'concept_code', 'name', 'source', 'reason']
    _PLATE_INFO_COLUMNS = ['stock_code', 'plate_code', 'plate_name', 'plate_type', 'source']

    def __init__(self) -> None:
        super().__init__()
