# -*- coding: utf-8 -*-
"""
@desc: 场内ETF相关数据
@author: 1nchaos
@time: 2023/4/4
@log: change log
"""

from adata.fund.info import info
from adata.fund.market import market


class Fund(object):

    def __init__(self) -> None:
        self.info = info
        self.market = market


fund = Fund()
