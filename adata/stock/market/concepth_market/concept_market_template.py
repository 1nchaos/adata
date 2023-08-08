# -*- coding: utf-8 -*-
"""
@summary: 股票概念 行情
"""


class ConceptMarketTemplate(object):
    """
    股票概念 行情
    """
    _MARKET_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'open', 'high', 'low', 'close', 'volume',
                       'amount', 'change', 'change_pct']
    _MARKET_CONCEPT_MIN_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'price', 'avg_price', 'volume', 'amount',
                                   'change', 'change_pct']
    _MARKET_CONCEPT_CURRENT_COLUMNS = ['index_code', 'trade_time', 'trade_date', 'open', 'high', 'low', 'price',
                                       'volume', 'amount', 'change', 'change_pct']
