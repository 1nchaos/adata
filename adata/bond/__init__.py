# -*- coding: utf-8 -*-
"""
@desc: 场内债券相关数据
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""
from adata.bond.info import info
from adata.bond.market import market


class Bond(object):

    def __init__(self) -> None:
        self.info = info
        self.market = market


bond = Bond()
