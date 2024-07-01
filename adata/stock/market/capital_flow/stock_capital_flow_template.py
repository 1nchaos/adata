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


class StockCapitalFlowTemplate(object):
    """股票资金流向"""
    _FLOW_MIN_COLUMNS = ['stock_code', 'trade_time', 'main_net_inflow', 'sm_net_inflow', 'mid_net_inflow',
                         'lg_net_inflow', 'max_net_inflow']
    # _FLOW_COLUMNS = ['stock_code', 'trade_date', 'main_net_inflow', 'sm_net_inflow', 'mid_net_inflow',
    #                  'lg_net_inflow', 'max_net_inflow',
    #                  'main_net_inflow_rate', 'sm_net_inflow_rate', 'mid_net_inflow_rate',
    #                  'lg_net_inflow_rate', 'max_net_inflow_rate']

    _FLOW_COLUMNS = ['stock_code', 'trade_date', 'main_net_inflow', 'sm_net_inflow', 'mid_net_inflow',
                     'lg_net_inflow', 'max_net_inflow']

    def get_capital_flow_min(self, stock_code: str = '000001'):
        """
        获取单个股票的今日分时资金流向
        :param stock_code: 股票代码
        :return: 当日分钟资金流向
        """

    pass

    def get_capital_flow(self, stock_code: str = '000001', start_date=None, end_date=None):
        """
        获取单个股票的资金流向-日度
        目前只有120天的数据
        :param end_date: 开始日期
        :param start_date: 结束日期
        :param stock_code: 股票代码
        :return: 资金流向-日度
        """
        pass
