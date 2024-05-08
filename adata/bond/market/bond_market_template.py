# -*- coding: utf-8 -*-
"""
@desc: readme
@author: 1nchaos
@time: 2024/05/05
@log: change log
"""


class BondMarketTemplate(object):
    """
    债券行情
    """
    _MARKET_CURRENT_COLUMNS = ['bond_code', 'bond_name', 'price', 'open', 'high', 'low', 'pre_close', 'change',
                               'change_pct', 'volume', 'amount', 'time']

    def list_market_current(self, code_list=None):
        """
        获取多个可转债的最新行情信息
        :param code_list: 可转债代码
        :return: 当前最新的行情价格信息
        _MARKET_CURRENT_COLUMNS
        """
        pass
