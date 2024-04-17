# -*- coding: utf-8 -*-
"""
@summary: etf 行情
"""


class ETFMarketTemplate(object):
    """
    etf 行情
    """
    _MARKET_COLUMNS = ['fund_code', 'trade_time', 'trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount',
                       'change', 'change_pct']
    _MARKET_ETF_MIN_COLUMNS = ['fund_code', 'trade_time', 'trade_date', 'price', 'avg_price', 'volume', 'amount',
                               'change', 'change_pct']
    _MARKET_ETF_CURRENT_COLUMNS = ['fund_code', 'trade_time', 'trade_date', 'open', 'high', 'low', 'price', 'volume',
                                   'amount', 'change', 'change_pct']
