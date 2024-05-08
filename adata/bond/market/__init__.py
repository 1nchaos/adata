# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/5/31
@log: change log
"""
from adata.bond.market.bond_market import BondMarket


class Market(BondMarket):

    def __init__(self) -> None:
        super().__init__()


market = Market()
