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
import datetime

import pandas as pd

from adata.common.headers import baidu_headers
from adata.common.utils import requests
from adata.common.utils.unit_conver import convert_to_yuan
from adata.stock.market.capital_flow.stock_capital_flow_template import StockCapitalFlowTemplate


class StockCapitalFlowBaidu(StockCapitalFlowTemplate):

    def get_capital_flow_min(self, stock_code: str = '000001'):
        """
        获取单个股票的今日分时资金流向
        :param stock_code: 股票代码
        :return: 当日分钟资金流向
        """
        url = f"https://finance.pae.baidu.com/vapi/v1/fundflow?finance_type=stock&fund_flow_type=&" \
              f"type=stock&market=ab&code={stock_code}&belongs=stocklevelone&finClientType=pc"
        res = requests.request('get', url, headers=baidu_headers.json_headers, proxies={})
        data_str = res.json()["Result"]["content"]["fundFlowMinute"]["data"]
        data_list = data_str.split(';')
        data = []
        for row_str in data_list:
            row = row_str.split(',')
            data.append({
                "stock_code": stock_code,
                "trade_time": row[0],
                "main_net_inflow": float(row[2]) * 10000 * 10000,
                "sm_net_inflow": float(row[7]) * 10000 * 10000,
                "mid_net_inflow": float(row[6]) * 10000 * 10000,
                "lg_net_inflow": float(row[5]) * 10000 * 10000,
                "max_net_inflow": float(row[4]) * 10000 * 10000
            })
        #  2024-07-01 9:30, 0.00, -0.08, 0.08, -0.05, -0.03, 0.02, 0.06, 10.48, -0.76 %;
        df = pd.DataFrame(data, columns=self._FLOW_MIN_COLUMNS)
        return df

    def get_capital_flow(self, stock_code: str = '000001', start_date=None, end_date=None):
        """
        获取单个股票的资金流向-日度
        :param end_date: 开始日期
        :param start_date: 结束日期
        :param stock_code: 股票代码
        :return: 资金流向-日度
        """
        # 1. 日期处理
        if end_date is None:
            now = datetime.datetime.now()
            end_date = now.strftime('%Y%m%d')
        else:
            end_date = end_date.replace('-', '')

        if start_date is not None:
            start_date = start_date.replace('-', '')

        # 2. 循环请求数据
        data = []
        is_end = False
        for i in range(0, 500):
            url = f"https://finance.pae.baidu.com/vapi/v1/fundsortlist?" \
                  f"code={stock_code}&market=ab&finance_type=stock&tab=day&" \
                  f"from=history&date={end_date}&pn=0&rn=20&finClientType=pc"
            res = requests.request('get', url, headers=baidu_headers.json_headers, proxies={})
            data_list = res.json()["Result"]["content"]
            if len(data_list) == 0:
                break
            for row in data_list:
                row = convert_to_yuan(row)
                # 日期范围判断
                if start_date is not None and row["date"].replace('/', '') < start_date:
                    is_end = True
                    break
                data.append({
                    "stock_code": stock_code,
                    "trade_date": row["date"].replace("/", '-'),
                    "main_net_inflow": row["extMainIn"],
                    "sm_net_inflow": row["littleNetIn"],
                    "mid_net_inflow": row["mediumNetIn"],
                    "lg_net_inflow": row["largeNetIn"],
                    "max_net_inflow": row["superNetIn"]
                })
            if is_end:
                break
            end_date = data[-1]["trade_date"].replace('-', '')
        df = pd.DataFrame(data, columns=self._FLOW_COLUMNS)
        return df


if __name__ == '__main__':
    print(StockCapitalFlowBaidu().get_capital_flow_min(stock_code='300059'))
    print(StockCapitalFlowBaidu().get_capital_flow(stock_code='300059', start_date='2024-01-01', end_date='2024-04-01'))
