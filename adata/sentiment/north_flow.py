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
import copy
import datetime
import json

import pandas as pd

from adata.common import requests
from adata.common.base.base_ths import BaseThs
from adata.common.exception.exception_msg import THS_IP_LIMIT_RES, THS_IP_LIMIT_MSG
from adata.common.headers import ths_headers


class NorthFlow(BaseThs):
    __NORTH_FLOW_MIN_COLUMNS = ['trade_time', 'hgt', 'sgt', 'tgt']
    __NORTH_FLOW_CURRENT_COLUMNS = __NORTH_FLOW_MIN_COLUMNS

    def __init__(self) -> None:
        super().__init__()

    def north_flow(self, start_date=None):
        pass

    def north_flow_min(self):
        """
        获取北向的分时数据，最新交易日的
        https://data.hexin.cn/market/hsgtApi/method/dayChart/
        """
        return self.__north_flow_min_ths()

    def north_flow_current(self):
        """
        获取北向的最新数据，最新交易日的
        """
        return self.north_flow_min().tail(1)

    def __north_flow_min_ths(self):
        # 1.接口 url
        api_url = f" https://data.hexin.cn/market/hsgtApi/method/dayChart/"
        headers = copy.deepcopy(ths_headers.json_headers)
        headers['Host'] = 'data.hexin.cn'
        res = requests.request('get', api_url, headers=headers, proxies={})
        text = res.text
        if THS_IP_LIMIT_RES in text:
            return Exception(THS_IP_LIMIT_MSG)
        if not text:
            return pd.DataFrame(data=[], columns=self.__NORTH_FLOW_CURRENT_COLUMNS)
        # 2. 解析数据
        result_json = json.loads(text)
        time_list = result_json['time']
        hgt_list = result_json['hgt']
        sgt_list = result_json['sgt']
        data = []
        for i in range(len(time_list)):
            row = [time_list[i], hgt_list[i], sgt_list[i], float(hgt_list[i]) + float(sgt_list[i])]
            data.append(row)
        # 3. 封装数据
        result_df = pd.DataFrame(data=data, columns=self.__NORTH_FLOW_CURRENT_COLUMNS)
        import adata
        trade_year = adata.stock.info.trade_calendar()
        # 获取当前日期
        today = datetime.datetime.today().date()
        # 筛选出小于等于今天并且 trade_status=1 的记录
        trade_year['trade_date'] = pd.to_datetime(trade_year['trade_date'])
        filtered_df = trade_year[(trade_year['trade_date'].dt.date <= today) & (trade_year['trade_status'] == 1)]
        max_date = filtered_df.loc[filtered_df['trade_date'].idxmax()]

        result_df['trade_time'] = max_date['trade_date'].strftime('%Y-%m-%d') + ' ' + result_df['trade_time']

        # 将 trade_time 字符串转换为日期时间类型
        result_df['trade_time'] = pd.to_datetime(result_df['trade_time'])
        return result_df[self.__NORTH_FLOW_CURRENT_COLUMNS]


if __name__ == '__main__':
    print(NorthFlow().north_flow('2022-01-01'))
    print(NorthFlow().north_flow_min())
    print(NorthFlow().north_flow_current())
