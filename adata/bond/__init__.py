# -*- coding: utf-8 -*-
"""
@desc: 场内债券相关数据
@author: 1nchaos
@time: 2023/3/29
@log: change log
"""
from adata.bond.info import info


class Bond(object):

    def __init__(self) -> None:
        self.info = info


bond = Bond()
