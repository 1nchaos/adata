# -*- coding: utf-8 -*-
"""
@desc: 股票资金流向

东方财富：个股
https://data.eastmoney.com/zjlx/000001.html
https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?cb=jQuery112303663243111530894_1718714074308&lmt=0&klt=101&fields1=f1%2Cf2%2Cf3%2Cf7&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61%2Cf62%2Cf63%2Cf64%2Cf65&ut=b2884a393a59ad64002292a3e90d46a5&secid=1.600519&_=1718714074309

@author: 1nchaos
@time: 2024/6/7
@log: change log
"""

from adata.stock.market.capital_flow.stock_capital_flow_baidu import StockCapitalFlowBaidu
from adata.stock.market.capital_flow.stock_capital_flow_east import StockCapitalFlowEast


class StockCapitalFlow(object):
    """股票资金流向"""

    def __init__(self) -> None:
        super().__init__()
        self.east_capital_flow = StockCapitalFlowEast()
        self.baidu_capital_flow = StockCapitalFlowBaidu()

    def get_capital_flow_min(self, stock_code: str = '000001'):
        """
        获取单个股票的今日分时资金流向
        :param stock_code: 股票代码
        :return: 当日分钟资金流向
        """
        return self.east_capital_flow.get_capital_flow_min(stock_code)

    def get_capital_flow(self, stock_code: str = '000001', start_date=None, end_date=None):
        """
        获取单个股票的资金流向-日度
        只能获取最近2年多的数据
        :param end_date: 结束日期
        :param start_date: 开始日期
        :param stock_code: 股票代码
        :return: 资金流向-日度
        """
        return self.baidu_capital_flow.get_capital_flow(stock_code, start_date=start_date, end_date=end_date)


if __name__ == '__main__':
    print(StockCapitalFlow().get_capital_flow_min(stock_code='300059'))
    print(StockCapitalFlow().get_capital_flow(stock_code='300059'))
