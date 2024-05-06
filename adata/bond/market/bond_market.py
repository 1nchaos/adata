# -*- coding: utf-8 -*-
"""
@desc:
http://www.iwencai.com/unifiedwap/result?typed=1&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=127093

@author: 1nchaos
@time:2023/4/5
@log: 
"""
from adata.bond.market.bond_market_sina import BondMarketSina


class BondMarket(object):
    """bond 行情"""

    def __init__(self) -> None:
        super().__init__()
        self.sina = BondMarketSina()

    def list_market_current(self, code_list=None):
        """
        获取多个可转债的最新行情信息
        :param code_list: 可转债代码
        :return: 当前最新的行情价格信息
        _MARKET_CURRENT_COLUMNS
        """
        return self.sina.list_market_current(code_list)


if __name__ == '__main__':
    print(BondMarket().list_market_current())
    print(BondMarket().list_market_current(code_list=['110044']))
