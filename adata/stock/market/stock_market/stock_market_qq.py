# -*- coding: utf-8 -*-
"""
@desc: 腾讯股票行情中心
https://stockapp.finance.qq.com/mstats/#

@author: 1nchaos
@time: 2023/6/19
@log: change log
"""

from .stock_market_template import StockMarketTemplate


class StockMarketQQ(StockMarketTemplate):
    """
    腾讯股票行情
    """

    def __init__(self) -> None:
        super().__init__()

    def list_market_current(self, code_list=None):
        """
        获取多个股票最新行情信息
        https://qt.gtimg.cn/r=0.5979076524724433&q=s_sh600011,s_r_hk00902,s_sh600012,s_r_hk00995,s_sh600016,whHKDCNY
        :param code_list: 股票代码
        :return: 当前最新的行情价格信息
        """


if __name__ == '__main__':
    print(StockMarketQQ().list_market_current(code_list=['000001', '600001', '000795', '872925']))
