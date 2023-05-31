# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2023/5/31
@log: change log
"""
from .bond_code import BondCode


class Info(BondCode):

    def __init__(self) -> None:
        super().__init__()


info = Info()
