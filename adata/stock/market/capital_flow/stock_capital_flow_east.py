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
import pandas as pd

from adata.common.utils import requests
from adata.stock.market.capital_flow.stock_capital_flow_template import StockCapitalFlowTemplate


class StockCapitalFlowEast(StockCapitalFlowTemplate):

    def get_capital_flow_min(self, stock_code: str = '000001'):
        """
        获取单个股票的今日分时资金流向
        :param stock_code: 股票代码
        :return: 当日分钟资金流向
        """
        # 1. 请求接口 url
        cid = 1 if stock_code.startswith('6') else 0
        url = f"https://push2.eastmoney.com/api/qt/stock/fflow/kline/get?lmt=0&klt=1&fields1=f1,f2,f3,f7&" \
              f"fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65&" \
              f"secid={cid}.{stock_code}"
        res = requests.request(method='get', url=url, headers={})
        data = res.json()['data']

        # 2. 解析数据
        if not data:
            return pd.DataFrame([], columns=self._FLOW_MIN_COLUMNS)
        lines = data['klines']

        # 3. 数据etl
        # 2024-06-19 09:31,-1943532.0,2710159.0,-766627.0,-5901648.0,3958116.0
        data = [[stock_code] + line.split(',') for line in lines]
        df = pd.DataFrame(data, columns=self._FLOW_MIN_COLUMNS)
        df = df.astype({'trade_time': 'datetime64[ns]', 'main_net_inflow': 'float64', 'sm_net_inflow': 'float64',
                        'mid_net_inflow': 'float64', 'lg_net_inflow': 'float64', 'max_net_inflow': 'float64'})
        return df

    def get_capital_flow(self, stock_code: str = '000001', start_date=None, end_date=None):
        """
        获取单个股票的资金流向-日度
        目前只有120天的数据
        :param end_date: 开始日期
        :param start_date: 结束结束
        :param stock_code: 股票代码
        :return: 资金流向-日度
        """
        # 1. 请求接口 url
        cid = 1 if stock_code.startswith('6') else 0
        url = f"https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?" \
              f"lmt=0&klt=101&fields1=f1,f2,f3,f7&" \
              f"fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&" \
              f"secid={cid}.{stock_code}"
        res = requests.request(method='get', url=url, headers={})
        data = res.json()['data']

        # 2. 解析数据
        if not data:
            return pd.DataFrame([], columns=self._FLOW_COLUMNS)
        lines = data['klines']

        # 3. 数据etl
        # '2023-12-18,-58234405.0,47874618.0,10359788.0,-13362003.0,-44872402.0,-9.72,7.99,1.73,-2.23,-7.49,8.41,-0.94,0.00,0.00'
        data = [[stock_code] + line.split(',')[0:6] for line in lines]
        df = pd.DataFrame(data, columns=self._FLOW_COLUMNS)
        df = df.astype({'main_net_inflow': 'float64', 'sm_net_inflow': 'float64',
                        'mid_net_inflow': 'float64', 'lg_net_inflow': 'float64', 'max_net_inflow': 'float64'
                        })
        return df


if __name__ == '__main__':
    print(StockCapitalFlowEast().get_capital_flow_min(stock_code='300059'))
    print(StockCapitalFlowEast().get_capital_flow(stock_code='000001'))
