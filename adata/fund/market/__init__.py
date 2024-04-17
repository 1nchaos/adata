# -*- coding: utf-8 -*-
"""
@desc: etf 行情
数据源：
深交所
http://www.sse.com.cn/market/price/trends/

雪球：
https://xueqiu.com

@author: 1nchaos
@time: 2023/6/5
@log: change log
"""
from adata.fund.market.etf_market import ETFMarket


class Market(ETFMarket):

    def __init__(self) -> None:
        super().__init__()


market = Market()
