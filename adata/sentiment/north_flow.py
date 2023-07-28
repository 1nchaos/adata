# -*- coding: utf-8 -*-
"""
@desc:
北向资金
来源：东方财富
https://data.eastmoney.com/hsgt/index.html
https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112304138107938255364_1690533543847&sortColumns=TRADE_DATE&sortTypes=-1&pageSize=1000&pageNumber=1&reportName=RPT_MUTUAL_DEAL_HISTORY&columns=ALL&source=WEB&client=WEB&filter=(MUTUAL_TYPE%3D%22001%22)

@author: 1nchaos
@time: 2023/7/28
@log: change log
"""


class NorthFlow(object):

    def __init__(self) -> None:
        super().__init__()

    def north_flow(self, start_date=None):
        pass


if __name__ == '__main__':
    print(NorthFlow().north_flow('2022-01-01'))
